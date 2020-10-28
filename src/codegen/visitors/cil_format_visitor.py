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

        @visitor.when(LoadNode)
        def visit(self, node: LoadNode):
            return f'{node.dest} = LOAD {node.msg}'

        @visitor.when(DynamicCallNode)
        def visit(self, node: DynamicCallNode):
            return f'{node.dest} = VCALL {node.type} {node.method}'

        @visitor.when(ArgNode)
        def visit(self, node: ArgNode):
            return f'ARG {node.name}'

        @visitor.when(ReturnNode)
        def visit(self, node: ReturnNode):
            return f'RETURN {node.value if node.value is not None else ""}'

        @visitor.when(GetAttribNode)
        def visit(self, node: GetAttribNode):
            return f'{node.dest} = GETATTR {node.obj} {node.attr.name}'

        @visitor.when(SetAttribNode)
        def visit(self, node: SetAttribNode):
            return f'SETATTR {node.obj} {node.attr.name} = {node.value}'

    printer = PrintVisitor()
    return lambda ast: printer.visit(ast)
