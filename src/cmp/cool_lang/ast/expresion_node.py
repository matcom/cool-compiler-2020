from .node import Node

class ExpressionNode(Node):
    def __init__(self, line: int, column: int):
        super(ExpressionNode, self).__init__(line, column)

