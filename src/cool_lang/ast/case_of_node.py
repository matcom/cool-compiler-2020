from .expresion_node import ExpressionNode


class CaseOfNode(ExpressionNode):
    def __init__(self, expression, branches, line, column):
        self.expression = expression
        self.branches = branches
        self.line = line
        self.column = column
