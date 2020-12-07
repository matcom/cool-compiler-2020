from ..utils.AST_definitions import *
from ..utils.errors import error, interceptError
from ..utils.functions_for_classes import funcs, functionSerializable
import json
import sys


class Context:
    def __init__(self, dictionaries ={}):

        self.types= {
                'Object': NodeClass (idName= 'Object',
                                    methods= [
                                        NodeClassMethod(idName = 'abort',
                                                        argNames='',
                                                        argTypes='',
                                                        returnType='Object',
                                                        body= funcs.abortFunc),
                                        NodeClassMethod(idName= 'type_name',
                                                        returnType= 'Object',
                                                        argTypes= [],
                                                        argNames= [],
                                                        body= funcs.typeNameFunc),
                                        NodeClassMethod(idName= 'copy',
                                                        returnType= 'SELF_TYPE',
                                                        argNames= [],
                                                        argTypes= [],
                                                        body= funcs.copyFunc)
                                    ],
                                    attributes= [    
                                    ],
                                    parent= None),
                'Int': NodeClass (idName= 'Int',
                                  methods= [
                                      
                                  ],
                                  attributes= [
                                      NodeAttr(
                                          idName= 'default',
                                          attrType= 'Int',
                                          value= 0
                                      )
                                  ],
                                  parent= 'Object'),
                'IO': NodeClass (idName= 'IO',
                                 methods= [
                                     NodeClassMethod( idName= "out_string",
                                                      returnType="SELF_TYPE",
                                                      argTypes= [],
                                                      argNames= [],
                                                      body= funcs.outStringFunc
                                                    ),
                                     NodeClassMethod( idName= "out_int",
                                                      returnType="SELF_TYPE",
                                                      argNames= ['x'],
                                                      argTypes= ['Int'],
                                                      body= funcs.outIntFunc),
                                     NodeClassMethod( idName= 'in_string',
                                                      returnType='String',
                                                      argTypes= [],
                                                      argNames= [],
                                                      body= funcs.readFromInputFunc),
                                     NodeClassMethod (idName='in_int',
                                                      returnType='Int',
                                                      argTypes= [],
                                                      argNames= [],
                                                      body= funcs.readFromInputFunc)
                                                            ],
                                 attributes= [],
                                 parent= 'Object'),
                'SELF_TYPE': NodeClass(idName='SELF_TYPE',
                                        parent= 'Object',
                                        attributes= [],
                                        methods=[]),
                'String': NodeClass(idName= 'String',
                                    methods= [
                                        NodeClassMethod(
                                            idName='length',
                                            returnType='String',
                                            argTypes= [],
                                            argNames= [],
                                            body= funcs.readFromInputFunc
                                        ),
                                        NodeClassMethod (
                                             idName= 'concat',
                                             returnType= 'Int',
                                             argTypes= ['String'],
                                             argNames= ['x'],
                                             body= funcs.concatFunc
                                        ),
                                        NodeClassMethod (
                                            idName= 'substr',
                                            returnType='String',
                                            argNames= ['i', 'l'],
                                            argTypes=['Int', 'Int'],
                                            body= funcs.substrFunc   
                                        )
                                    ],
                                    attributes= [NodeAttr(idName= 'default',
                                                          attrType='String',
                                                          value= '')],
                                    parent= 'Object'

                                )
            }
        
    def createType(self, node: NodeClass):
        return interceptError(
                validationFunc= lambda: not node.idName in self.types,
                errorType= 'repeated class',
                idName= node.idName
            ) or interceptError (
                validationFunc= lambda: node.idName != node.parent,
                errorType= 'Inherit from itself',
                idName= node.idName
            )or self.types.update({
                            node.idName:
                                    node
                            })

    def relateInheritance(self, node: NodeClass):
        return interceptError(
            validationFunc= lambda: node.idName in self.types,
            errorType= 'undefined type',
            idName= node.idName
        )  or interceptError (
            validationFunc= lambda: self.types[node.idName].parent in self.types,
            errorType= 'undefined type',
            idName = self.types[node.idName].parent
        )  or interceptError(
            validationFunc= lambda: not self.types[node.parent].builtIn,
            errorType= 'built-in inheritance',
            idName= node.idName
        )  or interceptError(
            validationFunc= lambda: not self.isAncestor (
                idChild= node.idName, idParent= node.parent),
            errorType= 'inheritance from child',
            idParent= node.parent,
            idChild= node.idName
        )  or not self.actualizeInherits(node.idName, node.parent) 
        
    def actualizeInherits (self, idName, parent):
        
        self.types[idName].inheritsAttr.update({attr.idName: attr  for attr in self.types[parent].attributes
                                            if not attr in self.types[idName].attributes})
        self.types[idName].inheritsAttr.update({attrName: self.types[parent].inheritsAttr[attrName]
                                                for attrName in self.types[parent].inheritsAttr
                                                if  self.types[parent].inheritsAttr[attrName] not
                                                in self.types[idName].attributes })
        self.types[idName].inheritsMethods.update({method.idName: method for method in self.types[parent].methods
                                                    if not method in self.types[idName].methods
                                                })
        self.types[idName].inheritsMethods.update({methodName: self.types[parent].inheritsMethods[methodName]
                                                   for methodName in self.types[parent].inheritsMethods
                                                   if not self.types[parent].inheritsMethods[methodName]
                                                   in self.types[idName].methods
                                                })
        

    def isAncestor(self, idChild: str, idParent: str):

        currentName = self.types[idParent].parent
        while currentName != 'Object' and currentName != idChild and currentName != idParent:
            try:
                currentName = self.types[currentName].parent
            except KeyError:
                break
        return currentName == idChild

    def getType(self, idName: str):
        return interceptError(
            validationFunc= lambda: idName in self.types,
            errorType= 'undefined type',
            idName= idName
        ) or self.types.get(idName)

    def defineAttrInType(self, typeName: str, attr: NodeAttr):
        
        err= interceptError(
                validationFunc= lambda : not attr in 
                [a for a in self.types[typeName].attributes if a.readed ],
                errorType= 'repeated attr',
                idName= attr.idName
            )
        if type(err) is error:
            return err
        attr.readed= True

    def defineMethod(self, typeName: str,
                           node: NodeClassMethod):
        err= interceptError(
            validationFunc= lambda: not node in
            [m for m in self.types[typeName].methods if m.readed],
            errorType= 'repeated method',
            idName= node.idName
        )
        if type(err) is error:
            return err
        node.readed= True
        
    def checkEqualTypes(self, attrType, returnType):
        
        pass

    def checkInheritedInfo(self, idName: str):
        
        pass

    def isUndefined(self, arg):
        
        pass

    def createContextForLetExpr(self, node: NodeLet, chainOfNames):
        return not self.letsExpr.update({
            chainOfNames:
                ContextLet(chainBefore= chainOfNames,
                           objectId= node.idName,
                           typeObject= node.type,
                           value= None)
        })
        

    def checkDynamicDispatch(self, typeName, method, arguments):
        methodInfo= self.methodInNodeOrParent(typeName, method)
        undefinedArgs= [ arg for arg in arguments if self.isUndefined(arg)]

        return interceptError(
            validationFunc= lambda : not methodInfo is None,
            errorType= 'undefined method in class',
            idName= method,
            className= typeName 
        ) or interceptError(
            validationFunc= lambda: undefinedArgs is [],
            errorType= 'undefined arguments for method in class',
            idName= method,
            className= typeName,
            undefinedArgs = undefined 
        )

    def methodInNodeOrParent(self, typeName, method):
        currentName= typeName

        while currentName and not method in self.types[currentName]['methods']:
            currentName = self.types[currentName]['parent']

        if not currentName: return None    
        return self.types[currentName]['methods'][method]
        

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.types, indent = 4, cls= MyEncoder)

    def buildEnv (self, typeName):
        typeInfo= self.types[typeName]
        d= { o.idName: {'value': o.value, 'type': o.type } for o in typeInfo.attributes }
        d.update( {o.idName: {'value': o.value, 'type': o.type} for o in typeInfo.inheritsAttr})
        return d
    
    def assignValue(self, node, exprResult):
        return interceptError(
            validationFunc= lambda : node.type == exprResult['type'],
            errorType='uncompatible types',
            type1= node.type,
            type2= exprResult['type']
            ) or not self.assign(node, exprResult)
    
    def assign(self, node, exprResult):
        node.value= exprResult['value']
        
    
    def searchValue(self, node: NodeObject, environment):
        return interceptError(
                        validationFunc= lambda: node.idName
                        in environment and environment[node.idName],
                        errorType='undefined symbol',
                        symbolName= node.idName) or environment[node.idName]

    def executeArithmetic(self, func, type1, type2):
        return interceptError(validationFunc= lambda: type1 == type2,
                            errorType= 'uncompatible types',
                            type1= type1,
                            type2= type2) or func()

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
       return obj.toJSON()

programContext = Context()

