from .ast import ProgramNode, TypeNode, FunctionNode, ParamNode, LocalNode, AssignNode, PlusNode \
    , MinusNode, StarNode, DivNode, AllocateNode, TypeOfNode, StaticCallNode, DynamicCallNode    \
    , ArgNode, ReturnNode, ReadNode, PrintNode, LoadNode, LengthNode, ConcatNode, PrefixNode     \
    , SubstringNode, ToStrNode, GetAttribNode, SetAttribNode, LabelNode, GotoNode, GotoIfNode    \
    , DataNode, LessNode, LessEqNode, ComplementNode, IsVoidNode, EqualNode
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
        attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
        methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

        return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

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

    @when(AssignNode)
    def visit(self, node: AssignNode):
        return f'{node.dest} = {node.source}'

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
        return f'{node.dest} = TYPEOF {node.type}'

    @when(StaticCallNode)
    def visit(self, node: StaticCallNode):
        return f'{node.dest} = CALL {node.function}'

    @when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):
        return f'{node.dest} = VCALL {node.type} {node.method}'

    @when(ArgNode)
    def visit(self, node: ArgNode):
        return f'ARG {node.name}'

    @when(ReturnNode)
    def visit(self, node: ReturnNode):
        return f'RETURN {node.value if node.value is not None else ""}'

    @when(ReadNode)
    def visit(self, node: ReadNode):
        return f'{node.dest} = READ'

    @when(PrintNode)
    def visit(self, node: PrintNode):
        return f'PRINT {node.str_addr}'

    @when(LoadNode)
    def visit(self, node: LoadNode):
        return f'{node.dest} = LOAD {node.msg}'
    
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
        return f'{node.dest} = SUBSTRING {node.msg1} {node.msg2}'

    @when(ToStrNode)
    def visit(self, node: ToStrNode):
        return f'{node.dest} = STR {node.ivalue}'

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
