import itertools as itt
import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.mips as mips
from core.cmp.utils import CountDict


USED   = 1
UNUSED = 0


class SimpleRegistersManager:
    def __init__(self, registers):
        self.registers = {reg: UNUSED for reg in registers}
            
    def get_free_reg(self):
        for reg, state in self.registers.items():
            if state == UNUSED:
                self.registers[reg] = USED
                return reg
        raise Exception("not free register")
        
    
    def free_reg(self, reg):
        self.registers[reg] = UNUSED
    
    def is_used(self, reg):
        return self.registers[reg] == USED

    def get_registers_for_save(self):
        regs = [reg for reg, state in self.registers.items() if state == USED]
        regs.extend([mips.RA_REG])
        return regs
    
    def __repr__(self):
        return str(len([0 for r in self.registers if self.registers[r] == USED ]))


class LabelGenerator:
    def __init__(self):
        self.data_count = 0
        self.type_count = 0
        self.code_count = 0

    def generate_type_label(self):
        self.type_count += 1        
        return f'type_{self.type_count}'
        
    def generate_data_label(self):
        self.data_count += 1
        return f'data_{self.data_count}'
    
    def generate_code_label(self):
        self.code_count += 1
        return f'L_{self.code_count}'


class CILToMIPSVisitor:
    def __init__(self, label_generator = LabelGenerator(), regiters_manager = SimpleRegistersManager(mips.REGISTERS)):
        self._label_generator = label_generator
        self._registers_manager = regiters_manager
        self._types = {}
        self._data_section = {}
        self._functions = {}
        self._actual_function = None
        self._name_func_map = {}
        self._pushed_args = 0
        self._labels_map = {}
    
    def generate_type_label(self):
        return self._label_generator.generate_type_label()
    
    def generate_data_label(self):
        return self._label_generator.generate_data_label()
    
    def generate_code_label(self):
        return self._label_generator.generate_code_label()
    
    def get_var_location(self, name):
        return self._actual_function.get_var_location(name)
    
    def register_function(self, name, function):
        self._functions[name] = function
        
    def init_function(self, function):
        self._actual_function = function
        self._labels_map = {}
    
    def finish_functions(self):
        self._actual_function = None
    
    def push_arg(self):
        self._pushed_args += 1
    
    def clean_pushed_args(self):
        self._pushed_args = 0
    
    def get_free_reg(self):
        return self._registers_manager.get_free_reg()
    
    def free_reg(self, reg):
        self._registers_manager.free_reg(reg)
    
    def in_entry_function(self):
        return self._actual_function.label == 'main'

    def register_label(self, cil_label, mips_label):
        self._labels_map[cil_label] = mips_label    
    
    def get_mips_label(self, label):
        return self._labels_map[label]
    
    @visitor.on('node')
    def collect_func_names(self, node):
        pass
    
    @visitor.when(cil.ProgramNode)
    def collect_func_names(self, node):
        for func in node.dotcode:
            self.collect_func_names(func)
        
    @visitor.when(cil.FunctionNode)
    def collect_func_names(self, node):
        if node.name == "entry":
            self._name_func_map[node.name] = 'main'
        else:
            self._name_func_map[node.name] = self.generate_code_label()
    
    @visitor.on('node')
    def collect_labels_in_func(self, node):
        pass
    
    @visitor.when(cil.LabelNode)
    def collect_labels_in_func(self, node):
        mips_label = self.generate_code_label()
        self.register_label(node.label, mips_label)
    
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cil.InstructionNode)
    def visit(self, node):
        print(type(node))
    
    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        #Get functions names
        self.collect_func_names(node)
        
        #Convert CIL ProgramNode to MIPS ProgramNode
        for tp in node.dottypes:
            self.visit(tp)
        
        for data in node.dotdata:
            self.visit(data)
        
        for func in node.dotcode:
            self.visit(func)
        
        return mips.ProgramNode( [data for data in self._data_section.values()], [tp for tp in self._types.values()], [func for func in self._functions.values()])

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        name_label = self.generate_data_label()
        self._data_section[node.name] = mips.StringConst(name_label, node.name)

        type_label = self.generate_type_label()
        methods = {key: self._name_func_map[value] for key, value in node.methods}
        new_type = mips.MIPSType(type_label, name_label, node.attributes, methods, len(self._types))

        self._types[node.name] = new_type
    
    @visitor.when(cil.DataNode)
    def visit(self, node):
        label = self.generate_data_label()
        self._data_section[node.name] = mips.StringConst(label, node.value)

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        used_regs_finder = UsedRegisterFinder()

        label = self._name_func_map[node.name]
        params = [param.name for param in node.params]
        localvars = [local.name for local in node.localvars]
        size_for_locals = len(localvars) * mips.ATTR_SIZE
        
        new_func = mips.FunctionNode(label, params, localvars)
        self.register_function(node.name, new_func)
        self.init_function(new_func)

        for instruction in node.instructions:
            self.collect_labels_in_func(instruction)

        initial_instructions = []
        if self.in_entry_function():
            initial_instructions.append(mips.JumpAndLinkNode("mem_manager_init"))


        initial_instructions.extend(mips.push_register(mips.FP_REG))
        initial_instructions.append(mips.AddInmediateNode(mips.FP_REG, mips.SP_REG, 4))
        initial_instructions.append(mips.AddInmediateNode(mips.SP_REG, mips.SP_REG, -size_for_locals))

        code_instructions = []
        
        #This try-except block is for debuggin purposes
        try:
            code_instructions = list(itt.chain.from_iterable([self.visit(instruction) for instruction in node.instructions]))
            
        except Exception as e:
            if node.name == "function_a2i_aux_at_A2I":
                print(e)
                # print(node.instructions)
            print(node.name)
            
            
            
        final_instructions = []
        
        if not self.in_entry_function():
            used_regs = used_regs_finder.get_used_registers(code_instructions)
            #TODO change this to grow the stack just once
            for reg in used_regs:
                initial_instructions.extend(mips.push_register(reg))
            
            #TODO change this to shrink the stack just once
            for reg in used_regs[::-1]:
                final_instructions.extend(mips.pop_register(reg))
        
        final_instructions.append(mips.AddInmediateNode(mips.SP_REG, mips.SP_REG, size_for_locals))
        final_instructions.extend(mips.pop_register(mips.FP_REG))

        if not self.in_entry_function():
            final_instructions.append(mips.JumpRegister(mips.RA_REG))
        else:
            final_instructions.extend(mips.exit_program())
        
        func_instructions = list(itt.chain(initial_instructions, code_instructions, final_instructions))
        new_func.add_instructions(func_instructions)
        self.finish_functions() 
        
       
    @visitor.when(cil.ArgNode)
    def visit(self, node):
        self.push_arg()
        instructions = []
                
        if type(node.name) == int:
            reg = self.get_free_reg()
            load_value = mips.LoadInmediateNode(reg, node.name)
            instructions.append(load_value)
            instructions.extend(mips.push_register(reg))
        else:
            reg = self.get_free_reg()
            # if not loaded:
            value_address = self.get_var_location(node.name)
            load_value = mips.LoadWordNode(reg, value_address)
            instructions.append(load_value)
            instructions.extend(mips.push_register(reg))
        
        self.free_reg(reg)
        return instructions
    
    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        
        instructions = []

        label = self._name_func_map[node.function]

        instructions.append(mips.JumpAndLinkNode(label))

        dst_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(mips.V0_REG, dst_location))

        if self._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(mips.SP_REG, mips.SP_REG, self._pushed_args * mips.ATTR_SIZE))
            self.clean_pushed_args()

        return instructions
    
    @visitor.when(cil.AssignNode)
    def visit(self, node):
        instructions = []
        
        reg = self.get_free_reg()

        if type(node.source) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(reg, 0))
        elif node.source.isnumeric():
            load_value = mips.LoadInmediateNode(reg, int(node.source))
            instructions.append(load_value)
        elif type(node.source) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(reg, 0))
        else:
            value_location = self.get_var_location(node.source)
            load_value = mips.LoadWordNode(reg, value_location)
            instructions.append(load_value)
        
        location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(reg, location))
        self.free_reg(reg)

        return instructions
    
    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        #TODO Save $a0, $a1 and $a2 registers if are beign used
        
        instructions = []

        reg1 = self.get_free_reg()
        reg2 = self.get_free_reg()
                
        tp = 0
        if node.type.isnumeric():
            tp = node.type
        else:
            tp = self._types[node.type].index
            
        instructions.append(mips.LoadInmediateNode(reg1, tp))
        instructions.extend(mips.create_object(reg1, reg2))
        
        location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(mips.V0_REG, location))

        self.free_reg(reg1)
        self.free_reg(reg2)
        
        return instructions
    
    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        instructions = []

        if node.value is None:
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0))
        elif type(node.value) == int:
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, node.value))
        else:
            location = self.get_var_location(node.value)
            instructions.append(mips.LoadWordNode(mips.V0_REG, location))
            
        return instructions
    
    @visitor.when(cil.LoadNode)
    def visit(self, node):
        instructions = []
        reg = self.get_free_reg()
        string_location = mips.LabelRelativeLocation(self._data_section[node.msg.name].label, 0)
        instructions.append(mips.LoadAddressNode(reg, string_location))

        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(reg, dest_location))

        self.free_reg(reg)
        return instructions
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 1))

        #TODO save $a0 if is beign used
        location = self.get_var_location(node.value)
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], location))
        instructions.append(mips.SyscallNode())

        return instructions
    
    @visitor.when(cil.PrintStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4))

        #TODO save $a0 if is beign used

        location = self.get_var_location(node.value)
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], location))
        instructions.append(mips.SyscallNode())

        return instructions
    
    @visitor.when(cil.TypeNameNode)
    def visit(self, node):
        instructions = []
        
        reg = self.get_free_reg()
        reg2 = self.get_free_reg()

        src_location = self.get_var_location(node.source)
        dst_location = self.get_var_location(node.dest)

        instructions.append(mips.LoadWordNode(reg, src_location))
        instructions.append(mips.LoadWordNode(reg, mips.RegisterRelativeLocation(reg, 0)))
        instructions.append(mips.ShiftLeftLogicalNode(reg, reg, 2))
        instructions.append(mips.LoadAddressNode(reg2, mips.TYPENAMES_TABLE_LABEL))
        instructions.append(mips.AddUnsignedNode(reg, reg, reg2))
        instructions.append(mips.LoadWordNode(reg, mips.RegisterRelativeLocation(reg, 0)))
        instructions.append(mips.StoreWordNode(reg, dst_location))

        self.free_reg(reg)
        self.free_reg(reg2)

        return instructions
    
    @visitor.when(cil.ExitNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10))
        instructions.append(mips.SyscallNode())

        return instructions
    
    @visitor.when(cil.GetAttribNode)
    def visit(self, node):
        instructions = []

        reg = self.get_free_reg()
        
        dest = node.dest if type(node.dest) == str else node.dest.name
        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(node.computed_type) == str else node.computed_type.name
        
        obj_location = self.get_var_location(obj)
        dst_location = self.get_var_location(dest)
        
        tp = self._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE

        instructions.append(mips.LoadWordNode(reg, obj_location))
        instructions.append(mips.LoadWordNode(reg, mips.RegisterRelativeLocation(reg, offset)))
        instructions.append(mips.StoreWordNode(reg, dst_location))

        self.free_reg(reg)
        return instructions
    
    @visitor.when(cil.SetAttribNode)
    def visit(self, node):
        instructions = []
        reg1 = self.get_free_reg()
        reg2 = self.get_free_reg()

        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(node.computed_type) == str else node.computed_type.name
        
        
        obj_location = self.get_var_location(obj)

        tp = self._types[comp_type]
        # print(self._actual_function.label)
        # print(node.value)
        # print(tp.attributes)
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE


        instructions.append(mips.LoadWordNode(reg2, obj_location))

        if type(node.value) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.value))
        else:
            src_location = self.get_var_location(node.value)
            instructions.append(mips.LoadWordNode(reg1, src_location))
        

        instructions.append(mips.StoreWordNode(reg1, mips.RegisterRelativeLocation(reg2, offset)))

        self.free_reg(reg1)
        self.free_reg(reg2)
        
        return instructions
    
    @visitor.when(cil.CopyNode)
    def visit(self, node):
        instructions = []

        #Save $a0, $a1, $a2

        reg1 = self.get_free_reg()
        reg2 = self.get_free_reg()

        src_location = self.get_var_location(node.source)
        instructions.append(mips.LoadWordNode(reg1, src_location))
        instructions.extend(mips.copy_object(reg1, reg2))

        dst_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(mips.V0_REG, dst_location))

        self.free_reg(reg1)
        self.free_reg(reg2)

        return instructions
    
    @visitor.when(cil.EqualNode)
    def visit(self, node):
        instructions = []

        #TODO save $a0 $a1 $v0

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], node.left))
        elif type(node.left) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], 0))
        else:
            location = self.get_var_location(node.left)
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], location))
        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.right))
        elif type(node.right) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], 0))
        else:
            location = self.get_var_location(node.right)
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], location))

        instructions.append(mips.JumpAndLinkNode("equals"))

        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))
        
        return instructions
    
    @visitor.when(cil.EqualStrNode)
    def visit(self, node):
        instructions = []

        location = self.get_var_location(node.left)
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], location))

        location = self.get_var_location(node.right)
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], location))

        instructions.append(mips.JumpAndLinkNode("equal_str"))

        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))
        
        return instructions




    @visitor.when(cil.LabelNode)
    def visit(self, node):
        return [mips.LabelNode(self.get_mips_label(node.label))]

    @visitor.when(cil.GotoIfNode)
    def visit(self, node):
        
        instructions = []

        reg = self.get_free_reg()
        
        mips_label = self.get_mips_label(node.label)

        location = self.get_var_location(node.condition)
        instructions.append(mips.LoadWordNode(reg, location))
        instructions.append(mips.BranchOnNotEqualNode(reg, mips.ZERO_REG, mips_label))

        self.free_reg(reg)
        
        return instructions
    
    @visitor.when(cil.GotoNode)
    def visit(self, node):
        mips_label = self.get_mips_label(node.label)
        return [mips.JumpNode(mips_label)]

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        instructions = []

        reg = self.get_free_reg()

        obj_location = self.get_var_location(node.obj)
        instructions.append(mips.LoadWordNode(reg, obj_location))
        instructions.append(mips.LoadWordNode(reg, mips.RegisterRelativeLocation(reg, 0)))
        
        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(reg, dest_location))

        self.free_reg(reg)

        return instructions

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        instructions = []

        reg1 = self.get_free_reg()
        reg2 = self.get_free_reg()

        comp_tp = self._types[node.computed_type]
        method_index = list(comp_tp.methods).index(node.method)
        dest_location = self.get_var_location(node.dest)

        tp_location = self.get_var_location(node.type)
        instructions.append(mips.LoadAddressNode(reg1, mips.PROTO_TABLE_LABEL))
        instructions.append(mips.LoadWordNode(reg2, tp_location))
        instructions.append(mips.ShiftLeftLogicalNode(reg2, reg2, 2))
        instructions.append(mips.AddUnsignedNode(reg1, reg1, reg2 ))
        instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, 0)))
        instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, 8)))
        instructions.append(mips.AddInmediateUnsignedNode(reg1, reg1, method_index*4))
        instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, 0)))
        instructions.append(mips.JumpRegisterAndLinkNode(reg1))
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        self.free_reg(reg1)
        self.free_reg(reg2)
        if self._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(mips.SP_REG, mips.SP_REG, self._pushed_args * mips.ATTR_SIZE))
            self.clean_pushed_args()

        return instructions
    

    @visitor.when(cil.ErrorNode)
    def visit(self, node):
        instructions = []

        mips_label = self._data_section[node.data_node.name].label

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4))
        instructions.append(mips.LoadAddressNode(mips.ARG_REGISTERS[0], mips_label))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10))
        instructions.append(mips.SyscallNode())

        return instructions


    @visitor.when(cil.NameNode)
    def visit(self, node):
        instructions = []

        reg = self.get_free_reg()

        instructions.append(mips.LoadAddressNode(reg, mips.TYPENAMES_TABLE_LABEL))
        tp_number = self._types[node.name].index
        instructions.append(mips.AddInmediateUnsignedNode(reg, reg, tp_number*4))
        instructions.append(mips.LoadWordNode(reg, mips.RegisterRelativeLocation(reg, 0)))

        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(reg, dest_location))

        self.free_reg(reg)

        return instructions
    
    @visitor.when(cil.PlusNode)
    def visit(self, node):
        instructions = []

        reg1 = self.get_free_reg()
        reg2 = self.get_free_reg()

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            left_location = self.get_var_location(node.left)
            instructions.append(mips.LoadWordNode(reg1, left_location))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            right_location = self.get_var_location(node.right)
            instructions.append(mips.LoadWordNode(reg2, right_location))

        instructions.append(mips.AddNode(reg1, reg1, reg2))

        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(reg1, dest_location))

        self.free_reg(reg1)
        self.free_reg(reg2)

        return instructions
    
    @visitor.when(cil.MinusNode)
    def visit(self, node):
        instructions = []

        reg1 = self.get_free_reg()
        reg2 = self.get_free_reg()

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            left_location = self.get_var_location(node.left)
            instructions.append(mips.LoadWordNode(reg1, left_location))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            right_location = self.get_var_location(node.right)
            instructions.append(mips.LoadWordNode(reg2, right_location))

        instructions.append(mips.SubNode(reg1, reg1, reg2))

        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(reg1, dest_location))

        self.free_reg(reg1)
        self.free_reg(reg2)

        return instructions
    
    @visitor.when(cil.StarNode)
    def visit(self, node):
        instructions = []

        reg1 = self.get_free_reg()
        reg2 = self.get_free_reg()

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            left_location = self.get_var_location(node.left)
            instructions.append(mips.LoadWordNode(reg1, left_location))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            right_location = self.get_var_location(node.right)
            instructions.append(mips.LoadWordNode(reg2, right_location))

        instructions.append(mips.MultiplyNode(reg1, reg1, reg2))

        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(reg1, dest_location))

        self.free_reg(reg1)
        self.free_reg(reg2)

        return instructions
    
    @visitor.when(cil.DivNode)
    def visit(self, node):
        instructions = []

        reg1 = self.get_free_reg()
        reg2 = self.get_free_reg()

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            left_location = self.get_var_location(node.left)
            instructions.append(mips.LoadWordNode(reg1, left_location))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            right_location = self.get_var_location(node.right)
            instructions.append(mips.LoadWordNode(reg2, right_location))

        instructions.append(mips.DivideNode(reg1, reg2))

        dest_location = self.get_var_location(node.dest)
        
        instructions.append(mips.MoveFromLowNode(reg1))
        instructions.append(mips.StoreWordNode(reg1, dest_location))

        self.free_reg(reg1)
        self.free_reg(reg2)

        return instructions

    @visitor.when(cil.ComplementNode)
    def visit(self, node):
        instructions = []

        reg1 = self.get_free_reg()
        
        if type(node.obj) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.obj))
        else:
            left_location = self.get_var_location(node.obj)
            instructions.append(mips.LoadWordNode(reg1, left_location))

        dest_location = self.get_var_location(node.dest)
        
        instructions.append(mips.ComplementNode(reg1, reg1))
        instructions.append(mips.AddInmediateNode(reg1, reg1, 1))
        instructions.append(mips.StoreWordNode(reg1, dest_location))

        self.free_reg(reg1)

        return instructions



    @visitor.when(cil.LessEqualNode)
    def visit(self, node):
        instructions = []
        #Save $a0, $a1, $v0

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            left_location = self.get_var_location(node.left)
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], left_location))
        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            right_location = self.get_var_location(node.right)
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], right_location))
        
        instructions.append(mips.JumpAndLinkNode('less_equal'))
        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        return instructions

    @visitor.when(cil.LessNode)
    def visit(self, node):
        instructions = []
        #Save $a0, $a1, $v0

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            left_location = self.get_var_location(node.left)
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], left_location))
        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            right_location = self.get_var_location(node.right)
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], right_location))
        
        instructions.append(mips.JumpAndLinkNode('less'))
        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        return instructions
    
    @visitor.when(cil.ReadStrNode)
    def visit(self, node):
        instructions = []
        #Save $v0
        instructions.append(mips.JumpAndLinkNode("read_str"))
        
        dest_location = self.get_var_location(node.dest)
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        return instructions

    @visitor.when(cil.LengthNode)
    def visit(self, node):
        instructions = []
        #save $a0 $v0

        src_location = self.get_var_location(node.source)
        dest_location = self.get_var_location(node.dest)

        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], src_location))
        instructions.append(mips.JumpAndLinkNode("len"))
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        return instructions

    @visitor.when(cil.ReadIntNode)
    def visit(self, node):
        instructions = []
        #save $v0
        dest_location = self.get_var_location(node.dest)

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 5))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        return instructions

    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        instructions = []

        #save $a0, $a1, $a2, $v0

        prefix_location = self.get_var_location(node.prefix)
        suffix_location = self.get_var_location(node.suffix)
        lenght_location = self.get_var_location(node.length)
        dest_location = self.get_var_location(node.dest)

        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], prefix_location))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], suffix_location))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[2], lenght_location))
        instructions.append(mips.JumpAndLinkNode("concat"))
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        return instructions

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        instructions = []

        #save $a0, $a1, $a2, $v0

        str_location = self.get_var_location(node.str_value)
        dest_location = self.get_var_location(node.dest)

        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], str_location))

        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.index))
        else:
            index_location = self.get_var_location(node.index)
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], index_location))
        
        if type(node.length) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[2], node.length))
        else:
            lenght_location = self.get_var_location(node.length)
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[2], lenght_location))
        
        instructions.append(mips.JumpAndLinkNode("substr"))
        instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        return instructions


        
    











    
    
        






