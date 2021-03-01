from ply.lex import LexToken

class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
 
class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

class ErrorNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx:LexToken, features, parent=None):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        if parent:
            self.parent = parent.value
            self.parent_pos = (parent.lineno, parent.column)
        else:
            self.parent = None
            self.parent_pos = (0, 0)
        self.features = features
        self.token = idx

class _Param:
    def __init__(self, tok):
        self.value = tok.value
        self.pos = (tok.lineno, tok.column)

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx:LexToken, params, return_type:LexToken, body):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.params = [(pname.value, _Param(ptype)) for pname, ptype in params]
        self.type = return_type.value
        self.type_pos = (return_type.lineno, return_type.column)
        self.body = body


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx:LexToken, typex, expr=None):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.type = typex.value
        self.type_pos = (typex.lineno, typex.column)
        self.expr = expr
        self.token = idx

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx:LexToken, typex, expr=None):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.type = typex.value
        self.type_pos = (typex.lineno, typex.column)
        self.expr = expr

class AssignNode(ExpressionNode):
    def __init__(self, idx:LexToken, expr):
        if isinstance(idx, LexToken):
            self.id = idx.value
            self.pos = (idx.lineno, idx.column)
        else:
            self.id = idx
            self.pos = None
        self.expr = expr

class CallNode(ExpressionNode):
    def __init__(self, obj, idx:LexToken, args):
        self.obj = obj
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.args = args

class BlockNode(ExpressionNode):
    def __init__(self, expr_list, tok):
        self.expr_list = expr_list
        self.pos = (tok.lineno, tok.column)
        self.token = tok

class BaseCallNode(ExpressionNode):
    def __init__(self, obj, typex:LexToken, idx:LexToken, args):
        self.obj = obj
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.args = args
        self.type = typex.value
        self.type_pos = (typex.lineno, typex.column)


class StaticCallNode(ExpressionNode):
    def __init__(self, idx:LexToken, args):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.args = args


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        try:
            self.lex = lex.value
            self.pos = (lex.lineno, lex.column)
        except AttributeError:
            self.lex = lex
            self.pos = (0, 0)

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.pos = left.pos

class BinaryLogicalNode(BinaryNode):
    pass

class BinaryArithNode(BinaryNode):
    pass

class UnaryNode(ExpressionNode):
    def __init__(self, expr, tok):
        self.expr = expr
        self.pos = (tok.lineno, tok.column)

class UnaryLogicalNode(UnaryNode):
    pass

class UnaryArithNode(UnaryNode):
    pass

# --------

class WhileNode(ExpressionNode):
    def __init__(self, cond, expr, tok):
        self.cond = cond
        self.expr = expr
        self.pos = (tok.lineno, tok.column)

class ConditionalNode(ExpressionNode):
    def __init__(self, cond, stm, else_stm, tok):
        self.cond = cond
        self.stm = stm
        self.else_stm = else_stm
        self.pos = (tok.lineno, tok.column)

class CaseNode(ExpressionNode):
    def __init__(self, expr, case_list, tok):
        self.expr = expr
        self.case_list = case_list
        self.pos = (tok.lineno, tok.column)

    def __hash__(self):
        return id(self)

class OptionNode(ExpressionNode):
    def __init__(self, idx:LexToken, typex, expr):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.typex = typex.value
        self.type_pos = (typex.lineno, typex.column)
        self.expr = expr
    

class LetNode(ExpressionNode):
    def __init__(self, init_list, expr, tok):
        self.init_list = init_list
        self.expr = expr
        self.pos = (tok.lineno, tok.column)    

    def __hash__(self):
        return id(self)

class ConstantNumNode(AtomicNode):
    pass

class ConstantBoolNode(AtomicNode):
    pass

class ConstantStrNode(AtomicNode):
    pass

class ConstantVoidNode(AtomicNode):
    def __init__(self, obj):
        super().__init__(obj)

class SelfNode(Node):
    pass

class VariableNode(AtomicNode):
    pass
 
class TypeNode(AtomicNode):
    pass

class InstantiateNode(AtomicNode):
    pass

class BinaryNotNode(UnaryArithNode):
    pass

class NotNode(UnaryLogicalNode):
    pass

class IsVoidNode(UnaryLogicalNode):
    pass

class PlusNode(BinaryArithNode):
    pass

class MinusNode(BinaryArithNode):
    pass

class StarNode(BinaryArithNode):
    pass

class DivNode(BinaryArithNode):
    pass

class LessNode(BinaryLogicalNode):
    pass

class LessEqNode(BinaryLogicalNode):
    pass

class EqualNode(BinaryLogicalNode):
    pass