from typing import List
from .expresion_node import ExpressionNode


class MemberCallNode(ExpressionNode):
    def __init__(self, idx: str, args: List[ExpressionNode], line: int, column: int):
        super(MemberCallNode, self).__init__(line, column)
        self.id: str = idx
        self.args: List[ExpressionNode] = args
