from ..utils.AST_definitions import *
from ..utils.errors import error

class context:
    def __init__(self, dictionaries ={}):
        self.types = { }

    def createType(self, node: NodeClass):
        if node.idName in self.types:
            return [error(
                error_type='Semantic error',
                row_and_col=(0,0), 
                message='Class %s already exist' %node.idName
                )]
        self.types.update({
            node.idName: {
            'parent': node.parent,
            'attrs': {},
            'methods': {} }
            } )
        return 'Success'

    """ def attachFeaturesToType (self, node: NodeClass):
        errors = []
        featureType = { NodeAttr: 'attrs', NodeClassMethod: 'methods' }
        classContext = self.types[node.idName]
        for feature in node.feature_list:
            if feature in self.types:
                errors.append(error(
                    error_type= 'Semantic error', row_and_col= (0, 0),
                    message='Feature %s already exist as a %s in the current scope' %(feature.idName, featureType[type(feature)][ :-1] ) ) )
            else:
                classContext[featureType[type(feature)]].update({
                        feature.idName: feature
                    })
        return errors """

    def getType(self, idName: str):
        return self.types.get(idName, False)

    def __repr__(self):
        return self.__str__()

programContext = context()
