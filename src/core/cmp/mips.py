import core.cmp.visitor as visitor

ATTR_SIZE = 32

class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottext, dotdata, types):
        self._dottext = dottext
        self._dotdata = dotdata

class TextSectionNode(Node):
    def __init__(self, functions):
        self.functions

class FunctionNode(Node):
    def __init__(self, instructions):
        self.instructions = instructions

class DataSectionNode(Node):
    def __init__(self, data):
        self.data = data

class DataNode(Node):
    def __init__(self, name, value):
        self.name  = name
        self.value = value

class InstructionNode(Node):
    pass

class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name



class MIPSType():
    def __init__(self, name, attributes):
        self.attributes = attributes

    def get_offset(self, attr_name):
        return ATTR_SIZE * self.attributes.index(attributes)