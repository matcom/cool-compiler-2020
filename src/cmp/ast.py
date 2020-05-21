from collections import deque
from collections.abc import Sequence

class ASTNode:
    def children(self):
        if isinstance(self, NodeContainer):
            return ([""] * len(self), list(self))

        attr_list = [ attr for attr in self.__dict__ if (not attr.startswith("_")
                                                                and getattr(self, attr) != None) ]

        name_list = [ getattr(self, attr) for attr in attr_list]

        return (attr_list, name_list)

    def class_name(self):
        return self.__class__.__name__

    def dfs(self, obj, pattr = "", depth = 0, width = 5):
        pad = depth * width * '.'
        info = f"{pattr}=" if pattr else ""

        if isinstance(self, Terminal):
            obj.__rep_node.append(f"{pad}{info}{repr(self.value)}")
            return

        obj.__rep_node.append(f"{pad}{info}{self.__class__.__name__}(")
        
        attrs, names = self.children()

        for attr, name in zip(attrs, names):
            name.dfs(obj, attr, depth + 1)

        obj.__rep_node.append(f"{pad})")

    def __repr__(self):
        self.__rep_node = []
        self.dfs(self)
        return "\n".join(self.__rep_node)

class Formal(ASTNode):
    def __init__(self, id, type):
        self.id = id
        self.type = type

class NodeContainer(deque, ASTNode): pass

class Program(ASTNode):
    def __init__(self, class_list = NodeContainer()):
        self.class_list = class_list

class Class(ASTNode):
    def __init__(self, type, opt_inherits, feature_list = NodeContainer()):
        self.type = type
        self.opt_inherits = opt_inherits  #can be None
        self.feature_list = feature_list

class Feature(ASTNode): pass

class Method(Feature):
    def __init__(self, id, formal_list, type, expr):
        self.id = id
        self.formal_list = formal_list
        self.type = type
        self.expr = expr

class Attribute(Feature):
    def __init__(self, formal, opt_expr_init):
        self.formal = formal
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

class Let(Expr):
    def __init__(self, attribute_list, body):
        self.attribute_list = attribute_list
        self.body = body

class CaseBranch(Expr):
    def __init__(self, formal, expr):
        self.formal = formal
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

class Terminal(Expr, ASTNode):
    def __init__(self, value):
        self.value = value

class Type(Terminal): pass
class Id(Terminal): pass
class Int(Terminal): pass
class String(Terminal): pass
class Bool(Terminal): pass

if __name__ == '__main__':
    plus = Plus(Int(123), Int(65))
    isvoid = IsVoid(Int(5))
    b = Block(NodeContainer([Plus(Int(1), Int(1)), IsVoid(String("asd"))]))
    b = Minus(Int(3), Int(4))

    block = Block(NodeContainer([plus, b, isvoid]))

    print(block)
    print(b)
    print(plus)
