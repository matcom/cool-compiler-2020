from .expresion_node import ExpressionNode


class AssignNode(ExpressionNode):
    def __init__(self, idx, expression, line, column):
        self.id = idx
        self.expression = expression
        self.line = line
        self.column = column
