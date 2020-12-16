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
        for _type in programContext.types:
            if _type != 'Object':
                result = self.visitForInherit(_type)
                if type (result) is error:
                    errors.append(result)
        return errors

    def visitForInherit(self, _type: str):
        return programContext.relateInheritance(_type,
        programContext.types[_type].parent)

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
        resultOp= programContext.defineAttrInType(self.currentTypeName,
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
            
        
        for nodeClassMethod in node.methods:
            result= self.visit(nodeClassMethod, environment= environment)
            if type(result) is error:
                errors.append(result)
        
        return errors

    def visit_NodeClassMethod(self, node: NodeClassMethod, environment):
        for i in range(len(node.argNames)):
            environment.update( {
                node.argNames[i]: node.argTypes[i]
            })
        
        typeResult = self.visit(node.body, environment= environment)

        for i in range(len(node.argNames)):
            environment.popitem()

        if type(typeResult) is error:
            return typeResult
        
        return programContext.checkReturnType(node, typeResult)        

    def visit_NodeString(self, node: NodeString, **kwargs):
        return 'String'
        
    def visit_NodeAttr(self, node: NodeAttr, environment):
        return self.visit(node.expr, 
                          environment= environment)
        
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

        result= self.visit( node.body,
                           environment= environment)
        for i in range(len(node.nestedLets)):
            environment.popitem()
        return result

    def visit_NodeLet(self, node: NodeLet, environment):
        errors= []
        return self.visit(node.body, 
                               environment= environment)
        
    def visit_NodeAssignment(self, node: NodeAssignment,
                             environment):
        result = self.visit(node.expr, environment= environment)
        
        if type(result) is error:
            return result
        return programContext.checkAssign(node, result, environment)
    
    def visit_NodeBinaryOperation(self,
                                  node: NodeBinaryOperation, 
                                  environment):
        
        
        typeFirstExpr= self.visit(node.first, 
                                    environment= environment)
        
        typeSecondExpr= self.visit(node.second, 
                                     environment= environment)
       
        if type (typeFirstExpr) is error:
            return typeFirstExpr

        if type (typeSecondExpr) is error:
            return typeSecondExpr

        return programContext.checkArithmetic(typeFirstExpr,
                                          typeSecondExpr)
        
        
    def visit_NodeNewObject(self, node: NodeNewObject, **kwargs):
        result = programContext.getType(node.type)
        if type(result) is error:
            return result 
        return node.type
        
    def visit_NodeExpr(self,
                       node: NodeExpr,
                       environment):
        return self.visit(node, environment= environment)
        
        
    def visit_NodeInteger(self, 
                          node: NodeInteger,
                          **args):
        return 'Int'
    
    def visit_NodeObject(self,
                         node: NodeObject,
                         environment):
        
        return programContext.searchValue(node,
                                          environment)
        
    def visit_NodeDynamicDispatch(self,
                                  node: NodeDynamicDispatch, 
                                  environment):
        
        typeExpr= self.visit(node.expr,
                                environment= environment)
        if type (typeExpr) is error:
            return typeExpr
        argTypes = []
        for arg in node.arguments:
            currenttypeExpr= self.visit(arg,
                    environment= environment)
            if type (currenttypeExpr) is error:
                return currenttypeExpr
            argTypes.append(currenttypeExpr)
        
        return programContext.checkDynamicDispatch(typeExpr,
        node.method, argTypes)

    def visit_NodeSelf(self, node: NodeSelf, environment):
        return environment['wrapperType']
        