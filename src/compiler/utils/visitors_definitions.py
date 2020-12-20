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

    def not_implemented(self, node: Node, **args):
        raise Exception('Not implemented visit_{} method'.format(node.clsname))

# We need to highlight here the inheritance relations between classes
class TypeCollectorVisitor(NodeVisitor):

    def visit_NodeProgram(self, node: NodeProgram):
        errors = []
        line_and_col = {}
        for nodeClass in node.class_list:
            line_and_col.update({
                nodeClass.idName: (nodeClass.line, nodeClass.column)
            })
            result= self.visit(nodeClass)
            if result:
                errors.append(result)
        return errors, line_and_col

    def visit_NodeClass(self, node: NodeClass):
        # When we create a type, we store it in the context, if there is no errors
        return programContext.createType(node)

class TypeInheritanceVisitor(NodeVisitor):
    def visit_NodeProgram(self, node: NodeProgram, line_and_col_dict):
        errors = []
        for _type in programContext.types:
            if _type != 'Object':
                result = self.visitForInherit(_type, 
                                    line_and_col_dict.get(_type, (0,0)))
                if type (result) is error:
                    errors.append(result)
        return errors

    def visitForInherit(self, _type: str, line_and_col):
        return programContext.relateInheritance(_type,
        programContext.types[_type].parent, line_and_col)

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
        [programContext.getType(node.returnType, (node.line, node.column))] +
        [programContext.getType(idName = formal_param._type, row_and_col= (formal_param.line, formal_param.column)) for formal_param in node.formal_param_list] +
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
            errors += self.visit(nodeClass, previousEnv= environment)
            
        return errors

    def visit_NodeClass(self, node: NodeClass, previousEnv):
        errors = []
        for nodeAttr in node.attributes:
            result= self.visit(nodeAttr, previousEnv= previousEnv)
            if type(result) is error:
                errors.append(result)
            
        
        for nodeClassMethod in node.methods:
            result= self.visit(nodeClassMethod, previousEnv= previousEnv)
            if type(result) is error:
                errors.append(result)
        
        return errors

    def visit_NodeClassMethod(self, node: NodeClassMethod, previousEnv):
        newEnv = programContext.buildEnvForMethod(node, previousEnv)
        if type(newEnv) is error:
            return newEnv
        
        typeResult = self.visit(node.body, previousEnv= newEnv)

        if type(typeResult) is error:
            return typeResult
        
        return programContext.checkReturnType(node.returnType, 
                                              typeResult, 
                                              (node.line, node.column),
                                              'uncompatible types')        

    def visit_NodeString(self, node: NodeString, **kwargs):
        return 'String'
        
    def visit_NodeAttr(self, node: NodeAttr, previousEnv):
        typeExpr= self.visit(node.expr, 
                          previousEnv= previousEnv)
        if type(typeExpr) is error:
            return typeExpr
        
        return programContext.checkAssign(nameObject= node.idName,
                                   nodeType= node._type,
                                   returnType= typeExpr,
                                   row_and_col= (node.expr.line, node.expr.column)
                                   if node.expr else (node.line, node.column),
                                   errorOption= 'uncompatible assign attr')
        
    def visit_NodeLetComplex(self,
                             node: NodeLetComplex,
                             previousEnv: dict):
        newEnv= previousEnv.copy()
        for nodeLet in node.nestedLets:
            result= self.visit(nodeLet, 
                               previousEnv= newEnv)
            if type(result) is error:
                return result
            newEnv.update({
                nodeLet.idName: result
            })

        result= self.visit( node.body,
                           previousEnv= newEnv)
        
        return result

    def visit_NodeLet(self, node: NodeLet, previousEnv):
        errors= []
        exprType= self.visit(node.body,
                               previousEnv= previousEnv)
        if type(exprType) is error:
            return exprType
        
        previousEnv.update( {
            node.idName: node.type
        })
        return programContext.checkAssign(node.idName,
                                          previousEnv[node.idName],
                                          exprType,
                                          (node.body.line, node.body.column),
                                          'uncompatible assing object')
                
    def visit_NodeAssignment(self, node: NodeAssignment,
                             previousEnv):
        
        resultObj = self.visit(node.nodeObject, previousEnv=  previousEnv)
        
        if type(resultObj) is error:
            return resultObj
        
        resultExpr = self.visit(node.expr, previousEnv= previousEnv)
        
        if type(resultExpr) is error:
            return resultExpr
        
        
        return programContext.checkAssign(nameObject= node.nodeObject.idName,
                                          nodeType= resultObj, 
                                          returnType= resultExpr, 
                                          row_and_col= (node.line, node.column ),
                                          errorOption= 'uncompatible assing object')
    
    def visit_NodeBinaryOperation(self,
                                  node: NodeBinaryOperation, 
                                  previousEnv):
        
        
        typeFirstExpr= self.visit(node.first, 
                                    previousEnv= previousEnv)
        
        typeSecondExpr= self.visit(node.second, 
                                     previousEnv= previousEnv)
       
        if type (typeFirstExpr) is error:
            return typeFirstExpr

        if type (typeSecondExpr) is error:
            return typeSecondExpr

        if type(node) is NodeEqual:
            return programContext.checkEqualOp(typeFirstExpr,
                                               typeSecondExpr,
                                               (node.line, node.column))
        
        
        arithmeticOp = type(node) in {NodeAddition,
                          NodeSubtraction,
                          NodeDivision,
                          NodeMultiplication}
            
        
        return programContext.checkArithmetic(typeFirstExpr,
                                        typeSecondExpr,
                                        (node.line, node.column),
                                        node.symbol,
                                        arithmeticOp)
            
        
        
    def visit_NodeNewObject(self, node: NodeNewObject, **kwargs):
        result = programContext.getType(node.type,
                                        row_and_col=(node.line, node.column))
        if type(result) is error:
            return result
        return node.type
        
    def visit_NodeExpr(self,
                       node: NodeExpr,
                       previousEnv):
        return self.visit(node, previousEnv= previousEnv)
        
        
    def visit_NodeInteger(self, 
                          node: NodeInteger,
                          **kwargs):
        return 'Int'
    
    def visit_NodeBoolean(self,
                         node: NodeBoolean,
                         **kwargs):
        return 'Bool'
    
    def visit_NodeBooleanComplement(self,
                                    node: NodeBooleanComplement,
                                    previousEnv):
        typeExpr = self.visit(node.boolean_expr, previousEnv= previousEnv)
        if type(typeExpr) is error:
            return typeExpr
        return programContext.checkReturnType(nodeType= "Bool", returnType= typeExpr,
                                              row_and_col= (node.line, node.boolean_expr.column -2),
                                              errorOption= 'bad not')
        

    
    
    def visit_NodeObject(self,
                         node: NodeObject,
                         previousEnv):
        
        return programContext.searchValue(node,
                                          (node.line, node.column),
                                          previousEnv)
        
    def visit_NodeDynamicDispatch(self,
                                  node: NodeDynamicDispatch, 
                                  previousEnv):
        
        typeExpr= self.visit(node.expr,
                                previousEnv= previousEnv)
        if type (typeExpr) is error:
            return typeExpr
        argTypes = []
        for arg in node.arguments:
            currenttypeExpr= self.visit(arg,
                    previousEnv= previousEnv)
            if type (currenttypeExpr) is error:
                return currenttypeExpr
            argTypes.append(currenttypeExpr)
        
        return programContext.checkDynamicDispatch(typeExpr,
        node.method, argTypes, (node.line, node.column))

    def visit_NodeSelf(self, node: NodeSelf, previousEnv):
        return previousEnv['wrapperType']
    
    def visit_NodeIntegerComplement(self, node: NodeIntegerComplement, 
                                    previousEnv):
        typeExpr = self.visit(node.integer_expr, previousEnv= previousEnv)
        if type(typeExpr) is error:
            return typeExpr
        return programContext.checkReturnType(nodeType= "Int", returnType= typeExpr,
                                              row_and_col= (node.line, node.column + 1),
                                              errorOption= 'bad ~')
    
    def visit_NodeBlock(self, node: NodeBlock, previousEnv):
        blockType = None
        for expr in node.expr_list:
            blockType = self.visit(expr, previousEnv= previousEnv)
            if type(blockType) is error:
                return blockType
        return blockType            
        
    def visit_NodeIf(self, node: NodeIf, previousEnv):
        predType = self.visit(node.predicate, previousEnv = previousEnv)
        if type(predType) is error:
            return predType
        
        resultCheck = programContext.checkReturnType(nodeType= 'Bool', returnType= predType,
                                                     row_and_col= (node.line, node.column),
                                                     errorOption= 'uncompatible types')
        
        if type(resultCheck) is error:
            return resultCheck
        
        thenType = self.visit(node.then_body, previousEnv= previousEnv)
        if type(thenType) is error:
            return thenType
        
        elseType = self.visit(node.else_body, previousEnv= previousEnv)
        if type(elseType) is error:
            return elseType
        
        return programContext.LCA(idName1 = thenType, idName2= elseType)