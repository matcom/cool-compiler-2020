from typing import List
from .expresion_node import ExpressionNode


class BlockNode(ExpressionNode):
    def __init__(self, expressions: List[ExpressionNode], line: int, column: int):
        super(BlockNode, self).__init__(line, column)
        self.expressions: List[ExpressionNode] = expressions
