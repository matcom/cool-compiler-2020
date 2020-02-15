from .exprNode import ExpressionNode

class OperationNode(ExpressionNode):
    pass

class BinaryOperationNode(OperationNode):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

class UnaryOperationNode(OperationNode):
    
    def __init__(self, expr):
        self.expr = expr

#Binaries

class SumNode(BinaryOperationNode):
    
    def __init__(self, left, right):
        super().__init__(left, right)

class DiffNode(BinaryOperationNode):
    
    def __init__(self, left, right):
        super().__init__(left, right)

class StarNode(BinaryOperationNode):
    
    def __init__(self, left, right):
        super().__init__(left, right)

class DivNode(BinaryOperationNode):
    
    def __init__(self, left, right):
        super().__init__(left, right)

class LessNode(BinaryOperationNode):
    
    def __init__(self, left, right):
        super().__init__(left, right)

class LessEqualNode(BinaryOperationNode):

    def __init__(self, left, right):
        super().__init__(left, right)

class EqualNode(BinaryOperationNode): 

    def __init__(self, left, right):
        super().__init__(left, right)

#Unaries

class BitNotNode(UnaryOperationNode):

    def __init__(self, expr):
        super().__init__(expr)

class IsVoidNode(UnaryOperationNode):

    def __init__(self, expr):
        super().__init__(expr)

class NotNode(UnaryOperationNode):
    
    def __init__(self, expr):
        super().__init__(expr)