from ..utils.AST_definitions import *
from ..utils.context import globalContex

#Necesito en ejecución definir nuevos tipos.
#Tal como hacen las interfaces en C#.
class NodeVisitor:
    def visit(self, node: Node):
        visitor_method_name = 'visit_' + node.clsname
        visitor = getattr(self, visitor_method_name, self.not_implemented)
        return visitor(node) # Return the new context result from the visit

    def not_implemented(self, node: Node):
        raise Exception('Not implemented visit_{} method'.format(node.clsname))        


class TypeCheckVisitor(NodeVisitor):

    def visit_NodeProgram(self, node: NodeProgram):
        self.programContext  = globalContex()
        self.programContext.initialize()
        for classNode in node.class_list:
            self.visit(classNode)

    def visit_NodeClass(self, node: NodeClass):
        self.programContext.createType(node)