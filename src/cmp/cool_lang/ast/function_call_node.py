from typing import List
from .expresion_node import ExpressionNode


class FunctionCallNode(ExpressionNode):
    def __init__(self, obj: ExpressionNode, idx: str, args: List[ExpressionNode], typex: str, line: int, column: int):
        super(FunctionCallNode, self).__init__(line, column)
        self.obj: ExpressionNode = obj
        self.id: str = idx
        self.args: List[ExpressionNode] = args
        self.type: str = typex
