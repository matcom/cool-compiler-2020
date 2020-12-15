from semantic import *

import visitors.visitor as visitor
from pipeline import State
from cl_ast import *

class TypeCollector(State):
    def __init__(self, name):
        super().__init__(name)
        self.context = Context()

    def run(self, ast):
        self.visit(ast)
        return ast, self.context 

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for dec in node.declarations:
            self.visit(dec)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)
        except ContextError as e:
            self.errors.append(CSemanticError(node.row, node.col, e.text))