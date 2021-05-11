import ply.lex as lex
from ..errors import LexicographicError
from ..utils import find_column


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
    'NOT',
]

def check_keyword(token):
    upper = token.value.upper()
    if upper in keywords:
        token.type = upper

literals = [
    # Literals
    'PLUS',
    'MINUS',
    'STAR',
    'DIV',
    'COLON',
    'SEMICOLON',
    'OPAR',
    'CPAR',
    'OBRA',
    'CBRA',
    'ARROB',
    'DOT',
    'COMMA',
]

tokens = [
	# Identifiers
	'TYPE', 'ID',
	# Primitive data types
	'NUMBER', 'STRING', 'BOOL',
	# Special keywords
	'ACTION',
	# Operators
	'ASSIGN', 'LESS', 'LESSEQUAL', 'EQUAL', 'INT_COMPLEMENT',
    # Comments
    'COMMENT',
] + literals + keywords

class COOL_LEXER(object):
    def __init__(self):
        self.errors = []
        self.code = None
        self.lexer = None
        self.tokens = tokens
        self.states = (
            ('string', 'exclusive'),
            ('simpleComment', 'exclusive'),
            ('multiComment', 'exclusive'),
        )
        self.result = []

        # Lexer regular expressions
        self.t_PLUS = r'\+'
        self.t_MINUS = r'\-'
        self.t_STAR = r'\*'
        self.t_DIV = r'\/'
        self.t_COLON = r'\:'
        self.t_SEMICOLON = r'\;'
        self.t_OPAR = r'\('
        self.t_CPAR = r'\)'
        self.t_OBRA = r'\{'
        self.t_CBRA = r'\}'
        self.t_ARROB = r'\@'
        self.t_DOT = r'\.'
        self.t_COMMA = r'\,'
        self.t_NUMBER = r'[0-9]+'        
        # self.t_BOOL = r't[rR][uU][eE]|f[aA][lL][sS][eE]'
        self.t_ACTION = r'=>'
        self.t_ASSIGN = r'<-'
        self.t_LESS = r'<'
        self.t_LESSEQUAL = r'<='
        self.t_EQUAL = r'='
        self.t_INT_COMPLEMENT = r'~'

        self.t_ignore = ' \t'
        self.t_string_ignore = ''
        self.t_simpleComment_ignore = ''
        self.t_multiComment_ignore = ''

        self.index = 0

    # Lexer methods
    def t_TYPE(self, t):
        r'[A-Z][A-Za-z0-9_]*'
        check_keyword(t)
        return t

    def t_ID(self, t):
        r'[a-z][A-Za-z0-9_]*'
        check_keyword(t)
        if t.type == 'ID':
            upper = t.value.upper()
            if upper == 'FALSE' or upper == 'TRUE':
                t.type = 'BOOL'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        self.errors.append(LexicographicError(t.lineno, find_column(self.code, t.lexpos), f'Invalid character "{t.value[0]}".'))

    # Lexer simple comment state methods

    def t_simpleComment(self, t):
        r'--'
        t.lexer.simpleComment_first = t.lexer.lexpos
        t.lexer.begin('simpleComment')

    def t_simpleComment_end(self, t):
        r'\n'
        t.value = t.lexer.lexdata[t.lexer.simpleComment_first: t.lexer.lexpos - 1]
        t.type = 'COMMENT'
        t.lexer.lineno += 1
        t.lexer.begin('INITIAL')
        return t

    def t_simpleComment_eof(self, t):
        t.value = t.lexer.lexdata[t.lexer.simpleComment_first: t.lexer.lexpos - 1]
        t.type = 'COMMENT'
        t.lexer.begin('INITIAL')
        return t

    def t_simpleComment_error(self, t):
        t.lexer.skip(1)

    # Lexer multi comment state methods

    def t_multiComment(self, t):
        r'\(\*'
        t.lexer.multuComment_start = t.lexer.lexpos
        t.lexer.level = 1
        t.lexer.begin('multiComment')

    def t_multiComment_lbrace(self, t):
        r'\(\*'
        t.lexer.level += 1

    def t_multiComment_rbrace(self, t):
        r'\*\)'
        t.lexer.level -= 1 
        if t.lexer.level == 0:
            t.value = t.lexer.lexdata[t.lexer.multuComment_start: t.lexer.lexpos - 2]
            t.type = "COMMENT"
            t.lexer.begin('INITIAL')
            return t

    def t_multiComment_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_multiComment_error(self, t):
        t.lexer.skip(1)

    def t_multiComment_eof(self, t):
        self.errors.append(LexicographicError(t.lexer.lineno, find_column(self.code, t.lexpos), f'EOF in comment.'))

    # Lexer string state methods

    def t_string(self, t):
        r'"'
        t.lexer.string_start = t.lexpos
        t.lexer.begin('string')

    def t_string_end(self, t):
        r'"'
        if t.lexer.lexdata[t.lexer.lexpos - 2] != '\\':
            t.value = t.lexer.lexdata[t.lexer.string_start: t.lexer.lexpos]
            t.type = 'STRING'
            t.lexer.begin('INITIAL')
            return t

    def t_string_eof(self, t):
        self.errors.append(LexicographicError(t.lineno, find_column(self.code, t.lexpos), f'Unexpected EOF.'))

    def t_string_error(self, t):
        val = t.value[0]
        if val in '\b\t\0\f':
            char = '\\f' if val == '\f' else '\\b' if val == '\b' else '\\t' if val == '\t' else 'null'
            self.errors.append(LexicographicError(t.lineno, find_column(self.code, t.lexpos), f'Invalid character "{char}" in a string.'))
        elif val == '\n':
            if t.lexer.lexdata[t.lexer.lexpos - 1] != '\\':
                self.errors.append(LexicographicError(t.lineno, find_column(self.code, t.lexpos), f'Invalid character "\\n" in a string.'))
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

    def token(self):
        if self.index >= len(self.result):
            return None
        result = None
        while True:
            if self.index >= len(self.result):
                return None
            result = self.result[self.index]
            self.index += 1
            if result.type != 'COMMENT':
                break
        return result
