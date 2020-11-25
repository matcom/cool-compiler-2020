from .ast import (
    ProgramNode,
    TypeNode,
    FunctionNode,
    ParamNode,
    LocalNode,
    AssignNode,
    PlusNode,
    MinusNode,
    StarNode,
    DivNode,
    AllocateNode,
    TypeOfNode,
    StaticCallNode,
    DynamicCallNode,
    ArgNode,
    ReturnNode,
    ReadStrNode,
    ReadIntNode,
    PrintStrNode,
    PrintIntNode,
    LengthNode,
    ConcatNode,
    PrefixNode,
    SubstringNode,
    GetAttribNode,
    SetAttribNode,
    LabelNode,
    GotoNode,
    GotoIfNode,
    DataNode,
    LessNode,
    LessEqNode,
    ComplementNode,
    IsVoidNode,
    EqualNode,
    ConformNode,
    CleanArgsNode,
    ErrorNode,
    CopyNode,
    TypeNameNode,
    StringEqualNode,
    ArithmeticNode
)
from .utils import on, when
from .utils.mips_syntax import Mips, Register as Reg


class CIL_TO_MIPS(object):
    def __init__(self):
        self.types = []
        self.types_offsets = dict()
        self.local_vars_offsets = dict()
        self.actual_args = dict()
        self.mips = Mips()

    @on("node")
    def visit(self, node):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode):  # noqa
        self.types = node.dottypes
        self.build_types_data(self.types)

        for datanode in node.dotdata:
            self.visit(datanode)

        self.mips.label("main")

        self.mips.jal("entry")

        self.mips.exit()

        for function in node.dotcode:
            self.visit(function)

    @when(DataNode)
    def visit(self, node: DataNode):  # noqa
        self.mips.var_label(node.name)
        self.mips.asciiz(node.value)

    @when(TypeNode)
    def visit(self, node: TypeNode):  # noqa
        pass

    @when(FunctionNode)
    def visit(self, node: FunctionNode):  # noqa
        self.mips.empty_line()
        self.mips.label(node.name)
        self.mips.push(Reg.fp)
        self.mips.add(Reg.fp, Reg.zero, Reg.sp)
        self.actual_args = dict()

        self.mips.empty_line()
        for idx, param in enumerate(node.params):
            self.visit(param, index=idx)

        self.mips.empty_line()
        for idx, local in enumerate(node.localvars):
            self.visit(local, index=idx)

        self.mips.empty_line()
        # self.store_registers()
        self.mips.empty_line()
        for instruction in node.instructions:
            self.visit(instruction)

        self.actual_args = None
        self.mips.empty_line()
        # self.load_registers()

        self.mips.addi(Reg.sp, Reg.sp, len(node.localvars) * 8)
        self.mips.pop(Reg.fp)
        self.mips.jr(Reg.ra)
        self.mips.empty_line()

    @when(ParamNode)
    def visit(self, node: ParamNode, index=0):  # noqa
        self.actual_args[node.name] = index

    @when(LocalNode)
    def visit(self, node: LocalNode, index=0):  # noqa
        self.mips.push(Reg.zero)
        assert node.name not in self.local_vars_offsets, \
            f"Impossible {node.name}..."
        self.local_vars_offsets[node.name] = index

    @when(CopyNode)
    def visit(self, node: CopyNode):  # noqa
        pass

    @when(TypeNameNode)
    def visit(self, node: TypeNameNode):  # noqa
        pass

    @when(ErrorNode)
    def visit(self, node: ErrorNode):  # noqa
        pass

    @when(AssignNode)
    def visit(self, node: AssignNode):  # noqa
        pass

    @when(ConformNode)
    def visit(self, node: ConformNode):  # noqa
        pass

    @when(IsVoidNode)
    def visit(self, node: IsVoidNode):  # noqa
        pass

    @when(ComplementNode)
    def visit(self, node: ComplementNode):  # noqa
        pass

    def load_arithmetic(self, node: ArithmeticNode):
        self.mips.load_memory(Reg.t0, node.left.address)
        self.mips.load_memory(Reg.t1, node.right.address)

    @when(LessNode)
    def visit(self, node: LessNode):  # noqa
        self.load_arithmetic(node)
        self.mips.slt(Reg.v0, Reg.t0, Reg.t1)

        self.mips.store_memory(Reg.v0, node.dest.address)

    @when(EqualNode)
    def visit(self, node: EqualNode):  # noqa
        """
        ((a < b) + (b < a)) < 1  -> ==
        """
        self.load_arithmetic(node)
        self.mips.slt(Reg.t2, Reg.t0, Reg.t1)
        self.mips.slt(Reg.t3, Reg.t1, Reg.t0)

        self.mips.add(Reg.t0, Reg.t2, Reg.t3)
        self.mips.slti(Reg.t1, Reg.t0, 1)

        self.mips.store_memory(Reg.t1, node.dest.address)

    @when(LessEqNode)
    def visit(self, node: LessEqNode):  # noqa
        """
         a <= b -> ! b < a -> 1 - (b < a)
        """
        self.load_arithmetic(node)
        self.mips.slt(Reg.t2, Reg.t1, Reg.t0)
        self.mips.li(Reg.t3, 1)
        self.mips.sub(Reg.t0, Reg.t3, Reg.t2)

        self.mips.store_memory(Reg.t0, node.dest.address)

    @when(PlusNode)
    def visit(self, node: PlusNode):  # noqa
        self.load_arithmetic(node)
        self.mips.add(Reg.t2, Reg.t0, Reg.t1)

        self.mips.store_memory(Reg.t2, node.dest.address)

    @when(MinusNode)
    def visit(self, node: MinusNode):  # noqa
        self.load_arithmetic(node)
        self.mips.sub(Reg.t2, Reg.t0, Reg.t1)

        self.mips.store_memory(Reg.t2, node.dest.address)

    @when(StarNode)
    def visit(self, node: StarNode):  # noqa
        self.load_arithmetic(node)
        self.mips.mult(Reg.t2, Reg.t0, Reg.t1)
        self.mips.mflo(Reg.t0)
        self.mips.store_memory(Reg.t0, node.dest.address)

    @when(DivNode)
    def visit(self, node: DivNode):  # noqa
        self.load_arithmetic(node)
        self.mips.div(Reg.t2, Reg.t0, Reg.t1)
        self.mips.mflo(Reg.t0)
        self.mips.store_memory(Reg.t0, node.dest.address)

    @when(AllocateNode)
    def visit(self, node: AllocateNode):  # noqa
        node.type
        pass

    @when(TypeOfNode)
    def visit(self, node: TypeOfNode):  # noqa
        pass

    @when(StaticCallNode)
    def visit(self, node: StaticCallNode):  # noqa
        pass

    @when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):  # noqa
        pass

    @when(ArgNode)
    def visit(self, node: ArgNode):  # noqa
        pass

    @when(CleanArgsNode)
    def visit(self, node: CleanArgsNode):  # noqa
        pass

    @when(ReturnNode)
    def visit(self, node: ReturnNode):  # noqa
        pass

    @when(ReadIntNode)
    def visit(self, node: ReadIntNode):  # noqa
        node.name
        pass

    @when(ReadStrNode)
    def visit(self, node: ReadStrNode):  # noqa
        pass

    @when(PrintIntNode)
    def visit(self, node: PrintIntNode):  # noqa
        pass

    @when(PrintStrNode)
    def visit(self, node: PrintStrNode):  # noqa
        pass

    @when(LengthNode)
    def visit(self, node: LengthNode):  # noqa
        pass

    @when(ConcatNode)
    def visit(self, node: ConcatNode):  # noqa
        pass

    @when(PrefixNode)
    def visit(self, node: PrefixNode):  # noqa
        pass

    @when(SubstringNode)
    def visit(self, node: SubstringNode):  # noqa
        pass

    @when(StringEqualNode)
    def visit(self, node: StringEqualNode):  # noqa
        pass

    @when(GetAttribNode)
    def visit(self, node: GetAttribNode):  # noqa
        pass

    @when(SetAttribNode)
    def visit(self, node: SetAttribNode):  # noqa
        pass

    @when(LabelNode)
    def visit(self, node: LabelNode):  # noqa
        pass

    @when(GotoNode)
    def visit(self, node: GotoNode):  # noqa
        pass

    @when(GotoIfNode)
    def visit(self, node: GotoIfNode):  # noqa
        pass
