from .AST_definitions import *
from compiler.utils.errors import error, interceptError
import json
import sys

class jsonable:
    def toJSON(self):
        return dumps(self, default=lambda  o: o.__dict__,
        sort_keys=True, indent=4, separators=(',', ': '))

    def __repr__(self):
        return self.toJSON()
class Type(jsonable):
    def __init__(self, idName, attributes, 
                 methods, builtIn= False, parent=None):

        self.idName= idName
        self.parent= parent
        self.attributes= attributes
        self.methods= methods
        self.builtIn= builtIn
        self.inheritsAttr= {}
        self.inheritsMethods= {}
        self.children= {}
    
class feature(jsonable):
    def __init__(self, idName, wrapperType):
        self.wrapperType = wrapperType
        self.idName= idName
    
    def __eq__(self, other):
        if type(self) == type(other):
            for f in self.__dict__:
                if not self.__dict__[f] == other.__dict__[f]:
                    return False
            return True
        return False
    
class Attribute(feature):
    def __init__(self, idName: str, _type: str, wrapperType):
        super().__init__(idName= idName, wrapperType= wrapperType)
        self._type = _type
        

class Method(feature):
    def __init__(self, idName: str, 
                 returnType: str, 
                 argNames,
                 argTypes,
                 wrapperType):
        super().__init__(idName= idName, wrapperType= wrapperType)
        self.returnType = returnType
        self.argNames = argNames
        self.argTypes= argTypes
        

