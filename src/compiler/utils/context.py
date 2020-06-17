from ..utils.AST_definitions import *


class globalContex:
    def __init__ (self):
        self.types = {}

    def createType(self, node: NodeClass):
        currentClassContext = classContext(node)
        currentClassContext.initialize()
        self.types.update({node.idName : currentClassContext.contextDir})

        pass

    def initialize(self):
        pass


class classContext:
    def __init__(self, node: NodeClass):
        self.contextDir = {}
        self.node = node

    def initialize(self):
        pass