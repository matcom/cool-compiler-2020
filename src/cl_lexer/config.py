""" PLY Lexer configuration module for COOL Language """

from utils import ERROR_FORMAT

states = (
    ('comments', 'exclusive'),
    ('str', 'exclusive')
)

#     Comments Actions and Globals
# ------------------------------------
balance = 0

def t_comments(t):
    r'\(\*'
    global balance
    balance = 1
    t.lexer.begin('comments')

def t_comments_open(t):
    r'\(\*'
    global balance
    balance += 1

def t_comments_close(t):
    r'\*\)'
    global balance
    balance -= 1

    if balance == 0:
        t.lexer.begin('INITIAL')

def t_comments_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_comments_ignore = r'  '

# Skip tokens inside comments using error method
def t_comments_error(t):
    t.lexer.skip(1)

def t_comments_eof(t):
    global balance
    if balance > 0:
        print(ERROR_FORMAT % (t.lineno, find_column(t.lexer.lexdata, t), "LexicographicError", "EOF in comment"))

#        String Matching State 
# ---------------------------------------

def t_str(t):
    r'\"'
    t.lexer.str_start = t.lexer.lexpos
    t.lexer.begin('str')

def t_str_end(t):
    r'\"'
    t.value = t.lexer.lexdata[t.lexer.str_start:t.lexer.lexpos - 1]
    t.type = 'STRING'
    t.lexer.begin('INITIAL')           
    return t

def t_str_newline(t):
    r'\\\n'
    #t.lexer.lineno += len(t.value)
    t.lexer.lineno += 1
    #pass

t_str_ignore = ''

def t_str_consume(t):
    r'([^\n\"\\]|\\.)+'
    fnil = t.value.rfind('\0')
    if  fnil != -1:
        print(ERROR_FORMAT % (t.lineno, find_column(t.lexer.lexdata, t) + fnil, "LexicographicError", "String contains null character"))

def t_str_error(t):
    if t.value[0] == '\n':
        print(ERROR_FORMAT % (t.lineno, find_column(t.lexer.lexdata, t), "LexicographicError", "Unterminated string constant"))
        t.lexer.lineno += 1
        t.lexer.skip(1)
        t.lexer.begin('INITIAL')
    else:
        print('??Error??')

def t_str_eof(t):
    print(ERROR_FORMAT % (t.lineno, find_column(t.lexer.lexdata, t), "LexicographicError", "EOF in string constant")) 

#           Initial State
# ---------------------------------------

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
    'TYPEID',
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

def t_BOOL(t):
    r'(t[Rr][Uu][Ee]|f[Aa][Ll][Ss][Ee])'
    t.value = (t.value.lower() == 'true')
    return t

def t_TYPEID(t):
    r'[A-Z][a-zA-Z_0-9]*'
    key = t.value.lower()
    t.type = reserved.get(key, 'TYPEID')
    return t

def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    key = t.value.lower() 
    t.type = reserved.get(key, 'ID') 
    return t

# OTHER RULES

# Comments rule
def t_COMMENT(t): # add more comments syntax
    r'--.*($|\n)'
    t.lexer.lineno += 1
    pass

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Special Ignore
def t_special_ign(t):
    r'(\ |\t)'
    t.lexer.skip(1)

# Ignored characters
t_ignore = '    '

#Error handling rule
def t_error(t):
    print(ERROR_FORMAT % (t.lineno, find_column(t.lexer.lexdata, t), "LexicographicError", f"ERROR {t.value[0]}"))
    t.lexer.skip(1)