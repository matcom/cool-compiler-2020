from typecheck.visitor import on, when
from abstract.semantics import *
from abstract.tree import *

class TypeChecker:
    def __init__(self, context:Context, errors = []):
        self.current_type = None
        self.context = context
        self.AUTO_TYPE = self.context.get_type('AUTO_TYPE')
        self.errors = errors

    @on('node')
    def visit(self, node, scope):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode, scope = None):
        scope = Scope()
        for class_ in node.class_list:
            self.visit(class_, scope.create_child())
    
    @when(ClassDef)
    def visit(self, node: ClassDef, scope: Scope):
        self.current_type = self.context.get_type(node.idx)
        for feature in node.features:
            self.visit(feature,scope) if isinstance(feature, AttributeDef) else pass
        
        for feature in node.features:
            self.visit(feature, scope.create_child()) if isinstance(feature, MethodDef) else pass
    
    @when(AttributeDef)
    def visit(self, node: AttributeDef, scope: Scope):
        att = self.current_type.get_attribute(node.idx)
        if att.type == self.AUTO_TYPE:
            self.errors.append(f'Cannot infer type of attribute {att.name}')
        scope.define_variable(typ.name, typ.type)
    
    @when(MethodDef)
    def visit(self, node: MethodDef, scope:Scope):
        m = self.current_type.get_method(node.idx)
        