from engine.cp.utils import Token
# AST Classes


class Node:
    def __init__(self):
        self.line = 0
        self.column = 0


class ErrorNode(Node):
    pass


class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
        self.line = declarations[0].line
        self.column = declarations[0].column


class DeclarationNode(Node):
    pass


class LetVariableDeclaration(DeclarationNode):
    def __init__(self, idx, typex, expression=None):
        self.id = idx
        self.type = typex
        self.expression = expression
        self.line = self.id.line
        self.column = self.id.column

    def __iter__(self):
        yield from (self.id, self.type, self.expression)


class CaseActionExpression(DeclarationNode):
    def __init__(self, idx, typex, expression=Node):
        self.id = idx
        self.type = Token(typex, 'ID') if isinstance(typex, str) else typex
        self.expression = expression
        self.line = self.id.line
        self.column = self.id.column

    def __iter__(self):
        yield from (self.id, self.type, self.expression)


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features
        self.line = idx.line
        self.column = idx.column


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex=None, expression=None):
        self.id = Token(idx, 'ID', 0, 0) if isinstance(idx, str) else idx
        self.type = typex
        self.expression = expression
        self.line = self.id.line
        self.column = self.id.column

    def __iter__(self):
        yield from (self.id, self.type, self.expression)


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
        self.line = idx.line
        self.column = idx.column


class ExpressionNode(Node):
    pass


class IfThenElseNode(ExpressionNode):
    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
        self.line = condition.line
        self.column = condition.column


class WhileLoopNode(ExpressionNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.line = condition.line
        self.column = condition.column


class BlockNode(ExpressionNode):
    def __init__(self, expressions):
        self.expressions = expressions
        self.line = expressions[-1].line
        self.column = expressions[-1].column


class LetInNode(ExpressionNode):
    def __init__(self, let_body, in_body=None):
        self.let_body = let_body  # [LetVariableDeclarations]
        self.in_body = in_body
        if in_body is None:
            last = self.let_body[-1]
            self.line = last.line
            self.column = last.column
        else:
            self.line = in_body.line
            self.column = in_body.column


class CaseOfNode(ExpressionNode):
    def __init__(self, expression, branches):
        self.expression = expression
        self.branches = branches
        self.line = expression.line
        self.column = expression.column


class AssignNode(ExpressionNode):
    def __init__(self, idx, expression):
        self.id = idx
        self.expression = expression
        self.line = idx.line
        self.column = idx.column


class UnaryNode(ExpressionNode):
    def __init__(self, expression):
        self.expression = expression
        self.line = expression.line
        self.column = expression.column


class NotNode(UnaryNode):
    pass


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.line = left.line
        self.column = left.column


class LessEqualNode(BinaryNode):
    pass


class LessNode(BinaryNode):
    pass


class EqualNode(BinaryNode):
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
    def __init__(self, obj, idx, args, typex=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex
        self.line = idx.line
        self.column = idx.column

    def __iter__(self):
        yield from (self.id, self.type, self.expression)


class MemberCallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args
        self.line = idx.line
        self.column = idx.column


class NewNode(ExpressionNode):
    def __init__(self, typex):
        self.type = typex
        self.line = typex.line
        self.column = typex.column


class AtomicNode(ExpressionNode):
    def __init__(self, token):
        self.token = token
        self.line = token.line
        self.column = token.column


class IntegerNode(AtomicNode):
    pass


class IdNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class BoolNode(AtomicNode):
    pass
