import ply.lex as lex


def printLexicograficError(error, token):
    print(f'({token.lexer.lineno}, {find_column(token)}) - LexicographicError: {error}')


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
t_TYPE = r'[A-Z]+([a-z]|[A-Z]|[0-9]|_)*'

t_ignore = ' \t'

states = (
    ('commentLine', 'exclusive'),
    ('commentText', 'exclusive'),
    ('string', 'exclusive'),
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
    print(f'({t.lexer.lineno}, {find_column(t)}) - LexicographicError: EOF in comment')


def t_STRING(t):
    r'"'
    t.lexer.stringValue = ""
    t.lexer.escape = False
    t.lexer.begin('string')


t_string_ignore = ''


def t_string_ESCAPE(t):
    r'\\'
    if t.lexer.escape:
        t.lexer.stringValue += "\\"
    else:
        t.lexer.escape = True


def t_string_CLOSESTRING(t):
    r'"'
    if t.lexer.escape:
        t.lexer.stringValue += "\""
    else:
        t.value = t.lexer.stringValue
        t.lexer.stringValue = None
        t.type = 'STRING'
        t.lexer.begin('INITIAL')
        return t


def t_string_eof(t):
    printLexicograficError("EOF in string constant", t)


def t_string_newline(t):
    r'\n+'
    if t.lexer.escape:
        t.lexer.escape = False
    else:
        print(f'({t.lexer.lineno}, {find_column(t)}) - LexicographicError: Unterminated string constant')
        t.lexer.begin('INITIAL')
    t.lexer.lineno += len(t.value)


def t_string_ALL(t):
    r'.'
    if t.lexer.escape:
        x = {
            "b": "\b",
            "t": "\t",
            "n": "\n",
            "f": "\f"
        }
        if t.value in x.keys():
            t.lexer.stringValue += x[t.value]
        elif t.value == "0":
            print(f'({t.lexer.lineno}, {find_column(t)}) - LexicographicError: String contains null character')
            t.lexer.begin('INITIAL')
        else:
            t.lexer.stringValue += t.value
        t.lexer.escape = False
    else:
        t.lexer.stringValue += t.value


def t_string_error(t):
    t_error(t)


def t_ID(t):
    r'[a-z]+([a-z]|[A-Z]|[0-9]|_)*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_error(t):
    printLexicograficError(f'ERROR \"{t.value[0]}\"', t)
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
