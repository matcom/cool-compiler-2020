# Get the token map from the lexer
from cl_ast import *
from cl_lexer.config import tokens

from utils import ERROR_FORMAT, find_column, PARSER_ERRORS

# Set the grammar start symbol
start = 'program'

# Program Rule
def p_program(p):
    '''program : class_list'''
    p[0] = ProgramNode(p[1])

# Empty Production
def p_empty(p):
    '''empty :'''
    pass

# Classes Rules
def p_class_list(p):
    '''class_list : def_class
                  | def_class class_list'''
    try:
        p[0] = [ p[1] ] + p[2]
    except:
        p[0] = [ p[1] ]

# Class Definition Rules
def p_def_class(p):
    '''def_class : CLASS TYPEID LBRACE feature_list RBRACE SEMI
                 | CLASS TYPEID INHERITS TYPEID LBRACE feature_list RBRACE SEMI'''
    if p[3].lower() == 'inherits':
        p[0] = ClassDeclarationNode(p[2], p[6], p[4])
    else:
        p[0] = ClassDeclarationNode(p[2], p[4])

# Class Feature List Rules
def p_feature_list(p):
    '''feature_list : empty
                    | def_attr SEMI feature_list
                    | def_func SEMI feature_list'''
    try:
        p[0] = [ p[1] ] + p[3]
    except:
        p[0] = []

# Attr Definition Rules
def p_def_attr(p):
    '''def_attr : ID COLON TYPEID
                | ID COLON TYPEID ASSIGN expr'''
    try:
        p[0] = AttrDeclarationNode(p[1], p[3], p[5])
    except:
        p[0] = AttrDeclarationNode(p[1], p[3])

# Func Definition Rules
def p_def_func(p):
    '''def_func : ID LPAREN param_list RPAREN COLON TYPEID LBRACE expr RBRACE'''
    p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8])

# Func Parameters List Rules
def p_param_list_ept(p):
    '''param_list : empty'''
    p[0] = []

def p_param_list_prm(p):
    '''param_list : param_build'''
    p[0] = p[1]

def p_param_build(p):
    '''param_build : param empty
                   | param COMMA param_build'''
    try:
        p[0] = [ p[1] ] + p[3]
    except:
        p[0] = [ p[1] ]

# Parameter Rule
def p_param(p):
    '''param : ID COLON TYPEID'''
    p[0] = (p[1], p[3]) # (ID, TYPE)

#    Expression Rules
#   ------------------

def p_expr(p):
    '''expr : LET let_list IN expr
            | CASE expr OF cases_list ESAC
            | IF expr THEN expr ELSE expr FI
            | WHILE expr LOOP expr POOL'''
    
    if p[1].lower() == 'let':
        p[0] = LetNode(p[2], p[4])
    elif p[1].lower() == 'case':
        p[0] = CaseNode(p[2], p[4])
    elif p[1].lower() == 'if':
        p[0] = ConditionalNode(p[2], p[4], p[6])
    elif p[1].lower() == 'while':
        p[0] = WhileNode(p[2], p[4])
        
# Assign Production
def p_expr_assign(p):
    '''expr : ID ASSIGN expr'''
    p[0] = AssignNode(p[1], p[3])

# Precedence Production
def p_expr_arith(p):
    '''expr : arith'''
    p[0] = p[1]

# Let Rules

def p_let_list(p):
    '''let_list : let_assign
                | let_assign COMMA let_list'''
    try:
        p[0] = [ p[1] ] + p[3]
    except:
        p[0] = [ p[1] ]

def p_let_assign(p):
    '''let_assign : param ASSIGN expr
                  | param'''
    try:
        p[0] = VarDeclarationNode(p[1][0], p[1][1], p[3])
    except:
        p[0] = VarDeclarationNode(p[1][0], p[1][1])

# Case Rules

def p_cases_list(p):
    '''cases_list : case SEMI
                  | case SEMI cases_list'''
    try:
        p[0] = [ p[1] ] + p[3]
    except:
        p[0] = [ p[1] ]

def p_case(p):
    '''case : ID COLON TYPEID WITH expr'''
    p[0] = OptionNode(p[1], p[3], p[5])

