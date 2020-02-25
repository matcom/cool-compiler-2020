from ply import lex as lex


reserved = {
    'class': 'CLASS',
    'else': 'ELSE',
    'false': 'FALSE',
    'fAlse': 'FALSE',
    'faLse': 'FALSE',
    'falSe': 'FALSE',
    'falsE': 'FALSE',
    'fALse': 'FALSE',
    'fAlSe': 'FALSE',
    'fAlsE': 'FALSE',
    'faLSe': 'FALSE',
    'faLsE': 'FALSE',
    'falSE': 'FALSE',
    'fALSe': 'FALSE',
    'fALsE': 'FALSE',
    'fAlSE': 'FALSE',
    'faLSE': 'FALSE',
    'fALSE': 'FALSE',
    'fi': 'FI',
    'if': 'IF',
    'inherits': 'INHERITS',
    'in': 'IN',
    'isvoid': 'ISVOID',
    'let': 'LET',
    'loop': 'LOOP',
    'pool': 'POOL',
    'then': 'THEN',
    'while': 'WHILE',
    'case': 'CASE',
    'esac': 'ESAC',
    'new': 'NEW',
    'of': 'OF',
    'not': 'NOT',
    'true': 'TRUE',
    'tRue': 'TRUE',
    'trUe': 'TRUE',
    'truE': 'TRUE',
    'tRUe': 'TRUE',
    'tRuE': 'TRUE',
    'trUE': 'TRUE',
    'tRUE': 'TRUE'
}

tokens = [
             'NUMBER',
             'STRING',
             'PLUS',
             'MINUS',
             'TIMES',
             'DIVIDE',
             'LPAREN',
             'RPAREN',
             'ID',
             'LBRACE',
             'RBRACE',
             'COLON',
             'SEMICOLON',
             'DECLARATION',
             'ASSIGNATION',
             'DOT',
             'LESS',
             'LESSEQUAL',
             'GREATER',
             'GREATEREQUAL',
             'EQUAL',
             'COMPLEMENT',
         ] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r','
t_SEMICOLON = r';'
t_DECLARATION = r':'
t_ASSIGNATION = r'<-'
t_DOT = r'\.'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_GREATER = r'>'
t_EQUAL = r'='
t_COMPLEMENT = r'~'

def t_NUMBER(self, t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(self, t):
    r'"([^"\n]*\\\n)*"'
    t.value = t.value[1:len(t.value) - 1]
    return t

def t_BADSTRING(self, t):
    r'"[^\n]*'
    print("Unterminated string constant (%s, %s)" % (t.lineno, t.lexpos))
    t.lexer.skip(1)

def t_ignore_BLOCKCOMMENT(self, t):
    r'\(\*((.*)\n?)*\*\)'
    t.lexer.skip(t)

def t_BADCOMMENT(self, t):
    r'\(\*((.*)\n?)*'
    print("EOF in comment")
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'
t_ignore_LINECOMMENT = r'==(.*)'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def make_lexer(data):
    lexer = lex.lex()
    lexer.input(data)
    return lexer
