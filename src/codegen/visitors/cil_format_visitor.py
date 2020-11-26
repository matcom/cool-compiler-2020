from utils import visitor
from codegen.cil_ast import *

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node: ProgramNode):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(TypeNode)
        def visit(self, node: TypeNode):
            attributes = '\n\t'.join(f'attribute {x}: {y}' for x, y in node.attributes)
            methods = '\n\t'.join(f'method {x}: {y}' for x, y in node.methods)

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(FunctionNode)
        def visit(self, node: FunctionNode):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'
        
        @visitor.when(DataNode)
        def visit(self, node: DataNode):
            return f'{node.name} = "{node.value}"'

        @visitor.when(ParamNode)
        def visit(self, node: ParamNode):
            return f'PARAM {node.name}'

        @visitor.when(LocalNode)
        def visit(self, node: LocalNode):
            return f'LOCAL {node.name}'

        @visitor.when(AssignNode)
        def visit(self, node: AssignNode):
            return f'{node.dest} = {node.source}'
        
        @visitor.when(NotNode)
        def visit(self, node: NotNode):
            return f'{node.dest} = ~{node.expr}'

        @visitor.when(LogicalNotNode)
        def visit(self, node: LogicalNotNode):
            return f'{node.dest} = NOT {node.expr}'

        @visitor.when(VoidConstantNode)
        def visit(self, node: VoidConstantNode):
            return f'{node.obj} = Void'

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

        @visitor.when(LessEqNode)
        def visit(self, node: LessEqNode):
            return f'{node.dest} = {node.left} <= {node.right}'

        @visitor.when(LessNode)
        def visit(self, node: LessNode):
            return f'{node.dest} = {node.left} < {node.right}'

        @visitor.when(EqualNode)
        def visit(self, node: StarNode):
            return f'{node.dest} = {node.left} = {node.right}'

        @visitor.when(AllocateNode)
        def visit(self, node: AllocateNode):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(TypeOfNode)
        def visit(self, node: TypeOfNode):
            return f'{node.dest} = TYPEOF {node.obj}'

        @visitor.when(GotoNode)
        def visit(self, node: GotoNode):
            return f'GOTO {node.label}'

        @visitor.when(GotoIfNode)
        def visit(self, node: GotoIfNode):
            return f'IF {node.cond} GOTO {node.label}'

        @visitor.when(GotoIfFalseNode)
        def visit(self, node: GotoIfFalseNode):
            return f'IF NOT {node.cond} GOTO {node.label}'

        @visitor.when(LabelNode)
        def visit(self, node: LabelNode):
            return f'LABEL {node.label}'

        @visitor.when(StaticCallNode)
        def visit(self, node: StaticCallNode):
            args = '\n\t'.join(self.visit(arg) for arg in node.args)
            return f'{args}\n' + f'\t{node.dest} = CALL {node.function}'

        @visitor.when(LoadNode)
        def visit(self, node: LoadNode):
            return f'{node.dest} = LOAD {node.msg}'

        @visitor.when(DynamicCallNode)
        def visit(self, node: DynamicCallNode):
            args = '\n\t'.join(self.visit(arg) for arg in node.args)
            return f'{args}\n' + f'\t{node.dest} = VCALL {node.type} {node.method}'

        @visitor.when(ArgNode)
        def visit(self, node: ArgNode):
            return f'ARG {node.dest}'

        @visitor.when(ReturnNode)
        def visit(self, node: ReturnNode):
            return f'RETURN {node.value if node.value is not None else ""}'

        @visitor.when(GetAttribNode)
        def visit(self, node: GetAttribNode):
            return f'{node.dest} = GETATTR {node.obj} {node.attr}'

        @visitor.when(SetAttribNode)
        def visit(self, node: SetAttribNode):
            return f'SETATTR {node.obj} {node.attr} = {node.value}'

        @visitor.when(LengthNode)
        def visit(self, node: LengthNode):
            return f'{node.dest} = LENGTH {node.arg}'

        @visitor.when(ConcatNode)
        def visit(self, node: ConcatNode):
            return f'{node.dest} = CONCAT {node.arg1} {node.arg2}'

        @visitor.when(SubstringNode)
        def visit(self, node: SubstringNode):
            return f'{node.dest} = SUBSTRING {node.word} {node.begin} {node.end}'

        @visitor.when(ToStrNode)
        def visit(self, node: ToStrNode):
            return f'{node.dest} = STR {node.ivalue}'

        @visitor.when(OutStringNode)
        def visit(self, node: OutStringNode):
            return f'OUT_STR {node.value}'

        @visitor.when(OutIntNode)
        def visit(self, node: OutIntNode):
            return f'OUT_INT {node.value}'

        @visitor.when(ReadStringNode)
        def visit(self, node: ReadStringNode):
            return f'{node.dest} = READ_STR'

        @visitor.when(ReadIntNode)
        def visit(self, node: ReadIntNode):
            return f'{node.dest} = READ_INT'

        @visitor.when(ExitNode)
        def visit(self, node: ExitNode):
            return f'EXIT {node.value}'

        @visitor.when(CopyNode)
        def visit(self, node: CopyNode):
            return f'{node.dest} = COPY {node.source}'

        @visitor.when(ConformsNode)
        def visit(self, node: ConformsNode):
            return f'{node.dest} = CONFORMS {node.expr} {node.type}'

        @visitor.when(ErrorNode)
        def visit(self, node: ErrorNode):
            return f'ERROR {node.type}'

    printer = PrintVisitor()
    return lambda ast: printer.visit(ast)
