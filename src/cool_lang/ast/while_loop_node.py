from .expresion_node import ExpressionNode


class WhileLoopNode(ExpressionNode):
    def __init__(self, condition, body, line, column):
        self.condition = condition
        self.body = body
        self.line = line
        self.column = column
