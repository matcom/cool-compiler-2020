import ply.yacc as yacc

from errors import add_parser_error
from .ast import *
from .lexer import *

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'DOT'),
    ('left', 'AT'),
    ('left', 'NOT'),
    ('left', 'ISVOID'),
    ('left', 'LOWEREQ', 'LOWER', 'EQUAL'),
    ('left', 'STAR', 'DIV'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'LNOT'),
)


def p_program(p):
    'program : class_list'
    p[0] = ProgramNode(p[1])


def p_empty(p):
    'empty :'
    pass


def p_class_list(p):
    '''class_list : def_class SEMICOLON class_list
                  | def_class SEMICOLON'''

    try:
        p[0] = [p[1]] + p[3]
    except IndexError:
        p[0] = [p[1]]


def p_def_class(p):
    '''def_class : CLASS TYPE OBRACKET feature_list CBRACKET
                  | CLASS TYPE INHERITS TYPE OBRACKET feature_list CBRACKET'''
    if len(p) == 8:
        p[0] = DefClassNode(p[2], p[6], p[4])
    else:
        p[0] = DefClassNode(p[2], p[4])

    p[0].add_location(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)))


def p_feature_list(p):
    '''feature_list : def_attr SEMICOLON feature_list
                    | def_func SEMICOLON feature_list
                    | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []


def p_def_attr_declaration(p):
    '''def_attr : ID COLON TYPE ASSIGN expr
                | ID COLON TYPE'''
    try:
        p[0] = DefAttrNode(p[1], p[3], p[5])
    except IndexError:
        p[0] = DefAttrNode(p[1], p[3])

    p[0].add_location(p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))


def p_def_func(p):
    '''def_func : ID OPAREN params CPAREN COLON TYPE OBRACKET expr CBRACKET'''
    p[0] = DefFuncNode(p[1], p[3], p[6], p[8])
    p[0].add_location(p.lineno(6), find_column(p.lexer.lexdata, p.lexpos(6)))


def p_params_ne(p):
    '''params : param_list'''
    p[0] = p[1]


def p_params_e(p):
    '''params : empty'''
    p[0] = []


def p_param_list(p):
    '''param_list : param COMMA param_list
                  | param empty'''
    try:
        p[0] = [p[1]] + p[3]
    except IndexError:
        p[0] = [p[1]]


def p_param(p):
    # noinspection PySingleQuotedDocstring
    '''param : ID COLON TYPE'''
    p[0] = (p[1], p[3])


def p_expr_flow(p):
    '''expr : LET let_attrs IN expr
            | CASE expr OF case_list ESAC
            | IF expr THEN expr ELSE expr FI
            | WHILE expr LOOP expr POOL'''

    if p[1].lower() == 'let':
        p[0] = LetNode(p[2], p[4])
    elif p[1].lower() == 'case':
        p[0] = CaseNode(p[2], p[4])
    elif p[1].lower() == 'if':
        p[0] = IfNode(p[2], p[4], p[6])
    elif p[1].lower() == 'while':
        p[0] = WhileNode(p[2], p[4])

    p[0].add_location(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)))


def p_expr_assign(p):
    '''expr : ID ASSIGN expr'''
    p[0] = AssignNode(p[1], p[3])
    p[0].add_location(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_func_all(p):
    '''expr : expr AT TYPE DOT ID OPAREN arg_list CPAREN
            | expr DOT ID OPAREN arg_list CPAREN
            | ID OPAREN arg_list CPAREN'''
    if len(p) == 9:
        if p[7] is None:
            p[7] = []
        p[0] = FuncCallNode(p[5], p[7], p[1], p[3])
        p[0].add_location(p.lineno(5), find_column(p.lexer.lexdata, p.lexpos(5)))
    elif len(p) == 7:
        if p[5] is None:
            p[5] = []
        p[0] = FuncCallNode(p[3], p[5], p[1])
        p[0].add_location(p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))
    else:
        if p[3] is None:
            p[3] = []
        p[0] = FuncCallNode(p[1], p[3])
        p[0].add_location(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))

    p[0].lineno = p.lineno(0)


def p_expr_operators_binary(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr STAR expr
            | expr DIV expr
            | expr LOWER expr
            | expr LOWEREQ expr
            | expr EQUAL expr'''
    if p[2] == '+':
        p[0] = PlusNode(p[1], p[3])
    elif p[2] == '-':
        p[0] = MinusNode(p[1], p[3])
    elif p[2] == '*':
        p[0] = StarNode(p[1], p[3])
    elif p[2] == '/':
        p[0] = DivNode(p[1], p[3])
    elif p[2] == '<':
        p[0] = LessThanNode(p[1], p[3])
    elif p[2] == '<=':
        p[0] = LessEqNode(p[1], p[3])
    elif p[2] == '=':
        p[0] = EqNode(p[1], p[3])

    p[0].add_location(p.lineno(0), find_column(p.lexer.lexdata, p.lexpos(0)))


