class ProgramNode:
    def __init__(self, classes: list):
        self.classes = classes


class DefClassNode:
    def __init__(self, type, features, parent_type=None):
        self.type = type
        self.feature_nodes = features
        self.parent_type = parent_type


class FeatureNode:
    pass


class DefAttrNode(FeatureNode):
    def __init__(self, id, type, expr=None):
        self.id = id
        self.type = type
        self.expr = expr

    def __index__(self):
        return None


class DefFuncNode(FeatureNode):
    def __init__(self, id, params, return_type, expressions):
        self.id = id
        self.params = params
        self.return_type = return_type
        self.expressions = expressions


class AssignNode:
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr


class FuncCallNode:
    def __init__(self, id, args, object=None, type=None):
        self.object = object
        self.type = type
        self.id = id
        self.args = args


class IfNode:
    def __init__(self, if_expr, then_expr, else_expr):
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr


class WhileNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class BlockNode:
    def __init__(self, expressions):
        self.expressions = expressions


class LetNode:
    def __init__(self, let_attrs, expr):
        self.let_attrs = let_attrs
        self.expr = expr


class CaseNode:
    def __init__(self, expr, case_list):
        self.expr = expr
        self.case_list = case_list


class CaseElemNode:
    def __init__(self, expr, id, type):
        self.expr = expr
        self.id = id
        self.type = type


class InitNode:
    def __init__(self, type):
        self.type = type


class ExpressionNode:
    pass


class BinaryNode(ExpressionNode):
    def __init__(self, lvalue, rvalue):
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
        self.val = val


class NegationNode(UnaryNode):
    pass


class LogicNegationNode(UnaryNode):
    pass


class AtomNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass


class VarNode:
    def __init__(self, id):
        self.id = id


class NewNode:
    def __init__(self, t):
        self.type = t


class ConstantNode:
    def __init__(self, value):
        self.value = value


class IntNode(ConstantNode):
    pass


class BoolNode(ConstantNode):
    pass


class StringNode(ConstantNode):
    pass
