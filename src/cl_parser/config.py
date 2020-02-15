# Get the token map from the lexer
from cl_ast import *
from cl_lexer.config import tokens

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

# Class Definition Rules (TODO: Try include TYPE tokens)
def p_def_class(p):
    '''def_class : CLASS ID LBRACE feature_list RBRACE SEMI
                 | CLASS ID INHERITS ID LBRACE feature_list RBRACE SEMI'''
    if p[3] == 'inherits':
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

# Attr Definition Rules (TODO: Try include TYPE tokens)
def p_def_attr(p):
    '''def_attr : ID COLON ID
                | ID COLON ID ASSIGN expr'''
    try:
        p[0] = AttrDeclarationNode(p[1], p[3], p[5])
    except:
        p[0] = AttrDeclarationNode(p[1], p[3])

# Func Definition Rules (TODO: Try include TYPE tokens)
def p_def_func(p):
    '''def_func : ID LPAREN param_list RPAREN COLON ID LBRACE expr RBRACE'''
    p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8])

# Func Parameters List Rules (TODO: Try include TYPE tokens)
def p_param_list(p):
    '''param_list : empty
                  | param
                  | param COMMA param_list'''
    try:
        p[0] = [ p[1] ] + p[3]
    except:
        try:
            p[0] = [ p[1] ]
        except:
            p[0] = []

# Parameter Rule (TODO: Try include TYPE )
def p_param(p):
    '''param : ID COLON ID'''
    p[0] = (p[1], p[3]) # (ID, TYPE)

#    Expression Rules
#   ------------------

def p_expr(p):
    '''expr : LET let_list IN expr
            | CASE expr OF cases_list ESAC
            | IF expr THEN expr ELSE expr FI
            | WHILE expr LOOP expr POOL
            | ID ASSIGN expr
            | arith'''
    
    if p[1] == 'let':
        p[0] = LetNode(p[2], p[4])
    elif p[1] == 'case':
        p[0] = CaseNode(p[2], p[4])
    elif p[1] == 'if':
        p[0] = ConditionalNode(p[2], p[4], p[6])
    elif p[1] == 'while':
        p[0] = WhileNode(p[2], p[4])
    else:
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
    '''case : ID COLON ID WITH expr'''
    p[0] = OptionNode(p[1], p[3], p[5])

#   Arith Operations
# -------------------

precedence = (
    ('right', 'BITNOT'),
    ('right', 'ISVOID'),
    ('left', 'STAR', 'DIVIDE'),
    ('left', 'PLUS', 'MINUS'),
    ('nonassoc', 'LESS', 'LESSQ', 'EQUALS'),
    ('right', 'NOT')
)

def p_arith_binary(p): #TODO: Change switch-case :(
    '''arith : arith PLUS arith
             | arith MINUS arith
             | arith STAR arith
             | arith DIVIDE arith
             | arith LESS arith
             | arith LESSQ arith
             | arith EQUALS arith'''
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

def p_arith_unary(p):
    '''arith : BITNOT arith
             | ISVOID arith
             | NOT arith'''
    if p[1] == '~':
        p[0] = BitNotNode(p[2])
    elif p[1] == 'isvoid':
        p[0] = IsVoidNode(p[2])
    elif p[1] == 'not':
        p[0] = NotNode(p[2])

def p_arith_basecall(p): 
    '''arith : base_call'''
    p[0] = p[1]

# Function Call Rules

def p_basecall(p): # Parent Call (Review)
    '''base_call : fact ARROBA ID DOT func_call
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

def p_arglist(p):
    '''arg_list : empty
                | expr
                | expr COMMA arg_list'''
    try:
        p[0] = [ p[1] ] + p[3]
    except:
        if p[1]:
            p[0] = [ p[1] ]
        else:
            p[0] = []

# Atomic Operations

def p_factatom(p):
    '''fact : LPAREN expr RPAREN
            | atom'''
    try:
        p[0] = p[2]
    except:
        p[0] = p[1]

def p_atom_int(p):
    '''atom : INTEGER'''
    p[0] = IntegerNode(p[1])

def p_atom_id(p):
    '''atom : ID'''
    p[0] = VariableNode(p[1])

def p_atom_new(p):
    '''atom : NEW ID'''
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