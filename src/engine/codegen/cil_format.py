from .cil_ast import *

from ..cp import visitor


class CIL_FORMATTER(object):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
        dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
        dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

        return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

    @visitor.when(DataNode)
    def visit(self, node: DataNode):
        return f'{node.name} = "{node.value}"'

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
        methods = '\n\t'.join(f'method {x}: {y}' for x, y in node.methods)

        return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        params = '\n\t'.join(self.visit(x) for x in node.params)
        localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
        instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

        return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

    @visitor.when(ParamNode)
    def visit(self, node: ParamNode):
        return f'PARAM {node.name}'

    @visitor.when(LocalNode)
    def visit(self, node: LocalNode):
        return f'LOCAL {node.name}'

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        return f'{node.dest} = {node.source}'

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        return f'{node.dest} = {node.left} + {node.right}'

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        return f'{node.dest} = {node.left} - {node.right}'

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        return f'{node.dest} = {node.left} * {node.right}'

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        return f'{node.dest} = {node.left} / {node.right}'

    @visitor.when(AllocateNode)
    def visit(self, node: AllocateNode):
        return f'{node.dest} = ALLOCATE {node.type}'

    @visitor.when(TypeOfNode)
    def visit(self, node: TypeOfNode):
        return f'{node.dest} = TYPEOF {node.obj}'

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode):
        return f'{node.dest} = CALL {node.function}'

    @visitor.when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):
        return f'{node.dest} = VCALL {node.type} {node.method}'

    @visitor.when(ArgNode)
    def visit(self, node: ArgNode):
        return f'ARG {node.name}'

    @visitor.when(ReturnNode)
    def visit(self, node: ReturnNode):
        return f'RETURN {node.value if node.value is not None else ""}'

    @visitor.when(ReadStrNode)
    def visit(self, node: ReadStrNode):
        return f'{node.dest} = READSTR'

    @visitor.when(PrintStrNode)
    def visit(self, node: PrintStrNode):
        return f'PRINTSTR {node.str_addr}'

    @visitor.when(LoadNode)
    def visit(self, node: LoadNode):
        return f'{node.dest} = LOAD {node.msg}'

    @visitor.when(LengthNode)
    def visit(self, node: LengthNode):
        return f'{node.dest} = LENGTH {node.msg}'

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        return f'{node.dest} = CONCAT {node.msg1} {node.msg2}'

    @visitor.when(EmptyArgs)
    def visit(self, node: EmptyArgs):
        return f'CLEAR {node.args} ARGS'

    @visitor.when(SubstringNode)
    def visit(self, node: SubstringNode):
        return f'{node.dest} = SUBSTRING {node.msg1} {node.start} {node.length}'

    @visitor.when(ReadIntNode)
    def visit(self, node: ReadIntNode):
        return f'{node.dest} = READINT'

    @visitor.when(PrintIntNode)
    def visit(self, node: PrintIntNode):
        return f'PRINTINT {node.str_addr}'

    @visitor.when(GetAttribNode)
    def visit(self, node: GetAttribNode):
        return f'{node.dest} = GETATTR {node.obj} {node.attrib}'

    @visitor.when(SetAttribNode)
    def visit(self, node: SetAttribNode):
        return f'SETATTR {node.attrib} OF {node.obj}_{node.type} = {node.value}'

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode):
        return f'LABEL {node.label}'

    @visitor.when(GotoNode)
    def visit(self, node: GotoNode):
        return f'GOTO {node.label}'

    @visitor.when(IfGotoNode)
    def visit(self, node: IfGotoNode):
        return f'IF {node.value} GOTO {node.label}'

    @visitor.when(ComplementNode)
    def visit(self, node: ComplementNode):
        return f'{node.dest} = COMPLEMENT {node.expression}'

    @visitor.when(LessNode)
    def visit(self, node: LessNode):
        return f'{node.dest} = {node.left} < {node.right}'

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode):
        return f'{node.dest} = ISVOID {node.expression}'

    @visitor.when(LessEqNode)
    def visit(self, node: LessEqNode):
        return f'{node.dest} = {node.left} <= {node.right}'

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        return f'{node.dest} = {node.left} == {node.right}'

    @visitor.when(ErrorNode)
    def visit(self, node: ErrorNode):
        return f'ERROR {node.error}'

    @visitor.when(BoxNode)
    def visit(self, node: BoxNode):
        return f'{node.dest} = {node.value}'

    @visitor.when(AbortNode)
    def visit(self, node: AbortNode):
        return f'ABORT'

    @visitor.when(VoidNode)
    def visit(self, node: VoidNode):
        return f'{node.dest} = VOID'

    @visitor.when(ConformsNode)
    def visit(self, node: ConformsNode):
        return f'{node.dest} = COMFORM {node.expr} {node.type}'

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        return f'{node.dest} = NOT {node.expression}'

    @visitor.when(StringEqualNode)
    def visit(self, node: StringEqualNode):
        return f'{node.dest} = STREQ {node.msg1} {node.msg2}'

    @visitor.when(CopyNode)
    def visit(self, node: CopyNode):
        return f'{node.dest} = COPY {node.obj}'

    @visitor.when(TypeNameNode)
    def visit(self, node: TypeNameNode):
        return f'{node.dest} = TYPENAME {node.type}'
