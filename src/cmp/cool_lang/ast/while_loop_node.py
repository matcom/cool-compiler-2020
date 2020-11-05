from .expresion_node import ExpressionNode


class WhileLoopNode(ExpressionNode):
    def __init__(self, condition: ExpressionNode, body: ExpressionNode, line: int, column: int):
        super(WhileLoopNode, self).__init__(line, column)
        self.condition: ExpressionNode = condition
        self.body: ExpressionNode = body
