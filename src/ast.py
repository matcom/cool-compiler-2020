class Node:
    def __init__(self, line_number):
        self.lineNumber = line_number

    def GetLineNumber(self):
        return self.lineNumber


class ProgramNode(Node):
    def __init__(self, classes, line_number=0):
        super().__init__(line_number)
        self.classes = classes


class ClassNode(Node):
    def __init__(self, type_name, features, father_type_name, line_number):
        super().__init__(line_number)
        self.typeName = type_name
        self.features = features
        self.fatherTypeName = father_type_name
        self.lineNumber = line_number


class FeatureNode(Node):
    pass


class AttributeFeatureNode(FeatureNode):
    def __init__(self, attr_id, type_name, expression, line_number):
        super().__init__(line_number)
        self.id = attr_id
        self.typeName = type_name
        self.expression = expression
        self.lineNumber = line_number


class FunctionFeatureNode(FeatureNode):
    def __init__(self, func_id, parameters, type_name, statement, line_number):
        super().__init__(line_number)
        self.id = func_id
        self.parameters = parameters
        self.typeName = type_name
        self.statement = statement
        self.lineNumber = line_number


class ParameterNode(Node):
    def __init__(self, param_id, type_name, line_number):
        super().__init__(line_number)
        self.id = param_id
        self.typeName = type_name
        self.lineNumber = line_number


class StatementNode(Node):
    pass


class AssignStatementNode(StatementNode):
    def __init__(self, assign_id, expression, line_number):
        super().__init__(line_number)
        self.id = assign_id
        self.expression = expression
        self.lineNumber = line_number


class ConditionalStatementNode(StatementNode):
    def __init__(self, eval_expr, if_expr, else_expr):
        super().__init__(0)
        self.evalExpr = eval_expr
        self.ifExpr = if_expr
        self.elseExpr = else_expr


class LoopStatementNode(StatementNode):
    def __init__(self, eval_expr, loop_expr):
        super().__init__(0)
        self.evalExpr = eval_expr
        self.loopExpr = loop_expr


class BlockStatementNode(StatementNode):
    def __init__(self, expressions):
        super().__init__(0)
        self.expressions = expressions


class LetStatementNode(StatementNode):
    def __init__(self, variables, expression):
        super().__init__(0)
        self.variables = variables
        self.expression = expression


class CaseStatementNode(StatementNode):
    def __init__(self, expression, body):
        super().__init__(0)
        self.expression = expression
        self.body = body


class CaseBranchNode(StatementNode):
    def __init__(self, case_id, type_name, expression, line_number):
        super().__init__(line_number)
        self.lineNumber = line_number
        self.id = case_id
        self.typeName = type_name
        self.expression = expression


class NewStatementNode(StatementNode):
    def __init__(self, type_name, line_number):
        super().__init__(line_number)
        self.lineNumber = line_number
        self.typeName = type_name


class FunctionCallStatement(StatementNode):
    def __init__(self, instance, dispatch_type, function, args):
        super().__init__(0)
        self.instance = instance
        self.dispatchType = dispatch_type
        self.function = function
        self.args = args


class ExpressionNode(Node):
    pass


class AtomicNode(ExpressionNode):
    def __init__(self, lex, line_number):
        super().__init__(line_number)
        self.lex = lex
        self.lineNumber = line_number


class UnaryNode(ExpressionNode):
    def __init__(self, expression):
        super().__init__(0)
        self.expression = expression


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        super().__init__(0)
        self.left = left
        self.right = right


class ConstantNumericNode(AtomicNode):
    pass


class ConstantStringNode(AtomicNode):
    pass


class ConstantBoolNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    pass


class NotNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass


class ComplementNode(UnaryNode):
    pass


class LessEqualNode(BinaryNode):
    pass


class LessNode(BinaryNode):
    pass


class EqualNode(BinaryNode):
    pass


class PlusNode(BinaryNode):
    pass


class MinusNode(BinaryNode):
    pass


class TimesNode(BinaryNode):
    pass


class DivideNode(BinaryNode):
    pass
