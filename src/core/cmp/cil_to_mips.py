import itertools as itt
import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.mips as mips
from random import choice
from collections import defaultdict
from core.cmp.utils import CountDict
from pprint import pprint


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

class MemoryManager:
    def __init__(self, registers, vars_with_addresses, function_for_assign):
        self.registers = registers
        self.func = function_for_assign
        self.place_in_memory = dict(vars_with_addresses)
        self.updated_in_mem = {var : True for var, _ in vars_with_addresses} 
        self.vars_in_reg = { reg : [] for reg in registers }
        self.locked = []
    
    def lock(self, reg):
        self.locked.append(reg)

    def value_updated(self, var):
        self.updated_in_mem[var] = False

    def use_register(self, reg, var):
        instructions = []
        for v in self.vars_in_reg[reg]:
            if v == var:
                continue
            instructions.extend(self.remove_from_reg(reg, v))
        
        if not var in self.vars_in_reg[reg]:
            self.vars_in_reg[reg].append(var)
        
        return instructions
    
    def use_register_for_value(self, reg):
        instructions = []
        for v in self.vars_in_reg[reg]:
            instructions.extend(self.remove_from_reg(reg, v))
        return instructions

    def load_in_register(self, reg, var):
        if var in self.vars_in_reg[reg]:
            return []

        instructions = []
        for v in self.vars_in_reg[reg]:
            instructions.extend(self.remove_from_reg(reg, v))
        location = self.place_in_memory[var]
        instructions.append( mips.LoadWordNode(reg, location))
        self.vars_in_reg[reg].append(var)
        return instructions
    
    def load_value_in_register(self, reg, val):
        instructions = []
        for v in self.vars_in_reg[reg]:
            instructions.extend(self.remove_from_reg(reg, v))
        instructions.append(mips.LoadInmediateNode(reg, val))
        return instructions
    
    def remove_from_reg(self, reg, var):
        instructions = []
        if var in self.vars_in_reg[reg]:
            if not self.is_in_mem(var):
                location = self.place_in_memory[var]
                instructions.append(mips.StoreWordNode(reg, location))
            self.vars_in_reg[reg].remove(var)
        return instructions
    
    def is_in_mem(self, var):
        return self.updated_in_mem[var]

    def get_register(self, var):
        index = self.func(var)
        if index == -1:
            return choice(self.registers)
        return self.registers[index]  

    def get_register_for_value(self):
        best = None
        occu = 0
        for reg, var in self.vars_in_reg.items():
            if reg in self.locked:
                continue
            if not best:
                best, occu = reg, len(var)
            if len(var) < occu:
                best, occu = reg, len(var)
        
        self.locked.append(best)
        return best
    
    def free(self, reg):
        try:
            self.locked.remove(reg)
        except:
            pass
    
    def save_values(self):
        instructions = []
        for reg in self.vars_in_reg:
            while self.vars_in_reg[reg]:
                instructions.extend(self.remove_from_reg(reg, self.vars_in_reg[reg][0]))
        return instructions


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

        for ins in enumerate(node.instructions):
            print(ins)
        
        new_func = mips.FunctionNode(label, params, localvars)
        self.register_function(node.name, new_func)
        self.init_function(new_func)

        ra = RegistersAllocator()
        reg_for_var = ra.get_registers_for_variables(node.instructions, node.params, len(mips.REGISTERS))

        vars_with_addresses = []
        for var in params + localvars:
            vars_with_addresses.append((var, self.get_var_location(var)))
        
        self.memory_manager = MemoryManager(mips.REGISTERS, vars_with_addresses, lambda x : reg_for_var[x])




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
            raise e
            if node.name == "function_a2i_aux_at_A2I":
                print(e)
                # print(node.instructions)
            print(e)
            print(node.name)
            
            
        code_instructions.extend(self.memory_manager.save_values())

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
        #print(mips.PrintVisitor().visit(new_func))
        if "a2i" in node.name:
            input()

        self.finish_functions() 
        
       
    @visitor.when(cil.ArgNode)
    def visit(self, node):
        self.push_arg()
        instructions = []
        locked = None
        if type(node.name) == int:
            #reg = self.get_free_reg()
            reg = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg, node.name)
            instructions.extend(load)
            locked = reg
            #load_value = mips.LoadInmediateNode(reg, node.name)
            #instructions.append(load_value)
            instructions.extend(mips.push_register(reg))
        else:
            #reg = self.get_free_reg()
            # if not loaded:
            reg = self.memory_manager.get_register(node.name)
            load = self.memory_manager.load_in_register(reg, node.name)
            instructions.extend(load)
            #value_address = self.get_var_location(node.name)
            #load_value = mips.LoadWordNode(reg, value_address)
            #instructions.append(load_value)
            instructions.extend(mips.push_register(reg))
        if locked:
            self.memory_manager.free(locked)
        #self.free_reg(reg)
        return instructions
    
    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        
        instructions = []

        label = self._name_func_map[node.function]

        instructions.append(mips.JumpAndLinkNode(label))            

        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)
        #dst_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dst_location))
        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)

        if self._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(mips.SP_REG, mips.SP_REG, self._pushed_args * mips.ATTR_SIZE))
            self.clean_pushed_args()

        return instructions
    
    @visitor.when(cil.AssignNode)
    def visit(self, node):
        instructions = []
        
        #reg = self.get_free_reg()

        reg1 = None
        if type(node.source) == cil.VoidNode:
            reg1 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg1, 0)
            instructions.extend(load)
            #instructions.append(mips.LoadInmediateNode(reg, 0))
        elif node.source.isnumeric():
            reg1 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg1, int(node.source))
            instructions.extend(load)
            #load_value = mips.LoadInmediateNode(reg, int(node.source))
            #instructions.append(load_value)
        else:
            reg1 = self.memory_manager.get_register(node.source)
            load = self.memory_manager.load_in_register(reg1, node.source)
            instructions.extend(load)
            #value_location = self.get_var_location(node.source)
            #load_value = mips.LoadWordNode(reg, value_location)
            #instructions.append(load_value)

        reg2 = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg2, node.dest)
        instructions.extend(load)
        instructions.append(mips.MoveNode(reg2, reg1))
        self.memory_manager.value_updated(node.dest)
        self.memory_manager.free(reg1)
        #location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(reg2, location))
        #self.free_reg(reg)

        return instructions
    
    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        #TODO Save $a0, $a1 and $a2 registers if are beign used
        
        instructions = []

        #reg1 = self.get_free_reg()
        #reg2 = self.get_free_reg()

        tp = 0
        if node.type.isnumeric():
            tp = node.type
        else:
            tp = self._types[node.type].index

        reg1 = self.memory_manager.get_register_for_value()
        load = self.memory_manager.load_value_in_register(reg1, tp)
        instructions.extend(load)

        reg2 = self.memory_manager.get_register_for_value()
        load = self.memory_manager.use_register_for_value(reg2)
        instructions.extend(load)
        
        #instructions.append(mips.LoadInmediateNode(reg1, tp))
        instructions.extend(mips.create_object(reg1, reg2))
        
        #location = self.get_var_location(node.dest)
        self.memory_manager.free(reg1)
        self.memory_manager.free(reg2)
        
        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)

        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)
        #instructions.append(mips.StoreWordNode(mips.V0_REG, location))
        

        #self.free_reg(reg1)
        #self.free_reg(reg2)
        
        return instructions
    
    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        instructions = []

        if node.value is None:
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0))
        elif type(node.value) == int:
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, node.value))
        else:
            reg = self.memory_manager.get_register(node.value)
            load = self.memory_manager.load_in_register(reg, node.value)
            instructions.extend(load)
            #location = self.get_var_location(node.value)
            #instructions.append(mips.LoadWordNode(mips.V0_REG, location))
            instructions.append(mips.MoveNode(mips.V0_REG, reg))
            
        return instructions
    
    @visitor.when(cil.LoadNode)
    def visit(self, node):
        instructions = []

        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)


        #reg = self.get_free_reg()
        string_location = mips.LabelRelativeLocation(self._data_section[node.msg.name].label, 0)
        instructions.append(mips.LoadAddressNode(reg, string_location))
        self.memory_manager.value_updated(node.dest)

        #dest_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(reg, dest_location))

        #self.free_reg(reg)
        return instructions
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 1))

        #TODO save $a0 if is beign used
        #location = self.get_var_location(node.value)
        reg = self.memory_manager.get_register(node.value)
        load = self.memory_manager.load_in_register(reg, node.value)
        instructions.extend(load)
        #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], location))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        instructions.append(mips.SyscallNode())

        return instructions
    
    @visitor.when(cil.PrintStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4))

        #TODO save $a0 if is beign used
        reg = self.memory_manager.get_register(node.value)
        load = self.memory_manager.load_in_register(reg, node.value)
        instructions.extend(load)
        #location = self.get_var_location(node.value)
        #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], location))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        instructions.append(mips.SyscallNode())

        return instructions
    
    @visitor.when(cil.TypeNameNode)
    def visit(self, node):
        instructions = []
        
        #reg = self.get_free_reg()
        #reg2 = self.get_free_reg()
        reg1 = self.memory_manager.get_register(node.source)
        load = self.memory_manager.load_in_register(reg1, node.source)
        instructions.extend(load)
        self.memory_manager.lock(reg1)

        reg2 = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg2, node.dest)
        instructions.extend(load)
        self.memory_manager.lock(reg2)

        reg3 = self.memory_manager.get_register_for_value()
        load = self.memory_manager.use_register_for_value(reg3)
        instructions.extend(load)

        reg4 = self.memory_manager.get_register_for_value()
        load = self.memory_manager.use_register_for_value(reg4)
        instructions.extend(load)

        #src_location = self.get_var_location(node.source)
        #dst_location = self.get_var_location(node.dest)

        #instructions.append(mips.LoadWordNode(reg, src_location))
        instructions.append(mips.LoadWordNode(reg3, mips.RegisterRelativeLocation(reg1, 0)))
        instructions.append(mips.ShiftLeftLogicalNode(reg3, reg3, 2))
        instructions.append(mips.LoadAddressNode(reg4, mips.TYPENAMES_TABLE_LABEL))
        instructions.append(mips.AddUnsignedNode(reg3, reg3, reg4))
        instructions.append(mips.LoadWordNode(reg3, mips.RegisterRelativeLocation(reg3, 0)))
        #instructions.append(mips.StoreWordNode(reg1, dst_location))
        instructions.append(mips.MoveNode(reg2, reg3))
        self.memory_manager.value_updated(node.dest)

        self.memory_manager.free(reg1)
        self.memory_manager.free(reg2)
        self.memory_manager.free(reg3)
        self.memory_manager.free(reg4)

