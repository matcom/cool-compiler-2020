from .arithmetic_node import ArithmeticNode
from .expresion_node import ExpressionNode


class PlusNode(ArithmeticNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode, line: int, column: int):
        super(PlusNode, self).__init__(left, right, line, column)
