from ..utils.AST_definitions import *
from ..utils.context import programContext
from ..utils.errors import error

class NodeVisitor:

    def __init__(self):
        self.errors = []

    def visit(self, node: Node):
        visitor_method_name = 'visit_' + node.clsname
        visitor = getattr(self, visitor_method_name, self.not_implemented)
        return visitor(node) # Return the new context result from the visit

    def not_implemented(self, node: Node):
        raise Exception('Not implemented visit_{} method'.format(node.clsname))        

# We need to highlight here the inheritance relations between classes
class TypeCheckVisitor(NodeVisitor):

    def visit_NodeProgram(self, node: NodeProgram):
        for nodeClass in node.class_list:
            self.visit(nodeClass)

    def visit_NodeClass(self, node: NodeClass):
        # When we create a type, we store it in the context
        result = programContext.createType(node) 
        if not result is 'Success':
            self.errors += result

class TypeBuilderVisitor(NodeVisitor):

    def visit_NodeClass(self, node: NodeClass):
        currentClassContext = programContext.types[node.idName]
        for attr in currentClassContext.attrs:
            self.visit(attr)
        for method in currentClassContext.methods:
            self.visit(method)
