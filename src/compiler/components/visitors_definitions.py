from ..components.semantic.AST_definitions import *

from compiler.utils.errors import error


class NodeVisitor:
    def __init__(self, programContext):
        self.programContext= programContext
    
    def visit(self, node: Node, **args):
        if isinstance(self, TypeCheckerVisitor):
            if issubclass(type(node), NodeBinaryOperation):
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
        for nodeClass in node.class_list:
            result= self.visit(nodeClass)
            if type (result) is error: # This ugly return is because we only need a one error, this is the panic mode!
                errors.append(result)
                return errors

    def visit_NodeClass(self, node: NodeClass):
        # When we create a type, we store it in the context, if there is no errors
        return self.programContext.createType(node)

class TypeInheritanceVisitor(NodeVisitor):
    def visit_NodeProgram(self, node: NodeProgram):
        errors = []
        for nodeClass in node.class_list:
            result = self.visit(nodeClass)
            if type(result) is error:
                errors.append(result)
        return [errors.pop()] if errors else []

    def visit_NodeClass(self, node: NodeClass):
        result= self.programContext.checkGoodInheritance(node)
        if type(result) is error:
            return result

        if node.idName == 'Object':
            return
        
        for nodeAttr in node.attributes:
            resultVisitAttr= self.visit(nodeAttr, idType= node.idName)
            if type(resultVisitAttr) is error:
                return resultVisitAttr
        
        for nodeClassMethod in node.methods:
            resultVisitClassMethod= self.visit(nodeClassMethod, idType= node.idName)
            if type(resultVisitClassMethod) is error:
                return resultVisitClassMethod
        
        self.programContext.actualizeInherits(node)    
    
    
    def visit_NodeAttr(self, node: NodeAttr, idType):
        return self.programContext.checkNotOverwriteAttr(node, idType)
        

    def visit_NodeClassMethod(self, node: NodeClassMethod, idType):
        return self.programContext.checkGoodOverwriteMethod(node, idType)
        
        
class TypeBuilderVisitor(NodeVisitor):
    def __init__(self, programContext):
        super().__init__(programContext)
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
        resultOp= self.programContext.defineAttrInType(self.currentTypeName,
        node)
        
        if type (resultOp) is error:
            return [resultOp]
        
        return []

    def visit_NodeClassMethod(self, node: NodeClassMethod):
        return [definition for definition in
        [self.programContext.getType(node.returnType, (node.line, node.column))] +
        [self.programContext.getType(idName = formal_param._type, row_and_col= (formal_param.line, formal_param.column)) for formal_param in node.formal_param_list] +
        [self.programContext.defineMethod(
            typeName = self.currentTypeName,
            node= node
            )]
        if type(definition) is error
        ]


