from itertools import chain
import core.cmp.visitor as visitor

ATTR_SIZE           = 4
RESGISTER_SIZE      = 4
REGISTER_NAMES      = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7','t8', 't9']
ARG_REGISTERS_NAMES = ['a0', 'a1', 'a2', 'a3']


INSTANCE_METADATA_SIZE  = 4



class Register():
    def __init__(self, name):
        self.name = name

REGISTERS           = { name: Register(name) for name in REGISTER_NAMES }
ARG_REGISTERS       = [ Register(name) for name in ARG_REGISTERS_NAMES ]
FP_REG              = Register('fp') 
SP_REG              = Register('sp')
RA_REG              = Register('ra')
V0_REG              = Register('v0')
V1_REG              = Register('v1')

class Node:
    pass

class ProgramNode(Node):
    def __init__(self, data, types, functions):
        self._data = data
        self._types = types
        self._functions = functions

    @property
    def data(self):
        return self._data
    
    @property
    def types(self):
        return self._types
    
    @property
    def functions(self):
        return self._functions

class FunctionNode(Node):
    def __init__(self, label, params, localvars, instructions = []):
        self._label = label
        self._instructions = instructions
        self._params = params
        self._localvars = localvars
    
    def add_instructions(self, instructions):
        self._instructions.extend(instructions)
    
    def get_param_stack_location(self, name):
        #TODO Tener en cuenta que los primeros argumentos se guardan en los registros para argumentos 
        index = self._params.index(name)
        offset = ((len(self._params) -1 ) - index) * ATTR_SIZE
        return RegisterRelativeLocation(FP_REG, offset)

    def get_local_stack_location(self, name):
        index = self._localvars.index(name)
        offset = (index + 2) * -ATTR_SIZE
        return RegisterRelativeLocation(FP_REG, offset)
    
    def get_var_location(self, name):
        try:
            return self.get_param_stack_location(name)
        except ValueError:
            return self.get_local_stack_location(name)
        

class DataNode(Node):
    def __init__(self, label):
        self._label  = label
    
    @property
    def label(self):
        return self._label

class StringConst(DataNode):
    def __init__(self, label, string):
        super().__init__(label)
        self._string = string
    

class InstructionNode(Node):
    pass

class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class MoveNode(InstructionNode):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

class LoadInmediateNode(InstructionNode):
    def __init__(self, reg, value):
        self.reg = reg
        self.value = value

class LoadWordNode(InstructionNode):
    def __init__(self, reg, addr):
        self.reg = reg
        self.addr = addr

class SyscallNode(InstructionNode):
    pass

class LoadAddressNode(InstructionNode):
    def __init__(self, reg, label):
        self.reg   = reg
        self.label = label

class StoreWordNode(InstructionNode):
    def __init__(self, reg, addr):
        self.reg  = reg
        self.addr = addr

class JumpAndLinkNode(InstructionNode):
    def __init__(self, label):
        self.label = label

class JumpRegisterAndLinkNode(InstructionNode):
    def __init__(self, reg):
        self.reg = reg

class JumpRegister(InstructionNode):
    def __init__(self, reg):
        self.reg = reg

class AddInmediateNode(InstructionNode):
    def __init__(self, dest, src, value):
        self.dest  = dest
        self.src   = src
        self.value = value


class MIPSType:
    def __init__(self, label, name_addr, attributes, methods):
        self._label = label
        self._name = name_addr
        self._attributes = attributes
        self._methods = methods
        

    @property
    def size(self):
        return (len(self.attributes) * ATTR_SIZE) + INSTANCE_METADATA_SIZE
    
    @property
    def label(self):
        return self._label
    
    @property
    def string_name_label(self):
        return self._name
   



class MemoryLocation:
    pass

class RegisterRelativeLocation(MemoryLocation):
    def __init__(self, register, offset):
        self._register = register
        self._offset = offset
    
    @property
    def register(self):
        return self._register
    
    @property
    def offset(self):
        return self._offset

class LabelRelativeLocation(MemoryLocation):
    def __init__(self, label, offset):
        self._label = label
        self._offset = offset
    
    @property
    def label(self):
        return self._label
    
    @property
    def offset(self):
        return self._offset

##Snippets

def push_register(reg):
    move_stack = AddInmediateNode(SP_REG, SP_REG, -RESGISTER_SIZE)
    save_location = RegisterRelativeLocation(SP_REG, 0)
    save_register = StoreWordNode(reg, save_location)
    return [move_stack, save_register]

def pop_register(reg):
    load_value = LoadWordNode(reg, RegisterRelativeLocation(SP_REG, 0))
    move_stack = AddInmediateNode(SP_REG, SP_REG, RESGISTER_SIZE)
    return [load_value, move_stack]

def alloc_memory(size):
    instructions = []
    instructions.append(LoadInmediateNode(V0_REG, 9))
    instructions.append(LoadInmediateNode(ARG_REGISTERS[0], size))
    instructions.append(SyscallNode())
    return instructions

def exit_program():
    instructions = []
    instructions.append(LoadInmediateNode(V0_REG, 10))
    instructions.append(SyscallNode())
    return instructions
