from typing import List
from .expresion_node import ExpressionNode
from .let_node import LetNode


class LetInNode(ExpressionNode):
    def __init__(self, let_body: List[LetNode], in_body: ExpressionNode, line: int, column: int):
        super(LetInNode, self).__init__(line, column)
        self.let_body: List[LetInNode] = let_body
        self.in_body: ExpressionNode = in_body
