from .binary_node import BinaryNode
from .expresion_node import ExpressionNode


class LessEqualNode(BinaryNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode, line: int, column: int):
        super(LessEqualNode, self).__init__(left, right, line, column)
