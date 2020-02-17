class AST:
    def __init__(self):
        pass


# <program> ::= <classes>
class Program(AST):
    def __init__(self, classes):
        super(Program, self).__init__()
        self.classes = classes


# <class> ::= class TYPE <inheritance> { <features_list_opt> } ;
class Class(AST):
    def __init__(self, TYPE, parentClass, features):
        super(Class, self).__init__()
        self.TYPE = TYPE
        self.inherparentClassitance = parentClass
        self.features = features


# A class Feature is either a ClassMethod or ClassAttribute
class Feature(AST):
    def __init__(self):
        super(Feature, self).__init__()


# <feature> ::= ID ( <formal_params_list_opt> ) : TYPE { <expression> }
class ClassMethod(Feature):
    def __init__(self, name, params, return_type, expr):
        super(ClassMethod, self).__init__()
        self.name = name
        self.params = params
        self.return_type = return_type
        self.expr = expr


# <formal> ::= ID : TYPE <- <expression> |  ID : TYPE
class ClassAttribute(Feature):
    def __init__(self, name, Type, expr):
        super(ClassAttribute, self).__init__()
        self.name = name
        self.type = Type
        self.expr = expr


# <formal_param> ::= ID : TYPE
class Parameter(AST):
    def __init__(self, ID, TYPE, expr):
        super(Parameter, self).__init__()
        self.ID = ID
        self.TYPE = TYPE
        self.expr = expr

# <expression>
class Expr(AST):
    def __init__(self):
        super(Expression, self).__init__()

# <expression> ::= ID <- <expr>
class AssingExpr(Expr):
    def __init__(self, name, expr):
        super(AssingExpr, self).__init__()
        self.name = name
        self.expr = expr

# <expression> ::= <expression>.ID( <arguments_list_opt> )
class DynamicCall(Expr):
    def __init__(self, instance, method, args):
        super(DynamicCall, self).__init__()
        self.instance = instance
        self.method = method
        self.args = args

# <expression> ::= <expression><at-type>.ID( <arguments_list_opt> )
class StaticCall(Expr):
    def __init__(self, instance, static_type, method, args):
        super(StaticCall, self).__init__()
        self.instance = instance
        self.method = method
        self.static_type = static_type
        self.args = args

# <arguments_list>  ::= <arguments_list_opt> , <expression>
#                   |   <expression>

class Arg(Expr):
    def __init__(self, expr):
        super(Arg, self)
        self.expr = expr

# <expression> ::= <case>
# <case> ::= case <expression> of <actions> esac
class Case(Expr):
    def __init__(self, expr, actions):
        super(Case, self).__init__()
        self.expr = expr
        self.actions = actions

# <actions> ::= <action>
#            |   <action> <actions>
# <action> ::= ID : TYPE => <expr>
class Action(Expr):
    def __init__(self, Type, expr):
        super(Action, self).__init__()
        self.type = Type
        self.expr = expr

# <expression> ::= <if_then_else>
# <if_then_else> ::= if <expression> then <expression> else <expression> fi
class If(Expr):
    def __init__(self, predicate, then_body, else_body):
        super(If, self).__init__()
        self.predicate = predicate
        self.then_body = then_body
        self.else_body = else_body

# <expression> ::= <while>
# <while> ::= while <expression> loop <expression> pool
class While(Expr):
    def __init__(self, predicate, body):
        super(While, self).__init__()
        self.predicate = predicate
        self.body = body

# <expression> ::= <block_expression>
# <block_expression> ::= { <block_list> }
# <block_list> ::= <block_list> <expression> ;
#               |   <expression> ;
class Block(Expr):
    def __init__(self, exprs):
        super(Block, self).__init__()
        self.exprs = exprs

# <expression> ::= <let_expression>
# <let_expression> ::= let <formal> in <expression>
#                   |   <nested_lets> , <formal>
#  <nested_lets> ::= <formal> IN <expression>
#                 |   <nested_lets> , <formal>
class Let(Expr):
    def __init__(self, instance, return_type, init_expr, body):
        super(Let, self).__init__()
        self.instance = instance
        self.return_type = return_type
        self.init_expr = init_expr
        self.body = body

# <expression> ::= new TYPE
class NewType(Expr):
    def __init__(self, Type):
        super(NewType, self)
        self.type = Type

# <expression> ::= isvoid <expr>
class IsVoid(Expr):
    def __init__(self, expr):
        super(IsVoid, self).__init__()
        self.expr = expr

# <expression> ::= <expression> + <expression>
class Sum(Expr):
    def __init__(self, summand1, summand2):
        super(Sum, self).__init__()
        self.summand1 = summand1
        self.summand2 = summand2


# <expression> ::= <expression> - <expression>
class Sub(Expr):
    def __init__(self, minuend, subtrahend):
        super(Sub, self).__init__()
        self.minuend = minuend
        self.subtrahend = subtrahend


# <expression> ::= <expression> * <expression>
class Mult(Expr):
    def __init__(self, factor1, factor2):
        super(Mult, self).__init__()
        self.factor1 = factor1
        self.factor2 = factor2


# <expression> ::= <expression> / <expression>
class Div(Expr):
    def __init__(self, dividend , divisor):
        super(Div, self).__init__()
        self.dividend  = dividend 
        self.divisor = divisor


# <expression> ::= ~ <expression>
class LogicalNot(Expr):
    def __init__(self, expr):
        super(LogicalNot, self).__init__()
        self.expr = expr


# <expression> ::= <expression> < <expression>
class LessThan(Expr):
    def __init__(self, left, right):
        super(LessThan, self).__init__()
        self.left = left
        self.right = right


# <expression> ::= <expression> <= <expression>
class LessOrEqualThan(Expr):
    def __init__(self, left, right):
        super(LessOrEqualThan, self).__init__()
        self.left = left
        self.right = right

# <expression> ::= <expression> = <expression>
class Equals(Expr):
    def __init__(self, left, right):
        super(Equals, self).__init__()
        self.left = left
        self.right = right


# <expression> ::= not <expression>
class Not(Expr):
    def __init__(self, expr):
        super(Not, self).__init__()
        self.expr = expr


# DUDA: Object debe existir? y debería heradar de Expr o de AST?
class Object(Expr):
    def __init__(self, name):
        super(Object, self).__init__()
        self.name = name


# <expression> ::= SELF
class SELF(Object):
    def __init__(self):
        super(Self, self).__init__("SELF")


# <expression> ::= INTEGER
class INTEGER(Expr):
    def __init__(self, value):
        super(Integer, self).__init__()
        self.value = value


# <expression> ::= INTEGER
class STRING(Expr):
    def __init__(self, value):
        super(Integer, self).__init__()
        self.value = value

# <expression> ::= TRUE | FALSE
class Boolean(Constant):
    def __init__(self, value):
        super(Boolean, self).__init__()
        self.value = value