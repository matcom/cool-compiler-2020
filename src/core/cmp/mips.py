from itertools import chain
import core.cmp.visitor as visitor

ATTR_SIZE           = 4
RESGISTER_SIZE      = 4
REGISTER_NAMES      = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7','t8', 't9']
ARG_REGISTERS_NAMES = ['a0', 'a1', 'a2', 'a3']
OBJECT_MARK = -1


INSTANCE_METADATA_SIZE  = 4

TYPENAMES_TABLE_LABEL   = "type_name_table"
PROTO_TABLE_LABEL       = "proto_table"

class Register():
    def __init__(self, name):
        self.name = name

REGISTERS           = [ Register(name) for name in REGISTER_NAMES ]
ARG_REGISTERS       = [ Register(name) for name in ARG_REGISTERS_NAMES ]
FP_REG              = Register('fp') 
SP_REG              = Register('sp')
RA_REG              = Register('ra')
V0_REG              = Register('v0')
V1_REG              = Register('v1')
ZERO_REG            = Register('zero')
LOW_REG             = Register('low')

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
    def __init__(self, label, params, localvars):
        self._label = label
        self._instructions = []
        self._params = params
        self._localvars = localvars
    
    @property
    def label(self):
        return self._label
    
    @property
    def instructions(self):
        return self._instructions
    
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
    
    @property
    def string(self):
        return self._string
    

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
    
class AddInmediateUnsignedNode(InstructionNode):
    def __init__(self, dest, src, value):
        self.dest  = dest
        self.src   = src
        self.value = value

class AddUnsignedNode(InstructionNode):
    def __init__(self, dest, sum1, sum2):
        self.dest = dest
        self.sum1 = sum1
        self.sum2 = sum2

class ShiftLeftLogicalNode(InstructionNode):
    def __init__(self, dest, src, bits):
        self.dest = dest
        self.src  = src
        self.bits = bits
    
class BranchOnNotEqualNode(InstructionNode):
    def __init__(self, reg1, reg2, label):
        self.reg1 = reg1
        self.reg2 = reg2
        self.label = label
    
class JumpNode(InstructionNode):
    def __init__(self, label):
        self.label = label

class AddNode(InstructionNode):
    def __init__(self, reg1, reg2, reg3):
        self.reg1 = reg1
        self.reg2 = reg2
        self.reg3 = reg3

class SubNode(InstructionNode):
    def __init__(self, reg1, reg2, reg3):
        self.reg1 = reg1
        self.reg2 = reg2
        self.reg3 = reg3

class MultiplyNode(InstructionNode):
    def __init__(self, reg1, reg2, reg3):
        self.reg1 = reg1
        self.reg2 = reg2
        self.reg3 = reg3

class DivideNode(InstructionNode):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

class ComplementNode(InstructionNode):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

class MoveFromLowNode(InstructionNode):
    def __init__(self, reg):
        self.reg = reg
    


class MIPSType:
    def __init__(self, label, name_addr, attributes, methods, index):
        self._label = label
        self._name = name_addr
        self._attributes = attributes
        self._methods = methods
        self._index = index
        

    @property
    def size(self):
        return len(self.attributes) + INSTANCE_METADATA_SIZE
    
    @property
    def label(self):
        return self._label
    
    @property
    def string_name_label(self):
        return self._name
    
    @property
    def methods(self):
        return self._methods
    
    @property
    def attributes(self):
        return self._attributes
    
    @property
    def index(self):
        return self._index
   



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

def create_object(reg1, reg2):
    instructions = []

    instructions.append(ShiftLeftLogicalNode(reg1, reg1, 2))
    instructions.append(LoadAddressNode(reg2, PROTO_TABLE_LABEL))
    instructions.append(AddUnsignedNode(reg2, reg2, reg1))
    instructions.append(LoadWordNode(reg2, RegisterRelativeLocation(reg2, 0)))
    instructions.append(LoadWordNode(ARG_REGISTERS[0], RegisterRelativeLocation(reg2, 4)))
    instructions.append(ShiftLeftLogicalNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 2))
    instructions.append(JumpAndLinkNode("malloc"))
    instructions.append(MoveNode(ARG_REGISTERS[2], ARG_REGISTERS[0]))
    instructions.append(MoveNode(ARG_REGISTERS[0], reg2))
    instructions.append(MoveNode(ARG_REGISTERS[1], V0_REG))
    instructions.append(JumpAndLinkNode("copy"))
    
    return instructions

def copy_object(reg1, reg2):
    instructions = []
    
    instructions.append(LoadWordNode(ARG_REGISTERS[0], RegisterRelativeLocation(reg1, 4)))
    instructions.append(ShiftLeftLogicalNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 2))
    instructions.append(JumpAndLinkNode("malloc"))
    instructions.append(MoveNode(ARG_REGISTERS[2], ARG_REGISTERS[0]))
    instructions.append(MoveNode(ARG_REGISTERS[0], reg1))
    instructions.append(MoveNode(ARG_REGISTERS[1], V0_REG))
    instructions.append(JumpAndLinkNode("copy"))

    return instructions
    


