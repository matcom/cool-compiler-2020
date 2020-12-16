from ..utils.AST_definitions import *
from ..utils.errors import error, interceptError
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
    
class feature(jsonable):
    def __eq__(self, other):
        if type(self) == type(other):
            for f in self.__dict__:
                if not self.__dict__[f] == other.__dict__[f]:
                    return False
            return True
        return False
    
class Attribute(feature):
    def __init__(self, idName: str, _type: str):
        self.idName = idName
        self._type = _type
        

class Method(feature):
    def __init__(self, idName: str, 
                 returnType: str, 
                 argNames,
                 argTypes):

        self.idName = idName
        self.returnType = returnType
        self.argNames = argNames
        self.argTypes= argTypes
        

class globalContext:
    def __init__(self, dictionaries ={}):

        self.types= {
                'Object': Type( idName= 'Object',
                                methods= {
                                    'abort': Method(idName= 'abort',
                                                    argNames=[],
                                                    argTypes=[],
                                                    returnType='Object'),
                                    'type_name': Method(idName= 'type_name',
                                                        returnType= 'String',
                                                        argTypes= [],
                                                        argNames= []),
                                    'copy': Method(idName= 'copy',
                                                   returnType= 'SELF_TYPE',
                                                   argNames= [],
                                                   argTypes= [])
                                },
                                attributes= {},
                                parent= None),
                'Int': Type(idName= 'Int',
                            methods= {},
                            attributes= {
                                'default': Attribute(
                                    idName= 'default',
                                    _type= 'Int'
                                )
                            },
                            parent= 'Object'),
                'IO': Type( idName= 'IO',
                            methods= {
                                "out_string": Method( idName= "out_string",
                                                returnType="SELF_TYPE",
                                                argTypes= ['x'],
                                                argNames= ['String']
                                            ),
                                "out_int":  Method( idName= "out_int",
                                                returnType="SELF_TYPE",
                                                argNames= ['x'],
                                                argTypes= ['Int']),
                                'in_string': Method( idName= 'in_string',
                                                returnType='String',
                                                argTypes= [],
                                                argNames= []),
                                'in_int':   Method (idName='in_int',
                                                returnType='Int',
                                                argTypes= [],
                                                argNames= [])
                            },
                            attributes= {},
                            parent= 'Object'),
                'SELF_TYPE': Type(idName='SELF_TYPE',
                                        parent= 'Object',
                                        attributes= {},
                                        methods={}),
                'String': Type( idName= 'String',
                                methods= {
                                    'length': Method(
                                        idName='length',
                                        returnType='Int',
                                        argTypes= [],
                                        argNames= []
                                    ),
                                    'concat': Method (
                                            idName= 'concat',
                                            returnType= 'String',
                                            argTypes= ['String'],
                                            argNames= ['x']
                                    ),
                                    'substr': Method (
                                        idName= 'substr',
                                        returnType='String',
                                        argNames= ['i', 'l'],
                                        argTypes=['Int', 'Int']
                                    )
                                },
                                attributes= {
                                            'default': Attribute(
                                                idName= 'default',
                                                _type='String')
                                            },
                                parent= 'Object'

                                ),
                'Bool': Type (idName= 'Bool',
                              attributes= {},
                              methods= {},
                              builtIn= True,
                              parent= 'Object')
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
                                    Type (idName= node.idName,
                                          attributes= {},
                                          methods= {},
                                          parent= node.parent if node else 'Object')
                            })

    def relateInheritance(self, idName : str, parent: str):
        return interceptError(
            validationFunc= lambda: idName in self.types,
            errorType= 'undefined type',
            idName= idName
        )  or interceptError (
            validationFunc= lambda: self.types[idName].parent in 
            self.types,
            errorType= 'undefined type',
            idName = self.types[idName].parent
        )  or interceptError(
            validationFunc= lambda: not self.types[parent].builtIn,
            errorType= 'built-in inheritance',
            idName= idName
        )  or interceptError(
            validationFunc= lambda: not self.isAncestor (
                idChild= idName, idParent= parent),
            errorType= 'inheritance from child',
            idParent= parent,
            idChild= idName
        ) or not self.actualizeInherits(idName, parent)
        
    def actualizeInherits (self, idName, parentName):
        for attr in self.types[parentName].attributes:
            result= self.actualizeInheritAttr(
                idName= idName, 
                childInfoAttr = self.types[idName].attributes.get(attr, None),
                parentInfoAttr= self.types[parentName].attributes[attr])
            if type(result) is error:
                return error

        for attr in self.types[parentName].inheritsAttr:
            result = self.actualizeInheritAttr(
                idName= idName,
                childInfoAttr= self.types[idName].attributes.get(attr, None),
                parentInfoAttr= self.types[parentName].inheritsAttr[attr]
            )
            if type(result) is error:
                return error
        for method in self.types[parentName].methods:
            result = self.actualizeInheritMethod(
                idName= idName,
                childInfoMethod= self.types[idName].methods.get(method, None),
                parentInfoMethod= self.types[parentName].methods[method]
            )
            if type(result) is error:
                return result
        
        
        for method in self.types[parentName].inheritsMethods:
            result = self.actualizeInheritMethod(
                idName= idName, 
                childInfoMethod= self.types[idName].methods.get(method, None),
                parentInfoMethod= self.types[parentName].inheritsMethods[method]
            )
            if type(result) is error:
                return result
            
        
        
    def actualizeInheritMethod(self,
                               idName,
                               childInfoMethod: Method,
                               parentInfoMethod: Method):
        return interceptError(
            validationFunc= lambda: not childInfoMethod or 
            childInfoMethod.returnType == parentInfoMethod.returnType and 
            len(childInfoMethod.argNames) == len(parentInfoMethod.argNames) and
            childInfoMethod.argTypes == parentInfoMethod.argTypes,
            errorType= 'bad redefine method',
            nameClass= idName,
            methodName = childInfoMethod.idName if childInfoMethod else None
        )or self.types[idName].inheritsMethods.update({
            parentInfoMethod.idName: parentInfoMethod
        })
    
    def actualizeInheritAttr(self,
            idName,
            childInfoAttr: Attribute,
            parentInfoAttr: Attribute):

        return interceptError(
            validationFunc= lambda: not (childInfoAttr and childInfoAttr._type != parentInfoAttr._type),
            errorType= "bad redefine attr",
            nameClass= idName,
            attrName= childInfoAttr.idName if childInfoAttr else None,
            attrType= childInfoAttr._type if childInfoAttr else None
        ) or childInfoAttr or self.types[idName].inheritsAttr.update({
            parentInfoAttr.idName: parentInfoAttr
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
        
        return interceptError(
                validationFunc= lambda : not attr.idName in
                self.types[typeName].attributes,
                errorType= 'repeated attr',
                idName= attr.idName
            ) or self.types[typeName].attributes.update({
                attr.idName: Attribute(idName= attr.idName,
                                       _type= attr._type )
            })

    def defineMethod(self, typeName: str,
                           node: NodeClassMethod):
        return interceptError(
            validationFunc= lambda: not node.idName in
            self.types[typeName].methods,
            errorType= 'repeated method',
            idName= node.idName
        ) or self.types[typeName].methods.update({
            node.idName: Method(idName= node.idName,
                                returnType= node.returnType,
                                argNames= node.argNames,
                                argTypes= node.argTypes)    
        })
        
    def checkEqualTypes(self, _type, returnType):
        
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
        

    def checkDynamicDispatch(self, 
                             typeName, method, arguments):
        
        
        methodInfo = self.types[typeName].methods.get(method, None)
        if not methodInfo:
            methodInfo= self.types[typeName].inheritsMethods.get(method, None)
        notAncestorArgs= [arguments[i] for i in range (len(arguments))
                           if arguments[i] != methodInfo.argTypes[i]
                           and not self.isAncestor(arguments[i],
                                        methodInfo.argTypes[i])]
        
        
        return interceptError(
            validationFunc= lambda : not methodInfo is None,
            errorType= 'undefined method in class',
            idName= method,
            className= typeName 
        ) or interceptError (
            validationFunc= lambda : notAncestorArgs == [],
            errorType= 'argument types in dispatch are not subtypes',
            idName= method,
            badArgs= notAncestorArgs
        ) or methodInfo.returnType

    

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.types, indent = 4, cls= MyEncoder)

    def buildEnv (self, typeName):
        typeInfo= self.types[typeName]
        d = {typeInfo.attributes[attr].idName: 
            {'type': typeInfo.attributes[attr]._type }
             for attr in typeInfo.attributes }
        d.update({ typeInfo.inheritsAttr[attr].idName:
            {'type': typeInfo.inheritsAttr[attr]._type}
                  for attr in typeInfo.inheritsAttr } )
        return d
    
    def checkAssign(self, node, _type, environment):
        
        return interceptError(
            validationFunc= lambda : node.idName in environment,
            errorType='undefined symbol',
            symbol= node.idName
        ) or interceptError(
            validationFunc= lambda : nodeType == _type
            or self.isAncestor(idChild=_type,
            idParent= nodeType),
            errorType='uncompatible types',
            type1= node.type,
            type2= exprResult['type']
            ) or nodeType
        
    
    def searchValue(self, node: NodeObject, environment):
        return interceptError(
                        validationFunc= lambda: node.idName
                        in environment and environment[node.idName],
                        errorType='undefined symbol',
                        symbolName= node.idName) or environment[node.idName]

    def checkArithmetic(self, type1, type2):
        return interceptError(validationFunc= lambda: type1 == type2,
                            errorType= 'uncompatible types',
                            type1= type1,
                            type2= type2) or type1

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

