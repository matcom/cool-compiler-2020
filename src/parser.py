import ply.yacc as yacc
from src.lexer import tokens
import src.ast as ast


def p_program(p):
    'program : class_list'
    p[0]= ast.ProgramNode(p[1])


def p_empty(p):
    'empty :'
    pass


def p_class_list(p):
    '''class_list : def_class ; class_list
                  | def_class ;'''
    try:
        p[0]=[p[1]]+p[3]
    except:
        p[0]=[p[1]]


def p_def_class(p):
    '''dedf_class : CLASS TYPE { feature_list }
                  | CLASS TYPE INHERITS TYPE { feature_list }'''
    try:
        p[0]=ast.DefClassNode(p[2], p[6], p[4])
    except:
        p[0]=ast.DefClassNode(p[2], p[4])
        

def p_feature_list(p):
    '''feature_list : def_attr ; feature_list
                    | def_function ; feature_list
                    | empty'''
    try:
        p[0]=[p[1]]+p[3]
    except:
        p[0]=[]


def p_def_attr(p):
    '''def_attr : assign_elem'''
    p[0]=ast.DefAttrNode(p[1])


def p_def_func(p):
    '''def_func : ID ( param_list ) : TYPE { expr_list }'''
    p[0]=ast.DefFuncNode(p[1], p[3], p[6], p[8])


def p_param_list(p):
    '''param_list : param , param_list
                  | param
                  | empty'''
    #:( aqui no se como manejar la diferencia entre las ultimas dos producciones#


def p_param(p):
    '''param : ID : TYPE'''
    p[0]=(p[1], p[3])


def p_expr_list(p):
    '''expr_list : expr expr_list
                 | expr'''
    try:
        p[0]=[p[1]]+p[2]
    except:
        p[0]=[p[1]]


def p_assign(p):
    '''assign : ID <- expr'''
    p[0]=ast.AssignNode(p[1], p[3])


def p_func_call(p):
    '''func_call : expr @  TYPE . ID ( arg_list )
                 | expr . ID ( arg_list )
                 | ID ( arg_list )'''                
    try:
        p[0]=ast.FuncCallNode(p[1], p[3], p[5], p[7])
    except:
        try:
            p[0]=ast.FuncCallNode(p[1], null, p[3], p[5])
        except:
            p[0]=ast.FuncCallNode(null, null, p[1], p[3])
        


def p_arg_list(p):
    '''arg_list : expr , arg_list
                | expr
                | empty'''
    #aqui me pasa lo mismo que con el de arriba#
    pass


def p_if_expr(p):
    '''if_expr : IF expr THEN expr ELSE expr FI'''
    p[0]=ast.IfNode(p[2], p[4], p[6])


def p_loop_expr(p):
    '''loop_expr : WHILE expr LOOP expr POOL'''
    p[0]=ast.LoopNode(p[2], p[4])


def p_block(p):
    '''block : { block_list }'''
    p[0]=p[2]


def p_block_list(p):
    '''block_list : expr ; block_list
                  | expr ;'''
    try:
        p[0]=[p[1]]+p[3]
    except:
        p[0]=[p[1]]


def p_let_expr(p):
    '''let_expr : LET assign_list IN expr'''
    p[0]=ast.LetNode(p[2], p[4])


def p_assign_list(p):
    '''assign_list : assign_elem , assign_list
                   | assign_elem'''
    try:
        p[0]=[p[1]]+p[3]
    except:
        p[0]=[p[1]]


def p_assign_elem(p):
    '''assign_elem : ID : TYPE assign_oper'''
    p[0]=(p[1], p[4], p[3])


def p_assign_oper(p):
    '''assign_oper : <- expr
                    | empty'''
    try:
        p[0]=p[2]
    except:
        p[0]=null


def p_case_expr(p):
    '''case_expr : CASE expr  OF case_list ESAC'''
    p[0]=ast.CaseNode(p[2], p[4])


def p_case_list(p):
    '''case_list : case_elem ; case_list
                 | case_elem ;'''
    try:
        p[0]=[p[1]]+p[3]
    except:
        p[0]=[p[1]]


def p_case_elem(p):
    '''case_elem : ID : TYPE => expr'''
    p[0]=ast.CaseElemNode(p[5], p[1], p[3])


def p_init_expr(p):
    '''init_expr : NEW TYPE'''
    p[0]=ast.InitNode(p[2])


def p_expr(p):
    '''expr : NOT expr
            | cmp
            | e'''
    #no se separar#


def p_cmp(p):
    '''cmp : e > e
           | e < e
           | e = e
           | e >= e
           | e <= e'''
    #no se separar#
    pass


def p_e(p):
    '''e : e + t
         | e - t
         | t'''
    #no se separar#
    pass


def p_t(p):
    '''t : t * f
         | t / f
         | f'''
    #no se separar#
    pass


def p_f(p):
    '''f : ~ f
         | ( expr )
         | atom
         | ISVOID f'''
    #no se separar#
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
    #no se separar en la vida#
    pass
