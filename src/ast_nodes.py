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
    def __init__(self, name, parent, features, line, column):
        super(Class, self).__init__()
        self.name = name
        self.parent = parent
        self.features = features
        self.line = line
        self.column = column


# <feature> ::= ID ( <formal_params_list_opt> ) : TYPE { <expression> }
class ClassMethod(AST):
    def __init__(self, name, params, return_type, expr, line, column):
        super(ClassMethod, self).__init__()
        self.name = name
        self.params = params
        self.return_type = return_type
        self.expr = expr
        self.line = line
        self.column = column
        


# <attribute_init> ::= ID : TYPE <- <expression> | <attribute_def>
class AttributeInit(AST):
    def __init__(self, name, Type, expr, line, column):
        super(AttributeInit, self).__init__()
        self.name = name
        self.type = Type
        self.expr = expr
        self.line = line
        self.column = column


# <attribute_def> ::= ID : TYPE
class AttributeDef(AST):
    def __init__(self, name, Type, line, column):
        super(AttributeDef, self).__init__()
        self.name = name
        self.type = Type
        self.line = line
        self.column = column


# <formal_param> ::= ID : TYPE
class FormalParameter(AST):
    def __init__(self, name, param_type, line, column):
        super(FormalParameter, self).__init__()
        self.name = name
        self.param_type = param_type
        self.line = line
        self.column = column


# <expression>
class Expr(AST):
    def __init__(self):
        super(Expr, self).__init__()

# <expression> ::= ID <- <expr>


class AssignExpr(Expr):
    def __init__(self, instance, expr, line, column):
        super(AssignExpr, self).__init__()
        self.name = instance
        self.expr = expr
        self.line = line
        self.column = column

# <expression> ::= <expression>.ID( <arguments_list_opt> )


class DynamicCall(Expr):
    def __init__(self, instance, method, args, line, column):
        super(DynamicCall, self).__init__()
        self.instance = instance
        self.method = method
        self.args = args
        self.line = line
        self.column = column

# <expression> ::= <expression><at-type>.ID( <arguments_list_opt> )


class StaticCall(Expr):
    def __init__(self, instance, static_type, method, args, line, column):
        super(StaticCall, self).__init__()
        self.instance = instance
        self.method = method
        self.static_type = static_type
        self.args = args
        self.line = line
        self.column = column

# <expression> ::= <case>
# <case> ::= case <expression> of <actions> esac


class Case(Expr):
    def __init__(self, expr, actions, line, column):
        super(Case, self).__init__()
        self.expr = expr
        self.actions = actions
        self.line = line
        self.column = column

# <actions> ::= <action>
#            |   <action> <actions>
# <action> ::= ID : TYPE => <expr>


class Action(AST):
    def __init__(self, name, action_type, body, line, column):
        super(Action, self).__init__()
        self.name = name
        self.action_type = action_type
        self.body = body
        self.line = line
        self.column = column

# <expression> ::= <if_then_else>
# <if_then_else> ::= if <expression> then <expression> else <expression> fi


class If(Expr):
    def __init__(self, predicate, then_body, else_body, line, column):
        super(If, self).__init__()
        self.predicate = predicate
        self.then_body = then_body
        self.else_body = else_body
        self.line = line
        self.column = column

# <expression> ::= <while>
# <while> ::= while <expression> loop <expression> pool


class While(Expr):
    def __init__(self, predicate, body, line, column):
        super(While, self).__init__()
        self.predicate = predicate
        self.body = body
        self.line = line
        self.column = column

# <expression> ::= <block_expression>
# <block_expression> ::= { <block_list> }
# <block_list> ::= <block_list> <expression> ;
#               |   <expression> ;


class Block(Expr):
    def __init__(self, exprs, line, column):
        super(Block, self).__init__()
        self.exprs = exprs
        self.line = line
        self.column = column

# <expression> ::= <let_expression>
# <let_expression> ::= let <nested_vars> in <expression>
# <nested_vars> ::= <let_var_init>
#                  |   <nested_vars> , <let_var_def>


class Let(Expr):
    def __init__(self, var_list, body, line, column):
        super(Let, self).__init__()
        self.var_list = var_list
        self.body = body
        self.line = line
        self.column = column


