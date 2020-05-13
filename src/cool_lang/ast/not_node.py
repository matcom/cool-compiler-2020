from .expresion_node import ExpressionNode
from .unary_node import UnaryNode


class NotNode(UnaryNode):
    def __init__(self, expression: ExpressionNode, line: int = None, column: int = None):
        super(NotNode, self).__init__(expression, line, column)
