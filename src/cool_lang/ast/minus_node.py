from .arithmetic_node import ArithmeticNode
from .expresion_node import ExpressionNode


class MinusNode(ArithmeticNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode, line: int, column: int):
        super(MinusNode, self).__init__(left, right, line, column)
