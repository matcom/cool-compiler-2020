""" PLY Lexer configuration module for COOL Language """

# COOL Keywords
reserved = {
    'class' : 'CLASS',
    'inherits' : 'INHERITS',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'fi' : 'FI',
    'while': 'WHILE',
    'loop' : 'LOOP',
    'pool' : 'POOL',
    'let' : 'LET',
    'in' : 'IN',
    'case' : 'CASE',
    'of' : 'OF',
    'esac' : 'ESAC',
    'new' : 'NEW',
    'isvoid' : 'ISVOID',
    'not' : 'NOT',
}

# Tokens
tokens = [
    'INTEGER',             # int
    'STRING',              # string
    'BOOL',                # bool
    'PLUS',                # +
    'MINUS',               # -
    'STAR',                # *
    'DIVIDE',              # /
    'BITNOT',              # ~
    'LESS',                # <
    'LESSQ',               # <=
    'EQUALS',              # =
    'WITH',                # =>
    'ASSIGN',              # <-
    'LPAREN',              # (
    'RPAREN',              # )
    'LBRACE',              # {
    'RBRACE',              # }
    'SEMI',                # ;
    'COLON',               # :
    'COMMA',               # ,
    'DOT',                 # .
    'ARROBA',              # @
    # 'BTYPE',               # Types
    'ID'
] + list(reserved.values())

#Regular Expressions for Tokens

# VARS
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_DIVIDE = r'/'
t_BITNOT = r'~'
t_LESS = r'<'
t_LESSQ = r'<='
t_EQUALS = r'='
t_WITH = r'=>'
t_ASSIGN = r'<-'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_DOT = r'\.'
t_ARROBA = r'@'

# METHODS

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_BOOL(t):
    r'(true|false)'
    t.value = (t.value == 'true')
    return t

# def t_BTYPE(t):
#     r'(String|Bool|Int|Object|IO)'
#     return t

def t_ID(t):
    r'[a-zA-z_][a-zA-Z_0-9]*'
    key = t.value.lower() 
    t.type = reserved.get(key, 'ID') 
    return t


# OTHER RULES

# Comments rule
def t_COMMENT(t): # add more comments syntax
    r'--.*--'
    pass

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters
t_ignore = r'   '

#Error handling rule
def t_error(t):
    print(f"Unknown token {t.value[0]}")
    t.lexer.skip(1)