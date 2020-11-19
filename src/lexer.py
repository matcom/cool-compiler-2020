from ply import lex as lex

errors = []
reserved = {
    'class': 'CLASS',
    'else': 'ELSE',
    'false': 'FALSE',
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
             'ATTRIBUTEID',
             'CLASSID',
             'LBRACE',
             'RBRACE',
             'COMMA',
             'SEMICOLON',
             'COLON',
             'ASSIGNATION',
             'ARROW',
             'DOT',
             'LESS',
             'LESSEQUAL',
             'GREATER',
             'GREATEREQUAL',
             'EQUAL',
             'COMPLEMENT',
             'DISPATCH'
         ] + list(reserved.values())

t_ignore = ' \t\r\v\f'


def t_INLINECOMMENT(t):
    r'--.*'
    pass

def t_start_comment(t):
    r'\(\*'
    t.lexer.push_state("COMMENT")
    t.lexer.counter = 1
    t.lexer.star = False
    t.lexer.lparen = False


def t_start_string(t):
    r'"'
    t.lexer.push_state("STRING")
    t.lexer.string_backslashed = False
    t.lexer.stringbuf = ""
    t.lexer.string_containsNull = False
    t.lexer.string_nullrow = 0
    t.lexer.string_nullcol = 0


def t_PLUS(t):
    r'\+'
    t.value = '+'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_MINUS(t):
    r'-'
    t.value = '-'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_TIMES(t):
    r'\*'
    t.value = '*'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_DIVIDE(t):
    r'/'
    t.value = '/'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_LPAREN(t):
    r'\('
    t.value = '('
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_RPAREN(t):
    r'\)'
    t.value = ')'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_LBRACE(t):
    r'\{'
    t.value = '{'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_RBRACE(t):
    r'\}'
    t.value = '}'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_COMMA(t):
    r','
    t.value = ','
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_SEMICOLON(t):
    r';'
    t.value = ';'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_COLON(t):
    r':'
    t.value = ':'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_ASSIGNATION(t):
    r'<-'
    t.value = '<-'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_ARROW(t):
    r'=>'
    t.value = '=>'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_DOT(t):
    r'\.'
    t.value = '.'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_LESSEQUAL(t):
    r'<='
    t.value = '<='
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_LESS(t):
    r'<'
    t.value = '<'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_GREATEREQUAL(t):
    r'>='
    t.value = '>='
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_GREATER(t):
    r'>'
    t.value = '>'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_EQUAL(t):
    r'='
    t.value = '='
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_COMPLEMENT(t):
    r'~'
    t.value = '~'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_DISPATCH(t):
    r'@'
    t.value = '@'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    t.colno = find_column(t.lexer.lexdata, t)
    return t


states = (
    ('STRING', 'exclusive'),
    ('COMMENT', 'exclusive'),
)


def t_STRING_newline(t):
    r'\n'
    global errors
    t.lexer.lineno += 1
    if not t.lexer.string_backslashed:
        errors.append(
            "(%s, %s) - LexicographicError: Unterminated string constant" % (t.lineno, find_column(t.lexer.lexdata, t)))
        t.lexer.pop_state()
    else:
        t.lexer.string_backslashed = False


def t_COMMENT_eof(t):
    r'\$'
    global errors
    s = t.lexer.lexdata
    lineCount = s.count('\n') + 1
    posCount = 1
    i = len(s) - 1
    while i >= 0 and s[i] != '\n':
        posCount += 1
        i -= 1
    errors.append("(%s, %s) - LexicographicError: EOF in comment" % (lineCount, find_column(t.lexer.lexdata, t) - 1))


def t_COMMENT_star(t):
    r'\*'
    if (t.lexer.lparen):
        t.lexer.lparen = False
        t.lexer.counter += 1
    else:
        t.lexer.star = True


def t_COMMENT_lparen(t):
    r'\('
    t.lexerlparen = True
    if (t.lexer.star):
        t.lexer.start = False


def t_STRING_eof(t):
    r'\$'
    global errors
    errors.append("(%s, %s) - LexicographicError: EOF in string constant" %
                  (t.lineno, find_column(t.lexer.lexdata, t) - 1))
    t.lexer.pop_state()


def t_COMMENT_rparen(t):
    r'\)'
    if t.lexer.star:
        t.lexer.star = False
        t.lexer.counter -= 1
        if t.lexer.counter == 0:
            t.lexer.pop_state()


def t_STRING_end(t):
    r'"'
    global errors
    if not t.lexer.string_backslashed:
        t.lexer.pop_state()
        if t.lexer.string_containsNull:
            errors.append("(%s, %s) - LexicographicError: String contains null character" % (
            t.lexer.string_nullrow, t.lexer.string_nullcol))
            t.lexer.skip(1)
        else:
            t.value = t.lexer.stringbuf
            t.type = "STRING"
            t.colno = find_column(t.lexer.lexdata, t)
            return t
    else:
        t.lexer.stringbuf += '"'
        t.lexer.string_backslashed = False


def t_COMMENT_anything(t):
    r'(.|\n)'
    pass


def t_STRING_anything(t):
    r'[^\n]'
    if t.lexer.string_backslashed:
        if t.value == 'b':
            t.lexer.stringbuf += '\b'
        elif t.value == 't':
            t.lexer.stringbuf += '\t'
        elif t.value == 'n':
            t.lexer.stringbuf += '\n'
        elif t.value == 'f':
            t.lexer.stringbuf += '\f'
        elif t.value == '\\':
            t.lexer.stringbuf += '\\'
        elif t.value == '0':
            t_STRING_error(t)
        else:
            t.lexer.stringbuf += t.value
        t.lexer.string_backslashed = False
    else:
        if t.value != '\\':
            t.lexer.stringbuf += t.value
        else:
            t.lexer.string_backslashed = True


t_STRING_ignore = ''


def t_STRING_error(t):
    t.lexer.string_containsNull = True
    t.lexer.string_nullrow = t.lineno + 1
    t.lexer.string_nullcol = find_column(t.lexer.lexdata, t) - 1


t_COMMENT_ignore = ''


def t_COMMENT_error(t):
    t.lexer.counter = 0
    t.lexer.star = False
    t.lexer.lparen = False

def t_COMMENT_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ATTRIBUTEID(t):
    r'[a-z][a-zA-Z_0-9]*'
    if reserved.get(t.value.lower()) is None:
        t.type = 'ATTRIBUTEID'
    else:
        t.type = reserved.get(t.value.lower())
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_CLASSID(t):
    r'[A-Z][a-zA-Z_0-9]*'
    if reserved.get(t.value.lower()) is None or reserved.get(t.value.lower()) == 'TRUE' or reserved.get(
            t.value.lower()) == 'FALSE':
        t.type = 'CLASSID'
    else:
        t.type = reserved.get(t.value.lower())
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    global errors
    if not (t.value[0] == '$' and t.lexpos + 1 == len(t.lexer.lexdata)):
        errors.append('(%s, %s) - LexicographicError: ERROR "%s"' % (t.lineno, find_column(t.lexer.lexdata, t), t.value[0]))
    t.lexer.skip(1)


def make_lexer(data):
    global errors
    errors = []

    data = data + '$'
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
    lexer.lineno = 1
    return lexer, errors


lexer = lex.lex()
