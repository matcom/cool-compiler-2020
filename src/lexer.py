import ply.lex as lex

# List of token names.   This is always required
tokens = [
    'ASSIGN',
    'ARROW',
    'GREATEREQ',
    'LOWEREQ',
    'INT',
    'STRING',
    'TYPE',
    'ID'
]

reserved = {
    'if': 'IF',
    'fi': 'FI',
    'else': 'ELSE',
    'true': 'TRUE',
    'false': 'FALSE',
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'then': 'THEN',
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

literals = [';', '{', '}', '(', ')', ':', '@', '.', '>', '<', '=', '+', '-', '*', '/', '~', ',']

tokens += list(reserved.values())

# Regular expression rules for simple tokens
t_ASSIGN = r'<-'
t_ARROW = r'=>'
t_GREATEREQ = r'>='
t_LOWEREQ = r'<='
t_STRING = r'".*"'
t_TYPE = r'[A-Z]+([a-z]|[A-Z]|[0-9]|_)*'

t_ignore = ' \t'

states = (
    ('commentLine', 'exclusive'),
    ('commentText', 'exclusive'),
)


def t_INT(t):
    r'[0-9]+[0-9]*'
    t.value = int(t.value)
    return t


def t_LINECOMMENT(t):
    r'--'
    if t.lexpos == 0 or t.lexer.lexdata[t.lexpos - 1] == '\n':
        t.lexer.begin('commentLine')
    else:
        t_error(t)


t_commentLine_ignore = ' \t'


def t_commentLine_error(t):
    t_error(t)


def t_commentLine_ALL(t):
    r'.'
    return None


def t_commentLine_newline(t):
    r'\n+'
    t.lexer.begin('INITIAL')
    t.lexer.lineno += len(t.value)
    return None


def t_TEXTCOMMENT(t):
    r'\(\*'
    t.lexer.comment_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.begin('commentText')


t_commentText_ignore = ' \t'


def t_commentText_error(t):
    t_error(t)


def t_commentText_OPENTEXT(t):
    r'\(\*'
    t.lexer.level += 1


def t_commentText_CLOSETEXT(t):
    r'\*\)'
    t.lexer.level -= 1
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')


def t_commentText_ALL(t):
    r'.'
    return None


def t_commentText_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_commentText_eof(t):
    print(f'({t.lexer.lineno}:{find_column(t)}) LexicographicError: EOF in comment')


def t_ID(t):
    r'[a-z]+([a-z]|[A-Z]|[0-9]|_)*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_error(t):
    print(f'({t.lexer.lineno}, {find_column(t)}) - LexicographicError: ERROR \"{t.value[0]}\"')
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def find_column(token):
    line_start = lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def test(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f'#{tok.lineno} {tok.type} {tok.value}')


lexer = lex.lex()
