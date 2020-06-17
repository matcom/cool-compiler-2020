from ..utils.AST_definitions import *

class context:
    def __init__(self, dictionaries):
        self.dictionaries = dictionaries
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        toReturn= ""
        for dictio in self.dictionaries:
            toReturn += "%s: {\n" %(dictio.__name__)
            for key in dictio:
                toReturn += "\t%s: %s\n" %(key, dictio[key])
            toReturn +="\n}"
        return toReturn

class globalContex(context):
    def __init__ (self):
        self.types = {}
        super().__init__(dictionaries = [self.types])

    def createType(self, node: NodeClass):
        currentClassContext = classContext(node)
        currentClassContext.initialize()
        self.types.update({node.idName : currentClassContext})


    def initialize(self):
        pass


class classContext(context):
    def __init__(self, node: NodeClass):
        self.classInfo = {}
        self.methods = {}
        self.attrs ={}
        self.node = node
        super().__init__(dictionaries = [self.classInfo, 
        self.methods, self.attrs])

    def initialize(self):
        self.classInfo.update({"idName": self.node.idName,
        "parent": self.node.parent})


