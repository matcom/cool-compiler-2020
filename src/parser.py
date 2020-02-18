import ply.yacc as yacc
from src.lexer import tokens


def p_program(p):
    'program : class_list'
    pass


def p_empty(p):
    'empty :'
    pass


def p_class_list(p):
    '''class_list : def_class ; class_list
                  | def_class ;'''
    pass


def p_def_class(p):
    '''dedf_class : CLASS TYPE { feature_list }
                  | CLASS TYPE INHERITS TYPE { feature_list }'''
    pass


def p_feature_list(p):
    '''feature_list : def_attr ; feature_list
                    | def_function ; feature_list
                    | empty'''


def p_def_attr(p):
    '''def_attr : assign_elem'''
    pass


def p_def_func(p):
    '''def_func : ID ( param_list ) : TYPE { expr_list }'''
    pass


def p_param_list(p):
    '''param_list : param , param_list
                  | param
                  | empty'''
    pass


def p_param(p):
    '''param : ID : TYPE'''
    pass


def p_expr_list(p):
    '''expr_list : expr expr_list
                 | expr'''
    pass


def p_assign(p):
    '''assign : ID <- expr'''
    pass


def p_func_call(p):
    '''func_call : expr @  TYPE . ID ( arg_list )
                 | expr . ID ( arg_list )
                 | ID ( arg_list )'''


def p_arg_list(p):
    '''arg_list : expr , arg_list
                | expr
                | empty'''
    pass


def p_if_expr(p):
    '''if_expr : IF expr THEN expr ELSE expr FI'''
    pass


def p_loop_expr(p):
    '''loop_expr : WHILE expr LOOP expr POOL'''
    pass


def p_block(p):
    '''block : { block_list }'''
    pass


def p_block_list(p):
    '''block_list : expr ; block_list
                  | expr ;'''
    pass


def p_let_expr(p):
    '''let_expr : LET assign_list IN expr'''
    pass


def p_assign_list(p):
    '''assign_list : assign_elem , assign_list
                   | assign_elem'''
    pass


def p_assign_elem(p):
    '''assign_elem : ID : TYPE assign_oper'''
    pass


def p_assign_oper(p):
    '''assign_oper : <- expr
                    | empty'''
    pass


def p_case_expr(p):
    '''case_expr : CASE expr  OF case_list ESAC'''
    pass


def p_case_list(p):
    '''case_list : case_elem ; case_list
                 | case_elem ;'''
    pass


def p_case_elem(p):
    '''case_elem : ID : TYPE => expr'''
    pass


def p_init_expr(p):
    '''init_expr : NEW TYPE'''
    pass


def p_expr(p):
    '''expr : NOT expr
            | cmp
            | e'''
    pass


def p_cmp(p):
    '''cmp : e > e
           | e < e
           | e = e
           | e >= e
           | e <= e'''
    pass


def p_e(p):
    '''e : e + t
         | e - t
         | t'''
    pass


def p_t(p):
    '''t : t * f
         | t / f
         | f'''
    pass


def p_f(p):
    '''f : ~ f
         | ( expr )
         | atom
         | ISVOID f'''
    pass


def p_atom(p):
    '''atom : ID
            | INT
            | TRUE
            | FALSE
            | STRING
            | assign
            | func_call
            | if_expr
            | loop_expr
            | block
            | let_expr
            | case_expr
            | init_expr
            | is_void_expr'''
    pass
