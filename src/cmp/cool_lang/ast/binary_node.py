from .expresion_node import ExpressionNode


class BinaryNode(ExpressionNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode, line: int, column: int):
        super(BinaryNode, self).__init__(line, column)
        self.left: ExpressionNode = left
        self.right: ExpressionNode = right
