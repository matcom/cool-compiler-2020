from .declaration_node import DeclarationNode


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent, line, column):
        self.id = idx
        self.parent = parent
        self.features = features
        self.line = line
        self.column = column
