class AstNode:
    def __init__(self):      
        self.lineno = 0
        self.colno = 0

    def add_location(self, line, column):
        self.lineno = line
        self.colno = column

    def accept(self, visitor):
        return visitor.visit(self)


class ProgramNode(AstNode):
    def __init__(self, classes: list):
        self.classes = classes


class DefClassNode(AstNode):
    def __init__(self, type, features, parent_type=None):
        self.type = type
        self.feature_nodes = features
        self.parent_type = parent_type


class FeatureNode(AstNode):
    def __init__(self, id):
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


class AssignNode(AstNode):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr


class FuncCallNode(AstNode):
    def __init__(self, id, args, object=None, type=None):
        self.object = object
        self.type = type
        self.id = id
        self.args = args


class IfNode(AstNode):
    def __init__(self, if_expr, then_expr, else_expr):
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr


class WhileNode(AstNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class BlockNode(AstNode):
    def __init__(self, expressions):
        self.expressions = expressions


class LetNode(AstNode):
    def __init__(self, let_attrs, expr):
        self.let_attrs = let_attrs
        self.expr = expr


class CaseNode(AstNode):
    def __init__(self, expr, case_list):
        self.expr = expr
        self.case_list = case_list


class CaseElemNode(AstNode):
    def __init__(self, expr, id, type):
        self.expr = expr
        self.id = id
        self.type = type


class InitNode(AstNode):
    def __init__(self, type):
        self.type = type


class ExpressionNode(AstNode):
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


class VarNode(AstNode):
    def __init__(self, id):
        self.id = id


class NewNode(AstNode):
    def __init__(self, t):
        self.type = t


class ConstantNode(AstNode):
    def __init__(self, value):
        self.value = value


class IntNode(ConstantNode):
    pass


class BoolNode(ConstantNode):
    pass


class StringNode(ConstantNode):
    pass
