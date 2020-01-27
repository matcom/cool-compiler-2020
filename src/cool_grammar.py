import ply.yacc as yacc
from tools.tokens import tokens
from tools.ast import *
from lexer import CoolLexer

# TODO: juntar las producciones 
#? TODO: If siempre tiene else

def p_program(p):
    'program : class_list'
    p[0] = p[1]

def p_epsilon(p):
    'epsilon :'
    pass

def p_class_list(p):
    '''class_list : def_class class_list 
                  | def_class'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_def_class(p):
    '''def_class : class id ocur feature_list ccur semi 
                 | class id inherits id ocur feature_list ccur semi'''
    if len(p) == 7:
        p[0] = ClassDeclarationNode(p[2], p[4])
    else:
        p[0] = ClassDeclarationNode(p[2], p[6], p[4])

def p_feature_list(p):
    '''feature_list : epsilon
                    | def_attr semi feature_list
                    | def_func semi feature_list'''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]


def p_def_attr(p):
    '''def_attr : id colon id
                | id colon id larrow expr'''
    if len(p) == 4:
        p[0] = AttrDeclarationNode(p[1], p[3])
    else:
        p[0] = AttrDeclarationNode(p[1], p[3], p[5])

def p_def_func(p):
    'def_func : id opar param_list cpar colon id ocur expr ccur' 
    p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8])

def p_param_list(p):
    '''param_list : param
                  | param comma param_list'''   
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_param_list_empty(p):
    'param_list : epsilon'
    p[0] = []

def p_param(p):
    'param : id colon id'
    p[0] = (p[1], p[3])

def p_expr_let(p):
    'expr : let let_list in expr'
    p[0] = LetNode(p[2], p[4])

def p_expr_case(p):
    'expr : case expr of cases_list esac'        
    p[0] = CaseNode(p[2], p[4])

def p_expr_if(p):
    'expr : if expr then expr else expr fi'
    p[0] = ConditionalNode(p[2], p[4], p[6])

def p_expr_while(p):
    'expr : while expr loop expr pool'
    p[0] = WhileNode(p[2], p[4])

def p_expr_arith(p):
    'expr : arith'
    p[0] = p[1]


def p_let_list(p):
    '''let_list : let_assign
                | let_assign comma let_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_let_assign(p):
    '''let_assign : param larrow expr
                  | param'''
    if len(p) == 2:
        p[0] = VariableNode(p[1][0], p[1][1])
    else:
        p[0] = VarDeclarationNode(p[1][0], p[1][1], p[3])


def p_cases_list(p):
    '''cases_list : casep semi
                  | casep semi cases_list'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_case(p):
    'casep : id colon id rarrow expr'
    p[0] = OptionNode(p[1], p[3], p[5])


def p_arith(p):
    '''arith : id larrow expr
             | not comp
             | comp
    '''
    if len(p) == 4:
        p[0] = AssignNode(p[1], p[3])
    elif len(p) == 3:
        p[0] = NotNode(p[2])
    else:
        p[0] = p[1]

def p_comp(p):
    '''comp : comp less op
            | comp lesseq op
            | comp equal op
            | op'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '<':
        p[0] = LessNode(p[1], p[3])
    elif p[2] == '<=':
        p[0] = LessEqNode(p[1], p[3])
    elif p[2] == '=':
        p[0] = EqualNode(p[1], p[3])


def p_op(p):
    '''op : op plus term
          | op minus term
          | term'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = PlusNode(p[1], p[3])
    elif p[2] == '-':
        p[0] = MinusNode(p[1], p[3])

def p_term(p):
    '''term : term star base_call
            | term div base_call
            | isvoid base_call
            | nox base_call
            | base_call'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == 'isvoid':
        p[0] = IsVoidNode(p[2])
    elif p[1] == '~':
        p[0] = BinaryNotNode(p[2])
    elif p[2] == '*':
        p[0] = StarNode(p[1], p[3])
    elif p[2] == '/': 
        p[0] = DivNode(p[1], p[3])

def p_base_call(p):
    '''base_call : factor arroba id dot func_call
                 | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BaseCallNode(p[1], p[3], *p[5])

def p_factor1(p):
    '''factor : atom
              | opar expr cpar''' 
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_factor2(p):
    '''factor : factor dot func_call
              | func_call'''
    if len(p) == 2:
        p[0] = StaticCallNode(*p[1])
    else:
        p[0] = CallNode(p[1], *p[3])

def p_atom_num(p):
    'atom : num'
    p[0] = ConstantNumNode(p[1])
 
def p_atom_id(p):
    'atom : id'
    p[0] = VariableNode(p[1])

def p_atom_new(p):
    'atom : new id'
    p[0] = InstantiateNode(p[2])

def p_atom_block(p):
    'atom : ocur block ccur'
    p[0] = BlockNode(p[2])

def p_atom_boolean(p):
    '''atom : true
            | false'''
    p[0] = ConstantBoolNode(p[1])

def p_atom_string(p):
    'atom : string'
    p[0] = ConstantStrNode(p[1])

def p_block(p):
    '''block : expr semi
             | expr semi block'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_func_call(p):
    'func_call : id opar arg_list cpar'
    p[0] = (p[1], p[3])

def p_arg_list(p):
    '''arg_list : expr  
                | expr comma arg_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_arg_list_empty(p):
    'arg_list : epsilon'
    p[0] = []

 # Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

if __name__ == "__main__":
    parser = yacc.yacc(start='program')
    lexer = CoolLexer()

    s = '''
    class A {
        ackermann ( m : AUTO_TYPE , n : AUTO_TYPE ) : AUTO_TYPE {
            if ( m = 0 ) then n + 1 else
                if ( n = 0 ) then ackermann ( m - 1 , 1 ) else
                ackermann ( m - 1 , ackermann ( m , n - 1 ) )
                fi
            fi
        } ;
    } ;
    '''
    result = parser.parse(s, lexer.lexer, debug=True)
    print(result)