"""
Copyright (c) 2020 School of Math and Computer Science, University of Havana

COOL compiler project
"""

class AstNode:
    def __init__(self):
        self.lineno = 0
        self.colno = 0

    def add_location(self, line, column):
        self.lineno = line
        self.colno = column


class ProgramNode(AstNode):
    def __init__(self, classes: list):
        super().__init__()
        self.classes = classes


class DefClassNode(AstNode):
    def __init__(self, type, features, parent_type=None):
        super().__init__()
        self.type = type
        self.feature_nodes = features
        self.parent_type = parent_type


class FeatureNode(AstNode):
    def __init__(self, id):
        super().__init__()
        self.id = id


class DefAttrNode(FeatureNode):
    def __init__(self, id, type, expr=None):
        super().__init__(id)
        self.type = type
        self.expr = expr

    def __index__(self):
        return None


class DefFuncNode(FeatureNode):
    def __init__(self, id, params, return_type, expressions):
        super().__init__(id)
        self.params = params
        self.return_type = return_type
        self.expressions = expressions


class ExpressionNode(AstNode):
    def __init__(self):
        super().__init__()
        self.returned_type = None


class AssignNode(ExpressionNode):
    def __init__(self, id, expr):
        super().__init__()
        self.id = id
        self.expr = expr


class FuncCallNode(ExpressionNode):
    def __init__(self, id, args, object=None, type=None):
        super().__init__()
        self.object = object
        self.type = type
        self.id = id
        self.args = args
        self.self_type = None


class IfNode(ExpressionNode):
    def __init__(self, if_expr, then_expr, else_expr):
        super().__init__()
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr


class WhileNode(ExpressionNode):
    def __init__(self, cond, body):
        super().__init__()
        self.cond = cond
        self.body = body


class BlockNode(ExpressionNode):
    def __init__(self, expressions):
        super().__init__()
        self.expressions = expressions


class LetNode(ExpressionNode):
    def __init__(self, let_attrs, expr):
        super().__init__()
        self.let_attrs = let_attrs
        self.expr = expr


class CaseNode(ExpressionNode):
    def __init__(self, expr, case_list):
        super().__init__()
        self.expr = expr
        self.case_list = case_list


class CaseElemNode(AstNode):
    def __init__(self, expr, id, type):
        super().__init__()
        self.expr = expr
        self.id = id
        self.type = type


class BinaryNode(ExpressionNode):
    def __init__(self, lvalue, rvalue):
        super().__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue


class PlusNode(BinaryNode):
    pass


class MinusNode(BinaryNode):
    pass


class StarNode(BinaryNode):
    pass


class DivNode(BinaryNode):
    pass


class LessThanNode(BinaryNode):
    pass


class LessEqNode(BinaryNode):
    pass


class EqNode(BinaryNode):
    pass


class UnaryNode(ExpressionNode):
    def __init__(self, val):
        super().__init__()
        self.val = val


class NegationNode(UnaryNode):
    pass


class LogicNegationNode(UnaryNode):
    pass


class AtomNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass


class VarNode(ExpressionNode):
    def __init__(self, id):
        super().__init__()
        self.id = id


class NewNode(ExpressionNode):
    def __init__(self, t):
        super().__init__()
        self.type = t


class ConstantNode(ExpressionNode):
    def __init__(self, value):
        super().__init__()
        self.value = value


class IntNode(ConstantNode):
    pass


class BoolNode(ConstantNode):
    pass


class StringNode(ConstantNode):
    pass
