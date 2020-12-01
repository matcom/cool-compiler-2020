from .utils import *
from ...visitors import visitor
from ...cmp import cool_ast as cool, SemanticError

# Type Verifier
class TypeVerifier:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cool.ProgramNode)
    def visit(self, node):
        for def_class in node.declarations:
            self.visit(def_class)         
    
    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        
        for feature in node.features:
            self.visit(feature)
            
    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node):
        pass
        
    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node):
        try:
            m1 = node.method
            m2 = self.current_type.parent.get_method(m1.name)
            assert m1.return_type == m2.return_type and m1.param_types == m2.param_types
        except AttributeError: 
            pass
        except SemanticError:
            pass
        except AssertionError:
            self.errors.append((SemanticError(f'Method "{m1.name}" already defined in {self.current_type.name} with a different signature.'), node.tid))
            