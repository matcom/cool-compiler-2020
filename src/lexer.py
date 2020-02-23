import ply.lex as lex
from utils import *
from errors import add_lexer_error

states = (
    ('commentLine', 'exclusive'),
    ('commentText', 'exclusive'),
    ('string', 'exclusive'),
)

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',
    'let': 'LET',
    'in': 'IN',
    'case': 'CASE',
    'isvoid': 'ISVOID',
    'esac': 'ESAC',
    'new': 'NEW',
    'of': 'OF',
    'not': 'LNOT'
}

tokens = [
    'ASSIGN',
    'ARROW',
    'GREATEREQ',
    'LOWEREQ',
    'INT',
    'STRING',
    'TYPE',
    'ID',
    'SEMICOLON',
    'OBRACKET',
    'CBRACKET',
    'OPAREN',
    'CPAREN',
    'COLON',
    'AT',
    'DOT',
    'LOWER',
    'GREATER',
    'EQUAL',
    'PLUS',
    'MINUS',
    'STAR',
    'DIV',
    'NOT',
    'COMMA',
    'BOOL'
]

t_SEMICOLON = r';'
t_OBRACKET = r'{'
t_CBRACKET = r'}'
t_OPAREN = r'\('
t_CPAREN = r'\)'
t_COLON = r':'
t_AT = r'@'
t_DOT = r'\.'
t_LOWER = r'<'
t_GREATER = r'>'
t_EQUAL = r'='
t_GREATEREQ = r'>='
t_LOWEREQ = r'<='
t_ASSIGN = r'<-'
t_ARROW = r'=>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_DIV = r'/'
t_NOT = r'~'
t_COMMA = r','
t_TYPE = r'[A-Z]+([a-z]|[A-Z]|[0-9]|_)*'


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_BOOL(t):
    r'f[Aa][Ll][Ss][Ee]|t[Rr][Uu][Ee]'
    t.value = (t.value.lower == 'true')
    return t


def t_LINECOMMENT(t):
    r'--'
    t.lexer.begin('commentLine')



def t_TEXTCOMMENT(t):
    r'\(\*'
    t.lexer.comment_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.begin('commentText')


def t_STRING(t):
    r'"'
    t.lexer.string_start = t.lexer.lexpos
    t.lexer.begin('string')


tokens += list(reserved.values())

t_ignore = ' \t'

t_commentLine_ignore = ' \t'


def t_commentLine_error(t):
    t.lexer.skip(1)


def t_commentLine_newline(t):
    r'\n+'
    t.lexer.begin('INITIAL')
    t.lexer.lineno += len(t.value)


t_commentText_ignore = ' \t'


def t_commentText_error(t):
    t.lexer.skip(1)


def t_commentText_OPENTEXT(t):
    r'\(\*'
    t.lexer.level += 1


def t_commentText_CLOSETEXT(t):
    r'\*\)'
    t.lexer.level -= 1
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')


def t_commentText_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_commentText_eof(t):
    add_lexer_error(t.lexer.lineno, find_column(t.lexer.lexdata, t.lexer.lexpos), "EOF in comment")


t_string_ignore = ''


def t_string_CLOSESTRING(t):
    r'"'
    t.value = t.lexer.lexdata[t.lexer.string_start:t.lexer.lexpos - 1]
    t.type = 'STRING'
    t.lexer.begin('INITIAL')
    return t


def t_string_newline(t):
    r'\\\n'
    t.lexer.lineno += 1


def t_string_body(t):
    r'([^\n\"\\]|\\.)+'
    if t.value.rfind('\0') != -1:
        add_lexer_error(t.lineno, find_column(t.lexer.lexdata, t.lexpos), "String contains null character")


def t_string_error(t):
    if t.value[0] == '\n':
        add_lexer_error(t.lineno, find_column(t.lexer.lexdata, t.lexpos), "Unterminated string constant")
        t.lexer.lineno += 1
        t.lexer.skip(1)
        t.lexer.begin('INITIAL')


def t_string_eof(t):
    add_lexer_error(t.lineno, find_column(t.lexer.lexdata, t.lexpos), "EOF in string constant")


def t_error(t):
    add_lexer_error(t.lineno, find_column(t.lexer.lexdata, t.lexpos), f'ERROR \"{t.value[0]}\"')
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def test(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        # print(f'#{tok.lineno} {tok.type} {tok.value}')


lexer = lex.lex()
