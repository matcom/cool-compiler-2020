import itertools as itt

from ...visitors import visitor
from ..cil import cil
from ..mips import mips
from random import choice
from collections import defaultdict


class MemoryManager:
    def __init__(self, registers, function_for_assign):
        self.registers = registers
        self.func = function_for_assign
    
    def get_reg_for_var(self, var):
        index = self.func(var)
        if index == -1:
            return None 
        return self.registers[index]  
    
    def get_reg_unusued(self, used = []):
        possibles = list(set(self.registers).difference(set(used)))
        return choice(possibles)


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
    def __init__(self, label_generator = LabelGenerator()):
        self._label_generator = label_generator
        self.memory_manager = None
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

        self._data_section["default_str"] = mips.StringConst("default_str", "") 
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
        defaults = []
        if node.name == "String":
            defaults = [('value', 'default_str'), ('length', 'type_4_proto')]
        new_type = mips.MIPSType(type_label, name_label, node.attributes, methods, len(self._types), default=defaults)

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

        ra = RegistersAllocator()

        if len(node.instructions):
            reg_for_var = ra.get_registers_for_variables(node.instructions, node.params, len(mips.REGISTERS))
            self.memory_manager = MemoryManager(mips.REGISTERS, lambda x : reg_for_var[x])

        for instruction in node.instructions:
            self.collect_labels_in_func(instruction)

        initial_instructions = []
        if self.in_entry_function():
            initial_instructions.append(mips.JumpAndLinkNode("mem_manager_init"))

        initial_instructions.extend(mips.push_register(mips.FP_REG))
        initial_instructions.append(mips.AddInmediateNode(mips.FP_REG, mips.SP_REG, 4))
        initial_instructions.append(mips.AddInmediateNode(mips.SP_REG, mips.SP_REG, -size_for_locals))

        code_instructions = []
        
        code_instructions = list(itt.chain.from_iterable([self.visit(instruction) for instruction in node.instructions]))
            
        final_instructions = []

        for param in params:
            reg = self.memory_manager.get_reg_for_var(param)
            if reg is not None:
                code_instructions.insert(0,mips.LoadWordNode(reg, self.get_var_location(param)))
        
        if not self.in_entry_function():
            used_regs = used_regs_finder.get_used_registers(code_instructions)
            for reg in used_regs:
                initial_instructions.extend(mips.push_register(reg))
            
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
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], node.name))
            instructions.extend(mips.push_register(mips.ARG_REGISTERS[0]))
        else:
            reg = self.memory_manager.get_reg_for_var(node.name)
            if reg is None:
                reg = mips.ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.name)))
            instructions.extend(mips.push_register(reg))
        return instructions
    
    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        instructions = []
        label = self._name_func_map[node.function]
        instructions.append(mips.JumpAndLinkNode(label))            

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        if self._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(mips.SP_REG, mips.SP_REG, self._pushed_args * mips.ATTR_SIZE))
            self.clean_pushed_args()
        return instructions
    
    @visitor.when(cil.AssignNode)
    def visit(self, node):
        instructions = []
        
        reg1 = None
        if type(node.source) == cil.VoidNode:
            reg1 = mips.ZERO_REG
        elif node.source.isnumeric():
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, int(node.source)))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.source)
            if reg1 is None:
                reg1 = mips.ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.source)))

        reg2 = self.memory_manager.get_reg_for_var(node.dest)
        if reg2 is None:
            instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg2, reg1))

        return instructions
    
    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        instructions = []

        tp = 0
        if node.type.isnumeric():
            tp = node.type
        else:
            tp = self._types[node.type].index

        reg1 = self.memory_manager.get_reg_unusued()
        reg2 = self.memory_manager.get_reg_unusued([reg1])
        instructions.extend(mips.push_register(reg1))
        instructions.extend(mips.push_register(reg2))
                
        instructions.append(mips.LoadInmediateNode(reg1, tp))

        instructions.extend(mips.create_object(reg1, reg2))
        
        instructions.extend(mips.pop_register(reg2))
        instructions.extend(mips.pop_register(reg1))
        
        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg3, mips.V0_REG))
        
        return instructions
    
    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        instructions = []

        if node.value is None:
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0))
        elif isinstance(node.value, int):
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, node.value))
        elif isinstance(node.value, cil.VoidNode):
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0))
        else:
            reg = self.memory_manager.get_reg_for_var(node.value)
            if reg is None:
                instructions.append(mips.LoadWordNode(mips.V0_REG, self.get_var_location(node.value)))
            else:
                instructions.append(mips.MoveNode(mips.V0_REG, reg))
        return instructions
    
    @visitor.when(cil.LoadNode)
    def visit(self, node):
        instructions = []

        string_location = mips.LabelRelativeLocation(self._data_section[node.msg.name].label, 0)
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.LoadAddressNode(mips.ARG_REGISTERS[0], string_location))
            instructions.append(mips.StoreWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.LoadAddressNode(reg, string_location))

        return instructions
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 1))

        reg = self.memory_manager.get_reg_for_var(node.value)
        if reg is None:
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.value)))
        else:
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))

        instructions.append(mips.SyscallNode())

        return instructions
    
    @visitor.when(cil.PrintStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4))

        reg = self.memory_manager.get_reg_for_var(node.value)
        if reg is None:
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0]. self.get_var_location(node.value)))
        else:
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        instructions.append(mips.SyscallNode())

        return instructions
    
    @visitor.when(cil.TypeNameNode)
    def visit(self, node):
        instructions = []
        
        reg1 = self.memory_manager.get_reg_for_var(node.source)
        pushed = False
        if reg1 is None:                
            reg1 = self.memory_manager.get_reg_unusued()
            instructions.extend(mips.push_register(reg1))
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.source)))
            pushed = True
        
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], mips.RegisterRelativeLocation(reg1, 0))) 

        if pushed:
            instructions.extend(mips.pop_register(reg1))

        instructions.append(mips.ShiftLeftLogicalNode(mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[0], 2))
        instructions.append(mips.LoadAddressNode(mips.ARG_REGISTERS[1], mips.TYPENAMES_TABLE_LABEL))
        instructions.append(mips.AddUnsignedNode(mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[1]))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[0], 0)))
        
        reg2 = self.memory_manager.get_reg_for_var(node.dest)
        if reg2 is None:
            instructions.append(mips.StoreWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg2, mips.ARG_REGISTERS[0]))

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

        dest = node.dest if type(node.dest) == str else node.dest.name
        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(node.computed_type) == str else node.computed_type.name

        reg = self.memory_manager.get_reg_for_var(obj)
        if reg is None:
            reg = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(reg, self.get_var_location(obj)))
        
        tp = self._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(reg, offset)))

        reg = self.memory_manager.get_reg_for_var(dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.ARG_REGISTERS[1], self.get_var_location(dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.ARG_REGISTERS[1]))

        return instructions
    
    @visitor.when(cil.SetAttribNode)
    def visit(self, node):
        instructions = []

        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(node.computed_type) == str else node.computed_type.name

        tp = self._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE

        reg1 = self.memory_manager.get_reg_for_var(obj)
        if reg1 is None:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(obj)))

        reg2 = None
        if type(node.value) == int:
            reg2 = instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.value))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.value)
            if reg2 is None:
                reg2 = mips.ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.value)))

        instructions.append(mips.StoreWordNode(reg2, mips.RegisterRelativeLocation(reg1, offset)))
        
        return instructions
    
    @visitor.when(cil.CopyNode)
    def visit(self, node):
        instructions = []

        pushed = False
        reg = self.memory_manager.get_reg_for_var(node.source)
        if reg is None:
            reg = self.memory_manager.get_reg_unusued()
            instructions.extend(mips.push_register(reg))
            instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.source)))
            pushed = True
                
        instructions.extend(mips.copy_object(reg, mips.ARG_REGISTERS[3]))            

        if pushed:
            instructions.extend(mips.pop_register(reg))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions
    
    @visitor.when(cil.EqualNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], node.left))
        elif type(node.left) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], 0))
        else:
            reg = self.memory_manager.get_reg_for_var(node.left)
            if reg is None:
                instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.left)))
            else:
                instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.right))
        elif type(node.right) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], 0))
        else:
            reg = self.memory_manager.get_reg_for_var(node.right)
            if reg is None:
                instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], self.get_var_location(node.right)))
            else:
                instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))

        instructions.append(mips.JumpAndLinkNode("equals"))            

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))
        
        return instructions
    
    @visitor.when(cil.EqualStrNode)
    def visit(self, node):
        instructions = []

        reg = self.memory_manager.get_reg_for_var(node.left)
        if reg is None:
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.left)))
        else:
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        
        reg = self.memory_manager.get_reg_for_var(node.right)
        if reg is None:
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], self.get_var_location(node.right)))
        else:
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))

        instructions.append(mips.JumpAndLinkNode("equal_str"))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))
        
        return instructions

    @visitor.when(cil.LabelNode)
    def visit(self, node):
        return [mips.LabelNode(self.get_mips_label(node.label))]

    @visitor.when(cil.GotoIfNode)
    def visit(self, node):
        instructions = []

        mips_label = self.get_mips_label(node.label)

        reg = self.memory_manager.get_reg_for_var(node.condition)
        if reg is None:
            reg = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.condition)))  
        
        instructions.append(mips.BranchOnNotEqualNode(reg, mips.ZERO_REG, mips_label))
        
        return instructions
    
    @visitor.when(cil.GotoNode)
    def visit(self, node):
        mips_label = self.get_mips_label(node.label)
        return [mips.JumpNode(mips_label)]

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        instructions = []

        reg1 = self.memory_manager.get_reg_for_var(node.obj)
        if reg1 is None:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.obj)))
        
        reg2 = self.memory_manager.get_reg_for_var(node.dest) 
        if reg2 is None:                
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(reg1, 0)))
            instructions.append(mips.StoreWordNode(mips.ARG_REGISTERS[1], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.LoadWordNode(reg2, mips.RegisterRelativeLocation(reg1, 0)))

        return instructions

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        instructions = []

        comp_tp = self._types[node.computed_type]
        method_index = list(comp_tp.methods).index(node.method)
        reg = self.memory_manager.get_reg_for_var(node.type)
        if reg is None:
            reg = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.type)))

        instructions.append(mips.LoadAddressNode(mips.ARG_REGISTERS[1], mips.PROTO_TABLE_LABEL))
        instructions.append(mips.ShiftLeftLogicalNode(mips.ARG_REGISTERS[2], reg, 2))
        instructions.append(mips.AddUnsignedNode(mips.ARG_REGISTERS[1], mips.ARG_REGISTERS[1], mips.ARG_REGISTERS[2]))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[1], 0)))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[1], 8)))
        instructions.append(mips.AddInmediateUnsignedNode(mips.ARG_REGISTERS[1], mips.ARG_REGISTERS[1], method_index * 4))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[1], 0)))
        instructions.append(mips.JumpRegisterAndLinkNode(mips.ARG_REGISTERS[1]))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))
        
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

        save = False
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            reg = mips.ARG_REGISTERS[0]
            save = True
            
        instructions.append(mips.LoadAddressNode(reg, mips.TYPENAMES_TABLE_LABEL))

        tp_number = self._types[node.name].index
        instructions.append(mips.AddInmediateUnsignedNode(reg, reg, tp_number*4))
        instructions.append(mips.LoadWordNode(reg, mips.RegisterRelativeLocation(reg, 0)))

        if save:
            instructions.append(mips.StoreWordNode(reg, self.get_var_location(node.dest)))

        return instructions
    
    @visitor.when(cil.PlusNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.left)
            if reg1 is None:
                reg1 = mips.ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        if type(node.right) == int:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.right)
            if reg2 is None:
                reg2 = mips.ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))

        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.AddNode(mips.ARG_REGISTERS[0], reg1, reg2))
            instructions.append(mips.StoreWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.AddNode(reg3, reg1, reg2))

        return instructions
    
    @visitor.when(cil.MinusNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.left)
            if reg1 is None:
                reg1 = mips.ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.right)
            if reg2 is None:
                reg2 = mips.ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))

        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.SubNode(mips.ARG_REGISTERS[0], reg1, reg2))
            instructions.append(mips.StoreWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.SubNode(reg3, reg1, reg2))

        return instructions
    
    @visitor.when(cil.StarNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.left)
            if reg1 is None:
                reg1 = mips.ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        if type(node.right) == int:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.right)
            if reg2 is None:
                reg2 = mips.ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))

        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.MultiplyNode(mips.ARG_REGISTERS[0], reg1, reg2))
            instructions.append(mips.StoreWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MultiplyNode(reg3, reg1, reg2))

        return instructions
    
    @visitor.when(cil.DivNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.left)
            if reg1 is None:
                reg1 = mips.ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        if type(node.right) == int:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.right)
            if reg2 is None:
                reg2 = mips.ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))

        instructions.append(mips.DivideNode(reg1, reg2))
        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.MoveFromLowNode(mips.ARG_REGISTERS[0]))
            instructions.append(mips.StoreWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveFromLowNode(reg3))

        return instructions

    @visitor.when(cil.ComplementNode)
    def visit(self, node):
        instructions = []

        reg1 = None
        
        if type(node.obj) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.obj))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.obj)
            if reg1 is None:
                reg1 = mips.ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.obj)))

        reg2 = self.memory_manager.get_reg_for_var(node.dest)
        if reg2 is None:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.ComplementNode(reg2, reg1))
            instructions.append(mips.AddInmediateNode(reg2, reg2, 1))
            instructions.append(mips.StoreWordNode(reg2, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.ComplementNode(reg2, reg1))
            instructions.append(mips.AddInmediateNode(reg2, reg2, 1))

        return instructions

    @visitor.when(cil.LessEqualNode)
    def visit(self, node):
        instructions = []
        #Save $a0, $a1, $v0

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], node.left))
        else:
            reg = self.memory_manager.get_reg_for_var(node.left)
            if reg is None:
                instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.left)))
            else:
                instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.right))
        else:
            reg = self.memory_manager.get_reg_for_var(node.right)
            if reg is None:
                instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], self.get_var_location(node.right)))
            else:
                instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))
        
        instructions.append(mips.JumpAndLinkNode('less_equal'))
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions

    @visitor.when(cil.LessNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], node.left))
        else:
            reg = self.memory_manager.get_reg_for_var(node.left)
            if reg is None:
                instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.left)))
            else:
                instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.right))
        else:
            reg = self.memory_manager.get_reg_for_var(node.right)
            if reg is None:
                instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], self.get_var_location(node.right)))
            else:
                instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))
        
        instructions.append(mips.JumpAndLinkNode('less'))
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions
    
    @visitor.when(cil.ReadStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.JumpAndLinkNode("read_str"))
        
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions

    @visitor.when(cil.LengthNode)
    def visit(self, node):
        instructions = []

        reg = self.memory_manager.get_reg_for_var(node.source)
        if reg is None:
            reg = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.source)))

        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        instructions.append(mips.JumpAndLinkNode("len"))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions

    @visitor.when(cil.ReadIntNode)
    def visit(self, node):
        instructions = []

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 5))
        instructions.append(mips.SyscallNode())
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions

    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        instructions = []

        reg = self.memory_manager.get_reg_for_var(node.prefix)
        if reg is None:
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.prefix)))
        else:
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
            
        reg = self.memory_manager.get_reg_for_var(node.suffix)
        if reg is None:
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], self.get_var_location(node.suffix)))
        else:
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))

        reg = self.memory_manager.get_reg_for_var(node.length)
        if reg is None:
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[2], self.get_var_location(node.lenght)))
        else:
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[2], reg))

        instructions.append(mips.JumpAndLinkNode("concat"))
        
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        instructions = []

        reg = self.memory_manager.get_reg_for_var(node.str_value)
        if reg is None:
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.str_value)))
        else:
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))

        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.index))
        else:
            reg = self.memory_manager.get_reg_for_var(node.index)
            if reg is None:
                instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], self.get_var_location(node.index)))
            else:
                instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))
        
        if type(node.length) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[2], node.length))
        else:
            reg = self.memory_manager.get_reg_for_var(node.length)
            if reg is None:
                instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[2], self.get_var_location(node.length)))
            else:
                instructions.append(mips.MoveNode(mips.ARG_REGISTERS[2], reg))
        
        instructions.append(mips.JumpAndLinkNode("substr"))
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))
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
    
    @visitor.when(mips.JumpRegisterAndLinkNode)
    def visit(self, node):
        self.used_registers.add(mips.RA_REG)


