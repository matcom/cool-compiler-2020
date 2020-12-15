from .exprNode import ExpressionNode

class OperationNode(ExpressionNode):
    pass

class BinaryOperationNode(OperationNode):
    def __init__(self, row, col, left, right):
        super().__init__(row, col)
        self.left = left
        self.right = right

class UnaryOperationNode(OperationNode):
    def __init__(self, row, col, expr):
        super().__init__(row, col)
        self.expr = expr

#Binaries

class BinaryArithOperationNode(BinaryOperationNode):
    pass

class SumNode(BinaryArithOperationNode):
    pass

class DiffNode(BinaryArithOperationNode):
    pass

class StarNode(BinaryArithOperationNode):
    pass

class DivNode(BinaryArithOperationNode):
    pass

class BinaryLogicalOperationNode(BinaryOperationNode):
    pass

class LessNode(BinaryLogicalOperationNode):
    pass

class LessEqualNode(BinaryLogicalOperationNode):
    pass

class EqualNode(BinaryLogicalOperationNode): 
    pass

#Unaries

class BitNotNode(UnaryOperationNode):
    pass

class NotNode(UnaryOperationNode):
    pass