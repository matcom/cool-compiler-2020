from .arithmetic_node import ArithmeticNode
from .expresion_node import ExpressionNode


class StarNode(ArithmeticNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode, line: int, column: int):
        super(StarNode, self).__init__(left, right, line, column)