#Change Name
class RegistersAllocator:
    def __init__(self):
        self.mark = False
        
    def get_registers_for_variables(self, instructions, params, n):
        self.numbered_instructions(instructions)
        basic_blocks = self.divide_basics_blocks(instructions)
        flow_graph = RegistersAllocator.create_flow_graph(basic_blocks)
        gk, io = self.liveness_analysis((basic_blocks, flow_graph), params)
        interference = RegistersAllocator.interference_compute(gk, io)
        return RegistersAllocator.assign_registers(interference, n)

    def divide_basics_blocks(self, instructions):
        self.mark = True
        for instruction in instructions:
            self.mark_leaders(instruction)

        blocks = []

        for instruction in instructions:
            if instruction.leader:
                blocks.append([instruction])
            else:
                blocks[-1].append(instruction)
        
        return blocks

    def liveness_analysis(self, graph, params):
        blocks, ady_list = graph

        instructions = []
        for block in blocks:
            instructions.extend(block)
        instructions_total = len(instructions)

        suc = [ 0 for _ in range(instructions_total) ]
        for block_index, block in enumerate(blocks):
            for ins_index, instruction in enumerate(block):
                if ins_index == len(block) - 1:
                    ady = [ i for i in range(len(blocks)) if ady_list[block_index][i] == 1 ]
                    suc[instruction.number] = [ blocks[b][0].number for b in ady ]
                else:
                    suc[instruction.number] = [ block[ins_index + 1].number ]
        
        gk = [self.gen_kill(inst) for inst in instructions] 
        io = RegistersAllocator.out_in_compute(suc, gk)
        gk = [([], [param.name for param in params ] )] + gk
        io = [([], io[0][0])] + io

        return gk, io

    @staticmethod
    def interference_compute(gk, in_out):
        neigs = {}
        for g, k in gk:
            for v in g:
                neigs[v] = set()
            for v in k:
                neigs[v] = set()

        for i,(_, k) in enumerate(gk):
            for v in k:
                neigs[v].update(in_out[i][1])

        for k, v in neigs.items():
            for n in v:
                neigs[n].add(k)

        for k, v in neigs.items():
            neigs[k] = list(v.difference([k]))

        return neigs

    @staticmethod
    def assign_registers(interference_graph, n):
        stack = []
        var_registers = defaultdict(lambda : -1)
        nodes = set(interference_graph.keys())

        def myLen(l):
            count = 0
            for v in l:
                if v in nodes:
                    count += 1
            return count

        #remove nodes with less than n edges
        while nodes:
            to_remove = None 
            for node in nodes:
                if myLen(interference_graph[node]) < n:
                    stack.append((node, interference_graph[node]))
                    to_remove = node
                    break
            
            if to_remove:
                nodes.remove(to_remove)
            else:
                selection = choice(list(nodes))
                stack.append((selection, interference_graph[selection]))
                nodes.remove(selection)
        
        while stack:
            node, ady = stack.pop()
            regs = set(range(n))
            for neig in ady:
                reg = var_registers[neig]
                if reg != -1:
                    try:
                        regs.remove(reg)
                    except:
                        pass
            if regs:
                var_registers[node] = min(regs)    
            else:
                var_registers[node] = -1
        
        return var_registers 

    @staticmethod
    def out_in_compute(suc, gk):
        n_instructions = len(gk)
        in_out = [[set(), set()] for _ in range(n_instructions)]
        next_in_out = [[set(), set()] for _ in range(n_instructions)]

        def add(set1, set2):
            return not set2.issubset(set1)

        changed = True
        while changed:
            changed = False
            for i in range(n_instructions)[::-1]:
                for i_suc in suc[i]:
                    if i_suc < i:
                        changed |= add(next_in_out[i][1], in_out[i_suc][0])
                        next_in_out[i][1] = next_in_out[i][1].union(in_out[i_suc][0])
                    else:
                        changed |= add(next_in_out[i][1], next_in_out[i_suc][0])
                        next_in_out[i][1] = next_in_out[i][1].union(next_in_out[i_suc][0])

                g_i = set(gk[i][0])
                k_i = set(gk[i][1])
                new = g_i.union(next_in_out[i][1].difference(k_i))
                changed |= add(next_in_out[i][0], new)
                next_in_out[i][0] = next_in_out[i][0].union(new)

            in_out = next_in_out
        
        return in_out

    @staticmethod
    def create_flow_graph(blocks): #graph between blocks in a same function does not include relations between functions
        graph = [[-1 for _ in range(len(blocks))] for _ in range(len(blocks)) ]
        labels = {b[0].label : i for i, b in enumerate(blocks) if isinstance(b[0], cil.LabelNode)}

        for i, block in enumerate(blocks):
            if isinstance(block[-1], cil.GotoNode):
                graph[i][labels[block[-1].label]] = 1
            elif isinstance(block[-1], cil.GotoIfNode):
                graph[i][labels[block[-1].label]] = 1
                graph[i][i + 1] = 1 if i + 1 < len(blocks) else -1
            elif i != len(blocks) - 1:
                graph[i][i + 1] = 1
                
        return graph            

    @staticmethod
    def numbered_instructions(instructions):
        for i, instr in enumerate(instructions):
            instr.number = i

    @visitor.on('instruction')
    def gen_kill(self, instruction):
        pass
    
    @visitor.when(cil.ArgNode)
    def gen_kill(self, instruction):
        if isinstance(instruction.name, int):
            return ([], [])
        return ([instruction.name], [])

    @visitor.when(cil.StaticCallNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])
    
    @visitor.when(cil.AssignNode)
    def gen_kill(self, instruction):
        gen = []
        if isinstance(instruction.source, str):
            if not instruction.source.isnumeric():
                gen = [ instruction.source ]
        return (gen, [ instruction.dest ]) 

    @visitor.when(cil.AllocateNode)
    def gen_kill(self, instruction):
        return ([], [ instruction.dest ])
    
    @visitor.when(cil.ReturnNode)
    def gen_kill(self, instruction):
        gen = [ instruction.value ] if isinstance(instruction.value, str) else []
        return (gen, [])
    
    @visitor.when(cil.LoadNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])
    
    @visitor.when(cil.PrintIntNode)
    def gen_kill(self, instruction):
        return ([ instruction.value ], []) 
    
    @visitor.when(cil.PrintStrNode)
    def gen_kill(self, instruction):
        return ([ instruction.value ], [])
    
    @visitor.when(cil.TypeNameNode)
    def gen_kill(self, instruction):
        return ([ instruction.source ], [ instruction.dest ])
    
    @visitor.when(cil.ExitNode)
    def gen_kill(self, instruction):
        return ( [], [])
    
    @visitor.when(cil.GetAttribNode)
    def gen_kill(self, instruction):
        return ([ instruction.obj ], [ instruction.dest ])
        
    @visitor.when(cil.SetAttribNode)
    def gen_kill(self, instruction):
        gen = [ instruction.obj ]
        if not isinstance(instruction.value, int):
            gen.append(instruction.value)
        return (gen, [])
    
    @visitor.when(cil.CopyNode)
    def gen_kill(self, instruction):
        return ([ instruction.source ], [ instruction.dest ])
    
    @visitor.when(cil.ArithmeticNode)
    def gen_kill(self, instruction):
        gen = [x for x in [instruction.left, instruction.right] if isinstance(x, str)]
        return (gen, [instruction.dest])
        
    @visitor.when(cil.GotoIfNode)
    def gen_kill(self, instruction):
        return ([ instruction.condition ], [])
    
    @visitor.when(cil.GotoNode)
    def gen_kill(self, instruction):
        return ([], [])

    @visitor.when(cil.TypeOfNode)
    def gen_kill(self, instruction):
        return ([instruction.obj], [instruction.dest])

    @visitor.when(cil.DynamicCallNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])

    @visitor.when(cil.NameNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])

    @visitor.when(cil.ComplementNode)
    def gen_kill(self, instruction):
        gen = [ instruction.obj ] if isinstance(instruction.obj, str) else []
        return (gen, [ instruction.dest ])

    @visitor.when(cil.ReadStrNode)
    def gen_kill(self, instruction):
        return ([], [ instruction.dest ])

    @visitor.when(cil.LengthNode)
    def gen_kill(self, instruction):
        return ([ instruction.source ], [ instruction.dest ])

    @visitor.when(cil.ReadIntNode)
    def gen_kill(self, instruction):
        return ([], [ instruction.dest ])

    @visitor.when(cil.ConcatNode)
    def gen_kill(self, instruction):
        return ( [ instruction.prefix, instruction.suffix ], [ instruction.dest ])

    @visitor.when(cil.SubstringNode)
    def gen_kill(self, instruction):
        gen = [ instruction.str_value ]
        if isinstance(instruction.index, str):
            gen.append(instruction.index)
        if isinstance(instruction.length, str):
            gen.append(instruction.length)

        return (gen, [ instruction.dest ])
    
    @visitor.when(cil.LabelNode)
    def gen_kill(self, instruction):
        return ([], [])
    
    @visitor.when(cil.ErrorNode)
    def gen_kill(self, instruction):
        return ([], [])

    @visitor.on('instruction')
    def mark_leaders(self, instruction):
        pass

    @visitor.when(cil.LabelNode)
    def mark_leaders(self, instruction):
        instruction.leader = True
        self.mark = False

    @visitor.when(cil.GotoNode)
    def mark_leaders(self, instruction):
        instruction.leader = self.mark
        self.mark = True

    @visitor.when(cil.GotoIfNode)
    def mark_leaders(self, instruction):
        instruction.leader = self.mark
        self.mark = True
    
    @visitor.when(cil.InstructionNode)
    def mark_leaders(self, instruction):
        instruction.leader = self.mark
        self.mark = False
