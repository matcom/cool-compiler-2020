from ..utils.AST_definitions import *
from ..utils.context import globalContex
from ..utils.errors import error


class NodeVisitor:
    def visit(self, node: Node):
        visitor_method_name = 'visit_' + node.clsname
        visitor = getattr(self, visitor_method_name, self.not_implemented)
        return visitor(node) # Return the new context result from the visit

    def not_implemented(self, node: Node):
        raise Exception('Not implemented visit_{} method'.format(node.clsname))        

# We need to highlight here the inheritance relations between classes
class TypeCheckVisitor(NodeVisitor):

    def visit_NodeProgram(self, node: NodeProgram):
        self.programContext = globalContex()
        self.programContext.initialize()
        errors = []
        for nodeClass in node.class_list:
            if nodeClass.idName in self.programContext.types:
                errors.append(
                    error(error_type="Semantic error",
                    row_and_col=(0, 0),
                    message="The class %s is already declared" %nodeClass.idName ))
            #If I get an error in type declaration, I pass its declaration
            else:
                self.visit(nodeClass)
        return self.programContext, errors

    def visit_NodeClass(self, node: NodeClass):
        # When we create a type, we store it in the programContext 
        self.programContext.createType(node)
        return self.programContext
    
