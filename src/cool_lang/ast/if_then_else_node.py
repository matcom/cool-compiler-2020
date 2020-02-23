from .expresion_node import ExpressionNode


class IfThenElseNode(ExpressionNode):
    def __init__(self, condition, if_body, else_body, line, column):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
        self.line = line
        self.column = column
