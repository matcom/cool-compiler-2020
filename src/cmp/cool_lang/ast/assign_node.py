from .expresion_node import ExpressionNode


class AssignNode(ExpressionNode):
    def __init__(self, idx: str, expression: ExpressionNode, line: int, column: int):
        super(AssignNode, self).__init__(line, column)
        self.id: str = idx
        self.expression: ExpressionNode = expression
