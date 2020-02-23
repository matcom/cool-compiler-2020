from .expresion_node import ExpressionNode


class BinaryNode(ExpressionNode):
    def __init__(self, left, right, line, column):
        self.left = left
        self.right = right
        self.line = line
        self.column = column
