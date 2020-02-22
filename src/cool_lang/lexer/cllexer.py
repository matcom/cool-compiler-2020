import ply.lex as lex
from ..errors import LexicographicError

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1    

keywords = [
	'CLASS',
	'INHERITS',
	'IF',
	'THEN',
	'ELSE',
	'FI',
	'WHILE',
	'LOOP',
	'POOL',
	'LET',
	'IN',
	'CASE',
	'OF',
	'ESAC',
	'NEW',
	'ISVOID',
]

def check_keyword(token):
    upper = token.value.upper()
    if upper in keywords:
        token.type = upper

tokens = [
    # Literals
    'LIT',
	# Identifiers
	'TYPE', 'ID',
	# Primitive data types
	'NUMBER', 'STRING', 'BOOL',
	# Special keywords
	'ACTION',
	# Operators
	'ASSIGN', 'LESS', 'LESSEQUAL', 'EQUAL', 'INT_COMPLEMENT', 'NOT',
] + keywords

class COOL_LEXER(object):
    def __init__(self):
        self.errors = []
        self.code = None
        self.lexer = None
        self.tokens = tokens
        self.result = []

        # Lexer regular expressions
        self.t_LIT = r'[\+\-\*\/\:\;\(\)\{\}\@\.\,]'
        self.t_NUMBER = r'[0-9]+'        
        self.t_BOOL = r't[rR][uU][eE]|f[aA][lL][sS][eE]'
        self.t_ACTION = r'=>'
        self.t_ASSIGN = r'<-'
        self.t_LESS = r'<'
        self.t_LESSEQUAL = r'<='
        self.t_EQUAL = r'='
        self.t_INT_COMPLEMENT = r'~'
        self.t_NOT = r'[nN][oO][tT]'

        self.t_ignore = ' \t'
    
    # Lexer methods
    def t_TYPE(self, t):
        r'[A-Z][A-Za-z0-9_]*'
        check_keyword(t)
        return t

    def t_ID(self, t):
        r'[a-z][A-Za-z0-9_]*'
        check_keyword(t)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        
        self.errors.append(LexicographicError(t.lineno, find_column(self.code, t), f'Invalid character "{t.value[0]}".'))

    # Non lexer methods
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenize(self, data):
        self.code = data
        if self.lexer is None:
            self.build()
        self.lexer.input(data)
        while True:
            try:
                token = self.lexer.token()
            except lex.LexError:
                return False
            self.result.append(token)
        return True
