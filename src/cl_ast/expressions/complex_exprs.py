from .exprNode import ExpressionNode

#Atomic
class VariableNode(ExpressionNode):

    def __init__(self, idx):
        self.id = idx

class NewNode(ExpressionNode):
    
    def __init__(self, typex):
        self.type = typex

#Exprs

class ConditionalNode(ExpressionNode):
    
    def __init__(self, cond, stm, else_stm):
        self.cond = cond
        self.stm = stm
        self.else_stm = else_stm

class WhileNode(ExpressionNode):
    
    def __init__(self, cond, expr):
        self.cond = cond
        self.expr = expr

class LetNode(ExpressionNode):

    def __init__(self, init_list, expr):
        self.init_list = init_list
        self.expr = expr
    
    def __hash__(self):
        return id(self)

class BlockNode(ExpressionNode):

    def __init__(self, expr_list):
        self.expr_list = expr_list

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

class AssignNode(ExpressionNode):

    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class IsVoidNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr

#Dispatch

class ExprCallNode(ExpressionNode): #CallNode

    def __init__(self, obj, idx, args):
        self.obj = obj
        self.id = idx
        self.args = args

class SelfCallNode(ExpressionNode): #StaticCallNode

    def __init__(self, idx, args):
        self.id = idx
        self.args = args
    

class ParentCallNode(ExpressionNode): #BaseCallNode
    
    def __init__(self, obj, typex, idx, args):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex