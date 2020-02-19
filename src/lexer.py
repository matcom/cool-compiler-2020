import ply.lex as lex

# List of token names.   This is always required
tokens = [
    'ASSIGN',
    'ARROW',
    'GREATHER',
    'GREATHEREQ',
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

literals = [';', '{', '}', '(', ')', ':', '@', '.', '>', '<', '=', '+', '-', '*', '/', '~']

tokens += list(reserved.values())

# Regular expression rules for simple tokens
t_ASSIGN = r'<-'
t_ARROW = r'=>'
t_GREATEREQ = r'>='
t_LOWEREQ = r'<='
t_STRING = r'".*"'
t_TYPE = r'[A-Z]+([a-z]|[A-Z]|[0-9]|_)*'

t_ignore = ' \t'


def t_INT(t):
    r'[1-9]+[0-9]*'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-z]+([a-z]|[A-Z]|[0-9]|_)*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_error(t):
    print(f'({t.lexer.lineno}:{find_column(t)}) LexicographicError: illegal token {t.value[0]}')
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
        print(tok)


lexer = lex.lex()
