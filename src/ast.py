class Node:
    def GetLineNumber(self, lineNumber):
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

class AttributeFeatureNode():
    def __init__(self, id, typeName, expression, lineNumber):
        self.id = id
        self.typeName = typeName
        self.expression = expression
        self.lineNumber = lineNumber

class FunctionFeatureNode():
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

class AssignStatementNode():
    def __init__(self, id, expression, lineNumber):
        self.id = id
        self.expression = expression
        self.lineNumber = lineNumber

class DispatchStatementNode():
    def __init__(self, idRef, idFunc, args, typeDispatch, lineNumber):
        self.lineNumber = lineNumber
        self.variableName = idRef
        self.functionName = idFunc
        self.args = args

class ConditionalStatementNode():
    def __init__(self, evalExpr, ifExpr, elseExpr):
        self.evalExpr = evalExpr
        self.ifExpr = ifExpr
        self.elseExpr = elseExpr

class LoopStatementNode():
    def __init__(self, evalExpr, loopExpr):
        self.evalExpr = evalExpr
        self.loopExpr = loopExpr

class BlockStatementNode():
    def __init__(self, expressions):
        self.expressions = expressions

class LetStatementNode():
    def __init__(self, variables, expression):
        self.variables = variables
        self.expression = expression

class CaseStatementNode():
    def __init__(self, expression, body):
        self.expression = expression
        self.body = body

class CaseBranchNode():
    def __init__(self, id, typeName, expression, lineNumber):
        self.lineNumber = lineNumber
        self.id = id
        self.typeName = typeName
        self.expression = expression

class NewStatementNode():
    def __init__(self, typeName, lineNumber):
        self.lineNumber = lineNumber
        self.typeName = typeName

class FunctionCallStatement():
    def __init__(self, instance, dispatchType, function, args):
        self.instance = instance
        self.dispatchType = dispatchType
        self.function = function
        self.args = args

class ConstantNumericNode(Node):
    def __init__(self, lex, lineNumber):
        self.lex = lex
        self.lineNumber = lineNumber

class ConstantStringNode(Node):
    def __init__(self, lex, lineNumber):
        self.lex = lex
        self.lineNumber = lineNumber

class ConstantBoolNode(Node):
    def __init__(self, lex, lineNumber):
        self.lex = lex
        self.lineNumber = lineNumber

class VariableNode(Node):
    def __init__(self, lex, lineNumber):
        self.lex = lex
        self.lineNumber = lineNumber

class NotNode(Node):
    def __init__(self, expression):
        self.expression = expression

class IsVoidNode(Node):
    def __init__(self, expression):
        self.expression = expression

class ComplementNode(Node):
    def __init__(self, expression):
        self.expression = expression

class LessEqualNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class LessNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class EqualNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class PlusNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class MinusNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class TimesNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class DivideNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