#   Arith Operations
# -------------------

# Operators Precedence
precedence = (
    ('right', 'BITNOT'),
    ('right', 'ISVOID'),
    ('left', 'STAR', 'DIVIDE'),
    ('left', 'PLUS', 'MINUS'),
    ('nonassoc', 'LESS', 'LESSQ', 'EQUALS'),
    ('right', 'NOT')
)

# Binary Operations Rules

def p_expr_binary(p): #TODO: Change switch-case :(
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr STAR expr
            | expr DIVIDE expr
            | expr LESS expr
            | expr LESSQ expr
            | expr EQUALS expr'''
    if p[2] == '+':
        p[0] = SumNode(p[1], p[3])
    elif p[2] == '-':
        p[0] = DiffNode(p[1], p[3])
    elif p[2] == '*':
        p[0] = StarNode(p[1], p[3])
    elif p[2] == '/':
        p[0] = DivNode(p[1], p[3])
    elif p[2] == '<':
        p[0] = LessNode(p[1], p[3])
    elif p[2] == '<=':
        p[0] = LessEqualNode(p[1], p[3])
    elif p[2] == '=':
        p[0] = EqualNode(p[1], p[3])

# Unary Operations Rules

def p_expr_unary(p):
    '''expr : BITNOT expr
            | ISVOID expr
            | NOT expr'''
    if p[1] == '~':
        p[0] = BitNotNode(p[2])
    elif p[1].lower() == 'isvoid':
        p[0] = IsVoidNode(p[2])
    elif p[1].lower() == 'not':
        p[0] = NotNode(p[2])

def p_arith_basecall(p): 
    '''arith : base_call'''
    p[0] = p[1]

# Function Call Rules

def p_basecall(p): # Parent Call (Review)
    '''base_call : fact ARROBA TYPEID DOT func_call
                 | fact'''
    try:
        p[0] = ParentCallNode(p[1], p[3], p[5][0], p[5][1])
    except:
        p[0] = p[1]

def p_factcall(p):
    '''fact : fact DOT func_call
            | func_call'''
    try:
        p[0] = ExprCallNode(p[1], p[3][0], p[3][1])
    except:
        p[0] = SelfCallNode(p[1][0], p[1][1])

def p_func_call(p):
    '''func_call : ID LPAREN arg_list RPAREN'''
    p[0] = (p[1], p[3])

def p_arglist_ept(p):
    '''arg_list : empty'''
    p[0] = []

def p_arglist_prm(p):
    '''arg_list : arg_build'''
    p[0] = p[1]

def p_arg_build(p):
    '''arg_build : expr empty
                 | expr COMMA arg_build'''
    try:
        p[0] = [ p[1] ] + p[3]
    except:
        p[0] = [ p[1] ]

# Atomic Operations

def p_factatom(p):
    '''fact : atom'''
    p[0] = p[1]

def p_fact_group(p):
    '''fact : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_atom_int(p):
    '''atom : INTEGER'''
    p[0] = IntegerNode(p[1])

def p_atom_id(p):
    '''atom : ID'''
    p[0] = VariableNode(p[1])

def p_atom_new(p):
    '''atom : NEW TYPEID'''
    p[0] = NewNode(p[2])

def p_atom_block(p):
    '''atom : LBRACE block RBRACE'''
    p[0] = BlockNode(p[2])

def p_block(p):
    '''block : expr SEMI
             | expr SEMI block'''
    try:
        p[0] = [ p[1] ] + p[3]
    except:
        p[0] = [ p[1] ]

def p_atom_bool(p):
    '''atom : BOOL'''
    p[0] = BoolNode(p[1])

def p_atom_string(p):
    '''atom : STRING'''
    p[0] = StringNode(p[1])

def p_error(p):
    if p:
       line = p.lexer.lineno
       col = find_column(p.lexer.lexdata, p.lexpos)  
       PARSER_ERRORS.append(ERROR_FORMAT % (line, col, "SyntacticError", f"ERROR at or near {p.value}"))
    else:
       PARSER_ERRORS.append(ERROR_FORMAT % (0, 0, "SyntacticError", "ERROR at or near EOF"))