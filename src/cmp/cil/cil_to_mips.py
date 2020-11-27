from .ast import (
    AllocateNode,
    ArgNode,
    ArithmeticNode,
    AssignNode,
    CleanArgsNode,
    ComplementNode,
    ConcatNode,
    CopyNode,
    DataNode,
    DivNode,
    DynamicCallNode,
    EqualNode,
    ErrorNode,
    FunctionNode,
    GetAttribNode,
    GotoIfNode,
    GotoNode,
    IsVoidNode,
    LabelNode,
    LengthNode,
    LessEqNode,
    LessNode,
    LocalNode,
    MinusNode,
    ParamNode,
    PlusNode,
    PrintIntNode,
    PrintStrNode,
    ProgramNode,
    ReadIntNode,
    ReadStrNode,
    ReturnNode,
    SetAttribNode,
    StarNode,
    StaticCallNode,
    StringEqualNode,
    SubstringNode,
    TypeNameNode,
    TypeNode,
    TypeOfNode,
)
from .utils import TypeData, on, when
from .utils.mips_syntax import Mips
from .utils.mips_syntax import Register as Reg


class CIL_TO_MIPS(object):
    def __init__(self, data_size: int = 8):
        self.types = []
        self.types_offsets = dict()
        self.local_vars_offsets = dict()
        self.actual_args = dict()
        self.mips = Mips()
        self.data_size = data_size
        self.label_count = -1

    def build_types_data(self, types):
        for idx, typex in enumerate(types):
            self.types_offsets[typex.name] = TypeData(idx, typex)

    def get_label(self):
        self.label_count += 1
        return f"mip_label_{self.label_count}"

    def load_memory(self, dst: Reg, arg: str):
        if arg in self.actual_args or arg in self.local_vars_offsets:
            offset = (
                self.actual_args[arg] + 1
                if arg in self.actual_args
                else -self.local_vars_offsets[arg]
            ) * self.data_size

            self.mips.load_memory(dst, self.mips.offset(Reg.fp, offset))
        else:
            raise Exception(f"load_memory: The direction {arg} isn't an address")
        self.mips.empty()

    def store_memory(self, dst: Reg, arg: str):
        if arg in self.local_vars_offsets:
            offset = -self.local_vars_offsets[arg] * self.data_size
            self.mips.store_memory(dst, self.mips.offset(Reg.fp, offset))
        else:
            raise Exception(f"store_memory: The direction {arg} isn't an address")
        self.mips.empty()

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
        self.mips.data_label(node.name)
        self.mips.asciiz(node.value)

    @when(TypeNode)
    def visit(self, node: TypeNode):  # noqa
        pass

    @when(FunctionNode)
    def visit(self, node: FunctionNode):  # noqa
        self.mips.empty()
        self.mips.label(node.name)

        self.mips.comment("Set stack frame")
        self.mips.push(Reg.fp)
        self.mips.move(Reg.fp, Reg.sp)

        self.actual_args = dict()

        for idx, param in enumerate(node.params):
            self.visit(param, index=idx)

        self.mips.empty()
        self.mips.comment("Allocate memory for Local variables")
        for idx, local in enumerate(node.localvars):
            self.visit(local, index=idx)

        self.mips.empty()
        # self.store_registers()
        self.mips.empty()
        self.mips.comment("Generating body code")
        for instruction in node.instructions:
            self.visit(instruction)

        self.actual_args = None
        self.mips.empty()
        # self.load_registers()

        self.mips.comment("Clean stack variable space")
        self.mips.addi(
            Reg.sp,
            Reg.sp,
            len(node.localvars) * self.data_size,
        )
        self.mips.comment("Return")
        self.mips.pop(Reg.fp)
        self.mips.jr(Reg.ra)
        self.mips.empty()

    @when(ParamNode)
    def visit(self, node: ParamNode, index=0):  # noqa
        self.actual_args[node.name] = index

    @when(LocalNode)
    def visit(self, node: LocalNode, index=0):  # noqa
        self.mips.push(Reg.zero)
        assert node.name not in self.local_vars_offsets, f"Impossible {node.name}..."
        self.local_vars_offsets[node.name] = index

    @when(CopyNode)
    def visit(self, node: CopyNode):  # noqa
        pass

    @when(TypeNameNode)
    def visit(self, node: TypeNameNode):  # noqa
        self.mips.comment("TypeNameNode")
        self.mips.la(Reg.t0, node.type)
        self.load_memory(Reg.t1, self.mips.offset(Reg.t0, self.data_size))
        self.store_memory(Reg.t1, node.dest)
        self.mips.empty()

    @when(ErrorNode)
    def visit(self, node: ErrorNode):  # noqa
        self.mips.comment("ErrorNode")
        self.mips.li(Reg.a0, 1)
        self.mips.exit2()
        self.mips.empty()

    @when(AssignNode)
    def visit(self, node: AssignNode):  # noqa
        self.mips.comment("AssignNode")
        self.load_memory(Reg.t0, node.source)
        self.store_memory(Reg.t0, node.dest)
        self.mips.empty()

    @when(IsVoidNode)
    def visit(self, node: IsVoidNode):  # noqa
        self.mips.comment("IsVoidNode")
        self.load_memory(Reg.t0, node.body)

        label = self.get_label()

        self.mips.li(Reg.t1, 0)
        self.mips.bne(Reg.t0, Reg.t1, label)
        self.mips.li(Reg.t1, 1)
        self.mips.label(label)
        self.store_memory(Reg.t1, node.dest)

        self.mips.empty()

    @when(ComplementNode)
    def visit(self, node: ComplementNode):  # noqa
        self.mips.comment("ComplementNode")

        self.load_memory(Reg.t0, node.body)
        self.mips.nor(Reg.t1, Reg.t0, Reg.t0)
        self.store_memory(Reg.t1, node.dest)

        self.mips.empty()

    def load_arithmetic(self, node: ArithmeticNode):
        self.load_memory(Reg.t0, node.left)
        self.load_memory(Reg.t1, node.right)

    @when(LessNode)
    def visit(self, node: LessNode):  # noqa
        self.load_arithmetic(node)
        self.mips.slt(Reg.t2, Reg.t0, Reg.t1)
        self.store_memory(Reg.t2, node.dest)

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

        self.store_memory(Reg.t1, node.dest)

    @when(LessEqNode)
    def visit(self, node: LessEqNode):  # noqa
        """
        a <= b -> ! b < a -> 1 - (b < a)
        """
        self.load_arithmetic(node)
        self.mips.slt(Reg.t2, Reg.t1, Reg.t0)
        self.mips.li(Reg.t3, 1)
        self.mips.sub(Reg.t0, Reg.t3, Reg.t2)
        self.store_memory(Reg.t0, node.dest)

    @when(PlusNode)
    def visit(self, node: PlusNode):  # noqa
        self.load_arithmetic(node)
        self.mips.add(Reg.t2, Reg.t0, Reg.t1)
        self.store_memory(Reg.t2, node.dest)

    @when(MinusNode)
    def visit(self, node: MinusNode):  # noqa
        self.load_arithmetic(node)
        self.mips.sub(Reg.t2, Reg.t0, Reg.t1)
        self.store_memory(Reg.t2, node.dest)

    @when(StarNode)
    def visit(self, node: StarNode):  # noqa
        self.load_arithmetic(node)
        self.mips.mult(Reg.t2, Reg.t0, Reg.t1)
        self.mips.mflo(Reg.t0)
        self.store_memory(Reg.t0, node.dest)

    @when(DivNode)
    def visit(self, node: DivNode):  # noqa
        self.load_arithmetic(node)
        self.mips.div(Reg.t2, Reg.t0, Reg.t1)
        self.mips.mflo(Reg.t0)
        self.store_memory(Reg.t0, node.dest)

    @when(AllocateNode)
    def visit(self, node: AllocateNode):  # noqa
        pass

    @when(TypeOfNode)
    def visit(self, node: TypeOfNode):  # noqa
        self.mips.comment("TypeOfNode")
        self.mips.la(Reg.t0, node.obj)
        self.load_memory(Reg.t1, self.mips.offset(Reg.t0))
        self.store_memory(Reg.t1, node.dest)
        self.mips.empty()

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
        self.mips.comment("ReturnNode")
        self.load_memory(Reg.v0, node.value)

    @when(ReadIntNode)
    def visit(self, node: ReadIntNode):  # noqa
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
        self.mips.comment("LabelNode")
        self.mips.label(node.label)

    @when(GotoNode)
    def visit(self, node: GotoNode):  # noqa
        self.mips.comment("GotoNode")
        self.mips.j(node.label)

    @when(GotoIfNode)
    def visit(self, node: GotoIfNode):  # noqa
        self.mips.comment("GotoIfNode")
        self.load_memory(Reg.t0, node.value)
        self.mips.li(Reg.t1, 0)
        self.mips.bne(Reg.t0, Reg.t1, node.label)
