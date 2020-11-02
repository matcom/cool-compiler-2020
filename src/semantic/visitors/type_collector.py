from utils.errors import SemanticError
from semantic.tools import Context
from utils import visitor
from semantic.types import *
from utils.ast import *

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        self.context = Context()
        self.context.types['String'] = StringType()
        self.context.types['Int'] = IntType()
        self.context.types['Object'] = ObjectType()
        self.context.types['Bool'] = BoolType()
        self.context.types['SELF_TYPE'] = SelfType()
        self.context.types['IO'] = IOType()
        # self.context.create_type('SELF_TYPE', (0, 0))
        for dec in node.declarations:
            self.visit(dec)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode):
        try:
            self.context.create_type(node.id, node.pos)
        except SemanticError as e:
            self.errors.append(e)
        # añade un como padre Object si este no tiene
        if not node.parent:
            node.parent = 'Object'
