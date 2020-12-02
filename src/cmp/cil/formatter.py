from .ast import (
    AbortNode,
    AllocateNode,
    ArgNode,
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
    NotNode,
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
    VoidNode,
    StaticTypeOfNode,
    SetNode
)
from .utils import on, when


class CIL_FORMATTER(object):
    @on("node")
    def visit(self, node):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode):  # noqa:F811
        dottypes = "\n".join(self.visit(t) for t in node.dottypes)
        dotdata = "\n".join(self.visit(t) for t in node.dotdata)
        dotcode = "\n".join(self.visit(t) for t in node.dotcode)

        return f".TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}"

    @when(DataNode)
    def visit(self, node: DataNode):  # noqa:F811
        return f'{node.name} = "{node.value}"'

    @when(TypeNode)
    def visit(self, node: TypeNode):  # noqa:F811
        features = "\n\t".join(
            f"attribute {feature}"
            if isinstance(feature, str)
            else f"method {feature[0]}: {feature[1]}"
            for feature in node.features
        )

        return f"type {node.name} {{\n\t{features}\n}}"

    @when(FunctionNode)
    def visit(self, node: FunctionNode):  # noqa:F811
        params = "\n\t".join(self.visit(x) for x in node.params)
        localvars = "\n\t".join(self.visit(x) for x in node.localvars)
        instructions = "\n\t".join(self.visit(x) for x in node.instructions)

        result = f"function {node.name} {{\n\t{params}\n\n\t"
        result += f"{localvars}\n\n\t{instructions}\n}}"
        return result

    @when(ParamNode)
    def visit(self, node: ParamNode):  # noqa:F811
        return f"PARAM {node.name}"

    @when(LocalNode)
    def visit(self, node: LocalNode):  # noqa:F811
        return f"LOCAL {node.name}"

    @when(CopyNode)
    def visit(self, node: CopyNode):  # noqa:F811
        return f"{node.dest} = COPY {node.obj}"

    @when(TypeNameNode)
    def visit(self, node: TypeNameNode):  # noqa:F811
        return f"{node.dest} = TYPENAME {node.type}"

    @when(ErrorNode)
    def visit(self, node: ErrorNode):  # noqa:F811
        return f"ERROR {node.error}"

    @when(AssignNode)
    def visit(self, node: AssignNode):  # noqa:F811
        return f"{node.dest} = {node.source}"

    @when(SetNode)
    def visit(self, node: SetNode):  # noqa:F811
        return f"{node.dest} = {node.value}"

    @when(IsVoidNode)
    def visit(self, node: IsVoidNode):  # noqa:F811
        return f"{node.dest} = ISVOID {node.body}"

    @when(VoidNode)
    def visit(self, node: VoidNode):  # noqa:F811
        return f"{node.dest} = VOID"

    @when(ComplementNode)
    def visit(self, node: ComplementNode):  # noqa:F811
        return f"{node.dest} = COMPLEMENT {node.body}"

    @when(NotNode)
    def visit(self, node: NotNode):  # noqa:F811
        return f"{node.dest} = NOT {node.body}"

    @when(LessNode)
    def visit(self, node: LessNode):  # noqa:F811
        return f"{node.dest} = {node.left} < {node.right}"

    @when(EqualNode)
    def visit(self, node: EqualNode):  # noqa:F811
        return f"{node.dest} = {node.left} == {node.right}"

    @when(LessEqNode)
    def visit(self, node: LessEqNode):  # noqa:F811
        return f"{node.dest} = {node.left} <= {node.right}"

    @when(PlusNode)
    def visit(self, node: PlusNode):  # noqa:F811
        return f"{node.dest} = {node.left} + {node.right}"

    @when(MinusNode)
    def visit(self, node: MinusNode):  # noqa:F811
        return f"{node.dest} = {node.left} - {node.right}"

    @when(StarNode)
    def visit(self, node: StarNode):  # noqa:F811
        return f"{node.dest} = {node.left} * {node.right}"

    @when(DivNode)
    def visit(self, node: DivNode):  # noqa:F811
        return f"{node.dest} = {node.left} / {node.right}"

    @when(AllocateNode)
    def visit(self, node: AllocateNode):  # noqa:F811
        return f"{node.dest} = ALLOCATE {node.type}"

    @when(TypeOfNode)
    def visit(self, node: TypeOfNode):  # noqa:F811
        return f"{node.dest} = TYPEOF {node.obj}"

    @when(StaticTypeOfNode)
    def visit(self, node: StaticTypeOfNode):  # noqa:F811
        return f"{node.dest} = TYPE {node.type}"

    @when(StaticCallNode)
    def visit(self, node: StaticCallNode):  # noqa:F811
        return f"{node.dest} = CALL {node.function}"

    @when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):  # noqa:F811
        return f"{node.dest} = VCALL {node.type} {node.method}"

    @when(ArgNode)
    def visit(self, node: ArgNode):  # noqa:F811
        return f"ARG {node.name}"

    @when(CleanArgsNode)
    def visit(self, node: CleanArgsNode):  # noqa:F811
        return f"CLEANARG {node.nargs}"

    @when(ReturnNode)
    def visit(self, node: ReturnNode):  # noqa:F811
        return f'RETURN {node.value if node.value is not None else ""}'

    @when(ReadIntNode)
    def visit(self, node: ReadIntNode):  # noqa:F811
        return f"{node.dest} = READINT"

    @when(ReadStrNode)
    def visit(self, node: ReadStrNode):  # noqa:F811
        return f"{node.dest} = READSTR"

    @when(PrintIntNode)
    def visit(self, node: PrintIntNode):  # noqa:F811
        return f"PRINTINT {node.str_addr}"

    @when(PrintStrNode)
    def visit(self, node: PrintStrNode):  # noqa:F811
        return f"PRINTSTR {node.str_addr}"

    @when(LengthNode)
    def visit(self, node: LengthNode):  # noqa:F811
        return f"{node.dest} = LENGTH {node.msg}"

    @when(ConcatNode)
    def visit(self, node: ConcatNode):  # noqa:F811
        return f"{node.dest} = CONCAT {node.msg1} {node.msg2}"

    @when(SubstringNode)
    def visit(self, node: SubstringNode):  # noqa:F811
        result = f"{node.dest} = SUBSTRING {node.msg1} "
        result += f"{node.start} {node.length}"
        return result

    @when(StringEqualNode)
    def visit(self, node: StringEqualNode):  # noqa:F811
        return f"{node.dest} = STREQ {node.msg1} {node.msg2}"

    @when(GetAttribNode)
    def visit(self, node: GetAttribNode):  # noqa:F811
        return f"{node.dest} = GETATTR {node.obj} {node.attrib} {node.type}"

    @when(SetAttribNode)
    def visit(self, node: SetAttribNode):  # noqa:F811
        return f"SETATTR {node.obj} {node.attrib} {node.value} {node.type}"

    @when(LabelNode)
    def visit(self, node: LabelNode):  # noqa:F811
        return f"LABEL {node.label}"

    @when(GotoNode)
    def visit(self, node: GotoNode):  # noqa:F811
        return f"GOTO {node.label}"

    @when(GotoIfNode)
    def visit(self, node: GotoIfNode):  # noqa:F811
        return f"IF {node.value} GOTO {node.label}"

    @when(AbortNode)
    def visit(self, node: AbortNode):  # noqa:F811
        return "ABORT"
