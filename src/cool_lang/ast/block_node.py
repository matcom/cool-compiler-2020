from .expresion_node import ExpressionNode


class BlockNode(ExpressionNode):
    def __init__(self, expressions, line, column):
        self.expressions = expressions
        self.line = line
        self.column = column
