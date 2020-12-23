class Node:
    line = 0
    index = 0

class Program(Node):
    def __init__(self, classes = None):
        self.classes = classes
        if classes is None:
            self.classes = []

class Class(Node):
    def __init__(self, _type, inherit, features=None):
        self.name = _type
        self.inherit = inherit
        self.methods = []
        self.attributes = []

        if features is not None:
            for feature in features:
                if isinstance(feature, Method):
                    self.methods.append(feature)
                else:
                    self.attributes.append(feature)

class Type:
    def __init__(self, type):
        self.name = type

class Branch:
    def __init__(self, _var, _expr):
        self.var = _var
        self.expr = _expr

class Feature(Node):
    pass

class Method(Feature):
    def __init__(self, id, parameters, return_type, expr=None):
        self.id = id
        self.parameters = parameters
        self.return_type = return_type
        self.expression = expr

class Attribute(Feature):
    def __init__(self, id, _type, _expr = None):
        self.type = _type
        self.expr = _expr
        self.id = id

class Expression(Node):
    computed_type = None

class Atom(Expression):
    pass

class Assign(Expression):
    def __init__(self, _id, expr):
        self.id = _id
        self.expression = expr

class Dispatch(Atom):
    def __init__(self, func_id, params = None, left_expr = None):
        self.left_expression = left_expr
        self.func_id = func_id
        self.parameters = params
        self.className = 'dispatch'

        if params is None:
            self.parameters = []

class StaticDispatch(Atom):
    def __init__(self, func_id, params, left_expr, parent_type):
        self.left_expression = left_expr
        self.func_id = func_id
        self.parameters = params
        self.parent_type = parent_type
        self.className = 'dispatch'

class Conditional(Atom):
    def __init__(self, if_expr, then_expr, else_expr):
        self.if_expression = if_expr
        self.then_expression = then_expr
        self.else_expression = else_expr
        self.className = 'conditional'

class Loop(Atom):
    def __init__(self, while_expr, loop_exprs):
        self.while_expression = while_expr
        self.loop_expression = loop_exprs
        self.className = 'loop'

class LetVar(Atom):
    def __init__(self, declarations, in_expr):
        self.in_expression = in_expr
        self.declarations = declarations

class Var(Atom):
    def __init__(self, _name, _type):
        self.id = _name
        self.type = _type

class Case(Atom):
    def __init__(self, case_expr, implications):
        self.case_expression = case_expr
        self.implications = implications
        self.className = 'case'

class NewType(Atom):
    def __init__(self, _type_name):
        self.type_name = _type_name

class UnaryOperator(Expression):
    def __init__(self,expr):
        self.expression = expr

class BinaryOperator(Expression):
    def __init__(self, left_expr, right_expr):
        self.left_expression = left_expr
        self.right_expression = right_expr

class BAritmeticOperation(BinaryOperator):
    pass

class Plus(BAritmeticOperation):
    def __init__(self, _first, _second):
        self.symbol = "+"
        self.first = _first
        self.second = _second

class Minus(BAritmeticOperation):
    def __init__(self, _first, _second):
        self.symbol = "-"
        self.first = _first
        self.second = _second

class Star(BAritmeticOperation):
    def __init__(self, _first, _second):
        self.symbol = "*"
        self.first = _first
        self.second = _second

class Div(BAritmeticOperation):
    def __init__(self, _first, _second):
        self.symbol = "/"
        self.first = _first
        self.second = _second

class Not(UnaryOperator):
    def __init__(self, _expr):
        self.expr = _expr

class IntegerComplement(Atom):
    def __init__(self, _expr):
        self.expression = _expr

class IsVoid(UnaryOperator):
    def __init__(self, _expr):
        self.expression = _expr

class LowerThan(BinaryOperator):
    def __init__(self, _first, _second):
        self.symbol = "<"
        self.first = _first
        self.second = _second

class LowerEqualThan(BinaryOperator):
    def __init__(self, _first, _second):
        self.symbol = "<="
        self.first = _first
        self.second = _second

class EqualThan(BinaryOperator):
    def __init__(self, _first, _second):
        self.symbol = "="
        self.first = _first
        self.second = _second

class Block(Atom):
    def __init__(self, exprs):
        self.expressions = exprs
        self.className = 'block'

class Interger(Atom):
    def __init__(self,value):
        self.value = value

class String(Atom):
    def __init__(self, value):
        self.value = value

class Boolean(Atom):
    def __init__(self,value):
        self.value = value