class PrintVisitor:
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Register)
    def visit(self, node):
        return f'${node.name}'

    @visitor.when(int)
    def visit(self, node):
        return str(node)
    
    @visitor.when(str)
    def visit(self, node):
        return node

    @visitor.when(ProgramNode)
    def visit(self, node):
        data_section_header = "\t.data"
        static_strings = '\n'.join([self.visit(string_const) for string_const in node.data])
        
        
        names_table = f"{TYPENAMES_TABLE_LABEL}:\n" + "\n".join([f"\t.word\t{tp.string_name_label}" for tp in node.types])
        proto_table = f"{PROTO_TABLE_LABEL}:\n" + "\n".join([f"\t.word\t{tp.label}_proto" for tp in node.types])



        types = "\n\n".join([self.visit(tp) for tp in node.types])
        
        code = "\n".join([self.visit(func) for func in node.functions])
        return f'{data_section_header}\n{static_strings}\n\n{names_table}\n\n{proto_table}\n\n{types}\n\t.text\n\t.globl main\n{code}' 
    
    @visitor.when(StringConst)
    def visit(self, node):
        return f'{node.label}: .asciiz "{node.string}"'
    
    @visitor.when(MIPSType)
    def visit(self, node):
        methods = "\n".join([f"\t.word\t {node.methods[k]}" for k in node.methods])
        dispatch_table = f"{node.label}_dispatch:\n{methods}"
        proto_begin = f"{node.label}_proto:\n\t.word\t{node.index}\n\t.word\t{node.size}\n\t.word\t{node.label}_dispatch"
        proto_attr = "\n".join(['\t.word\t0' for _ in node.attributes])
        proto_end = f"\t.word\t{OBJECT_MARK}"
        proto = f"{proto_begin}\n{proto_attr}\n{proto_end}" if proto_attr != "" else f"{proto_begin}\n{proto_end}"
        
        return f'{dispatch_table}\n\n{proto}'

    @visitor.when(SyscallNode)
    def visit(self, node):
        return 'syscall'
    
    @visitor.when(LabelRelativeLocation)
    def visit(self, node):
        return f'{node.label} + {node.offset}'
    
    @visitor.when(RegisterRelativeLocation)
    def visit(self, node):
        return f'{node.offset}({self.visit(node.register)})'
    
    @visitor.when(FunctionNode)
    def visit(self, node):
        instr = [self.visit(instruction) for instruction in node.instructions]
        #TODO la linea de abajo sobra, es necesaria mientras la traduccion del AST de CIL este incompleta
        instr2 = [inst for inst in instr if type(inst) == str]
        instructions = "\n\t".join(instr2)
        return f'{node.label}:\n\t{instructions}'
    
    @visitor.when(AddInmediateNode)
    def visit(self, node):
        return f'addi {self.visit(node.dest)}, {self.visit(node.src)}, {self.visit(node.value)}'
    
    @visitor.when(StoreWordNode)
    def visit(self, node):
        return f'sw {self.visit(node.reg)}, {self.visit(node.addr)}'
    
    @visitor.when(LoadInmediateNode)
    def visit(self, node):
        return f'li {self.visit(node.reg)}, {self.visit(node.value)}'

    @visitor.when(JumpAndLinkNode)
    def visit(self, node):
        return f'jal {node.label}'
    
    @visitor.when(JumpRegister)
    def visit(self, node):
        return f'jr {self.visit(node.reg)}'
    
    @visitor.when(JumpRegisterAndLinkNode)
    def visit(self, node):
        return f'jal {self.visit(node.reg)}'
    
    @visitor.when(LoadWordNode)
    def visit(self, node):
        return f'lw {self.visit(node.reg)}, {self.visit(node.addr)}'
    
    @visitor.when(LoadAddressNode)
    def visit(self, node):
        return f'la {self.visit(node.reg)}, {self.visit(node.label)}'
    
    @visitor.when(MoveNode)
    def visit(self, node):
        return f'move {self.visit(node.reg1)} {self.visit(node.reg2 )}'
    
    @visitor.when(ShiftLeftLogicalNode)
    def visit(self, node):
        return f"sll {self.visit(node.dest)} {self.visit(node.src)} {node.bits}"
    
    @visitor.when(AddInmediateUnsignedNode)
    def visit(self, node):
        return f"addiu {self.visit(node.dest)} {self.visit(node.src)} {self.visit(node.value)}"

    @visitor.when(AddUnsignedNode)
    def visit(self, node):
        return f"addu {self.visit(node.dest)} {self.visit(node.sum1)} {self.visit(node.sum2)}"
    
    @visitor.when(LabelNode)
    def visit(self, node):
        return f"{node.name}:"

    @visitor.when(BranchOnNotEqualNode)
    def visit(self, node):
        return f"bne {self.visit(node.reg1)} {self.visit(node.reg2)} {node.label}"
    
    @visitor.when(JumpNode)
    def visit(self, node):
        return f"j {node.label}"
    
    @visitor.when(AddNode)
    def visit(self, node):
        return f"add {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"
    
    @visitor.when(SubNode)
    def visit(self, node):
        return f"sub {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"
    
    @visitor.when(MultiplyNode)
    def visit(self, node):
        return f"mul {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"
    
    @visitor.when(DivideNode)
    def visit(self, node):
        return f"div {self.visit(node.reg1)} {self.visit(node.reg2)}"
    
    @visitor.when(ComplementNode)
    def visit(self, node):
        return f"not {self.visit(node.reg1)} {self.visit(node.reg2)}"

    @visitor.when(MoveFromLowNode)
    def visit(self, node):
        return f"mflo {self.visit(node.reg)}"