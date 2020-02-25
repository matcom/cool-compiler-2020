import ply.yacc as yacc
from lexer import tokens

# AST Classes
class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
        self.line = declarations[0].line
        self.column = declarations[0].column

class DeclarationNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features
        self.line = idx.line
        self.column = idx.column

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expression=None):
        self.id = idx
        self.type = typex
        self.expression = expression
        self.line = idx.line
        self.column = idx.column

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
    def __init__(self, let_body, in_body):
        self.let_body = let_body
        self.in_body = in_body
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


 # Get the token map from the lexer.  This is required.
from calclex import tokens
 

def p_program(p):
    'program : class_list'
    p[0]=ProgramNode(p[1])

def p_class_list(p):
    'class_list : def_class class_list'
    p[0]=[p[1]] + p[2]

def p_class_list_s(p):
    'class_list : def_class'
    p[0]=[p[1]]

def p_def_class(p):
    'def_class : CLASS TYPE OCUR feature_list CCUR SEMI'
    p[0]=ClassDeclarationNode(p[2],p[4])

def p_def_class_h(p):
    'def_class : CLASS TYPE INHERITS TYPE OCUR feature_list CCUR SEMI'
    p[0]=ClassDeclarationNode(p[2],p[6],p[4])


def p_feature_list(p):
    'feature_list : feature feature_list'
    p[0]=[p[1]]+p[2]

def p_feature_list_e(p):
    'feature_list : empty'
    
def p_feature_1(p):
    'feature : OBJECT COLON TYPE SEMI'
    p[0]=AttrDeclarationNode(p[1],p[3])

def p_feature_2(p):
    'feature : OBJECT COLON LARROW expr SEMI'
    p[0]=AttrDeclarationNode(p[1],p[3],p[5])

def p_feature_3(p):
    'feature : OBJECT OPAR param_list CPAR COLON TYPE OCUR expr CCUR SEMI'
    p[0]=FuncDeclarationNode(p[1], p[3], p[6], p[8]) 

def p_feature_4(p):
    'feature : OBJECT CPAR COLON TYPE OCUR expr CCUR SEMI'
    p[0]=FuncDeclarationNode(p[1], [], p[5], p[7])


def p_param_list_1(p):
    'param_list : param'
    p[0]=[p[1]]

def p_param_list_2(p):
    'param_list : param COMMA param_list'
    p[0]=[p[1]] + p[3]


# <expr-list>    ???
def p_expr_list_1(p):
    'expr_list : expr SEMI'
    p[0]=[p[1]]

def p_expr_list_2(p):
    'expr_list : expr SEMI expr_list'
    p[0]=[p[1]]+p[3]

# <let-list>     ???
def p_let_list1(p):
    'let_list : OBJECT COLON TYPE'
    p[0]=[(p[1], p[3], None)]

def p_let_list2(p):
    'let_list : OBJECT COLON TYPE LARROW expr'
    p[0]=[(p[1], p[3], p[5])]

def p_let_list3(p):
    'let_list : OBJECT COLON TYPE COMMA let_list'
    p[0]=[(p[1], p[3], None)] + p[5]

def p_let_list4(p):
    'let_list : OBJECT COLON TYPE LARROW expr COMMA let_list'
    p[0]=[(p[1], p[3], p[5])] + p[7]

# <case-list>    ???
def p_case_list_1(p):
    'case_list : OBJECT COLON TYPE RARROW expr SEMI'
    p[0] = [(p[1], p[3], p[5])]

def p_case_list_2(p):
    'case_list : OBJECT COLON TYPE RARROW expr SEMI case_list'
    p[0] = [(p[1], p[3], p[5])] + p[7]

# <truth-expr>   ???

def p_expr_2(p):
    'expr : comp_expr'
    p[0]=p[1]

# <comp-expr>    ???

def p_comp_expr_1(p):
    'comp_expr : comp_expr LEQ arith'
    p[0]= LessEqualNode(p[1], p[3])

def p_comp_expr_2(p):
    'comp_expr : comp_expr LESS arith'
    p[0]= LessNode(p[1], p[3])

def p_comp_expr_3(p):
    'comp_expr : comp_expr EQUAl arith'
    p[0]= EqualNode(p[1], p[3])

