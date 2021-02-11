from lexer_rules import tokens
import AST
#from expressions import *

from operator import add, mul
#from expressions import BinaryOperation, Number

my_bool = False
result = ''

# Parsing rules
precedence = (
    ('right', 'ASSIGN'),
    ('right', 'NOT'),
    ('nonassoc', 'LTEQ', 'LT', 'EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'ISVOID'),
    ('right', 'INT_COMP'),
    ('left', 'AT'),
    ('left', 'DOT')
)
# precedence = (
#     ('left','PLUS','MINUS'),
#     ('left','MULTIPLY','DIVIDE'),
#     ('right','ASSIGN'),
#     ('left','NOT'),
#     ('nonassoc','LT','LTEQ','EQ'),
#     ('right','ISVOID'),
#     ('right','INT_COMP'),
#     ('left','AT'),
#     ('left','DOT')
# )

def p_program(production):
    '''program : classSet'''
    production[0] = AST.Program(production[1])
    production[0].line = 1

def p_classSet(production):
    '''
    classSet : class SEMICOLON classSet
            | class SEMICOLON
    '''
    if len(production) == 3:
        production[0] = [production[1]]
    else: production[0] = [production[1]] + production[3]

def p_class(production):
    'class : CLASS TYPE _inherits LBRACE ffeature RBRACE'
    production[0] = AST.Class(production[2], production[3], production[5])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_inherits(production):
    '''_inherits : INHERITS TYPE
                    | empty'''
    if len(production) == 3:
        production[0] = AST.Type(production[2])
    else: production[0] = None

def p_ffeature(production):
    '''ffeature : feature SEMICOLON ffeature
                | empty'''
    if len(production) == 4:
        production[0] = [production[1]] + production[3] #creo la lista de metodos y atributos
    else: production[0] = []

def p_feature(production):  #metodo || atributo
    #definition: name (args):returnType{expr}
    '''feature : ID LPAREN formal RPAREN TDOTS TYPE LBRACE expr RBRACE
                | ID LPAREN RPAREN TDOTS TYPE LBRACE expr RBRACE
                | temp
    '''
    if len(production) == 10:
        production[0] = AST.Method(production[1], production[3], production[6], production[8])
        production[0].line = production.lineno(1)
        line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
        production[0].index = production.lexpos(1) - line_start + 1
    elif len(production) == 9:
        production[0] = AST.Method(production[1], [], production[5], production[7])
        production[0].line = production.lineno(1)
        line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
        production[0].index = production.lexpos(1) - line_start + 1
    else:#atr
        production[0] = production[1]
        production[0].line = production[1].line
        production[0].index = production[1].index

#cambiar temp por atributos o variables
def p_temp(production):
    '''
    temp : idDots
        | idDots ASSIGN expr
    '''
    if len(production) == 2:
        production[0] = production[1]
    else: 
        production[0] = AST.Attribute(production[1].id, production[1].type, production[3])
        production[0].line = production.lineno(2)
        line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(2)) + 1
        production[0].index = production.lexpos(2) - line_start + 1

def p_idDots(production):
    'idDots : ID TDOTS TYPE'
    production[0] = AST.Var(production[1], production[3])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_formal(production):
    '''formal : idDots COMMA formal
                | idDots'''
    if len(production) == 2:
        production[0] = [production[1]]
    else: production[0] = [production[1]] + production[3]

def p_expression_list(production):
    '''expression_list : expression_list expr SEMICOLON 
                        | expr SEMICOLON
    '''
    if len(production) == 3:
        production[0] = [production[1]]
    else: production[0] = production[1] + [production[2]]

def p_expression_not(production): #boolean complement of <expr>
    '''expr : NOT expr'''
    production[0] = AST.Not(production[2])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_expression_binop(production):
    '''expr : expr PLUS expr    
            | expr MINUS expr
            | expr MULTIPLY expr
            | expr DIVIDE expr'''
    if production[2] == '+':
        production[0] = AST.Plus(production[1], production[3])
    elif production[2] == '-':
        production[0] = AST.Minus(production[1], production[3])
    elif production[2] == '*':
        production[0] = AST.Star(production[1], production[3])
    elif production[2] == '/':
        production[0] = AST.Div(production[1], production[3])
    production[0].line = production.lineno(2)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(2)) + 1
    production[0].index = production.lexpos(2) - line_start + 1

def p_expression_g(production):
    '''
    expr : LPAREN expr RPAREN
            | ISVOID expr
            | block
            | conditional
            | loop
            | case
            | dispatch
            | INT_COMP expr
    '''
    if len(production) == 4:
        production[0] = production[2]
    elif len(production) == 3:
        if production[1] == 'isvoid':
            production[0] = AST.IsVoid(production[2])
            production[0].line = production.lineno(1)
            line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
            production[0].index = production.lexpos(1) - line_start + 1
        else: 
            production[0] = AST.IntegerComplement(production[2])
            production[0].line = production.lineno(1)
            production[0].index = production[2].index
            # line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
            # production[0].index = production.lexpos(1) - line_start + 1
    else: production[0] = production[1]

