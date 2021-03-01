from ..utils import Token, empty_token

# AST Classes
class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations

class DeclarationNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx.lex
        self.tid = idx
        self.features = features
        if not parent:
            parent = Token("Object", "type")
            parent.row = idx.row
            parent.column = idx.column
        self.parent = parent.lex
        self.tparent = parent

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None, arrow=empty_token):
        self.id = idx.lex
        self.tid = idx
        self.type = typex.lex
        self.ttype = typex
        self.arrow = arrow
        self.expr = expr

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx.lex
        self.tid = idx
        self.params = params
        self.type = return_type.lex
        self.ttype = return_type
        self.body = body

class ExpressionNode(Node):
    pass

class IfThenElseNode(ExpressionNode):
    def __init__(self, condition, if_body, if_token, else_body):
        self.token = if_token
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class WhileLoopNode(ExpressionNode):
    def __init__(self, condition, body, token):
        self.token = token
        self.condition = condition
        self.body = body

class BlockNode(ExpressionNode):
    def __init__(self, exprs):
        self.exprs = exprs

class LetInNode(ExpressionNode):
    def __init__(self, let_body, in_body):
        self.let_body = let_body
        self.in_body = in_body

class CaseOfNode(ExpressionNode):
    def __init__(self, expr, branches):
        self.expr = expr
        self.branches = branches

class CaseExpressionNode(AttrDeclarationNode):
    	pass

class LetAttributeNode(AttrDeclarationNode):
	pass

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx.lex
        self.tid = idx
        self.expr= expr

class UnaryNode(ExpressionNode):
    def __init__(self, expr, symbol):
        self.symbol = symbol
        self.expr = expr

class NotNode(UnaryNode):
    pass

class BinaryNode(ExpressionNode):
    def __init__(self, left, right, symbol):
        self.symbol = symbol
        self.left = left
        self.right = right

class ComparisonNode(BinaryNode):
    pass

class LessEqualNode(ComparisonNode):
    pass

class LessNode(ComparisonNode):
    pass

class EqualNode(ComparisonNode):
    pass

class ArithmeticNode(BinaryNode):
    pass

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class StarNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass

class IsVoidNode(UnaryNode):
    pass

class ComplementNode(UnaryNode):
    pass

class FunctionCallNode(ExpressionNode):
    def __init__(self, obj, idx, args, typex=empty_token):
        self.obj = obj
        self.id = idx.lex
        self.tid = idx
        self.args = args
        self.type = typex.lex
        self.ttype = typex

class MemberCallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx.lex
        self.tid = idx
        self.args = args

class NewNode(ExpressionNode):
    def __init__(self, typex):
        self.type = typex.lex
        self.ttype = typex

class AtomicNode(ExpressionNode):
    def __init__(self, token):
        self.lex = token.lex
        self.token = token

class IntegerNode(AtomicNode):
    pass

class IdNode(AtomicNode):
    pass

class StringNode(AtomicNode):
    pass

class BoolNode(AtomicNode):
    pass

class Param(Node):
    def __init__(self, tid, ttype):
        self.tid = tid
        self.ttype = ttype
        self.type = ttype.lex
        
    def __iter__(self):
        yield self.tid.lex
        yield self.type