def p_expr_operators_unary(p):
    '''expr : NOT expr
            | ISVOID expr
            | LNOT expr'''
    if p[1] == '~':
        p[0] = NegationNode(p[2])
    elif p[1].lower() == 'isvoid':
        p[0] = IsVoidNode(p[2])
    elif p[1].lower() == 'not':
        p[0] = LogicNegationNode(p[2])

    p[0].add_location(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)))


def p_expr_group(p):
    '''expr : OPAREN expr CPAREN'''
    p[0] = p[2]


def p_expr_atom(p):
    '''expr : atom'''
    p[0] = p[1]


def p_let_attrs(p):
    '''let_attrs : def_attr COMMA let_attrs
                | def_attr'''
    try:
        p[0] = [p[1]] + p[3]
    except IndexError:
        p[0] = [p[1]]


def p_case_list(p):
    '''case_list : case_elem SEMICOLON case_list
                 | case_elem SEMICOLON'''
    try:
        p[0] = [p[1]] + p[3]
    except IndexError:
        p[0] = [p[1]]


def p_case_elem(p):
    '''case_elem : ID COLON TYPE ARROW expr'''
    p[0] = CaseElemNode(p[5], p[1], p[3])
    p[0].add_location(p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))


def p_arg_list(p):
    '''arg_list : arg_list_ne
                | empty'''
    p[0] = p[1]


def p_arg_list_ne(p):
    '''arg_list_ne : expr COMMA arg_list_ne
                   | expr '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_atom_int(p):
    '''atom : INT'''
    p[0] = IntNode(int(p[1]))
    p[0].add_location(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_atom_id(p):
    '''atom : ID'''
    p[0] = VarNode(p[1])
    p[0].add_location(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_atom_new(p):
    '''atom : NEW TYPE'''
    p[0] = NewNode(p[2])
    p[0].add_location(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)))


def p_atom_block(p):
    '''atom : block'''
    p[0] = p[1]


def p_atom_bool(p):
    '''atom :  BOOL'''
    p[0] = BoolNode(p[1])
    p[0].add_location(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_atom_atring(p):
    '''atom : STRING'''
    p[0] = StringNode(p[1])
    p[0].add_location(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_block(p):
    '''block : OBRACKET block_list CBRACKET'''
    p[0] = p[2]


def p_block_list(p):
    '''block_list : expr SEMICOLON block_list
                  | expr SEMICOLON'''
    if len(p) == 4:
        p[0] = BlockNode([p[1]] + p[3].expressions)
    else:
        p[0] = BlockNode([p[1]])


def p_error(p):
    if p:
        add_parser_error(p.lineno, find_column(p.lexer.lexdata, p.lexpos), f'ERROR at or near \'{p.value}\'')
    else:
        add_parser_error(0, 0, "ERROR at or near EOF")


parser = yacc.yacc()
