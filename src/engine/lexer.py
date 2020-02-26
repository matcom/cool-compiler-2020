import ply.lex as lex
from errors import LexicographicError
from parser import CoolGrammar
from cp import Token

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
     return (token.lineno, (token.lexpos - line_start) + 1)

def lexer_error(t, message):
    t.lexer.errors.append(LexicographicError(*find_position(t.lexer.lexdata, t), message))
    

##### TOKEN RULES ##### 

t_ignore = ' \t\f\r\v'
t_ignore_single_comment = r'\-\-[^\n]*'

# count line number
def t_INITIAL_comment_newline(t):
    r'\n+'
    addline(t)

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

def t_error(t):
    lexer_error(t,f'ERROR "{t.value}"')
    t.lexer.skip(1)

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
    lexer_error(t,'EOF in comment')

def t_comment_error(t):
    print(t.value, 'error en comment')
    t.lexer.skip(1)

# string state
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
        lexer_error(t,'Unterminated string constant')
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
    lexer_error(t,'EOF in string constant')
    pass

def t_string_all(t):
    r'[^\n]'
    if t.lexer.unterminated_slash:
        spec = {'b':'\b','t':'\t','n':'\n','f':'\f'}
        if t.value == '0':
            lexer_error(t,'String contains null character')
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
        
lexer = lex.lex(debug=1)
lexer.errors = []
lexer.unterminated_slash = False

###### CoolGrammar ######

tokens_dict = dict()

tokens_dict['ACTION'] = CoolGrammar['=>']
tokens_dict['ASSIGN'] = CoolGrammar['<-']
tokens_dict['LESS'] = CoolGrammar['<']
tokens_dict['LESSEQUAL'] = CoolGrammar['<=']
tokens_dict['EQUAL'] = CoolGrammar['=']
tokens_dict['INT_COMPLEMENT'] = CoolGrammar['~']

for tok in tokens + literals:
	if tok not in tokens_dict:
		tokens_dict[tok] = CoolGrammar[tok.lower()]


###### TOKENIZER ######

def tokenizer(code):

    tokens = []
    lexer.input(code)
    while True:
        token = lexer.token()
        if token is None:
            break
        tokens.append(Token(token.value, tokens_dict[token.type], *find_position(lexer.lexdata, token)))

    tokens.append(Token('$', CoolGrammar.EOF))

    return tokens, lexer.errors
