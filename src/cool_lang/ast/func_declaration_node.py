from .declaration_node import DeclarationNode


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body, line, column):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
        self.line = line
        self.column = column
