from .declaration_node import DeclarationNode


class ParamDeclarationNode(DeclarationNode):
    def __init__(self, idx: str, typex: str, line: int = None, column: int = None):
        super(ParamDeclarationNode, self).__init__(idx, line, column)
        self.type: str = typex
