import typecheck.visitor as visitor
from abstract.tree import *
from abstract.semantics import SemanticError, Type, VoidType, IntegerType, StringType, ObjectType, Attribute, Method, Context, BoolType, AutoType

class TypeCollector:
    def __init__(self, errors= []):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self,node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self,node):
        self.context = Context()
        OBJECT, INTEGER, STRING, BOOL, VOID = ObjectType(), IntegerType(), StringType(), BoolType(), VoidType()
        INTEGER.set_parent(OBJECT)
        STRING.set_parent(OBJECT)
        BOOL.set_parent(OBJECT)

        self.context.types['object'] = OBJECT
        self.context.types['int'] = INTEGER
        self.context.types['string'] = STRING
        self.context.types['bool'] = BOOL
        self.context.types['void'] = VOID
        self.context.types['AUTO_TYPE'] = AutoType()
        for class_ in node.class_list:
            self.visit(class_)
    
    @visitor.when(ClassDef)
    def visit(self,node):
        try:
            self.context.create_type(node.idx)
        except SemanticError as e:
            self.errors.append(e.text)
        
