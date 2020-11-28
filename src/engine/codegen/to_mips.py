from .cil_ast import *
from ..cp import visitor
from .mips import MipsCode as mips
from .mips import Registers as reg


class CIL_TO_MIPS:

    def __init__(self):
        self.reg = Registers
        self.code = []

    def _write(self, line):
        self.code.append(line)

    def visit_ArithNode(self, node: ArithmeticNode):
        # Setting
        self.visit(node.left)
        self.visit(node.right)

        self._write(mips.lw(reg.t0, 8, reg.sp))
        self._write(mips.lw(reg.t0, 4, reg.sp))

        self._write(mips.lw(reg.a0, 8, reg.sp))
        self._write(mips.lw(reg.a1, 8, reg.sp))

        self._write(mips.addiu(reg.sp, reg.sp, 8))
        # Operation
        if isinstance(node, PlusNode):
            self._write(mips.add(reg.a1, reg.a0, reg.a1))
        elif isinstance(node, MinusNode):
            self._write(mips.sub(reg.a1, reg.a0, reg.a1))
        elif isinstance(node, StarNode):
            self._write(mips.mult(reg.a0, reg.a1))
        elif isinstance(node, DivNode):
            self._write("la $t0, zero_error")
            self._write("sw $t0, ($sp)")
            self._write("subu $sp, $sp, 4")
            self._write(mips.beqz(reg.a1, ))
            self._write("beqz $a1, .raise")
            self._write(mips.addiu(reg.sp, reg.sp, 4))
            self._write(mips.div(reg.a0, reg.a1))
            self._write(mips.mflo(reg.a1))
        elif isinstance(node, LessNode):
            self._write("slt $a1, $a0, $a1")
        elif isinstance(node, LessEqNode):
            self._write("sle $a1, $a0, $a1")

        # Return
        self._write("li $v0, 9")
        self._write("li $a0, 12")
        self._write("syscall")
        if isinstance(node, EqualNode) or isinstance(node, LessNode):
            self._write("la $t0, Bool")
        else:
            self._write("la $t0, Int")

        self._write("sw $t0, ($v0)")

        self._write("li $t0, 1")
        self._write("sw $t0, 4($v0)")

        self._write("sw $a1, 8($v0)")
        self._write("sw $v0, ($sp)")

        self._write("subu $sp, $sp, 4")

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):

        for typex in node.dottypes:
            self.visit(typex)

        for data in node.dotdata:
            self.visit(data)

        for code in node.dotcode:
            self.visit(code)

        return self.data_code, self.code

    @visitor.when(TypeNode)
    def visit(self, node):

    @visitor.when(FunctionNode)
    def visit(self, node):
        pass

    @visitor.when(DataNode)
    def visit(self, node):
        pass

    @visitor.when(ParamNode)
    def visit(self, node):
        pass

    @visitor.when(LocalNode)
    def visit(self, node):
        pass

    @visitor.when(GetAttribNode)
    def visit(self, node):
        pass

    @visitor.when(SetAttribNode)
    def visit(self, node):
        pass

    @visitor.when(AssignNode)
    def visit(self, node):
        pass

    @visitor.when(ComplementNode)
    def visit(self, node):
        pass

    @visitor.when(NotNode)
    def visit(self, node):
        pass

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        self.visit_ArithNode(node)

    @visitor.when(MinusNode)
    def visit(self, node):
        self.visit_ArithNode(node)

    @visitor.when(StarNode)
    def visit(self, node):
        self.visit_ArithNode(node)

    @visitor.when(DivNode)
    def visit(self, node):
        self.visit_ArithNode(node)

    @visitor.when(EqualNode)
    def visit(self, node):
        self.visit_ArithNode(node)

    @visitor.when(LessEqNode)
    def visit(self, node):
        self.visit_ArithNode(node)

    @visitor.when(LessNode)
    def visit(self, node):
        self.visit_ArithNode(node)

    @visitor.when(AllocateNode)
    def visit(self, node):
        pass

    @visitor.when(TypeOfNode)
    def visit(self, node):
        pass

    @visitor.when(LabelNode)
    def visit(self, node):
        pass

    @visitor.when(GotoNode)
    def visit(self, node):
        pass

    @visitor.when(IfGotoNode)
    def visit(self, node):
        pass

    @visitor.when(StaticCallNode)
    def visit(self, node):
        pass

    @visitor.when(DynamicCallNode)
    def visit(self, node):
        pass

    @visitor.when(ArgNode)
    def visit(self, node):
        pass

    @visitor.when(ErrorNode)
    def visit(self, node):
        pass

    @visitor.when(CopyNode)
    def visit(self, node):
        pass

    @visitor.when(TypeNameNode)
    def visit(self, node):
        pass

    @visitor.when(LengthNode)
    def visit(self, node):
        pass

    @visitor.when(ConcatNode)
    def visit(self, node):
        pass

    @visitor.when(StringEqualNode)
    def visit(self, node):
        pass

    @visitor.when(ConcatNode)
    def visit(self, node):
        pass

    @visitor.when(LoadNode)
    def visit(self, node):
        pass

    @visitor.when(SubstringNode)
    def visit(self, node):
        pass

    @visitor.when(ToStrNode)
    def visit(self, node):
        pass

    @visitor.when(ToIntNode)
    def visit(self, node):
        pass

    @visitor.when(ReadNode)
    def visit(self, node):
        pass

    @visitor.when(PrintNode)
    def visit(self, node):
        pass

    @visitor.when(ReturnNode)
    def visit(self, node):
        pass
