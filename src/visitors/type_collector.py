from semantic import *

import visitors.visitor as visitor
from pipeline import State
from cl_ast import *

class TypeCollector(State):
    def __init__(self, name):
        super().__init__(name)
        self.context = Context()
        # register default types ( #TODO Move to Context class and add functions and attributes for each default types )
        self.context.types['String'] = StringType()
        self.context.types['Int'] = IntType()
        self.context.types['Object'] = ObjectType()
        self.context.types['Bool'] = BoolType()
        self.context.types['IO'] = IOType()

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
        except SemanticError as e:
            self.errors.append(e.text) # report error in valid format