import ply.yacc as yacc
from lexer import *
from errors import add_parser_error
from ast import *

precedence = (
    ('left', 'DOT'),
    ('left', 'AT'),
    ('left', 'NOT'),
    ('left', 'ISVOID'),
    ('left', 'STAR', 'DIV'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'GREATEREQ', 'LOWEREQ', 'LOWER', 'GREATER', 'EQUAL'),
    ('left', 'LNOT'),
    ('right', 'ASSIGN'),
)


def p_program(p):
    'program : class_list'
    p[0] = ProgramNode(p[1])


def p_empty(p):
    'empty :'
    pass


def p_class_list(p):
    '''class_list : def_class class_list
                  | def_class'''

    if len(p) == 3:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_def_class(p):
    '''def_class : CLASS TYPE OBRACKET feature_list CBRACKET SEMICOLON
                  | CLASS TYPE INHERITS TYPE OBRACKET feature_list CBRACKET SEMICOLON'''
    if len(p) == 8:
        p[0] = DefClassNode(p[2], p[6], p[4])
    else:
        p[0] = DefClassNode(p[2], p[4])


def p_feature_list(p):
    '''feature_list : def_attr SEMICOLON feature_list
                    | def_func SEMICOLON feature_list
                    | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []


def p_def_attr(p):
    '''def_attr : assign_elem'''
    p[0] = DefAttrNode(*p[1])


def p_def_func(p):
    '''def_func : ID OPAREN param_list CPAREN COLON TYPE OBRACKET expr_list CBRACKET'''
    p[0] = DefFuncNode(p[1], p[3], p[6], p[8])


def p_param_list(p):
    '''param_list : param COMMA param_list
                  | param
                  | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_param(p):
    '''param : ID COLON TYPE'''
    p[0] = (p[1], p[3])


def p_expr_list(p):
    '''expr_list : expr expr_list
                 | expr'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_assign(p):
    '''assign : ID ASSIGN expr'''
    p[0] = AssignNode(p[1], p[3])


def p_func_call(p):
    '''func_call : expr AT TYPE DOT ID OPAREN arg_list CPAREN
                 | expr DOT ID OPAREN arg_list CPAREN
                 | ID OPAREN arg_list CPAREN'''
    if len(p) == 9:
        p[0] = FuncCallNode(p[1], p[3], p[5], p[7])
    elif len(p) == 7:
        p[0] = FuncCallNode(p[3], p[5], p[1])
    else:
        p[0] = FuncCallNode(p[1], p[3])


def p_arg_list(p):
    '''arg_list : expr COMMA arg_list
                | expr
                | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_if_expr(p):
    '''if_expr : IF expr THEN expr ELSE expr FI'''
    p[0] = IfNode(p[2], p[4], p[6])


def p_loop_expr(p):
    '''loop_expr : WHILE expr LOOP expr POOL'''
    p[0] = LoopNode(p[2], p[4])


def p_block(p):
    '''block : OBRACKET block_list CBRACKET'''
    p[0] = p[2]


def p_block_list(p):
    '''block_list : expr SEMICOLON block_list
                  | expr SEMICOLON'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_let_expr(p):
    '''let_expr : LET assign_list IN expr'''
    p[0] = LetNode(p[2], p[4])


def p_assign_list(p):
    '''assign_list : assign_elem COMMA assign_list
                   | assign_elem'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_assign_elem(p):
    '''assign_elem : ID COLON TYPE assign_oper'''
    p[0] = (p[1], p[4], p[3])


def p_assign_oper(p):
    '''assign_oper : ASSIGN expr
                    | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_case_expr(p):
    '''case_expr : CASE expr  OF case_list ESAC'''
    p[0] = CaseNode(p[2], p[4])


def p_case_list(p):
    '''case_list : case_elem SEMICOLON case_list
                 | case_elem SEMICOLON'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_case_elem(p):
    '''case_elem : ID COLON TYPE ARROW expr'''
    p[0] = CaseElemNode(p[5], p[1], p[3])


def p_init_expr(p):
    '''init_expr : NEW TYPE'''
    p[0] = InitNode(p[2])


def p_expr(p):
    '''expr : NOT expr
            | cmp
            | e'''
    if len(p) == 3:
        p[0] = LogicNegationNode(p[2])
    else:
        p[0] = p[1]


def p_cmp(p):
    '''cmp : e LOWER e
           | e GREATER e
           | e EQUAL e
           | e GREATEREQ e
           | e LOWEREQ e'''
    if p[2] == '>':
        p[0] = GreaterThanNode(p[1], p[3])
    elif p[2] == '<':
        p[0] = LessThanNode(p[1], p[3])
    elif p[2] == 'GREATEREQ':
        p[0] = GreaterEqNode(p[1], p[3])
    elif p[2] == 'LOWEREQ':
        p[0] = LessEqNode(p[1], p[3])
    elif p[2] == '=':
        p[0] = EqNode(p[1], p[3])


def p_e(p):
    '''e : e PLUS t
         | e MINUS t
         | t'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
        elif p[2] == '-':
            p[0] = MinusNode(p[1], p[3])


def p_t(p):
    '''t : t STAR f
         | t DIV f
         | f'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '*':
            p[0] = StarNode(p[1], p[3])
        elif p[2] == '/':
            p[0] = DivNode(p[1], p[3])
    pass


def p_f(p):
    '''f : NOT f
         | OPAREN expr CPAREN
         | atom
         | ISVOID f'''
    if len(p) == 4:
        p[0] = p[2]
    if len(p) == 3:
        if p[1] == '~':
            p[0] = NegationNode(p[2])
        if p[1] == 'ISVOID':
            p[0] = IsVoidNode(p[2])
    else:
        p[0] = p[1]
    pass


def p_atom(p):
    '''atom : ID
            | INT
            | BOOL
            | STRING
            | assign
            | func_call
            | if_expr
            | loop_expr
            | block
            | let_expr
            | case_expr
            | init_expr'''
    p[0] = AtomNode(p[1])


def p_error(p):
    add_parser_error(p.lineno, find_column(p.lexer.lexdata, p.lexpos), f'ERROR at or near \"{p.value[0]}\"')


parser = yacc.yacc()
