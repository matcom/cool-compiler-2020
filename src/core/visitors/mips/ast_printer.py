from .mips import *
from ...visitors import visitor

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
        proto_attr = "\n".join([f'\t.word\t{node._default_attributes.get(attr, "0")}' for attr in node.attributes])
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
        