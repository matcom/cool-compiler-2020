from itertools import chain
import core.cmp.visitor as visitor

ATTR_SIZE           = 4
RESGISTER_SIZE      = 4
REGISTER_NAMES      = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7','t8', 't9', 'v0', 'v1', 'a0', 'sp', 'ra']
STRING_TYPE         = "string_type"

# TYPE_NAME_LABEL     = f"type_name_{}"
TYPE_METADATA_SIZE  = 4



class Register():
    def __init__(self, name):
        self.name = name

REGISTERS           = { name: Register(name) for name in REGISTER_NAMES }

class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottext, dotdata, types):
        self._dottext = dottext
        self._dotdata = dotdata


class FunctionNode(Node):
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

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
    
    def __repr__(self):
        return f'STRING_CONST {self._label} {STRING_TYPE} {self._string}'

class TypeDesc(DataNode):
    def __init__(self, label, name, size,  methods):
        super().__init__(label)
        self._size    = size
        self._name    = name
        self._methods = methods
    
    def __repr__(self):
        print(self._name)
        print(self._size)
        return f'TYPE_DESC {self._name} {self._size} {self._label} {self._methods}'

        
        

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

class JumpRegister(InstructionNode):
    def __init__(self, reg):
        self.reg = reg

class AddInmediateNode(InstructionNode):
    def __init__(self, dest, src, value):
        self.dest  = dest
        self.src   = src
        self.value = value





class MIPSType():
    def __init__(self, label, name, size, methods):
        self._label = label
        self._name = name
        self._size = size
        self._methods = methods
        

    @property
    def size(self):
        return len(self.attributes) * ATTR_SIZE 
    
    @property
    def data_label(self):
        return self.data_label

    def set_data_label(self, data_label):
        self.data_label = string

    def get_attr_offset(self, attr_name):
        return ATTR_SIZE * self.attributes.index(attributes)
    
    def get_func(self, method_name):
        return self.methods[method_name]

class Label():
    def __init__(self, name):
        self._name = name
    
    def __repr__(self):
        return self._name
    
    
    
    


class Address():
    def __init__(self, reg, offset):
        self.offset = offset
        self.reg    = reg

def save_register(reg):
    move_stack = AddInmediateNode(REGISTERS['sp'], REGISTERS['sp'], -RESGISTER_SIZE)
    addr       = Address(REGISTERS['sp'], 0)
    save_value = StoreWordNode(reg, addr)
    return [move_stack, save_value]

def save_registers(registers):
    instructions = []
    instructions.extend(chain.from_iterable([save_register(reg) for reg in registers]))
    return instructions   

def load_reg_from_stack(reg):
    addr       = Address(REGISTERS['sp'], 0)
    load_value = LoadWordNode(reg, addr)
    move_stack = AddInmediateNode(REGISTERS['sp'], REGISTERS['sp'], RESGISTER_SIZE)
    return [load_value, move_stack]

def load_registers_from_stack(registers):
    instructions = []
    instructions.extend(chain.from_iterable([load_reg_from_stack(reg) for reg in registers]))
    return instructions

def allocate_memory(addr, size):
    set_operation_number = LoadInmediateNode(REGISTERS['v0'], 9)
    set_size             = LoadInmediateNode(REGISTERS['a0'], size)
    syscall              = SyscallNode()
    save_pointer         = StoreWordNode(REGISTERS['v0'], addr)
    return [set_operation_number, set_size, syscall, save_pointer]




