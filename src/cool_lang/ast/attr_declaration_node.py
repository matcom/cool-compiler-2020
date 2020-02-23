from .declaration_node import DeclarationNode


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expression, line, column):
        self.id = idx
        self.type = typex
        self.expression = expression
        self.line = line
        self.column = column
