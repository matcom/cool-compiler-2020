from .cil_ast import *
from ..cp import visitor
from .mips import *

class CIL_TO_MIPS:

    def __init__(self):
        self.data_code = []
        self.mips_code = []
        self.reg = Registers
        self.code = MipsCode
        
    def visit_ArithNode(self, node: ArithmeticNode ):
        # Setting
        self.visit(node.left)
        self.visit(node.right)

        self.mips_code.append("lw $t0, 8($sp)")
        self.mips_code.append("lw $t1, 4($sp)")

        self.mips_code.append("lw $a0, 8($t0)")
        self.mips_code.append("lw $a1, 8($t1)")

        self.mips_code.append("addiu $sp, $sp, 8")
        # Operation
        if isinstance(node, PlusNode):
            self.mips_code.append("add $a1, $a0, $a1")
        elif isinstance(node, MinusNode):
            self.mips_code.append("sub $a1, $a0, $a1")
        elif isinstance(node, StarNode):
            self.mips_code.append("mult $a0, $a1")
            self.mips_code.append("mflo $a1")
        elif isinstance(node, DivNode):
            self.mips_code.append("la $t0, zero_error")
            self.mips_code.append("sw $t0, ($sp)")
            self.mips_code.append("subu $sp, $sp, 4")
            self.mips_code.append("beqz $a1, .raise")
            self.mips_code.append("addu $sp, $sp, 4")
            self.mips_code.append("div $a0, $a1")
            self.mips_code.append("mflo $a1")
        elif isinstance(node, LessNode):
            self.mips_code.append("slt $a1, $a0, $a1")
        elif isinstance(node, LessEqNode):
            self.mips_code.append("sle $a1, $a0, $a1")

        # Return 
        self.mips_code.append("li $v0, 9")
        self.mips_code.append("li $a0, 12")
        self.mips_code.append("syscall")
        if isinstance(node, EqualNode) or isinstance(node, LessNode):
            self.mips_code.append("la $t0, Bool")
        else:
            self.mips_code.append("la $t0, Int")
            
        self.mips_code.append("sw $t0, ($v0)")

        self.mips_code.append("li $t0, 1")
        self.mips_code.append("sw $t0, 4($v0)")

        self.mips_code.append("sw $a1, 8($v0)")
        self.mips_code.append("sw $v0, ($sp)")

        self.mips_code.append("subu $sp, $sp, 4")

    @visitor.on('node')
    def visit(self,node):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node: ProgramNode):
        
        for typex in node.dottypes:
            self.visit(typex)
        
        for data in node.dotdata:
            self.visit(data)
        
        for code in node.dotcode:
            self.visit(code)
        
        return self.data_code, self.code

    @visitor.when(TypeNode)
    def visit(self,node):


    @visitor.when(FunctionNode)
    def visit(self,node):
        pass

    @visitor.when(DataNode)
    def visit(self,node):
        pass

    @visitor.when(ParamNode)
    def visit(self,node):
        pass

    @visitor.when(LocalNode)
    def visit(self,node):
        pass

    @visitor.when(GetAttribNode)
    def visit(self,node):
        pass

    @visitor.when(SetAttribNode)
    def visit(self,node):
        pass

    @visitor.when(AssignNode)
    def visit(self,node):
        pass

    @visitor.when(ComplementNode)
    def visit(self,node):
        pass

    @visitor.when(NotNode)
    def visit(self,node):
        pass

    @visitor.when(PlusNode)
    def visit(self,node : PlusNode):
        self.visit_ArithNode(node)

    @visitor.when(MinusNode)
    def visit(self,node):
        self.visit_ArithNode(node)

    @visitor.when(StarNode)
    def visit(self,node):
        self.visit_ArithNode(node)

    @visitor.when(DivNode)
    def visit(self,node):
        self.visit_ArithNode(node)

    @visitor.when(EqualNode)
    def visit(self,node):
        self.visit_ArithNode(node)

    @visitor.when(LessEqNode)
    def visit(self,node):
        self.visit_ArithNode(node)

    @visitor.when(LessNode)
    def visit(self,node):
        self.visit_ArithNode(node)

    @visitor.when(AllocateNode)
    def visit(self,node):
        pass

    @visitor.when(TypeOfNode)
    def visit(self,node):
        pass

    @visitor.when(LabelNode)
    def visit(self,node):
        pass

    @visitor.when(GotoNode)
    def visit(self,node):
        pass

    @visitor.when(IfGotoNode)
    def visit(self,node):
        pass

    @visitor.when(StaticCallNode)
    def visit(self,node):
        pass

    @visitor.when(DynamicCallNode)
    def visit(self,node):
        pass

    @visitor.when(ArgNode)
    def visit(self,node):
        pass

    @visitor.when(ErrorNode)
    def visit(self,node):
        pass

    @visitor.when(CopyNode)
    def visit(self,node):
        pass

    @visitor.when(TypeNameNode)
    def visit(self,node):
        pass

    @visitor.when(LengthNode)
    def visit(self,node):
        pass

    @visitor.when(ConcatNode)
    def visit(self,node):
        pass

    @visitor.when(StringEqualNode)
    def visit(self,node):
        pass

    @visitor.when(ConcatNode)
    def visit(self,node):
        pass

    @visitor.when(LoadNode)
    def visit(self,node):
        pass

    @visitor.when(SubstringNode)
    def visit(self,node):
        pass

    @visitor.when(ToStrNode)
    def visit(self,node):
        pass

    @visitor.when(ToIntNode)
    def visit(self,node):
        pass

    @visitor.when(ReadNode)
    def visit(self,node):
        pass

    @visitor.when(PrintNode)
    def visit(self,node):
        pass

    @visitor.when(ReturnNode)
    def visit(self,node):
        pass
