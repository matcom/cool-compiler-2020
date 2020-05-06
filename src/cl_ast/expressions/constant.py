from .exprNode import ExpressionNode

class ConstantNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

class IntegerNode(ConstantNode):
    pass

class StringNode(ConstantNode):
    pass

class BoolNode(ConstantNode):
    pass