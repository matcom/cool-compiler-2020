from .expresion_node import ExpressionNode


class NewNode(ExpressionNode):
    def __init__(self, typex):
        self.type = typex
        self.line = typex.line
        self.column = typex.column
