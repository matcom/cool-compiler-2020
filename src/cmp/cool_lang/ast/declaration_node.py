from .node import Node


class DeclarationNode(Node):
    def __init__(self, idx: str, line: int, column: int):
        super(DeclarationNode, self).__init__(line, column)
        self.id: str = idx
