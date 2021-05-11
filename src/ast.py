# clase base del AST
class Node:
    def __init__(self, line_number):
        self.lineNumber = line_number

    def getLineNumber(self):
        return 0 if len(self.lineNumber) != 1 else self.lineNumber[0][0]

    def getColumnNumber(self):
        return 0 if len(self.lineNumber) != 1 else self.lineNumber[0][1]


# nodo del programa, classes es una lista de nodos ClassNode
class ProgramNode(Node):
    def __init__(self, classes, line_number):
        super().__init__(line_number)
        self.classes = classes


# nodo de clase, features es una lista de FeatureNode
class ClassNode(Node):
    def __init__(self, type_name, features, father_type_name, line_number):
        super().__init__(line_number)
        self.typeName = type_name
        self.features = features
        self.fatherTypeName = father_type_name


# nodo base de caracteristicas de clases
class FeatureNode(Node):
    pass


# nodo de caracteristicas de atributo
class AttributeFeatureNode(FeatureNode):
    def __init__(self, attr_id, type_name, expression, line_number):
        super().__init__(line_number)
        self.id = attr_id
        self.typeName = type_name
        self.expression = expression


# nodo de caracteristicas de metodos
class FunctionFeatureNode(FeatureNode):
    def __init__(self, func_id, parameters, type_name, statement, line_number):
        super().__init__(line_number)
        self.id = func_id
        self.parameters = parameters
        self.typeName = type_name
        self.statement = statement


# nodo de parametro
class ParameterNode(Node):
    def __init__(self, param_id, type_name, line_number):
        super().__init__(line_number)
        self.id = param_id
        self.typeName = type_name


# nodo base de expresiones
class StatementNode(Node):
    pass


# nodo de expresion de asignacion
class AssignStatementNode(StatementNode):
    def __init__(self, assign_id, expression, line_number):
        super().__init__(line_number)
        self.id = assign_id
        self.expression = expression


# nodo de expresiones condicionales
class ConditionalStatementNode(StatementNode):
    def __init__(self, eval_expr, if_expr, else_expr, line_number):
        super().__init__(line_number)
        self.evalExpr = eval_expr
        self.ifExpr = if_expr
        self.elseExpr = else_expr


# nodo de expresiones while
class LoopStatementNode(StatementNode):
    def __init__(self, eval_expr, loop_expr, line_number):
        super().__init__(line_number)
        self.evalExpr = eval_expr
        self.loopExpr = loop_expr


# nodo de expresiones block, expressiones es una lista de expresiones
class BlockStatementNode(StatementNode):
    def __init__(self, expressions, line_number):
        super().__init__(line_number)
        self.expressions = expressions


# nodo de expresiones let, variables es una lista de AttributeFeatureNode
class LetStatementNode(StatementNode):
    def __init__(self, variables, expression, line_number):
        super().__init__(line_number)
        self.variables = variables
        self.expression = expression


# nodo de expresiones case, body es una lista de CaseBranchNode
class CaseStatementNode(StatementNode):
    def __init__(self, expression, body, line_number):
        super().__init__(line_number)
        self.expression = expression
        self.body = body


# nodo de una rama de expresion case
class CaseBranchNode(StatementNode):
    def __init__(self, case_id, type_name, expression, line_number):
        super().__init__(line_number)
        self.id = case_id
        self.typeName = type_name
        self.expression = expression


# nodo de expresion new
class NewStatementNode(StatementNode):
    def __init__(self, type_name, line_number):
        super().__init__(line_number)
        self.typeName = type_name


# nodo de llamado de funcion, dispatchType es None si no es de tipo alternativo donde se
# especifica la clase del metodo, sino es un string con la clase correspondiente
# args es una lista de StatementNode
class FunctionCallStatement(StatementNode):
    def __init__(self, instance, dispatch_type, function, args, line_number):
        super().__init__(line_number)
        self.instance = instance
        self.dispatchType = dispatch_type
        self.function = function
        self.args = args
        self.instance_type = ""


# nodo base de las expresiones aritmeticas y de comparacion
class ExpressionNode(Node):
    pass


# nodo base de atomos (variables y constantes)
class AtomicNode(ExpressionNode):
    def __init__(self, lex, line_number):
        super().__init__(line_number)
        self.lex = lex


# nodo base para operaciones unarias
class UnaryNode(ExpressionNode):
    def __init__(self, expression, line_number):
        super().__init__(line_number)
        self.expression = expression


# nodo base para operaciones binarias
class BinaryNode(ExpressionNode):
    def __init__(self, left, right, line_number):
        super().__init__(line_number)
        self.left = left
        self.right = right


# nodo de constantes numericas
class ConstantNumericNode(AtomicNode):
    pass


# nodo de constantes de cadenas
class ConstantStringNode(AtomicNode):
    pass


# nodo de constantes booleanas
class ConstantBoolNode(AtomicNode):
    pass


# nodo de variables
class VariableNode(AtomicNode):
    pass


# nodo de expresiones not
class NotNode(UnaryNode):
    pass


# nodo de expresiones isvoid
class IsVoidNode(UnaryNode):
    pass


# nodo de expresion complemento de entero
class ComplementNode(UnaryNode):
    pass


# nodo de <=
class LessEqualNode(BinaryNode):
    pass


# nodo de <
class LessNode(BinaryNode):
    pass


# nodo de =
class EqualNode(BinaryNode):
    pass


# nodo de +
class PlusNode(BinaryNode):
    pass


# nodo de -
class MinusNode(BinaryNode):
    pass


# nodo de *
class TimesNode(BinaryNode):
    pass


# nodo de /
class DivideNode(BinaryNode):
    pass