class globalContext:
    def __init__(self, dictionaries ={}):
        self.types= { }
        self.basics = ['Object', 'IO', 'String', 'Bool', 'Int']
        
    def createType(self, node: NodeClass):
        return interceptError(
                validationFunc= lambda: not node.idName in self.types,
                errorOption= 'repeated class' if not node.idName in self.basics else 'repeated class basic',
                idName= node.idName,
                row_and_col = (node.line, node.column)
            )or self.types.update({
                            node.idName:
                                    Type (idName= node.idName,
                                          attributes= {},
                                          methods= {},
                                          parent= node.parent,
                                          builtIn= node.idName in ['String', 'Bool', 'Int'])
                            })

    def checkGoodInheritance(self, node: NodeClass):
        return interceptError(
            validationFunc= lambda: node.idName in self.types,
            errorOption= 'undefined type',
            idName= node.idName,
            row_and_col= (node.line, node.column)
        )  or interceptError (
            validationFunc= lambda: node.idName == 'Object' or node.parent in 
            self.types,
            errorOption= 'undefined type',
            idName= node.parent,
            row_and_col= (node.line, node.parent_col)
        )  or interceptError(
            validationFunc= lambda: node.idName == 'Object' or not self.types[node.parent].builtIn,
            errorOption= 'built-in inheritance',
            idName= node.idName,
            idParent= node.parent,
            row_and_col= (node.line, node.parent_col)
        )  or interceptError(
            validationFunc= lambda: not self.isSubtype (
                superType= node.idName, subType= node.parent),
            errorOption= 'inheritance from child',
            idChild= node.idName,
            row_and_col= (node.line, node.parent_col)
        ) 
        
            
    def checkGoodOverwriteMethod(self, node: NodeClassMethod, idType):
        idParent= self.types[idType].parent
        childInfoMethod= self.types[idType].methods.get(node.idName)
        
        parentInfoMethod= self.types[idParent].methods.get(node.idName, None) or self.types[idParent].inheritsMethods.get(node.idName, None)
        if parentInfoMethod:
            badIndexParam = next((i for i in range (len( childInfoMethod.argTypes))
                         if childInfoMethod.argTypes[i] != parentInfoMethod.argTypes[i]), False) if len(node.formal_param_list) == len(parentInfoMethod.argTypes) else None
            return interceptError(
                validationFunc= lambda: len(node.formal_param_list) == len(parentInfoMethod.argTypes) ,
                errorOption= 'bad length in redefine',
                methodName= node.idName,
                row_and_col= (node.line, node.column)
            ) or interceptError (
                validationFunc= lambda: not badIndexParam,
                errorOption= 'bad redefine method',
                methodName= node.idName,
                badType= node.formal_param_list[badIndexParam]._type if badIndexParam else None,
                goodType= parentInfoMethod.argTypes[badIndexParam] if badIndexParam else None,
                row_and_col= (node.formal_param_list[badIndexParam].line if badIndexParam else None,
                              node.formal_param_list[badIndexParam].column if badIndexParam else None)
            ) or interceptError (
                validationFunc = lambda: node.returnType == parentInfoMethod.returnType,
                errorOption= 'bad returnType in redefine method',
                methodName= node.idName,
                badType= node.returnType,
                goodType= parentInfoMethod.returnType,
                row_and_col= (node.line, node.columnType)
            )
    
    def checkNotOverwriteAttr(self, node: NodeAttr, idType):
        idParent= self.types[idType].parent
        return interceptError(
            validationFunc= lambda : not (self.types[idParent].attributes.get(node.idName, None) or self.types[idParent].inheritsAttr.get(node.idName, None)),
            errorOption= 'bad redefine attr',
            badAttr= node.idName,
            row_and_col= (node.line, node.column)
        )
            
    def actualizeInherits(self, node: NodeClass):
        idParent= self.types[node.idName].parent
        self.actualizeFeatures(dictChild= self.types[node.idName].attributes,
                               dictToActualize= self.types[node.idName].inheritsAttr,
                               dictParent= self.types[idParent].inheritsAttr)
        self.actualizeFeatures(dictChild= self.types[node.idName].attributes,
                               dictToActualize= self.types[node.idName].inheritsAttr,
                               dictParent= self.types[idParent].attributes)
        self.actualizeFeatures(dictChild= self.types[node.idName].methods,
                               dictToActualize= self.types[node.idName].inheritsMethods,
                               dictParent= self.types[idParent].inheritsMethods)
        self.actualizeFeatures(dictChild= self.types[node.idName].methods,
                               dictToActualize= self.types[node.idName].inheritsMethods,
                               dictParent= self.types[idParent].methods)
        
    
    def actualizeFeatures(self, dictChild, dictToActualize, dictParent ):
        dictToActualize.update({
            f.idName: f for f in dictParent.values() if not f.idName in dictChild
        })


    def getType(self, idName: str, row_and_col):
        return interceptError(
            validationFunc= lambda: idName in self.types,
            errorOption= 'undefined type',
            idName= idName,
            row_and_col= row_and_col
        ) or self.types.get(idName)

    def defineAttrInType(self, typeName: str, attr: NodeAttr):
        
        return interceptError(
                validationFunc= lambda : not attr.idName in
                self.types[typeName].attributes,
                errorOption= 'repeated attr',
                idName= attr.idName,
                row_and_col= (attr.line, attr.column)
            ) or interceptError(
                validationFunc= lambda: ('__prim_zero_slot' == attr._type or '__prim_empty_slot'== attr._type) or attr._type in self.types,
                errorOption= 'undefined type in attr',
                idAttr= attr.idName,
                idBadType= attr._type,
                row_and_col= (attr.line, attr.columnTypeAttr )
                ) or self.types[typeName].attributes.update({
                attr.idName: Attribute(idName= attr.idName,
                                       _type= attr._type,
                                       wrapperType= typeName)
            })

    def defineMethod(self, typeName: str,
                           node: NodeClassMethod):
        appears = {}
        for f in node.formal_param_list:
            info = appears.get(f.idName, None)
            if not info:
                appears.update({f.idName: f})
            else:
                return error(
                    error_type='SemanticError',
                    row_and_col= (f.line, f.column),
                    message= 'Formal parameter %s is multiply defined.' %f.idName
                )

        return interceptError(
            validationFunc= lambda: not node.idName in
            self.types[typeName].methods,
            errorOption= 'repeated method',
            idName= node.idName,
            row_and_col= (node.line, node.column)
        ) or self.types[typeName].methods.update({
            node.idName: Method(idName= node.idName,
                                returnType= node.returnType,
                                argNames=  [f.idName for f in node.formal_param_list] ,
                                argTypes= [f._type for f in node.formal_param_list],
                                wrapperType= typeName)    
        })

    def checkDynamicDispatch(self, 
                             typeName, method, arguments, row_and_col):
        
        methodInfo = self.types[typeName].methods.get(method, None)
        if not methodInfo:
            methodInfo= self.types[typeName].inheritsMethods.get(method, None)
        notAncestorArgs= [arguments[i] for i in range (len(arguments))
                           if arguments[i] != methodInfo.argTypes[i]
                           and not self.isAncestor(arguments[i],
                                        methodInfo.argTypes[i])]
        
        return interceptError(
            validationFunc= lambda : not methodInfo is None,
            errorOption= 'undefined method in class',
            idName= method,
            className= typeName,
            row_and_col= row_and_col
        ) or interceptError (
            validationFunc= lambda : notAncestorArgs == [],
            errorOption= 'argument types in dispatch are not subtypes',
            idName= method,
            badArgs= notAncestorArgs,
            row_and_col= row_and_col
        ) or methodInfo.returnType

    

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.types, indent = 4, cls= MyEncoder)

    def buildEnv (self, typeName):
        typeInfo= self.types[typeName]
        d = {typeInfo.attributes[attr].idName: 
            typeInfo.attributes[attr]._type
            for attr in typeInfo.attributes }
        d.update({ typeInfo.inheritsAttr[attr].idName:
            typeInfo.inheritsAttr[attr]._type
            for attr in typeInfo.inheritsAttr } )
        d.update({'wrapperType': typeName})
        return d
    
    def buildEnvForMethod(self, node: NodeClassMethod, previousEnv):
        newEnv = previousEnv.copy()
        newEnv.update({ f.idName: f._type
                        for f in node.formal_param_list })
        badFormalParam = next((f for f in node.formal_param_list
                           if f.idName == 'self'), None)
        return interceptError(
            validationFunc= lambda : not badFormalParam,
            errorOption='self parameter',
            row_and_col= (badFormalParam.line, badFormalParam.column) if badFormalParam else  (0,0)
        )or newEnv
    
    def isSubtype(self, subType, superType): 
        while subType:
            if subType == superType:
                return True
            subType = self.types[subType].parent
        return False
    
    def checkAssign(self, nameObject,
                    nodeType, returnType,
                    row_and_col, errorOption, columnAssign = 0):
        
        return interceptError (
                validationFunc= lambda: nameObject != 'self',
                errorOption='self assign',
                row_and_col= (row_and_col[0], columnAssign)
        ) or interceptError (
                validationFunc= lambda : nodeType in self.types,
                errorOption= 'undefined type',
                idName= nodeType,
                row_and_col= row_and_col
            ) or  interceptError(
            validationFunc= lambda : self.isSubtype(subType= returnType, 
                                                    superType= nodeType),
            errorOption= errorOption,
            idName= nameObject,
            type1= returnType,
            type2= nodeType,
            row_and_col= row_and_col
            )

    def checkDispatchTypes(self, typeLeftMost, typeRight, returnType, row_and_col):
        return interceptError(validationFunc= lambda: self.isSubtype(subType= typeLeftMost,
                                                                     superType= typeRight),
                              errorOption= 'bad static dispatch',
                              typeLef = typeLeftMost,
                              typeRight= typeRight,
                              row_and_col= row_and_col) or returnType
        
    
    def checkMethodInType (self, idType, idMethod, row_and_col):
        return interceptError(validationFunc= lambda: idMethod in self.types[idType].methods or idMethod in self.types[idType].inheritsMethods,
                              errorOption= 'not method in class',
                              idMethod= idMethod,
                              row_and_col= row_and_col) or self.types[idType].methods.get(idMethod, None) or self.types[idType].inheritsMethods.get(idMethod, None)
        
    
    def checkReturnType(self, nodeType , returnType, row_and_col, errorOption):
        return interceptError(
            validationFunc= lambda : self.isSubtype(subType= returnType, 
                                                    superType= nodeType),
            errorOption= errorOption,
            type1= nodeType,
            type2= returnType,
            row_and_col= row_and_col
        ) or returnType
    
    def checkBoolInPredicate(self, node: NodeWhileLoop, resultExpr):
        return interceptError(
            validationFunc= lambda : resultExpr == 'Bool',
            errorOption= 'bad predicate',
            row_and_col= (node.line, node.predicate.column)
        ) or 'Bool'
    
    def checkNonRepetition(self, nodeActions):
        repetitionList = []
        for action in nodeActions:
            if not action.type in repetitionList:
                repetitionList.append(action.type)
            else:
                return error(error_type= 'SemanticError',
                             row_and_col= (action.line, action.typeColumn),
                             message = 'Duplicate branch %s in case statement.' %action.type)
        
    
    def searchValue(self, node: NodeObject, row_and_col, environment):
        return interceptError(
                        validationFunc= lambda: node.idName
                        in environment,
                        errorOption='undefined symbol',
                        row_and_col= row_and_col,
                        symbolName= node.idName) or environment[node.idName]

    def checkArithmetic(self, type1, type2, row_and_col, symbolOp, arithmeticOp):
        return interceptError(validationFunc= lambda: type1 == type2,
                            errorOption= 'arithmetic fail',
                            type1= type1,
                            type2= type2,
                            symbolOp= symbolOp,
                            row_and_col= row_and_col) or ('Int' * arithmeticOp) or 'Bool'

    def checkEqualOp(self, type1, type2, row_and_col):
        return interceptError(validationFunc= lambda: not (type1 or type2)
                            in {'Int', 'Bool', 'String'} or type1 == type2,
                            errorOption= 'comparison fail',
                            row_and_col = row_and_col) or self.types['Bool'].idName
    
    def checkArgumentsInDispatch(self,
                                 node,
                                 argNames,
                                 typeExprOfArgs, 
                                 argTypes):
        if len(typeExprOfArgs) != len(argTypes):
            return error(error_type= 'SemanticError',
                         row_and_col= (node.line, node.column + 1), # I don't like this +1. It looks like a patch.
                         message= "Method %s called with wrong number of arguments." %(node.method))
            
        badIndex = next((i for i in range(len( typeExprOfArgs))
                       if not self.isSubtype(subType=typeExprOfArgs[i],
                                        superType= argTypes[i])), None)
        (badArg, badType, realType, row_and_col)= (argNames[badIndex],
                                                   typeExprOfArgs[badIndex],
                                                   argTypes[badIndex], 
                                                   (node.arguments[badIndex].expr.line, node.arguments[badIndex].expr.column)) if badIndex else (None, None, None, None)
        
        return interceptError(validationFunc= lambda: not badIndex,
                              errorOption= 'bad dispatch',
                              idMethod= node.method,
                              badArg= badArg,
                              badType= badType,
                              realType= realType,
                              row_and_col= row_and_col)
        
        
    
    def LCA(self, idName1, idName2):
        path1 = self.pathToObject( idName1)
        path2 = self.pathToObject( idName2)
        possibleAncestor = ''
        while path1 and path2:
            anc1 = path1.pop()
            anc2 = path2.pop()
            if anc1 == anc2:
                possibleAncestor= anc1
            else:
                break
            
        return possibleAncestor

    
    def pathToObject(self, idName):
        path = []
        currentIdName= idName
        while currentIdName != 'Object':
            path.append(currentIdName)
            currentIdName = self.types[currentIdName].parent
        return path + ['Object']

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
       return obj.toJSON()

programContext = globalContext()


### Definition of basics classes

#ObjClass = NodeClass(idName= 'Object',
#                     methods= [
#                         NodeClassMethod(
#                             
#                         )
#                     ],
#                     attributes= [
#                         
#                     ],
#                     parent= None)