class TypeCheckerVisitor(NodeVisitor):
        

    def visit_NodeProgram(self, node: NodeProgram):
        self.mapExprWithType= {}
        errors = []
        for nodeClass in node.class_list:
            environment = self.programContext.buildEnv (typeName= nodeClass.idName)
            errors += self.visit(nodeClass, previousEnv= environment)
            
        return errors, self.mapExprWithType

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
        newEnv = self.programContext.buildEnvForMethod(node, previousEnv)
        if type(newEnv) is error:
            return newEnv
        
        typeResult = self.visit(node.body, previousEnv= newEnv)

        if type(typeResult) is error:
            return typeResult
        
        return self.programContext.checkReturnType(node.returnType, 
                                              typeResult, 
                                              (node.line, node.column),
                                              'uncompatible types')        

    def visit_NodeString(self, node: NodeString, **kwargs):
        return 'String'
        
    def visit_NodeAttr(self, node: NodeAttr, previousEnv):
        if node.expr:
            typeExpr= self.visit(node.expr, 
                            previousEnv= previousEnv)
            if type(typeExpr) is error:
                return typeExpr
            
            resultCheckAssign= self.programContext.checkAssign(nameObject= node.idName,
                                    nodeType= node._type,
                                    returnType= typeExpr,
                                    row_and_col= (node.expr.line, node.expr.column)
                                    if node.expr else (node.line, node.column),
                                    errorOption= 'uncompatible assign attr')
            if type(resultCheckAssign) is error:
                return resultCheckAssign
            
            return node._type
            
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
                               previousEnv= previousEnv) if node.body else node.type
        if type(exprType) is error:
            return exprType
        
        row_and_col = (node.body.line, node.body.column) if node.body else (node.line, node.column)
        
        resultCheckAssign= self.programContext.checkAssign(node.idName,
                                          node.type,
                                          exprType,
                                          row_and_col,
                                          'uncompatible assing object',
                                          node.column)
        if type(resultCheckAssign) is error:
            return resultCheckAssign
        
        return node.type
                
    def visit_NodeAssignment(self, node: NodeAssignment,
                             previousEnv):
        
        resultObj = self.visit(node.nodeObject, previousEnv=  previousEnv)
        
        if type(resultObj) is error:
            return resultObj
        
        resultExpr = self.visit(node.expr, previousEnv= previousEnv)
        
        if type(resultExpr) is error:
            return resultExpr
        
        
        resultCheckAssign= self.programContext.checkAssign(nameObject= node.nodeObject.idName,
                                          nodeType= resultObj, 
                                          returnType= resultExpr, 
                                          row_and_col= (node.nodeObject.line, node.nodeObject.column ),
                                          errorOption= 'uncompatible assing object',
                                          columnAssign= node.columnAssign)
        if type(resultCheckAssign) is error:
            return resultCheckAssign
        
        return resultExpr
    
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
            return self.programContext.checkEqualOp(typeFirstExpr,
                                               typeSecondExpr,
                                               (node.line, node.column))
        
        
        arithmeticOp = type(node) in {NodeAddition,
                          NodeSubtraction,
                          NodeDivision,
                          NodeMultiplication}
            
        
        return self.programContext.checkArithmetic(typeFirstExpr,
                                        typeSecondExpr,
                                        (node.line, node.column),
                                        node.symbol,
                                        arithmeticOp)
            
        
        
    def visit_NodeNewObject(self, node: NodeNewObject, **kwargs):
        result = self.programContext.getType(node.type,
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
        return self.programContext.checkReturnType(nodeType= "Bool", returnType= typeExpr,
                                              row_and_col= (node.line, node.boolean_expr.column -2),
                                              errorOption= 'bad not')
        

    
    
    def visit_NodeObject(self,
                         node: NodeObject,
                         previousEnv):
        if node.idName == 'self':
            return previousEnv['wrapperType']
        return self.programContext.searchValue(node,
                                          (node.line, node.column),
                                          previousEnv)
        
    def visit_NodeDynamicDispatch(self,
                                  node: NodeDynamicDispatch, 
                                  previousEnv):
        
        typeExpr= self.visit(node.expr,
                                previousEnv= previousEnv)
        if type (typeExpr) is error:
            return typeExpr
        
        self.mapExprWithType[(node.line, node.column)]= typeExpr
        methodInfo= self.programContext.checkMethodInType(idType= typeExpr, 
                                                    idMethod = node.method,
                                                    row_and_col= (node.line, node.column + 1))
        if type(methodInfo) is error:
            return methodInfo
        
        argTypes = []
        for arg in node.arguments:
            currenttypeExpr= self.visit(arg,
                    previousEnv= previousEnv)
            if type (currenttypeExpr) is error:
                return currenttypeExpr
            argTypes.append(currenttypeExpr)
        
        resultCheck= self.programContext.checkArgumentsInDispatch(
        node,
        methodInfo.argNames,
        argTypes, 
        methodInfo.argTypes)
        
        if type(resultCheck) is error:
            return resultCheck
        
        return methodInfo.returnType
        

    def visit_NodeSelf(self, node: NodeSelf, previousEnv):
        return previousEnv['wrapperType']
    
    def visit_NodeIntegerComplement(self, node: NodeIntegerComplement, 
                                    previousEnv):
        typeExpr = self.visit(node.integer_expr, previousEnv= previousEnv)
        if type(typeExpr) is error:
            return typeExpr
        return self.programContext.checkReturnType(nodeType= "Int", returnType= typeExpr,
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
        
        resultCheck = self.programContext.checkReturnType(nodeType= 'Bool', returnType= predType,
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
        
        return self.programContext.LCA(idName1 = thenType, idName2= elseType)
    
    def visit_NodeCase(self, node: NodeCase, previousEnv):
        resultTypeInit= self.visit(node.expr, previousEnv= previousEnv)
        if type(resultTypeInit) is error:
            return resultTypeInit
        
        return self.visit_NodeCaseActions(node.actions,
                                          previousEnv,
                                          resultTypeInit)
    
    def visit_NodeCaseActions(self, nodeActions, previousEnv, resultTypeInit):
        
        action, returnTypesExpressions= self.searchLessActionCaseAndReturnTypes(nodeActions,
                                                                                previousEnv,
                                                                                resultTypeInit)
        if type(action) is error:
            return action
        
        lca =  returnTypesExpressions[0]
        for typeExpr in returnTypesExpressions:
            lca= self.programContext.LCA(idName1= lca, idName2= typeExpr)
            
        return lca
    
    def searchLessActionCaseAndReturnTypes(self, nodeActions, 
                                           previousEnv, resultTypeInit):
        actionToReturn = None
        currentTypeCase= 'Object'
        returnTypesExpressions = []
        
        resultCheckNonRepetition= self.programContext.checkNonRepetition(nodeActions)
        if type(resultCheckNonRepetition) is error:
            return resultCheckNonRepetition, None
        
        for action in nodeActions:
            actionType= self.programContext.getType(idName= action.type,
                                                row_and_col= (action.line,
                                                              action.column))
            if type(actionType) is error:
                return actionType, None
            
            newEnv= previousEnv.copy()
            newEnv.update({
                action.idName: action.type
            })
            returnTypeAction= self.visit(action.expr, previousEnv= newEnv)
            if type(returnTypeAction) is error:
                return returnTypeAction, None

            returnTypesExpressions.append(returnTypeAction)
            
            if self.programContext.isSubtype(subType= resultTypeInit,
                superType= action.type) and self.programContext.isSubtype(
                subType= action.type,
                superType= currentTypeCase):
                actionToReturn= action
                currentTypeCase= action.type
                
        return actionToReturn, returnTypesExpressions
    
    
    def visit_NodeIsVoid(self, node: NodeIsVoid, previousEnv):
        typeExpr= self.visit(node.expr, previousEnv = previousEnv)
        if type(typeExpr) is error:
            return typeExpr
        return 'Bool'
    
    def visit_NodeStaticDispatch(self, node: NodeStaticDispatch, previousEnv):
        typeLeftMost= self.visit(node.expr, previousEnv= previousEnv)
        if type(typeLeftMost) is error:
            return typeLeftMost
        
        dispatchType= self.programContext.getType(idName= node.dispatch_type,
                                             row_and_col= (node.line, node.columnType))
        if type(dispatchType) is error:
            return dispatchType
                
        methodInfo= self.programContext.checkMethodInType(idType= node.dispatch_type,
                                                    idMethod= node.method, 
                                                    row_and_col= (node.line, node.columnIdMethod))
        if type(methodInfo) is error:
            return methodInfo

        typeExprOfArgs = []
        for arg in node.arguments:
            resultType= self.visit(node= arg,
                                     previousEnv = previousEnv)
            
            if type(resultType) is error:
                return resultType
            
            typeExprOfArgs.append(resultType)


        checkingArgumentsResult= self.programContext.checkArgumentsInDispatch(
                                            node,
                                            methodInfo.argNames,
                                            typeExprOfArgs,
                                            methodInfo.argTypes,) 
        
        if type(checkingArgumentsResult) is error:
            return checkingArgumentsResult
        
        return self.programContext.checkDispatchTypes(typeLeftMost= typeLeftMost,
                                                 typeRight= dispatchType.idName,
                                                 returnType= methodInfo.returnType,
                                                 row_and_col= (node.expr.line, node.expr.column))
        
    def visit_NodeWhileLoop(self, node: NodeWhileLoop, previousEnv):
        resultExprPred = self.visit(node.predicate, previousEnv= previousEnv)
        if type(resultExprPred) is error:
            return resultExprPred
        resultCheck = self.programContext.checkBoolInPredicate(node, resultExprPred)
        if type(resultCheck) is error:
            return resultCheck
        
        resultExpr = self.visit(node.body, previousEnv= previousEnv)
        if type(resultExpr) is error:
            return resultExpr
        
        return 'Object'
        