#        self.free_reg(reg)
#        self.free_reg(reg2)

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

        #reg = self.get_free_reg()
        
        dest = node.dest if type(node.dest) == str else node.dest.name
        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(node.computed_type) == str else node.computed_type.name
        print(obj)
        #input() 
        #obj_location = self.get_var_location(obj)
        #dst_location = self.get_var_location(dest)
        reg1 = self.memory_manager.get_register(obj)
        print(reg1)
        print(self.memory_manager.vars_in_reg.items())
        load = self.memory_manager.load_in_register(reg1, obj)
        instructions.extend(load)
        if obj == "local_a2i_at_A2I_return_value_of_substr_32":
            for i in load:
                print(mips.PrintVisitor().visit(i))
            input("here")
        #self.memory_manager.lock(reg1)

        reg2 = self.memory_manager.get_register(dest)
        load = self.memory_manager.use_register(reg2, dest)
        instructions.extend(load)

        #reg3 = self.memory_manager.get_register_for_value()
        #load = self.memory_manager.use_register_for_value(reg3)
        #instructions.extend(load)
        
        tp = self._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE

        #instructions.append(mips.LoadWordNode(reg, obj_location))

        #instructions.append(mips.LoadWordNode(reg, mips.RegisterRelativeLocation(reg, offset)))
        instructions.append(mips.LoadWordNode(reg2, mips.RegisterRelativeLocation(reg1, offset)))

       # instructions.append(mips.StoreWordNode(reg, dst_location))
        #instructions.append(mips.MoveNode(reg2, reg3))
        self.memory_manager.value_updated(dest)

       # self.memory_manager.free(reg1)
       # self.memory_manager.free(reg3)

        #self.free_reg(reg)
        return instructions
    
    @visitor.when(cil.SetAttribNode)
    def visit(self, node):
        instructions = []
        #reg1 = self.get_free_reg()
        #reg2 = self.get_free_reg()

        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(node.computed_type) == str else node.computed_type.name

        reg1 = self.memory_manager.get_register(obj)
        load = self.memory_manager.load_in_register(reg1, obj)
        instructions.extend(load)
        self.memory_manager.lock(reg1) 
        
        #obj_location = self.get_var_location(obj)

        tp = self._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE


        #instructions.append(mips.LoadWordNode(reg2, obj_location))

        reg2 = None
        if type(node.value) == int:
            reg2 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg2, node.value)
            instructions.extend(load)
            #instructions.append(mips.LoadInmediateNode(reg1, node.value))
        else:
            reg2 = self.memory_manager.get_register(node.value)
            load = self.memory_manager.load_in_register(reg2, node.value)
            instructions.extend(load)
            #src_location = self.get_var_location(node.value)
            #instructions.append(mips.LoadWordNode(reg1, src_location))
        
        instructions.append(mips.StoreWordNode(reg2, mips.RegisterRelativeLocation(reg1, offset)))

        self.memory_manager.free(reg1)
        self.memory_manager.free(reg2)
        

       # self.free_reg(reg1)
       # self.free_reg(reg2)
        
        return instructions
    
    @visitor.when(cil.CopyNode)
    def visit(self, node):
        instructions = []

        #Save $a0, $a1, $a2

        #reg1 = self.get_free_reg()
        #reg2 = self.get_free_reg()
        reg1 = self.memory_manager.get_register(node.source)
        load = self.memory_manager.load_in_register(reg1, node.source)
        instructions.extend(load)
        self.memory_manager.lock(reg1)

        reg2 = self.memory_manager.get_register_for_value()
        load = self.memory_manager.use_register_for_value(reg2)
        instructions.extend(load)

        
        #src_location = self.get_var_location(node.source)
        #instructions.append(mips.LoadWordNode(reg1, src_location))
        instructions.extend(mips.copy_object(reg1, reg2))            

        reg3 = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg3, node.dest)
        instructions.extend(load)

        #dst_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dst_location))

        instructions.append(mips.MoveNode(reg3, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)

        self.memory_manager.free(reg1)
        self.memory_manager.free(reg2)

        #self.free_reg(reg1)
        #self.free_reg(reg2)

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
            #location = self.get_var_location(node.left)
            reg = self.memory_manager.get_register(node.left)
            load = self.memory_manager.load_in_register(reg, node.left)
            instructions.extend(load)
            #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], location))
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))

        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.right))
        elif type(node.right) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], 0))
        else:
            #location = self.get_var_location(node.right)
            reg = self.memory_manager.get_register(node.right)
            load = self.memory_manager.load_in_register(reg, node.right)
            instructions.extend(load)
            #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], location))
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))

        instructions.append(mips.JumpAndLinkNode("equals"))            

        #dest_location = self.get_var_location(node.dest)
        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))
        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)
        
        return instructions
    
    @visitor.when(cil.EqualStrNode)
    def visit(self, node):
        instructions = []

        #location = self.get_var_location(node.left)
        reg = self.memory_manager.get_register(node.left)
        load = self.memory_manager.load_in_register(reg, node.left)
        instructions.extend(load)
        #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], location))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))

        #location = self.get_var_location(node.right)
        reg = self.memory_manager.get_register(node.right)
        load = self.memory_manager.load_in_register(reg, node.right)
        instructions.extend(load)
        #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], location))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))

        instructions.append(mips.JumpAndLinkNode("equal_str"))

        #dest_location = self.get_var_location(node.dest)
        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest) 
        instructions.extend(load)
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))
        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)
        
        return instructions


    @visitor.when(cil.LabelNode)
    def visit(self, node):
        return [mips.LabelNode(self.get_mips_label(node.label))]

    @visitor.when(cil.GotoIfNode)
    def visit(self, node):
        
        instructions = []

        #reg = self.get_free_reg()
        reg = self.memory_manager.get_register(node.condition)
        load = self.memory_manager.load_in_register(reg, node.condition)
        instructions.extend(load)
        
        mips_label = self.get_mips_label(node.label)

        #location = self.get_var_location(node.condition)
        #instructions.append(mips.LoadWordNode(reg, location))
        instructions.append(mips.BranchOnNotEqualNode(reg, mips.ZERO_REG, mips_label))

        #self.free_reg(reg)
        
        return instructions
    
    @visitor.when(cil.GotoNode)
    def visit(self, node):
        mips_label = self.get_mips_label(node.label)
        return [mips.JumpNode(mips_label)]

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        instructions = []

        #reg = self.get_free_reg()
        reg1 = self.memory_manager.get_register(node.obj)
        load = self.memory_manager.load_in_register(reg1, node.obj)
        instructions.extend(load)

        reg2 = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg2, node.dest)
        instructions.extend(load)



        #obj_location = self.get_var_location(node.obj)
        #instructions.append(mips.LoadWordNode(reg, obj_location))
        instructions.append(mips.LoadWordNode(reg2, mips.RegisterRelativeLocation(reg1, 0)))
        self.memory_manager.value_updated(node.dest)
        
        #dest_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(reg, dest_location))

        #self.free_reg(reg)

        return instructions

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        instructions = []

        #reg1 = self.get_free_reg()
        #reg2 = self.get_free_reg()
        reg1 = self.memory_manager.get_register(node.type)
        load = self.memory_manager.load_in_register(reg1, node.type)
        instructions.extend(load)
        self.memory_manager.lock(reg1)

        reg4 = self.memory_manager.get_register(node.dest)
        self.memory_manager.lock(reg4)
        

        reg2 = self.memory_manager.get_register_for_value()
        load = self.memory_manager.use_register_for_value(reg2)
        instructions.extend(load)

        reg3 = self.memory_manager.get_register_for_value()
        load = self.memory_manager.use_register_for_value(reg3)
        instructions.extend(load)

        

        comp_tp = self._types[node.computed_type]
        method_index = list(comp_tp.methods).index(node.method)
        #dest_location = self.get_var_location(node.dest)

        #tp_location = self.get_var_location(node.type)
        #instructions.append(mips.LoadAddressNode(reg1, mips.PROTO_TABLE_LABEL))
        #instructions.append(mips.LoadWordNode(reg2, tp_location))
        #instructions.append(mips.ShiftLeftLogicalNode(reg2, reg2, 2))
        #instructions.append(mips.AddUnsignedNode(reg1, reg1, reg2 ))
        #instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, 0)))
        #instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, 8)))
        #instructions.append(mips.AddInmediateUnsignedNode(reg1, reg1, method_index*4))
        #instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, 0)))
        #instructions.append(mips.JumpRegisterAndLinkNode(reg1))
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        instructions.append(mips.LoadAddressNode(reg2, mips.PROTO_TABLE_LABEL))
        instructions.append(mips.ShiftLeftLogicalNode(reg3, reg1, 2))
        instructions.append(mips.AddUnsignedNode(reg3, reg3, reg2))
        instructions.append(mips.LoadWordNode(reg3, mips.RegisterRelativeLocation(reg3, 0)))
        instructions.append(mips.LoadWordNode(reg3, mips.RegisterRelativeLocation(reg3, 8)))
        instructions.append(mips.AddInmediateUnsignedNode(reg3, reg3, method_index*4))
        instructions.append(mips.LoadWordNode(reg3, mips.RegisterRelativeLocation(reg3, 0)))
        instructions.append(mips.JumpRegisterAndLinkNode(reg3))

        load = self.memory_manager.use_register(reg4, node.dest)
        instructions.extend(load)

        instructions.append(mips.MoveNode(reg4, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)
        
        self.memory_manager.free(reg1)
        self.memory_manager.free(reg2)
        self.memory_manager.free(reg3)
        self.memory_manager.free(reg4)

        #self.free_reg(reg1)
        #self.free_reg(reg2)
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

        #reg = self.get_free_reg()
        reg1 = self.memory_manager.get_register_for_value()
        load = self.memory_manager.use_register_for_value(reg1)
        instructions.extend(load)

        instructions.append(mips.LoadAddressNode(reg1, mips.TYPENAMES_TABLE_LABEL))

        tp_number = self._types[node.name].index
        instructions.append(mips.AddInmediateUnsignedNode(reg1, reg1, tp_number*4))
        instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, 0)))

        reg2 = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg2, node.dest)
        instructions.extend(load)
        #dest_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(reg, dest_location))
        instructions.append(mips.MoveNode(reg2, reg1))

        self.memory_manager.value_updated(node.dest)
        self.memory_manager.free(reg1)

        #self.free_reg(reg)

        return instructions
    
    @visitor.when(cil.PlusNode)
    def visit(self, node):
        instructions = []

        #reg1 = self.get_free_reg()
        #reg2 = self.get_free_reg()
        reg1 = None
        reg2 = None
        reg3 = self.memory_manager.get_register(node.dest)

        if isinstance(node.left, str):
            reg1 = self.memory_manager.get_register(node.left)
            load = self.memory_manager.load_in_register(reg1, node.left)
            instructions.extend(load)
            self.memory_manager.lock(reg1)
            
        if isinstance(node.right, str):
            reg2 = self.memory_manager.get_register(node.right)
            load = self.memory_manager.load_in_register(reg2, node.right)
            instructions.extend(load)
            self.memory_manager.lock(reg2)
        
        if isinstance(node.left, int):
            reg1 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg1, node.left)
            instructions.extend(load)
        
        if isinstance(node.right, int):
            reg2 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg2, node.right)
            instructions.extend(load)
        
        load = self.memory_manager.use_register(reg3, node.dest)
        instructions.extend(load)

        instructions.append(mips.AddNode(reg3, reg2, reg1))
        self.memory_manager.value_updated(node.dest)
        self.memory_manager.free(reg1)
        self.memory_manager.free(reg2)
                    
        #if type(node.left) == int:
        #    #instructions.append(mips.LoadInmediateNode(reg1, node.left))
        #    reg1 = self.memory_manager.get
        #else:
        #    left_location = self.get_var_location(node.left)
        #    instructions.append(mips.LoadWordNode(reg1, left_location))

        #if type(node.right) == int:
        #    instructions.append(mips.LoadInmediateNode(reg2, node.right))
        #else:
        #    right_location = self.get_var_location(node.right)
        #    instructions.append(mips.LoadWordNode(reg2, right_location))

        #instructions.append(mips.AddNode(reg1, reg1, reg2))

        #dest_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(reg1, dest_location))

        #self.free_reg(reg1)
        #self.free_reg(reg2)

        return instructions
    
    @visitor.when(cil.MinusNode)
    def visit(self, node):
        instructions = []

        reg1 = None
        reg2 = None
        reg3 = self.memory_manager.get_register(node.dest)
        self.memory_manager.lock(reg3)

        if isinstance(node.left, str):
            reg1 = self.memory_manager.get_register(node.left)
            load = self.memory_manager.load_in_register(reg1, node.left)
            instructions.extend(load)
            self.memory_manager.lock(reg1)
            
        if isinstance(node.right, str):
            reg2 = self.memory_manager.get_register(node.right)
            load = self.memory_manager.load_in_register(reg2, node.right)
            instructions.extend(load)
            self.memory_manager.lock(reg2)
        
        if isinstance(node.left, int):
            reg1 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg1, node.left)
            instructions.extend(load)
        
        if isinstance(node.right, int):
            reg2 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg2, node.right)
            instructions.extend(load)
        
        load = self.memory_manager.use_register(reg3, node.dest)
        instructions.extend(load)

        instructions.append(mips.SubNode(reg3, reg1, reg2))
        self.memory_manager.value_updated(node.dest)
        self.memory_manager.free(reg1)
        self.memory_manager.free(reg2)
        self.memory_manager.free(reg3)

        #reg1 = self.get_free_reg()
        #reg2 = self.get_free_reg()

        #if type(node.left) == int:
        #    instructions.append(mips.LoadInmediateNode(reg1, node.left))
        #else:
        #    left_location = self.get_var_location(node.left)
        #    instructions.append(mips.LoadWordNode(reg1, left_location))

        #if type(node.right) == int:
        #    instructions.append(mips.LoadInmediateNode(reg2, node.right))
        #else:
        #    right_location = self.get_var_location(node.right)
        #    instructions.append(mips.LoadWordNode(reg2, right_location))

        #instructions.append(mips.SubNode(reg1, reg1, reg2))

        #dest_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(reg1, dest_location))

        #self.free_reg(reg1)
        #self.free_reg(reg2)

        return instructions
    
    @visitor.when(cil.StarNode)
    def visit(self, node):
        instructions = []

        reg1 = None
        reg2 = None
        reg3 = self.memory_manager.get_register(node.dest)

        if isinstance(node.left, str):
            reg1 = self.memory_manager.get_register(node.left)
            load = self.memory_manager.load_in_register(reg1, node.left)
            instructions.extend(load)
            self.memory_manager.lock(reg1)
            
        if isinstance(node.right, str):
            reg2 = self.memory_manager.get_register(node.right)
            load = self.memory_manager.load_in_register(reg2, node.right)
            instructions.extend(load)
            self.memory_manager.lock(reg2)
        
        if isinstance(node.left, int):
            reg1 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg1, node.left)
            instructions.extend(load)
        
        if isinstance(node.right, int):
            reg2 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg2, node.right)
            instructions.extend(load)
        
        load = self.memory_manager.use_register(reg3, node.dest)
        instructions.extend(load)

        instructions.append(mips.MultiplyNode(reg3, reg2, reg1))
        self.memory_manager.value_updated(node.dest)
        self.memory_manager.free(reg1)
        self.memory_manager.free(reg2)

        #reg1 = self.get_free_reg()
        #reg2 = self.get_free_reg()

        #if type(node.left) == int:
        #    instructions.append(mips.LoadInmediateNode(reg1, node.left))
        #else:
        #    left_location = self.get_var_location(node.left)
        #    instructions.append(mips.LoadWordNode(reg1, left_location))

        #if type(node.right) == int:
        #    instructions.append(mips.LoadInmediateNode(reg2, node.right))
        #else:
        #    right_location = self.get_var_location(node.right)
        #    instructions.append(mips.LoadWordNode(reg2, right_location))

        #instructions.append(mips.MultiplyNode(reg1, reg1, reg2))

        #dest_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(reg1, dest_location))

        #self.free_reg(reg1)
        #self.free_reg(reg2)

        return instructions
    
    @visitor.when(cil.DivNode)
    def visit(self, node):
        instructions = []

        reg1 = None
        reg2 = None
        reg3 = self.memory_manager.get_register(node.dest)

        if isinstance(node.left, str):
            reg1 = self.memory_manager.get_register(node.left)
            load = self.memory_manager.load_in_register(reg1, node.left)
            instructions.extend(load)
            self.memory_manager.lock(reg1)
            
        if isinstance(node.right, str):
            reg2 = self.memory_manager.get_register(node.right)
            load = self.memory_manager.load_in_register(reg2, node.right)
            instructions.extend(load)
            self.memory_manager.lock(reg2)
        
        if isinstance(node.left, int):
            reg1 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg1, node.left)
            instructions.extend(load)
        
        if isinstance(node.right, int):
            reg2 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg2, node.right)
            instructions.extend(load)
        
        load = self.memory_manager.use_register(reg3, node.dest)
        instructions.extend(load)

        instructions.append(mips.DivideNode(reg1, reg2))
        instructions.append(mips.MoveFromLowNode(reg3))
        self.memory_manager.value_updated(node.dest)
        self.memory_manager.free(reg1)
        self.memory_manager.free(reg2)

        #reg1 = self.get_free_reg()
        #reg2 = self.get_free_reg()

        #if type(node.left) == int:
        #    instructions.append(mips.LoadInmediateNode(reg1, node.left))
        #else:
        #    left_location = self.get_var_location(node.left)
        #    instructions.append(mips.LoadWordNode(reg1, left_location))

        #if type(node.right) == int:
        #    instructions.append(mips.LoadInmediateNode(reg2, node.right))
        #else:
        #    right_location = self.get_var_location(node.right)
        #    instructions.append(mips.LoadWordNode(reg2, right_location))

        #instructions.append(mips.DivideNode(reg1, reg2))

        #dest_location = self.get_var_location(node.dest)
        
        #instructions.append(mips.MoveFromLowNode(reg1))
        #instructions.append(mips.StoreWordNode(reg1, dest_location))

        #self.free_reg(reg1)
        #self.free_reg(reg2)

        return instructions

    @visitor.when(cil.ComplementNode)
    def visit(self, node):
        instructions = []

        reg1 = None

        
        if type(node.obj) == int:
            #instructions.append(mips.LoadInmediateNode(reg1, node.obj))
            reg1 = self.memory_manager.get_register_for_value()
            load = self.memory_manager.load_value_in_register(reg1, node.obj)
            instructions.extend(load)
        else:
            #left_location = self.get_var_location(node.obj)
            #instructions.append(mips.LoadWordNode(reg1, left_location))
            reg1 = self.memory_manager.get_register(node.obj)
            load = self.memory_manager.load_in_register(reg1, node.obj)
            instructions.extend(load)

        #dest_location = self.get_var_location(node.dest)
        reg2 = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg2, node.dest)
        instructions.extend(load)

        #instructions.append(mips.ComplementNode(reg1, reg1))
        #instructions.append(mips.AddInmediateNode(reg1, reg1, 1))
        #instructions.append(mips.StoreWordNode(reg1, dest_location))

        instructions.append(mips.ComplementNode(reg2, reg1))
        instructions.append(mips.AddInmediateNode(reg2, reg2, 1))
        self.memory_manager.value_updated(node.dest)

        self.memory_manager.free(reg1)

        #self.free_reg(reg1)

        return instructions



    @visitor.when(cil.LessEqualNode)
    def visit(self, node):
        instructions = []
        #Save $a0, $a1, $v0

        if isinstance(node.left, str):
            reg = self.memory_manager.get_register(node.left)
            load = self.memory_manager.load_in_register(reg, node.left)
            instructions.extend(load)
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
            
        if isinstance(node.right, str):
            reg = self.memory_manager.get_register(node.right)
            load = self.memory_manager.load_in_register(reg, node.right)
            instructions.extend(load)
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))

        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], node.left))

        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.right))
            
        instructions.append(mips.JumpAndLinkNode('less_equal'))
        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)
        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)


        #if type(node.left) == int:
        #    instructions.append(mips.LoadInmediateNode(reg1, node.left))
        #else:
        #    left_location = self.get_var_location(node.left)
        #    instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], left_location))
        
        #if type(node.right) == int:
        #    instructions.append(mips.LoadInmediateNode(reg2, node.right))
        #else:
        #    right_location = self.get_var_location(node.right)
        #    instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], right_location))
        
        #instructions.append(mips.JumpAndLinkNode('less_equal'))
        #dest_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        return instructions

    @visitor.when(cil.LessNode)
    def visit(self, node):
        instructions = []
        #Save $a0, $a1, $v0

        if isinstance(node.left, str):
            reg = self.memory_manager.get_register(node.left)
            load = self.memory_manager.load_in_register(reg, node.left)
            instructions.extend(load)
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
            
        if isinstance(node.right, str):
            reg = self.memory_manager.get_register(node.right)
            load = self.memory_manager.load_in_register(reg, node.right)
            instructions.extend(load)
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))

        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], node.left))

        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.right))
            
        instructions.append(mips.JumpAndLinkNode('less'))
        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)
        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)

        #if type(node.left) == int:
        #    instructions.append(mips.LoadInmediateNode(reg1, node.left))
        #else:
        #    left_location = self.get_var_location(node.left)
        #    instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], left_location))
        
        #if type(node.right) == int:
        #    instructions.append(mips.LoadInmediateNode(reg2, node.right))
        #else:
        #    right_location = self.get_var_location(node.right)
        #    instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], right_location))
        
        #instructions.append(mips.JumpAndLinkNode('less'))
        #dest_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        return instructions
    
    @visitor.when(cil.ReadStrNode)
    def visit(self, node):
        instructions = []
        #Save $v0
        instructions.append(mips.JumpAndLinkNode("read_str"))
        
        #dest_location = self.get_var_location(node.dest)
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))
        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)
        instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions

    @visitor.when(cil.LengthNode)
    def visit(self, node):
        instructions = []
        #save $a0 $v0
        #src_location = self.get_var_location(node.source)
        reg = self.memory_manager.get_register(node.source)
        load = self.memory_manager.load_in_register(reg, node.source)            
        instructions.extend(load)

        #dest_location = self.get_var_location(node.dest)

        #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], src_location))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        instructions.append(mips.JumpAndLinkNode("len"))

        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))
        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)
        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)

        return instructions

    @visitor.when(cil.ReadIntNode)
    def visit(self, node):
        instructions = []
        #save $v0
        #dest_location = self.get_var_location(node.dest)
        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.load_in_register(reg, node.dest)
        instructions.extend(load)

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 5))
        instructions.append(mips.SyscallNode())
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))
        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)

        return instructions

    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        instructions = []

        #save $a0, $a1, $a2, $v0

        #prefix_location = self.get_var_location(node.prefix)
        #suffix_location = self.get_var_location(node.suffix)
        #lenght_location = self.get_var_location(node.length)
        reg1 = self.memory_manager.get_register(node.prefix)
        load = self.memory_manager.load_in_register(reg1, node.prefix)
        instructions.extend(load)
        
        reg2 = self.memory_manager.get_register(node.suffix)
        load = self.memory_manager.load_in_register(reg2, node.suffix)
        instructions.extend(load)

        reg3 = self.memory_manager.get_register(node.length)
        load = self.memory_manager.load_in_register(reg3, node.length)
        instructions.extend(load)

        #dest_location = self.get_var_location(node.dest)

        #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], prefix_location))
        #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], suffix_location))
        #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[2], lenght_location))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg1))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg2))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[2], reg3))
        instructions.append(mips.JumpAndLinkNode("concat"))
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))

        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)
        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)

        return instructions

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        instructions = []

        #save $a0, $a1, $a2, $v0

        #str_location = self.get_var_location(node.str_value)
        reg = self.memory_manager.get_register(node.str_value)
        load = self.memory_manager.load_in_register(reg, node.str_value)
        instructions.extend(load)
        #dest_location = self.get_var_location(node.dest)

        #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], str_location))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))

        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[1], node.index))
        else:
            #index_location = self.get_var_location(node.index)
            #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[1], index_location))
            reg = self.memory_manager.get_register(node.index)
            load = self.memory_manager.load_in_register(reg, node.index)
            instructions.extend(load)
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg))

        
        if type(node.length) == int:
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[2], node.length))
        else:
            #lenght_location = self.get_var_location(node.length)
            #instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[2], lenght_location))
            reg = self.memory_manager.get_register(node.length)
            load = self.memory_manager.load_in_register(reg, node.length)
            instructions.extend(load)
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[2], reg))
        
        instructions.append(mips.JumpAndLinkNode("substr"))
        #instructions.append(mips.StoreWordNode(mips.V0_REG, dest_location))
        reg = self.memory_manager.get_register(node.dest)
        load = self.memory_manager.use_register(reg, node.dest)
        instructions.extend(load)
        instructions.append(mips.MoveNode(reg, mips.V0_REG))
        self.memory_manager.value_updated(node.dest)

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
class RegistersAllocator:
    def __init__(self):
        self.mark = False
        
    def get_registers_for_variables(self, instructions, params, n):
        self.numered_instructions(instructions)
        self.mark_leaders(instructions)
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
        interference = RegistersAllocator.interference_compute(gk, oi)
        
        RegistersAllocator.assign_registers(interference, 4)

    @staticmethod
    def interference_compute(gk, in_out):
        neigs = defaultdict(set)
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
        in_out = [(set(), set()) for _ in range(n_instructions)]
        next_in_out = [(set(), set()) for _ in range(n_instructions)]

        def add(set1, set2):
            new = not set1 == set2
            set1.update(set2)
            return new

        changed = True
        while changed:
            changed = False
            for i in range(n_instructions)[::-1]:
                for i_suc in suc[i]:
                    if i_suc < i:
                        changed = add(next_in_out[i][1], in_out[i_suc][0])
                    else:
                        changed = add(next_in_out[i][1], next_in_out[i_suc][0])
                g_i = set(gk[i][0])
                k_i = set(gk[i][1])
                new = g_i.union(next_in_out[i][1].difference(k_i))
                changed = add(next_in_out[i][0], new)
            in_out = next_in_out
        
        return in_out

    @staticmethod
    def create_flow_graph(blocks, debug = False): #graph between blocks in a same function does not include relations between functions
        graph = [[-1 for _ in range(len(blocks))] for _ in range(len(blocks)) ]
        labels = {b[0].label : i for i, b in enumerate(blocks) if isinstance(b[0], cil.LabelNode)}

        for i, block in enumerate(blocks):
            if isinstance(block[-1], cil.GotoNode):
                graph[i][labels[block[-1].label]] = 1
            elif isinstance(block[-1], cil.GotoIfNode):
                graph[i][labels[block[-1].label]] = 1
                graph[i][i + 1] = 1 if i + 1 < len(blocks) else -1
        return graph            

    @staticmethod
    def numered_instructions(instructions):
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
    
