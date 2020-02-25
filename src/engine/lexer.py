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

def addline(t):
    t.lexer.lineno += len(t.value)

def find_position(input, token):
     line_start = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - line_start) + 1, token.lineno

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
    r'\(\*'
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

def t_comment_eof(t):
    #error eof in comment
    pass

def t_comment_error(t):
    print(t.values, 'error en comment')
    t.lexer.skip(1)

# count line number
def t_INITIAL_comment_newline(t):
    r'\n+'
    addline(t)

def t_string(t):
    r'\"'
    t.lexer.begin('string')
    t.lexer.string = ''

t_string_ignore = ''

def t_string_end(t):
    r'\"'
    if not t.lexer.unterminated_slash:
        t.value = t.lexer.string
        t.type = 'STRING'
        t.lexer.begin('INITIAL')
        return t
    else:
        t.lexer.string += '"'
        t.lexer.unterminated_slash = False

def t_string_newline(t):
    r'\n'
    t.lexer.lineno += 1
    if not t.lexer.unterminated_slash:
        # error non-escaped newline may not appear in a string
        pass
    else:
        t.lexer.string += '\n'

def t_string_slash(t):
    r'\\'
    if t.lexer.unterminated_slash:
        t.lexer.string += '\\'
        t.lexer.unterminated_slash = False
    else:
        t.lexer.unterminated_slash = True

def t_string_eof(t):
    # eof in string
    pass

def t_string_all(t):
    r'[^\n]'
    if t.lexer.unterminated_slash:
        spec = {'b':'\b','t':'\t','n':'\n','f':'\f'}
        if t.value == '0':
            #null character in string
            t.lexer.unterminated_slash = False
            pass
        elif t.value in ['b','t','n','f']:
            t.string += spec[t.value]
            if t.value == 'n':
                t.lineno+=1
            t.lexer.unterminated_slash = False
        else:
            t.string += t.value
    else:
        t.lexer.string += t.value
        