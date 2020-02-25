import ply.lex as lex

####### Tokens #######

keywords = [
    'CLASS',
    'ELSE',
    ### false case is independently treated
    'FI',
    'IF',
    'IN',
    'INHERITS',
    'ISVOID',
    'LET',
    'LOOP',
    'POOL',
    'THEN',
    'WHILE',
    'CASE',
    'ESAC',
    'NEW',
    'OF',
    'NOT'
    ### true case is independently treated
]

literals = ['+', '-', '*', '/', ':', ';', '(', ')', '{', '}', '@', '.', ',']

tokens = [
	# Identifiers
	'TYPE', 'ID',
	# Primitive data types
	'INTEGER', 'STRING', 'BOOL',
	# Special keywords
	'ACTION',
	# Operators
	'ASSIGN', 'LESS', 'LESSEQUAL', 'EQUAL', 'INT_COMPLEMENT', 'NOT',
] + list(keywords)

####### Extra Methods #######

def iskeyword(t):
    d = t.value.upper()
    if d in keywords:
        t.type = d

##### TOKEN RULES ##### 

t_ignore = ' \t\f\r\v'
t_ignore_single_comment = r'\-\-[^\n]*'

def t_BOOL(t):
    r't[rR][uU][eE]|f[aA][lL][sS][eE]'
    d = t.value.lower()
    t.value = True if d == 'true' else False
    return t

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_TYPE(t):
    r'[A-Z][A-Za-z0-9_]*'
    iskeyword(t)
    return t

def t_ID(t):
    r'[a-z][A-Za-z0-9_]*'
    iskeyword(t)
    return t

t_ASSIGN = r'<-'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_EQUAL = r'='
t_INT_COMPLEMENT = r'~'

t_ACTION = r'=>'

states = (
   ('string','exclusive'),
   ('comment','exclusive')
 )

def t_comment(t):
    r'\('
    t.lexer.comments = 1
    #t.lexer.unterminated_slash = False
    t.lexer.begin('comment')

t_comment_ignore = ''

def t_comment_opar(t):
    r'\(\*'
    t.lexer.comments += 1

def t_comment_cpar(t):
    r'\*\)'
    t.lexer.comments -=1
    if not t.lexer.comments:
        t.lexer.begin('INITIAL')
