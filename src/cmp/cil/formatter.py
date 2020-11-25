from .ast import ProgramNode, TypeNode, FunctionNode, ParamNode, LocalNode, AssignNode, PlusNode \
    , MinusNode, StarNode, DivNode, AllocateNode, TypeOfNode, StaticCallNode, DynamicCallNode    \
    , ArgNode, ReturnNode, ReadStrNode, ReadIntNode, PrintStrNode, PrintIntNode, LengthNode, ConcatNode, PrefixNode     \
    , SubstringNode, GetAttribNode, SetAttribNode, LabelNode, GotoNode, GotoIfNode    \
    , DataNode, LessNode, LessEqNode, ComplementNode, IsVoidNode, EqualNode, ConformNode         \
    , CleanArgsNode, ErrorNode, CopyNode, TypeNameNode, StringEqualNode
from .utils import on, when


class CIL_FORMATTER(object):
    @on('node')
    def visit(self, node):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode):
        dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
        dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
        dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

        return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

    @when(DataNode)
    def visit(self, node: DataNode):
        return f'{node.name} = "{node.value}"'

    @when(TypeNode)
    def visit(self, node: TypeNode):
        features = '\n\t'.join(f'attribute {feature}' if isinstance(feature, str) else f'method {feature[0]}: {feature[1]}' for feature in node.features)
        
        return f'type {node.name} {{\n\t{features}\n}}'

    @when(FunctionNode)
    def visit(self, node: FunctionNode):
        params = '\n\t'.join(self.visit(x) for x in node.params)
        localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
        instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

        return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

    @when(ParamNode)
    def visit(self, node: ParamNode):
        return f'PARAM {node.name}'

    @when(LocalNode)
    def visit(self, node: LocalNode):
        return f'LOCAL {node.name}'

    @when(CopyNode)
    def visit(self, node: CopyNode):
        return f'{node.dest} = COPY {node.obj}'

    @when(TypeNameNode)
    def visit(self, node: TypeNameNode):
        return f'{node.dest} = TYPENAME {node.type}'

    @when(ErrorNode)
    def visit(self, node: ErrorNode):
        return f'ERROR {node.error}'

    @when(AssignNode)
    def visit(self, node: AssignNode):
        return f'{node.dest} = {node.source}'

    @when(ConformNode)
    def visit(self, node: ConformNode):
        return f'{node.dest} = COMFORM {node.obj} {node.type}'

    @when(IsVoidNode)
    def visit(self, node: IsVoidNode):
        return f'{node.dest} = ISVOID {node.body}'

    @when(ComplementNode)
    def visit(self, node: ComplementNode):
        return f'{node.dest} = COMPLEMENT {node.body}'

    @when(LessNode)
    def visit(self, node: LessNode):
        return f'{node.dest} = {node.left} < {node.right}'
        
    @when(EqualNode)
    def visit(self, node: EqualNode):
        return f'{node.dest} = {node.left} == {node.right}'

    @when(LessEqNode)
    def visit(self, node: LessEqNode):
        return f'{node.dest} = {node.left} <= {node.right}'

    @when(PlusNode)
    def visit(self, node: PlusNode):
        return f'{node.dest} = {node.left} + {node.right}'

    @when(MinusNode)
    def visit(self, node: MinusNode):
        return f'{node.dest} = {node.left} - {node.right}'

    @when(StarNode)
    def visit(self, node: StarNode):
        return f'{node.dest} = {node.left} * {node.right}'

    @when(DivNode)
    def visit(self, node: DivNode):
        return f'{node.dest} = {node.left} / {node.right}'

    @when(AllocateNode)
    def visit(self, node: AllocateNode):
        return f'{node.dest} = ALLOCATE {node.type}'

    @when(TypeOfNode)
    def visit(self, node: TypeOfNode):
        return f'{node.dest} = TYPEOF {node.obj}'

    @when(StaticCallNode)
    def visit(self, node: StaticCallNode):
        return f'{node.dest} = CALL {node.function}'

    @when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):
        return f'{node.dest} = VCALL {node.type} {node.method}'

    @when(ArgNode)
    def visit(self, node: ArgNode):
        return f'ARG {node.name}'

    @when(CleanArgsNode)
    def visit(self, node:CleanArgsNode):
        return f'CLEANARG {node.nargs}'

    @when(ReturnNode)
    def visit(self, node: ReturnNode):
        return f'RETURN {node.value if node.value is not None else ""}'

    @when(ReadIntNode)
    def visit(self, node: ReadIntNode):
        return f'{node.dest} = READINT'

    @when(ReadStrNode)
    def visit(self, node: ReadStrNode):
        return f'{node.dest} = READSTR'

    @when(PrintIntNode)
    def visit(self, node: PrintIntNode):
        return f'PRINTINT {node.str_addr}'

    @when(PrintStrNode)
    def visit(self, node: PrintStrNode):
        return f'PRINTSTR {node.str_addr}'

    @when(LengthNode)
    def visit(self, node: LengthNode):
        return f'{node.dest} = LENGTH {node.msg}'
    
    @when(ConcatNode)
    def visit(self, node: ConcatNode):
        return f'{node.dest} = CONCAT {node.msg1} {node.msg2}'

    @when(PrefixNode)
    def visit(self, node: PrefixNode):
        return f'{node.dest} = PREFIX {node.msg1} {node.msg2}'

    @when(SubstringNode)
    def visit(self, node: SubstringNode):
        return f'{node.dest} = SUBSTRING {node.msg1} {node.start} {node.length}'

    @when(StringEqualNode)
    def visit(self, node: StringEqualNode):
        return f'{node.dest} = STREQ {node.msg1} {node.msg2}'

    @when(GetAttribNode)
    def visit(self, node: GetAttribNode):
        return f'{node.dest} = GETATTR {node.obj} {node.attrib}'

    @when(SetAttribNode)
    def visit(self, node: SetAttribNode):
        return f'SETATTR {node.obj} {node.attrib} {node.value}'

    @when(LabelNode)
    def visit(self, node: LabelNode):
        return f'LABEL {node.label}'

    @when(GotoNode)
    def visit(self, node: GotoNode):
        return f'GOTO {node.label}'

    @when(GotoIfNode)
    def visit(self, node: GotoIfNode):
        return f'IF {node.value} GOTO {node.label}'
