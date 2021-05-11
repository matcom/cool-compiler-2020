from .declaration_node import DeclarationNode
from .expresion_node import ExpressionNode


class LetNode(DeclarationNode):
    def __init__(
        self,
        idx: str,
        typex: str,
        expression: ExpressionNode,
        line: int = -1,
        column: int = -1,
    ):
        super(LetNode, self).__init__(idx, line, column)
        self.type: str = typex
        self.expression: ExpressionNode = expression
