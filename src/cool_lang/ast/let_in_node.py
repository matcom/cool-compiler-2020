from .expresion_node import ExpressionNode


class LetInNode(ExpressionNode):
    def __init__(self, let_body, in_body, line, column):
        self.let_body = let_body
        self.in_body = in_body
        self.line = line
        self.column = column
