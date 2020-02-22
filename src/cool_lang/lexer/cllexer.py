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
    # Comments
    'COMMENT',
] + keywords

class COOL_LEXER(object):
    def __init__(self):
        self.errors = []
        self.code = None
        self.lexer = None
        self.tokens = tokens
        self.states = (
            ('string', 'exclusive'),
        )
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

    # Lexer string state methods

    def t_string(self, t):
        r'\"'
        t.lexer.string_start = t.lexpos
        t.lexer.begin('string')

    def t_string_end(self, t):
        r'\"'
        if t.lexer.lexdata[t.lexer.lexpos - 2] != '\\':
            t.value = t.lexer.lexdata[t.lexer.string_start: t.lexer.lexpos]
            t.type = 'STRING'
            t.lexer.begin('INITIAL')
            return t
        t.lexer.skip(1)
    
    def t_string_eof(self, t):
        self.errors.append(LexicographicError(t.lineno, find_column(self.code, t), f'Unexpected EOF.'))

    def t_string_error(self, t):
        val = t.value[0]
        if val in '\b\t\0\f':
            char = '\\f' if val == '\f' else '\\b' if val == '\b' else '\\t' if val == '\t' else 'null'
            self.errors.append(LexicographicError(t.lineno, find_column(self.code, t), f'Invalid character "{char}" in a string.'))
        elif val == '\n':
            if t.lexer.lexdata[t.lexer.lexpos - 1] != '\\':
                self.errors.append(LexicographicError(t.lineno, find_column(self.code, t), f'Invalid character "\\n" in a string.'))
            else:
                t.lexer.lineno += 1
        t.lexer.skip(1)

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
                if self.errors:
                    return False
                if not token:
                    break
            except lex.LexError:
                return False
            self.result.append(token)
        return True
