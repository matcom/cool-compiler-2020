from .exprNode import ExpressionNode

#Atomic
class VariableNode(ExpressionNode):
    def __init__(self, row, col, idx):
        super().__init__(row, col)
        self.id = idx

class NewNode(ExpressionNode):
    def __init__(self, row, col, typex):
        super().__init__(row, col)
        self.type = typex

#Exprs

class ConditionalNode(ExpressionNode):
    def __init__(self, row, col, cond, stm, else_stm):
        super().__init__(row, col)
        self.cond = cond
        self.stm = stm
        self.else_stm = else_stm

class WhileNode(ExpressionNode):
    def __init__(self, row, col, cond, expr):
        super().__init__(row, col)
        self.cond = cond
        self.expr = expr

class LetNode(ExpressionNode):
    def __init__(self, row, col, init_list, expr):
        super().__init__(row, col)
        self.init_list = init_list
        self.expr = expr
    
    def __hash__(self):
        return id(self)

class LetDeclarationNode(ExpressionNode):
    def __init__(self, row, col, idx, typex, expr=None):
        super().__init__(row, col)
        self.id = idx
        self.type = typex
        self.expr = expr
        self.type_pos = (0, 0)

class BlockNode(ExpressionNode):
    def __init__(self, row, col, expr_list):
        super().__init__(row, col)
        self.expr_list = expr_list

class CaseNode(ExpressionNode):
    def __init__(self, row, col, expr, case_list):
        super().__init__(row, col)
        self.expr = expr
        self.case_list = case_list

    def __hash__(self):
        return id(self)

class OptionNode(ExpressionNode):
    def __init__(self, row, col, idx, typex, expr):
        super().__init__(row, col)
        self.id = idx
        self.typex = typex
        self.expr = expr

class AssignNode(ExpressionNode):
    def __init__(self, row, col, idx, expr):
        super().__init__(row, col)
        self.id = idx
        self.expr = expr

class IsVoidNode(ExpressionNode):
    def __init__(self, row, col, expr):
        super().__init__(row, col)
        self.expr = expr

#Dispatch

class ExprCallNode(ExpressionNode): #CallNode
    def __init__(self, row, col, obj, idx, args):
        super().__init__(row, col)
        self.obj = obj
        self.id = idx
        self.args = args

class SelfCallNode(ExpressionNode): #StaticCallNode
    def __init__(self, row, col, idx, args):
        super().__init__(row, col)
        self.id = idx
        self.args = args
    

class ParentCallNode(ExpressionNode): #BaseCallNode
    def __init__(self, row, col, obj, typex, idx, args):
        super().__init__(row, col)
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex