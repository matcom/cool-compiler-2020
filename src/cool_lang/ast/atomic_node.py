from .expresion_node import ExpressionNode


class AtomicNode(ExpressionNode):
    def __init__(self, token, line, column):
        self.token = token
        self.line = line
        self.column = column
