from .cil import *
from ...visitors import visitor

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(TypeNode)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(DataNode)
        def visit(self, node):
            return f'{node.name} = {node.value}'

        @visitor.when(FunctionNode)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions if self.visit(x) != [])

            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

        @visitor.when(ParamNode)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalNode)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(AssignNode)
        def visit(self, node):
            return f'{node.dest} = {node.source}'

        @visitor.when(PlusNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} + {node.right}'

        @visitor.when(MinusNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} - {node.right}'

        @visitor.when(StarNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} * {node.right}'

        @visitor.when(DivNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} / {node.right}'

        @visitor.when(LessEqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} <= {node.right}'

        @visitor.when(LessNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} < {node.right}'

        @visitor.when(EqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} == {node.right}'

        @visitor.when(GetAttribNode)
        def visit(self, node):
            return f'{node.dest} = GETATTR {node.obj} {node.attr}'

        @visitor.when(SetAttribNode)
        def visit(self, node):
            return f'SETATTR {node.obj} {node.attr} {node.value}'

        @visitor.when(AllocateNode)
        def visit(self, node):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(TypeOfNode)
        def visit(self, node):
            return f'{node.dest} = TYPEOF {node.obj}'

        @visitor.when(LabelNode)
        def visit(self, node):
            return f'LABEL {node.label}'

        @visitor.when(GotoNode)
        def visit(self, node):
            return f'GOTO {node.label}'

        @visitor.when(GotoIfNode)
        def visit(self, node):
            return f'IF {node.condition} GOTO {node.label}'

        @visitor.when(StaticCallNode)
        def visit(self, node):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(DynamicCallNode)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.type} {node.method}'

        @visitor.when(ArgNode)
        def visit(self, node):
            return f'ARG {node.name}'

        @visitor.when(ReturnNode)
        def visit(self, node):
            return f'RETURN {node.value if node.value is not None else ""}'

        @visitor.when(LoadNode)
        def visit(self, node):
            return f'{node.dest} = Load {node.msg}'

        @visitor.when(ExitNode)
        def visit(self, node):
            return f'EXIT'

        @visitor.when(TypeNameNode)
        def visit(self, node):
            return f'{node.dest} = TYPENAME {node.source}'

        @visitor.when(NameNode)
        def visit(self, node):
            return f'{node.dest} = NAME {node.name}'

        @visitor.when(CopyNode)
        def visit(self, node):
            return f'{node.dest} = COPY {node.source}'

        @visitor.when(LengthNode)
        def visit(self, node):
            return f'{node.dest} = LENGTH {node.source}'

        @visitor.when(ConcatNode)
        def visit(self, node):
            return f'{node.dest} = CONCAT {node.prefix} {node.suffix}'

        @visitor.when(SubstringNode)
        def visit(self, node):
            return f'{node.dest} = SUBSTRING {node.index} {node.length}'

        @visitor.when(ReadStrNode)
        def visit(self, node):
            return f'{node.dest} = READSTR'

        @visitor.when(ReadIntNode)
        def visit(self, node):
            return f'{node.dest} = READINT'

        @visitor.when(PrintStrNode)
        def visit(self, node):
            return f'PRINT {node.value}'

        @visitor.when(PrintIntNode)
        def visit(self, node):
            return f'PRINT {node.value}'

        @visitor.when(ComplementNode)
        def visit(self, node):
            return f'{node.dest} = COMPL {node.obj}'

        @visitor.when(VoidNode)
        def visit(self, node):
            return 'VOID'

        @visitor.when(ErrorNode)
        def visit(self, node):
            return f'ERROR {node.data_node}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))
    