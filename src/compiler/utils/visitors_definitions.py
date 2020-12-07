from ..utils.AST_definitions import *
from ..utils.context import programContext
from ..utils.errors import error

class NodeVisitor:

    def visit(self, node: Node, **args):
        if node.__class__.__bases__[0] is NodeBinaryOperation:
            return self.visit_NodeBinaryOperation(node, **args)
        visitor_method_name = 'visit_' + node.clsname
        visitor = getattr(self, visitor_method_name, self.not_implemented)
        
        return visitor(node, **args) # Return the new context result from the visit

    def not_implemented(self, node: Node):
        raise Exception('Not implemented visit_{} method'.format(node.clsname))

# We need to highlight here the inheritance relations between classes
class TypeCollectorVisitor(NodeVisitor):

    def visit_NodeProgram(self, node: NodeProgram):
        errors = []
        for nodeClass in node.class_list:
            
            result= self.visit(nodeClass)
            if result:
                errors.append(result)
        return errors

    def visit_NodeClass(self, node: NodeClass):
        # When we create a type, we store it in the context, if there is no errors
        return programContext.createType(node)

class TypeInheritanceVisitor(NodeVisitor):
    def visit_NodeProgram(self, node: NodeProgram):
        errors = []
        for nodeClass in node.class_list:
            result = self.visit(nodeClass)
            if type (result) is error:
                errors.append(result)
        return errors

    def visit_NodeClass(self, node: NodeClass):
        return programContext.relateInheritance(node)

class TypeBuilderVisitor(NodeVisitor):
    def __init__(self):
        self.currentTypeName = ''

    def visit_NodeProgram(self, node: NodeProgram):
        errors = []
        for nodeClass in node.class_list:
            errors += self.visit(nodeClass)
        return errors

    def visit_NodeClass(self, node: NodeClass):
        errors= []
        self.currentTypeName= node.idName
        
        for nodeAttr in node.attributes:
            errors += self.visit(nodeAttr)
        for nodeClassMethod in node.methods:
            errors += self.visit(nodeClassMethod)
        return errors

    def visit_NodeAttr(self, node:NodeAttr):
        resultOp = programContext.defineAttrInType(self.currentTypeName,
        node)
        
        if type (resultOp) is error:
            return [resultOp]
        
        return []

    def visit_NodeClassMethod(self, node: NodeClassMethod):
        return [definition for definition in
        [programContext.getType(node.returnType)] +
        [programContext.getType(idName = arg) for arg in node.argTypes] +
        [programContext.defineMethod(
            typeName = self.currentTypeName,
            node= node
            )]
        if type(definition) is error
        ]


class TypeCheckerVisitor(NodeVisitor):
    def __init__(self):
        pass
        

    def visit_NodeProgram(self, node: NodeProgram):
        errors = []
        for nodeClass in node.class_list:
            environment = programContext.buildEnv (typeName= nodeClass.idName)
            errors += self.visit(nodeClass, environment= environment)
            
        return errors

    def visit_NodeClass(self, node: NodeClass, environment):
        errors = []
        for nodeAttr in node.attributes:
            result= self.visit(nodeAttr, environment= environment)
            if type(result) is error:
                errors.append(result)
            environment.update({
                nodeAttr.idName: result
            })
        
        for nodeClassMethod in node.methods:
            result= self.visit(nodeClassMethod, environment= environment)
            if type(result) is error:
                errors.append(result)
        
        programContext.checkInheritedInfo(node.idName)
        return errors

    def visit_NodeClassMethod(self, node: NodeClassMethod, environment):
        pass

    def visit_NodeAttr(self, node: NodeAttr, environment):
        exprResult= self.visit(node.expr, 
                          environment= environment)
        
        if type(exprResult) is error:
            return exprResult
        assignResult= programContext.assignValue(node, exprResult)
        if type(assignResult) is error:
            return assignResult
        return exprResult
        
        

    # Esto es un let complex, calcula todos los inner lets y a partir de ellos 
    # obtiene el valor de la expresión de la derecha del IN 
    def visit_NodeLetComplex(self,
                             node: NodeLetComplex,
                             environment):
        
        for nodeLet in node.nestedLets:
            result= self.visit(nodeLet, 
                               environment= environment)
            if type(result) is error:
                return result
            environment.update({
                nodeLet.idName: result
            })

        return self.visit( node.body,
                           environment= environment)

    def visit_NodeLet(self, node: NodeLet, environment):
        errors= []
        exprResult= self.visit(node.body, 
                               environment= environment)
        if type(exprResult) is error:
            return exprResult
        assingResult = programContext.assignValue(node,
                                                  exprResult)
        if type(assingResult) is error:
            return assingResult
        return exprResult
        
    
    def visit_NodeBinaryOperation(self,
                                  node: NodeBinaryOperation, 
                                  environment):
        
        exprResultFirst= self.visit(node.first, 
                                    environment= environment)
        
        exprResultSecond= self.visit(node.second, 
                                     environment= environment)
       
        if type (exprResultFirst) is error:
            return exprResultFirst

        if type (exprResultSecond) is error:
            return exprResultSecond

        func= None
        if type(node) is NodeAddition:
            func= lambda : {'value': exprResultFirst['value'] + exprResultSecond['value'], 'type': 'Int'}
        
        if type(node) is NodeSubtraction:
            func= lambda : {'value': exprResultFirst['value'] - exprResultSecond['value'], 'type': 'Int'}

        if type(node) is NodeMultiplication:
            func= lambda : {'value': exprResultFirst['value'] * exprResultSecond['value'], 'type': 'Int'}

        if type(node) is NodeDivision:
            func= lambda : {'value': exprResultFirst['value'] / exprResultSecond['value'], 'type': 'Int'}

        result= programContext.executeArithmetic(func, exprResultFirst['type'],
                                          exprResultSecond['type'])
        return result
        
    def visit_NodeNewObject(self, node: NodeNewObject):
        return programContext.getType(node.type)
        
    def visit_NodeExpr(self,
                       node: NodeExpr,
                       environment):
        return self.visit(node, environment= environment)
        
    def visit_NodeInteger(self, 
                          node: NodeInteger,
                          **args):
        return {"type": 'Int', "value": node.content}
    
    def visit_NodeObject(self,
                         node: NodeObject,
                         environment):
        
        return programContext.searchValue(node,
                                          environment)
        
    def visit_NodeDynamicDispatch(self, node: NodeDynamicDispatch):
        exprVal= self.visit_NodeExpr(node.instance)
        return programContext.checkDynamicDispatch(exprVal,
        node.method, node.arguments)
        