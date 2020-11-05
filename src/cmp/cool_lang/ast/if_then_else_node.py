from .expresion_node import ExpressionNode


class IfThenElseNode(ExpressionNode):
    def __init__(self, condition: ExpressionNode, if_body: ExpressionNode, else_body: ExpressionNode, line: int, column: int):
        super(IfThenElseNode, self).__init__(line, column)
        self.condition: ExpressionNode = condition
        self.if_body: ExpressionNode = if_body
        self.else_body: ExpressionNode = else_body