def p_comp_expr_4(p):
    'comp_expr : arith'
    p[0]= p[1]

# <arith>       ???

def p_arith_1(p):
    'arith : arith PLUS term'
    p[0]= PlusNode(p[1], p[3])

def p_arith_2(p):
    'arith : arith MINUS term'
    p[0]= MinusNode(p[1], p[3])

def p_arith_3(p):
    'arith : term'
    p[0]=p[1]

def p_arith_2_1(p):
    r'arith_2 : NOT arith'
    p[0]=NotNode(p[2])

def p_arith_2_2(p):
    r'arith_2 :arith'
    p[0]=p[1]


# <term>        ???
def p_term_1(p):
    'term : term STAR factor'
    p[0]=StarNode(p[1], p[3])

def p_term_2(p):
    'term : term DIV factor'
    p[0]=DivNode(p[1], p[3])

def p_term_3(p):
    'term : factor'
    p[0]=p[1]
# <factor>      ???
def p_factor_1(p):
    'factor : ISVOID factor2'
    p[0]= IsVoidNode(p[2])
def p_factor_2(0):
    'factor : factor2'
    p[0]=p[1]
# <factor-2>    ???
def p_factor_2_1(p):
    'factor_2 :COMPL atom'
    p[0]=ComplementNode(p[2])
def p_factor_2_1(p):
    'factor_2 : atom'
    p[0]=p[1]
# <atom>        ???

def p_atom_1(p):
    'atom : IF expr THEN expr ELSE expr FI'
    p[0]=IfThenElseNode(p[2], p[4], p[6])

def p_atom_2(p):
    'atom: WHILE expr LOOP expr POOL'
    p[0]=WhileLoopNode(p[2], p[4])

def p_atom_3(p):
    'atom : LET let_list INX expr'
    p[0]= LetInNode(p[2],p[4])

def p_atom_4(p):
    'atom : CASE expr OF ESAC '
    p[0]=CaseOfNode(p[2], p[4])

def p_atom_5 (p):
    'atom : idx LARROW expr'
    p[0]= AssignNode(p[1],p[3])

def p_atom_6(p):
    'atom : atom func_call'
    p[0]= FunctionCallNode(s[1],*s[2])

def p_atom_7(p):
    'atom : member_call'
    p[0]=p[1]

def p_atom_8(p):
    'atom : NEW TYPE'
    p[0]= NewNode(p[2])

def p_atom_9(p):
    'atom : OPAR expr CPAR'
    p[0]=p[2]

def p_atom_10(p):
    'atom : OBJECT'
    p[0]=IdNode(p[1])

def p_atom_11(p):
    'atom : INTEGER'
    p[0]= IntegerNode(p[1])

def p_atom_12(p):
    'atom : STRING'
    p[0]=StringNode(p[1])

def p_atom_13(p):
    'atom : BOOL'
    p[0]=BoolNode(p[1])

#<func-call> ???
def p_func_call_1(p):
    'func_call : DOT OBJECT OPAR arg_list CPAR'
    p[0]=(p[2],p[4])

def p_func_call_2(p):
    'func_call : DOT OBJECT OPAR CPAR'
    p[0]=(p[2],[])
    
def p_func_call_3(p):
    'func_call : AT TYPE DOT IDX OPAR arg_list CPAR'
    p[0]=(p[4],p[6],p[2])

def p_func_call_4(p):
    'func_call : AT TYPE DOT IDX OPAR  CPAR'
    p[0]=(p[4],[],p[2])

def p_arg_list_1(p):
    'arg_list : expr'
    p[0]=[p[1]]

def p_arg_list_1(p):
    'arg_list : expr COMMA arg_list'
    p[0]=[p[1]]+p[3]

def p_member_call_1(p):
    'member_call : OBJECT OPAR arg_list CPAR'
    p[0]= MemberCallNode(p[1],p[3])

def p_member_call_2(p):
    'member_call : OBJECT OPAR CPAR'
    p[0]= MemberCallNode(p[1],[])

def p_empty(p):
     'empty :'
     pass
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]
 
def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]
 
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]
 
def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]
 
def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]
 
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]
 
def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]
 
def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]
 
 # Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
 
 # Build the parser
parser = yacc.yacc()
 
while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)