from .expresion_node import ExpressionNode


class NewNode(ExpressionNode):
    def __init__(self, typex: str, line: int, column: int):
        super(NewNode, self).__init__(line, column)
        self.type: str = typex
