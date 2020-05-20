from collections import deque, namedtuple

# Definition of a Formal
Formal = namedtuple('Formal', ['id', 'type'])

class ASTNode: pass

class Program(ASTNode):
    def __init__(self, class_list = deque()):
        self.class_list = deque()

class Class(ASTNode):
    def __init__(self, type, opt_inherits, feature_list = deque()):
        self.type = type
        self.opt_inherits = opt_inherits  #can be None
        self.feature_list = feature_list

class Feature(ASTNode): pass

class Method(Feature):
    def __init__(self, id, formal_list, type, expr_list = deque()):
        self.id = id
        self.formal_list = formal_list
        self.type = type
        self.expr_list = expr_list

class Attribute(Feature):
    def __init__(self, formal, opt_init):
        self.formal = formal
        self.opt_init = opt_init  #can be None

class Expr(ASTNode): pass

class Assignment(Expr):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

class Dispatch(Expr):
    def __init__(self, expr, opt_type, id, expr_list = deque()):
        self.expr = expr
        self.opt_type = opt_type  #can be None
        self.id = id
        self.expr_list = expr_list

class SelfDispatch(Expr):
    def __init__(self, id, expr_list = deque()):
        self.id = id
        self.expr_list = expr_list

class If(Expr):
    def __init__(self, predicate, if_branch, else_branch):
        self.predicate = predicate
        self.if_branch = if_branch
        self.else_branch = else_branch

class While(Expr):
    def __init__(self, predicate, body):
        self.predicate = predicate
        self.body = body

class Block(Expr):
    def __init__(self, expr_list = deque()):
        self.expr_list = expr_list

class Let(Expr):
    def __init__(self, attribute_list, body):
        self.attribute_list = attribute_list
        self.body = body

class Case(Expr):
    # Case list is a deque of (Formal, Expr)

    def __init__(self, expr, case_list = deque()):
        self.expr = expr
        self.case_list = case_list

class New(Expr):
    def __init__(self, type):
        self.type = type

class UnaryOp(Expr):
    def __init__(self, expr):
        self.expr = expr

class IsVoid(UnaryOp): pass
class IntComp(UnaryOp): pass
class Not(UnaryOp): pass

class BinaryOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Plus(BinaryOp): pass
class Minus(BinaryOp): pass
class Mult(BinaryOp): pass
class Div(BinaryOp): pass

class Less(BinaryOp): pass
class LessEq(BinaryOp): pass
class Eq(BinaryOp): pass

if __name__ == '__main__':
    plus = Plus(123, 65)
    isvoid = IsVoid(5)
    b = Block(deque([Plus(1, 1), IsVoid("asd")]))

    block = Block(deque([plus, b, isvoid]))

    print(block)
