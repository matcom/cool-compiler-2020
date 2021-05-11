from .expresion_node import ExpressionNode


class UnaryNode(ExpressionNode):
    def __init__(self, expression: ExpressionNode, line: int = None, column: int = None):
        super(UnaryNode, self).__init__(expression.line if line is None else line, expression.column if column is None else column)
        self.expression: ExpressionNode = expression
