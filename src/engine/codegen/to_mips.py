from .cil_ast import *
from ..cp import visitor
from .mips import MipsCode as mips
from .mips import Registers as reg
from .mips import MipsLabel as label


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

        self._write(mips.lw(reg.t0, reg.sp, offset=8))
        self._write(mips.lw(reg.t0, reg.sp, offset=4))

        self._write(mips.lw(reg.a0, reg.sp, offset=8))
        self._write(mips.lw(reg.a1, reg.sp, offset=8))

        self._write(mips.addiu(reg.sp, reg.sp, 8))
        # Operation
        if isinstance(node, PlusNode):
            self._write(mips.add(reg.a1, reg.a0, reg.a1))
        elif isinstance(node, MinusNode):
            self._write(mips.sub(reg.a1, reg.a0, reg.a1))
        elif isinstance(node, StarNode):
            self._write(mips.mult(reg.a0, reg.a1))
        elif isinstance(node, DivNode):
            self._write(mips.la(reg.t0, label.zero_error))
            self._write(mips.sw(reg.t0, reg.sp))
            self._write(mips.subiu(reg.sp, reg.sp, 4))
            self._write(mips.beqz(reg.a1, label.raise_))
            self._write(mips.addiu(reg.sp, reg.sp, 4))
            self._write(mips.div(reg.a0, reg.a1))
            self._write(mips.mflo(reg.a1))
        elif isinstance(node, LessNode):
            self._write(mips.slt(reg.a1, reg.a0, reg.a1))
        elif isinstance(node, LessEqNode):
            self._write(mips.sle(reg.a1, reg.a0, reg.a1))

        # Return
        self._write(mips.li(reg.v0, 9))
        self._write(mips.li(reg.a0, 12))
        self._write(mips.syscall)

        if isinstance(node, EqualNode) or isinstance(node, LessNode) or isinstance(node, LessEqNode):
            self._write(mips.la(reg.t0, 'Bool'))
        else:
            self._write(mips.la(reg.t0, 'Int'))

        self._write(mips.sw(reg.t0, reg.v0))

        self._write(mips.li(reg.t0, 1))
        self._write(mips.sw(reg.t0, reg.v0, offset=4))

        self._write(mips.sw(reg.a1, reg.v0, offset=8))
        self._write(mips.sw(reg.v0, reg.sp))

        self._write(mips.subiu(reg.sp, reg.sp, 4))

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):

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
    def visit(self, node: DataNode):
        self._write('.data')
        self._write()

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
    def visit(self, node: ComplementNode):
        self.visit(node.expression)

        self._write(mips.lw(reg.t0, reg.sp, offset=4))

        self._write(mips.lw(reg.a0, reg.sp, offset=8))

        self._write(mips.nor(reg.a1, reg.a0))

        self._write(mips.li(reg.v0, 9))
        self._write(mips.li(reg.a0, 12))
        self._write(mips.syscall)

        self._write(mips.la(reg.t0, 'Int'))

        self._write(mips.sw(reg.t0, reg.v0))
        self._write(mips.li(reg.t0, 1))
        self._write(mips.sw(reg.t0, reg.v0, offset=4))

        self._write(mips.sw(reg.a1, reg.v0, offset=8))
        self._write(mips.sw(reg.v0, reg.sp))

        self._write(mips.subiu(reg.sp, reg.sp, 4))

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        self.visit_ArithNode(node)

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        self.visit_ArithNode(node)

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        self.visit_ArithNode(node)

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        self.visit_ArithNode(node)

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        self.visit_ArithNode(node)

    @visitor.when(LessEqNode)
    def visit(self, node: LessEqNode):
        self.visit_ArithNode(node)

    @visitor.when(LessNode)
    def visit(self, node: LessNode):
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
    def visit(self, node: IfGotoNode):
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
