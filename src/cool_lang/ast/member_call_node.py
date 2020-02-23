from .expresion_node import ExpressionNode


class MemberCallNode(ExpressionNode):
    def __init__(self, idx, args, line, column):
        self.id = idx
        self.args = args
        self.line = line
        self.column = column
