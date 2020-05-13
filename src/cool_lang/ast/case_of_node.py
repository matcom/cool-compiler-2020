from typing import List
from .case_node import CaseNode
from .expresion_node import ExpressionNode


class CaseOfNode(ExpressionNode):
    def __init__(self, expression: ExpressionNode, cases: List[CaseNode], line: int, column: int):
        super(CaseOfNode, self).__init__(line, column)
        self.expression: ExpressionNode = expression
        self.cases: List[CaseNode] = cases
