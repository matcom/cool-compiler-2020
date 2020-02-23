from .expresion_node import ExpressionNode


class NewNode(ExpressionNode):
    def __init__(self, typex, line, column):
        self.type = typex
        self.line = line
        self.column = column
