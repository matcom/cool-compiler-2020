class Node:
    def GetLineNumber(self):
        return self.lineNumber

class ProgramNode(Node):
    def __init__(self, classes):
        self.classes = classes

class ClassNode(Node):
    def __init__(self, typeName, features, fatherTypeName, lineNumber):
        self.typeName = typeName
        self.features = features
        self.fatherTypeName = fatherTypeName
        self.lineNumber = lineNumber

class FeatureNode(Node):
    pass

class AttributeFeatureNode(FeatureNode):
    def __init__(self, id, typeName, expression, lineNumber):
        self.id = id
        self.typeName = typeName
        self.expression = expression
        self.lineNumber = lineNumber

class FunctionFeatureNode(FeatureNode):
    def __init__(self, id, parameters, typeName, statements, lineNumber):
        self.id = id
        self.parameters = parameters
        self.typeName = typeName
        self.statements = statements
        self.lineNumber = lineNumber

class ParameterNode(Node):
    def __init__(self, id, typeName, lineNumber):
        self.id = id
        self.typeName = typeName
        self.lineNumber = lineNumber

class StatementNode(Node):
    def __init__(self, lineNumber):
        self.lineNumber = lineNumber

class AssignStatementNode(StatementNode):
    def __init__(self, id, expression, lineNumber):
        self.id = id
        self.expression = expression
        StatementNode.__init__(lineNumber)

class DispatchStatementNode(StatementNode):
    def __init__(self, idRef, idFunc, args, typeDispatch, lineNumber):
        StatementNode.__init__(lineNumber)
        self.variableName = idRef
        self.functionName = idFunc
        self.args = args

class ConditionalStatementNode(StatementNode):
    def __init__(self, evalExpr, ifExpr, elseExpr, lineNumber):
        StatementNode.__init__(lineNumber)
        self.evalExpr = evalExpr
        self.ifExpr = ifExpr
        self.elseExpr = elseExpr

class LoopStatementNode(StatementNode):
    def __init__(self, evalExpr, loopExpr, lineNumber):
        StatementNode.__init__(lineNumber)
        self.evalExpr = evalExpr
        self.loopExpr = loopExpr

class BlockStatementNode(StatementNode):
    def __init__(self, expressions, lineNumber):
        StatementNode.__init__(lineNumber)
        self.expressions = expressions

class LetStatementNode(StatementNode):
    def __init__(self, variables, expression, lineNumber):
        StatementNode.__init__(lineNumber)
        self.variables = variables
        self.expression = expression

class CaseStatementNode(StatementNode):
    def __init__(self, expression, body, lineNumber):
        StatementNode.__init__(lineNumber)
        self.expression = expression
        self.body = body

class CaseBranchNode(StatementNode):
    def __init__(self, id, typeName, expression, lineNumber):
        StatementNode.__init__(lineNumber)
        self.id = id
        self.typeName = typeName
        self.expression = expression

class NewStatementNode(StatementNode):
    def __init__(self, typeName, lineNumber):
        StatementNode.__init__(lineNumber)
        self.typeName = typeName

class ExpressionNode(Node):
    pass

class AtomicNode(ExpressionNode):
    def __init__(self, lex, lineNumber):
        self.lex = lex
        self.lineNumber = lineNumber

class UnaryNode(ExpressionNode):
    def __init__(self, expression, lineNumber):
        self.expression = expression
        self.lineNumber = lineNumber

class BinaryNode(ExpressionNode):
    def __init__(self, left, right, lineNumber):
        self.left = left
        self.right = right
        self.lineNumber = lineNumber

class ConstantNumericNode(AtomicNode):
    pass

class ConstantStringNode(AtomicNode):
    pass

class ConstantBoolNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    pass

class CallNode(AtomicNode):
    def __init__(self, id, args):
        AtomicNode.__init__(self, id)
        self.args = args

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