def p_block(production):
    'block : LBRACE expression_list RBRACE'
    production[0] = AST.Block(production[2])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_expression_id(production):
    '''expr : ID'''
    production[0] = AST.Type(production[1])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_expression_int(production):
    '''expr : INTEGER '''
    production[0] = AST.Interger(production[1])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_expression_str(production):
    '''expr : STRING'''
    production[0] = AST.String(production[1])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_expression_bool(production):
    '''expr : TRUE
            | FALSE'''
    production[0] = AST.Boolean(production[1])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_expression_newtype(production):
    '''expr : NEW TYPE'''
    production[0] = AST.NewType(production[2])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_expression_l(production):
    '''expr : let'''
    production[0] = production[1]

#e_0.f(e_1,...,e_n)
def p_dispatch(production):
    '''
    dispatch : expr DOT ID LPAREN arguments_list_opt RPAREN
            |  expr AT TYPE DOT ID LPAREN arguments_list_opt RPAREN
            |  ID LPAREN arguments_list_opt RPAREN
    '''
    if len(production) == 7:
        production[0] = AST.Dispatch(production[3], production[5], production[1])
        production[0].line = production.lineno(2)
        # line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(2)) + 1
        # production[0].index = production.lexpos(2) - line_start + 1
        production[0].index = production[1].index
    elif len(production) == 5:
        production[0] = AST.Dispatch(production[1], production[3], None)
        production[0].line = production.lineno(1)
        line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
        production[0].index = production.lexpos(1) - line_start + 1
    else: 
        production[0] = AST.StaticDispatch(production[5], production[7], production[1], production[3])
        production[0].line = production.lineno(2)
        line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(2)) + 1
        production[0].index = production.lexpos(2) - line_start + 1

def p_arguments_list(production):
    """
    arguments_list : arguments_list COMMA expr
                        | expr
    """
    if len(production) == 4:
        production[0] = production[1] + [production[3]]
    else: production[0] = [production[1]]

def p_arguments_list_opt(production):
    """
    arguments_list_opt : arguments_list
                        | empty
    """
    production[0] = [] if production.slice[1].type == "empty" else production[1]


def p_empty(production):
    'empty :'
    production[0] = None

def p_let_expression(production):
    'let : LET declaration_list IN expr'
    production[0] = AST.LetVar(production[2], production[4])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_declaration_list(production):
    '''
    declaration_list : temp COMMA declaration_list
                    | temp
    '''
    if len(production) == 2:
        production[0] = [production[1]]
    else: production[0] = [production[1]] + production[3]

def p_conditional(production):
    'conditional : IF expr THEN expr ELSE expr FI'
    production[0] = AST.Conditional(production[2], production[4], production[6])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_loop(production):
    'loop : WHILE expr LOOP expr POOL'
    production[0] = AST.Loop(production[2], production[4])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_case(production):
    'case : CASE expr OF add ESAC'
    production[0] = AST.Case(production[2], production[4])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def p_add(production):
    '''add : derivate SEMICOLON add
            | derivate SEMICOLON
    '''
    if len(production) == 4:
        production[0] = [production[1]] + production[3]
    else: production[0] = [production[1]]

def p_derivate(production):
    '''derivate : idDots ARROW expr'''
    production[0] = AST.Branch(production[1], production[3])
    production[0].line = production.lineno(2)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(2)) + 1
    production[0].index = production.lexpos(2) - line_start + 1


def p_expression_cmp(production):
    '''expr : expr LT expr
            | expr LTEQ expr
            | expr EQ expr'''
    if production[2] == '<':
            production[0] = AST.LowerThan(production[1], production[3])
    elif production[2] == '<=':
        production[0] = AST.LowerEqualThan(production[1], production[3])
    elif production[2] == '=':
        production[0] = AST.EqualThan(production[1], production[3])
    production[0].line = production.lineno(2)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(2)) + 1
    production[0].index = production.lexpos(2) - line_start + 1


def p_expression_assign(production):
    'expr : ID ASSIGN expr'
    production[0] = AST.Assign(production[1], production[3])
    production[0].line = production.lineno(1)
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos(1)) + 1
    production[0].index = production.lexpos(1) - line_start + 1

def find_column(production):
    line_start = production.lexer.lexdata.rfind('\n', 0, production.lexpos) + 1
    return production.lexpos - line_start + 1

def p_error(production):
    global my_bool
    global result
    """
    Error rule for Syntax Errors handling and reporting.
    """
    if production is None:
        result = '(0, 0) - SyntacticError: ERROR at or near EOF'
        #print('(0, 0) - SyntacticError: ERROR at or near EOF')
    else:
        result = '({}, {}) - SyntacticError: ERROR at or near "{}"'.format(production.lineno, find_column(production), production.value)
        #print('({}, {}) - SyntacticError: ERROR at or near "{}"'.format(   production.lineno, find_column(production), production.value))
    my_bool = True