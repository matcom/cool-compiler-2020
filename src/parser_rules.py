from lexer_rules import tokens
#from expressions import *

from operator import add, mul
#from expressions import BinaryOperation, Number
my_bool = False

# Parsing rules
precedence = (
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY','DIVIDE'),
    ('right','ASSIGN'),
    ('left','NOT'),
    ('nonassoc','LT','LTEQ','EQ'),
    ('right','ISVOID'),
    ('right','INT_COMP'),
    ('left','AT'),
    ('left','DOT')
    )


def p_program(t):
    '''program : class SEMICOLON program
               | class SEMICOLON'''


def p_class(t):
    'class : CLASS TYPE _inherits LBRACE ffeature RBRACE'


def p_inherits(t):
    '''_inherits : INHERITS TYPE
                 | empty'''


def p_ffeature(t):
    '''ffeature : feature SEMICOLON ffeature
                | empty'''


def p_feature(t):
    '''feature : ID LPAREN formal RPAREN TDOTS TYPE LBRACE expr RBRACE
               | ID LPAREN RPAREN TDOTS TYPE LBRACE expr RBRACE
               | temp
               '''


def p_formal(t):
    '''formal : idDots COMMA formal
              | idDots'''


def p_expression_list(t):
    '''expression_list : expr SEMICOLON expression_list
                       | expr SEMICOLON'''


def p_expression_not(t):
    '''expr : NOT expr'''


def p_expression_binop(t):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr MULTIPLY expr
            | expr DIVIDE expr'''




def p_expression_g(t):
    '''expr : LPAREN expr RPAREN
            | ISVOID expr
            | block
            | conditional
            | loop
            | case
            | dispatch
            | INT_COMP expr
            '''


def p_block(t):
    'block : LBRACE expression_list RBRACE'


def p_expression_id(t):
    '''expr : ID'''


def p_expression_int(t):
    '''expr : INTEGER '''


def p_expression_str(t):
    '''expr : STRING'''


def p_expression_bool(t):
    '''expr : TRUE
            | FALSE'''


def p_expression_newtype(t):
    '''expr : NEW TYPE'''


def p_expression_l(t):
    '''expr : let'''


def p_dispatch(t):
    '''dispatch : expr especific DOT dispatch_call
                | dispatch_call'''


def p_especific(t):
    '''especific : AT TYPE
                 | empty'''


def p_dispatch_call(t):
    '''dispatch_call : ID LPAREN RPAREN
                     | ID LPAREN expr RPAREN
                     | ID LPAREN expr params_expression RPAREN'''


def p_more_expression(t):
    '''params_expression : COMMA expr params_expression
                         | COMMA expr'''



def p_empty(t):
    'empty :'


def p_let_expression(t):
    'let : LET declaration_list IN expr'


def p_declaration_list(t):
    '''declaration_list : temp COMMA declaration_list
                        | temp'''

def p_temp(t):
    '''temp : idDots
            | idDots ASSIGN expr'''


def p_idDots(t):
    'idDots : ID TDOTS TYPE'


def p_conditional(t):
    'conditional : IF expr THEN expr ELSE expr FI'


def p_loop(t):
    'loop : WHILE expr LOOP expr POOL'


def p_case(t):
    'case : CASE expr OF add ESAC'


def p_add(t):
    '''add : derivate SEMICOLON add
           | derivate SEMICOLON'''


def p_derivate(t):
    '''derivate : idDots ARROW expr'''


def p_expression_cmp(t):
    '''expr : expr LT expr
            | expr LTEQ expr
            | expr EQ expr'''


def p_expression_assign(t):
    'expr : ID ASSIGN expr'


def find_column(t):
    line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
    return t.lexpos - line_start + 1


def p_error(t):
    global my_bool
    """
    Error rule for Syntax Errors handling and reporting.
    """
    if t is None:
        print('(0, 0) - SyntacticError: ERROR at or near EOF')
    else:
        print('({}, {}) - SyntacticError: ERROR at or near "{}"'.format(
                t.lineno, find_column(t), t.value))
    my_bool = True