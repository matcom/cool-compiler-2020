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

    try:
        p[0] = [p[1]] + p[3]
    except:
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


def p_error(p):
    if p:
        add_parser_error(p.lineno, find_column(p.lexer.lexdata, p.lexpos), f'ERROR at or near \"{p.value}\"')
    else:
        add_parser_error(0, 0, "ERROR at or near EOF")


parser = yacc.yacc()
