from ..utils.AST_definitions import *
from ..utils.errors import error, interceptError

class context:
    def __init__(self, dictionaries ={}):
        self.types = { }

    def createType(self, node: NodeClass):
        return interceptError(
            validationFunc= lambda: not node.idName in self.types,
            errorType= 'repeated class',
            idName= node.idName) or self.types.update({
                                node.idName: {
                                'parent': node.parent,
                                'attributes': {},
                                'methods': {} }
                                } )

    def getType(self, idName: str):
        return interceptError(
            validationFunc= lambda: idName in self.types,
            errorType= 'undefined type',
            idName= idName
        ) or self.types.get(idName)

    def defineAttrInType(self, typeName: str, attr: NodeAttr):
        return interceptError(
            validationFunc= lambda : not attr.idName in self.types[typeName],
            errorType= 'repeated attr',
            idName= attr.idName
        ) or not self.types[typeName]['attributes'].update({ attr.idName:
        { 'type': attr.attrType } }) 

    def defineMethod(self, typeNameForAttach: str,
                           methodName: str,
                           returnType,
                           argNames,
                           argTypes):
        return interceptError(
            validationFunc= lambda: not methodName in
            programContext.types[typeNameForAttach]['methods'],
            errorType= 'repeated method',
            idName= methodName
        ) and not programContext.types[typeNameForAttach]['methods'].update(
                { methodName: {
                'returnType': returnType,
                'argNames': argNames,
                'argTypesNames':argTypes 
            } })

    def __repr__(self):
        return self.__str__()

programContext = context()
