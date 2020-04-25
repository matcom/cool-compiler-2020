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
    def __init__(self, idx, features, pos, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features
        self.pos = pos

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body, pos):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
        self.pos = pos
        self.pos = pos

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, pos, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr
        self.pos = pos

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, pos, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr
        self.pos = pos

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr, pos):
        self.id = idx
        self.expr = expr
        self.pos = pos

class CallNode(ExpressionNode):
    def __init__(self, obj, idx, args, pos):
        self.obj = obj
        self.id = idx
        self.args = args
        self.pos = pos

class BlockNode(ExpressionNode):
    def __init__(self, expr_list, pos):
        self.expr_list = expr_list
        self.pos = pos

class BaseCallNode(ExpressionNode):
    def __init__(self, obj, typex, idx, args, pos):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex
        self.pos = pos


class StaticCallNode(ExpressionNode):
    def __init__(self, idx, args, pos):
        self.id = idx
        self.args = args
        self.pos = pos


class AtomicNode(ExpressionNode):
    def __init__(self, lex, pos):
        self.lex = lex
        self.pos = pos

class BinaryNode(ExpressionNode):
    def __init__(self, left, right, pos):
        self.left = left
        self.right = right
        self.pos = pos

class BinaryLogicalNode(BinaryNode):
    def __init__(self, left, right, pos):
        super().__init__(left, right, pos)

class BinaryArithNode(BinaryNode):
    def __init__(self, left, right, pos):
        super().__init__(left, right, pos)

class UnaryNode(ExpressionNode):
    def __init__(self, expr, pos):
        self.expr = expr
        self.pos = pos

class UnaryLogicalNode(UnaryNode):
    def __init__(self, operand, pos):
        super().__init__(operand, pos)

class UnaryArithNode(UnaryNode):
    def __init__(self, operand, pos):
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
 
class TypeNode(AtomicNode):
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