# <let_var_init> ::= ID : TYPE <- <expression> | <let_var_def>
class LetVarInit(AST):
    def __init__(self, name, Type, expr, line, column):
        super(LetVarInit, self).__init__()
        self.name = name
        self.type = Type
        self.expr = expr
        self.line = line
        self.column = column


# <let_var_def> ::= ID : TYPE
class LetVarDef(AST):
    def __init__(self, name, Type, line, column):
        super(LetVarDef, self).__init__()
        self.name = name
        self.type = Type
        self.line = line
        self.column = column


# <expression> ::= new TYPE


class NewType(Expr):
    def __init__(self, Type, line, column):
        super(NewType, self)
        self.type = Type
        self.line = line
        self.column = column

# <expression> ::= isvoid <expr>


class IsVoid(Expr):
    def __init__(self, expr, line, column):
        super(IsVoid, self).__init__()
        self.expr = expr
        self.line = line
        self.column = column

# <expression> ::= <expression> + <expression>


class ArithmeticBinOp(Expr):
    def __init__(self):
        super(ArithmeticBinOp, self).__init__()


class Sum(ArithmeticBinOp):
    def __init__(self, summand1, summand2, line, column):
        super(Sum, self).__init__()
        self.left = summand1
        self.right = summand2
        self.line = line
        self.column = column


# <expression> ::= <expression> - <expression>
class Sub(ArithmeticBinOp):
    def __init__(self, minuend, subtrahend, line, column):
        super(Sub, self).__init__()
        self.left = minuend
        self.right = subtrahend
        self.line = line
        self.column = column


# <expression> ::= <expression> * <expression>
class Mult(ArithmeticBinOp):
    def __init__(self, factor1, factor2, line, column):
        super(Mult, self).__init__()
        self.left = factor1
        self.right = factor2
        self.line = line
        self.column = column


# <expression> ::= <expression> / <expression>
class Div(ArithmeticBinOp):
    def __init__(self, dividend, divisor, line, column):
        super(Div, self).__init__()
        self.left = dividend
        self.right = divisor
        self.line = line
        self.column = column


class LogicBinOp(Expr):
    def __init__(self):
        super(LogicBinOp, self).__init__()


# <expression> ::= ~ <expression>
class LogicalNot(Expr):
    def __init__(self, expr, line, column):
        super(LogicalNot, self).__init__()
        self.expr = expr
        self.line = line
        self.column = column


# <expression> ::= <expression> < <expression>
class LessThan(LogicBinOp):
    def __init__(self, left, right, line, column):
        super(LessThan, self).__init__()
        self.left = left
        self.right = right
        self.line = line
        self.column = column


# <expression> ::= <expression> <= <expression>
class LessOrEqualThan(LogicBinOp):
    def __init__(self, left, right, line, column):
        super(LessOrEqualThan, self).__init__()
        self.left = left
        self.right = right
        self.line = line
        self.column = column

# <expression> ::= <expression> = <expression>


class Equals(Expr):
    def __init__(self, left, right, line, column):
        super(Equals, self).__init__()
        self.left = left
        self.right = right
        self.line = line
        self.column = column


# <expression> ::= not <expression>
class Not(Expr):
    def __init__(self, expr, line, column):
        super(Not, self).__init__()
        self.expr = expr
        self.line = line
        self.column = column


# <expression> ::= ID
class Identifier(Expr):
    def __init__(self, name, line, column):
        super(Identifier, self).__init__()
        self.name = name
        self.line = line
        self.column = column


# <expression> ::= SELF
# class SELF(Identifier):
#     def __init__(self, line, column):
#         super(SELF, self).__init__("self", line, column)


# <expression> ::= INTEGER
class INTEGER(Expr):
    def __init__(self, value, line, column):
        super(INTEGER, self).__init__()
        self.value = value
        self.line = line
        self.column = column


# <expression> ::= STRING
class STRING(Expr):
    def __init__(self, value, line, column):
        super(STRING, self).__init__()
        self.value = value
        self.line = line
        self.column = column

# <expression> ::= TRUE | FALSE


class Boolean(Expr):
    def __init__(self, value, line, column):
        super(Boolean, self).__init__()
        self.value = value
        self.line = line
        self.column = column