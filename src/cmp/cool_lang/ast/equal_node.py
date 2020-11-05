from .binary_node import BinaryNode
from .expresion_node import ExpressionNode


class EqualNode(BinaryNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode, line: int, column: int):
        super(EqualNode, self).__init__(left, right, line, column)