class UsedRegisterFinder:
    def __init__(self):
        self.used_registers = set()

    def get_used_registers(self, instructions):
        self.used_registers = set()
        
        for inst in instructions:
            self.visit(inst)
        self.used_registers = set.difference(self.used_registers, set([mips.SP_REG, mips.FP_REG, mips.V0_REG]))
        return [reg for reg in self.used_registers]


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(mips.LoadInmediateNode)
    def visit(self, node):
        self.used_registers.add(node.reg)
    
    @visitor.when(mips.LoadAddressNode)
    def visit(self, node):
        self.used_registers.add(node.reg)
    
    @visitor.when(mips.AddInmediateNode)
    def visit(self, node):
        self.used_registers.add(node.dest)
    
    @visitor.when(mips.MoveNode)
    def visit(self, node):
        self.used_registers.add(node.reg1)
    
    @visitor.when(mips.LoadWordNode)
    def visit(self, node):
        self.used_registers.add(node.reg)

    @visitor.when(mips.JumpAndLinkNode)
    def visit(self, node):
        self.used_registers.add(mips.RA_REG)

            

    
    








#Change Name
class FunctionDivider:
    def __init__(self):
        self.mark
        
        
    def divide_basics_blocks(self, intructions):
        self.mark = True
        for instruction in instructions:
            self.mark_leaders(instruction)

        blocks = []

        for instruction in instrucctions:
            if instruction.leader:
                block.append([instruction])
            block[-1].append(instruction)
        
        return blocks

    def create_flow_graph(blocks): #graph between blocks in a same function does not include relations between functions
        graph = [[-1 for _ in range(len(blocks))] for _ in range(len(blocks)) ]
        labels = {b.name : i for i, b in enumerate(blocks) if type(b[0]) == cil.LabelNode}

        for i, block in enumerate(blocks):
            tp = type(block[-1])
            if tp == cil.GotoNode:
                graph[i][labels[block[-1].label]] = 1

            elif tp == cil.GotoIfNode:
                graph[i][labels[block[-1].label]] = 1
                graph[i][min(len(blocks)-1, i+1)] = 1

            elif tp == cil.DynamicCallNode:
                pass #analize what to do with function calls
            elif tp == cil.StaticCallNode:
                pass #analize what to do with function calls

            return graph            



    @visitor.on('instruction')
    def mark_leaders(self, instruction):
        pass

    @visitor.when(cil.LabelNode)
    def mark_leaders(self, instruction):
        instruction.leader = True
        self.mark = False

    @visitor.when(cil.GotoNode)
    def mark_leaders(self, instruction):
        self.mark = True

    @visitor.when(cil.GotoIfNode)
    def mark_leaders(self, instruction):
        self.mark = True
    
    @visitor.when(cil.DynamicCallNode)
    def mark_leaders(self, instruction):
        self.mark = True

    @visitor.when(cil.StaticCallNode)
    def mark_leaders(self, instruction):
        self.mark = True
    
    @visitor.when(cil.InstructionNode)
    def mark_leaders(self, instruction):
        instruction.leader = self.mark
        self.mark = False

     











#TEST
CIL_TYPE_1 = cil.TypeNode("myType")
CIL_TYPE_1.attributes = ["attr1", "attr2", "attr3"]
CIL_TYPE_1.methods  = [("method1", "func1"), ("method2", "func2"), ("method3", "func3"), ("method4", "func4")]
CIL_TYPE_2 = cil.TypeNode("myType2")
CIL_TYPE_2.attributes = ["attr1", "attr2"]
CIL_TYPE_2.methods  = [("method1", "func5"), ("method2", "func2"), ("method3", "func6"), ("method4", "func7")]
CIL_AST_TEST = cil.ProgramNode([],[],[])
CIL_AST_TEST.dottypes = [CIL_TYPE_1, CIL_TYPE_2]


# if __name__ == '__main__':
def test():
    conv = CILToMIPSVisitor()
    conv.visit(CIL_AST_TEST)
    for d in conv.dotdata:
        print(d)
    
