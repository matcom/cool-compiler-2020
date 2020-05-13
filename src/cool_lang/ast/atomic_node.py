from .expresion_node import ExpressionNode


class AtomicNode(ExpressionNode):
    def __init__(self, token: str, line: int, column: int):
        super(AtomicNode, self).__init__(line, column)
        self.token: str = token
