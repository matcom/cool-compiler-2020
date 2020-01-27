class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations

class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class CallNode(ExpressionNode):
    def __init__(self, obj, idx, args):
        self.obj = obj
        self.id = idx
        self.args = args

class BlockNode(ExpressionNode):
    def __init__(self, expr_list):
        self.expr_list = expr_list

class BaseCallNode(ExpressionNode):
    def __init__(self, obj, typex, idx, args):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex


class StaticCallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class BinaryLogicalNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)

class BinaryArithNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)

class UnaryNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr

class UnaryLogicalNode(UnaryNode):
    def __init__(self, operand):
        super().__init__(operand)

class UnaryArithNode(UnaryNode):
    def __init__(self, operand):
        super().__init__(operand)

class WhileNode(ExpressionNode):
    def __init__(self, cond, expr):
        self.cond = cond
        self.expr = expr

class ConditionalNode(ExpressionNode):
    def __init__(self, cond, stm, else_stm):
        self.cond = cond
        self.stm = stm
        self.else_stm = else_stm

class CaseNode(ExpressionNode):
    def __init__(self, expr, case_list):
        self.expr = expr
        self.case_list = case_list

    def __hash__(self):
        return id(self)

class OptionNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        self.id = idx
        self.typex = typex
        self.expr = expr
    

class LetNode(ExpressionNode):
    def __init__(self, init_list, expr):
        self.init_list = init_list
        self.expr = expr
    
    def __hash__(self):
        return id(self)

class ConstantNumNode(AtomicNode):
    pass

class ConstantBoolNode(AtomicNode):
    pass

class ConstantStrNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    pass
 
class InstantiateNode(AtomicNode):
    pass

class BinaryNotNode(UnaryArithNode):
    pass

class NotNode(UnaryLogicalNode):
    pass

class IsVoidNode(UnaryArithNode):
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