from collections import deque
from collections import namedtuple

class ASTNode:
    def set_tracker(self, line, col):
        self.line = line
        self.col = col

    def set_static_type(self, t):
        self.static_type = t

    def get_children(self):
        if isinstance(self, NodeContainer):
            return list(self)

        attr_list = [ attr for attr in self.__dict__ if isinstance(getattr(self, attr), ASTNode) ]
        name_list = [ getattr(self, attr) for attr in attr_list ]

        return name_list

    def class_name(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.class_name()

class Formal(ASTNode):
    def __init__(self, id, type):
        self.id = id
        self.type = type

class NodeContainer(deque, ASTNode):
    def __repr__(self):
        return f'{self.class_name()}({len(self)})'

class Program(ASTNode):
    def __init__(self, cls_list = NodeContainer()):
        self.cls_list = cls_list

class Class(ASTNode):
    def __init__(self, type, opt_inherits, feature_list = NodeContainer(), can_inherit = True):
        self.type = type
        self.opt_inherits = opt_inherits  #can be None
        self.feature_list = feature_list
        self.children = []
        self.can_inherit = can_inherit
        self.methods = {}
        self.attrs = {}

        # data for type checker
        self.parent = None
        self.td = 0
        self.tf = 0
        self.level = 0

    def __str__(self):
        return f'<Class "{self.type}">'

class Feature(ASTNode): pass

class Method(Feature):
    def __init__(self, id, formal_list, type, expr):
        self.id = id
        self.formal_list = formal_list
        self.type = type
        self.expr = expr

class Attribute(Feature):
    def __init__(self, id, type, opt_expr_init):
        self.id = id
        self.type = type
        self.opt_expr_init = opt_expr_init  #can be None

class Expr(ASTNode): pass

class Assignment(Expr):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

class Dispatch(Expr):
    def __init__(self, expr, opt_type, id, expr_list = NodeContainer()):
        self.expr = expr
        self.opt_type = opt_type  #can be None
        self.id = id
        self.expr_list = expr_list

class SelfDispatch(Expr):
    def __init__(self, id, expr_list = NodeContainer()):
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
    def __init__(self, expr_list = NodeContainer()):
        self.expr_list = expr_list

class LetVar(Expr):
    def __init__(self, id, type, opt_expr_init):
        self.id = id
        self.type = type
        self.opt_expr_init = opt_expr_init

class Let(Expr):
    def __init__(self, let_list, body):
        self.let_list = let_list
        self.body = body

class CaseVar(Expr):
    def __init__(self, id, type):
        self.id = id
        self.type = type

class CaseBranch(Expr):
    def __init__(self, case_var, expr):
        self.case_var = case_var
        self.expr = expr

class Case(Expr):
    # Case list is a NodeContainer of CaseBranch

    def __init__(self, expr, case_list = NodeContainer()):
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

class Terminal(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'{self.class_name()}({repr(self.value)})'

class Type(Terminal): pass
class Id(Terminal): pass
class Int(Terminal): pass
class String(Terminal): pass
class Bool(Terminal): pass