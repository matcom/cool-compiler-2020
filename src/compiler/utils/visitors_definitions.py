from ..utils.AST_definitions import *
from ..utils.context import programContext
from ..utils.errors import error

class NodeVisitor:

    def visit(self, node: Node):
        visitor_method_name = 'visit_' + node.clsname
        visitor = getattr(self, visitor_method_name, self.not_implemented)
        return visitor(node) # Return the new context result from the visit

    def not_implemented(self, node: Node):
        raise Exception('Not implemented visit_{} method'.format(node.clsname))        

# We need to highlight here the inheritance relations between classes
class TypeCollectorVisitor(NodeVisitor):

    def visit_NodeProgram(self, node: NodeProgram):
        errors = []
        for nodeClass in node.class_list:
            result= self.visit(nodeClass)
            if result:
                errors.append (result)
        return errors

    def visit_NodeClass(self, node: NodeClass):
        # When we create a type, we store it in the context, if there is no errors
        return programContext.createType(node)

class TypeBuilderVisitor(NodeVisitor):
    def __init__(self):
        self.currentTypeName = ''

    def visit_NodeProgram(self, node: NodeProgram):
        errors = []
        for nodeClass in node.class_list:
            errors += self.visit(nodeClass)
        return errors

    def visit_NodeClass(self, node: NodeClass):
        errors = []
        self.currentTypeName = node.idName
        for nodeAttr in node.attributes:
            errors += self.visit(nodeAttr)
        for nodeClassMethod in node.methods:
            errors += self.visit(nodeClassMethod)
        return errors

    def visit_NodeAttr(self, node:NodeAttr):
        resultOp = programContext.defineAttrInType(self.currentTypeName, node)
        if type (resultOp) is error:
            return [resultOp]
        return []

    def visit_NodeClassMethod(self, node: NodeClassMethod):
        return [definition for definition in
        [programContext.getType(node.returnType)] +
        [programContext.getType(idName = arg) for arg in node.argTypesNames] +
        [programContext.defineMethod(
            self.currentTypeName,
            node.idName,
            node.returnType,
            node.argNames,
            node.argTypesNames
            )]
        if type(definition) is error    
        ]
