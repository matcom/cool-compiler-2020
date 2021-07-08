from ply import lex

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

def t_INLINECOMMENT(token):
    r'--.*'
    pass

def t_start_comment(token):
    r'\(\*'
    token.lexer.push_state("COMMENT")
    token.lexer.counter = 1
    token.lexer.star = False
    token.lexer.lparen = False

def t_start_string(token):
    r'"'
    token.lexer.push_state("STRING")
    token.lexer.string_backslashed = False
    token.lexer.stringbuf = ""
    token.lexer.string_containsNull = False
    token.lexer.string_nullrow = 0
    token.lexer.string_nullcol = 0

def t_PLUS(token):
    r'\+'
    token.value = '+'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_MINUS(token):
    r'-'
    token.value = '-'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_TIMES(token):
    r'\*'
    token.value = '*'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_DIVIDE(token):
    r'/'
    token.value = '/'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_LPAREN(token):
    r'\('
    token.value = '('
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_RPAREN(t):
    r'\)'
    t.value = ')'
    t.colno = find_column(t.lexer.lexdata, t)
    return t

def t_LBRACE(token):
    r'\{'
    token.value = '{'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_RBRACE(token):
    r'\}'
    token.value = '}'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_COMMA(token):
    r','
    token.value = ','
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_SEMICOLON(token):
    r';'
    token.value = ';'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_COLON(token):
    r':'
    token.value = ':'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_ASSIGNATION(token):
    r'<-'
    token.value = '<-'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_ARROW(token):
    r'=>'
    token.value = '=>'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_DOT(token):
    r'\.'
    token.value = '.'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_LESSEQUAL(token):
    r'<='
    token.value = '<='
    token.colno = find_column(token.lexer.lexdata, token)
    return token


def t_LESS(token):
    r'<'
    token.value = '<'
    token.colno = find_column(token.lexer.lexdata, token)
    return token


def t_GREATEREQUAL(token):
    r'>='
    token.value = '>='
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_GREATER(token):
    r'>'
    token.value = '>'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_EQUAL(token):
    r'='
    token.value = '='
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_COMPLEMENT(token):
    r'~'
    token.value = '~'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_DISPATCH(token):
    r'@'
    token.value = '@'
    token.colno = find_column(token.lexer.lexdata, token)
    return token

def t_NUMBER(token):
    r'\d+'
    token.value = int(token.value)
    token.colno = find_column(token.lexer.lexdata, token)
    return token


states = (
    ('STRING', 'exclusive'),
    ('COMMENT', 'exclusive'),
)


def t_STRING_newline(token):
    r'\n'
    global errors
    token.lexer.lineno += 1
    if not token.lexer.string_backslashed:
        errors.append(
            "(%s, %s) - LexicographicError: Unterminated string constant" % (token.lineno, find_column(token.lexer.lexdata, token)))
        token.lexer.pop_state()
    else:
        token.lexer.string_backslashed = False


def t_COMMENT_eof(token):
    r'\$'
    global errors
    s = token.lexer.lexdata
    lineCount = s.count('\n') + 1
    posCount = 1
    i = len(s) - 1
    while i >= 0 and s[i] != '\n':
        posCount += 1
        i -= 1
    errors.append("(%s, %s) - LexicographicError: EOF in comment" % (lineCount, find_column(token.lexer.lexdata, token) - 1))


def t_COMMENT_star(token):
    r'\*'
    if (token.lexer.lparen):
        token.lexer.lparen = False
        token.lexer.counter += 1
    else:
        token.lexer.star = True


def t_COMMENT_lparen(token):
    r'\('
    token.lexerlparen = True
    if (token.lexer.star):
        token.lexer.start = False


def t_STRING_eof(token):
    r'\$'
    global errors
    errors.append("(%s, %s) - LexicographicError: EOF in string constant" %
                  (token.lineno, find_column(token.lexer.lexdata, token) - 1))
    token.lexer.pop_state()


def t_COMMENT_rparen(token):
    r'\)'
    if token.lexer.star:
        token.lexer.star = False
        token.lexer.counter -= 1
        if token.lexer.counter == 0:
            token.lexer.pop_state()


def t_STRING_end(token):
    r'"'
    global errors
    if not token.lexer.string_backslashed:
        token.lexer.pop_state()
        if token.lexer.string_containsNull:
            errors.append("(%s, %s) - LexicographicError: String contains null character" % (
            token.lexer.string_nullrow, token.lexer.string_nullcol))
            token.lexer.skip(1)
        else:
            token.value = token.lexer.stringbuf
            token.type = "STRING"
            token.colno = find_column(token.lexer.lexdata, token)
            return token
    else:
        token.lexer.stringbuf += '"'
        token.lexer.string_backslashed = False


def t_COMMENT_anything(token):
    r'(.|\n)'
    pass


def t_STRING_anything(token):
    r'[^\n]'
    if token.lexer.string_backslashed:
        if token.value == 'b':
            token.lexer.stringbuf += '\b'
        elif token.value == 't':
            token.lexer.stringbuf += '\t'
        elif token.value == 'n':
            token.lexer.stringbuf += '\n'
        elif token.value == 'f':
            token.lexer.stringbuf += '\f'
        elif token.value == '\\':
            token.lexer.stringbuf += '\\'
        elif token.value == '0':
            t_STRING_error(token)
        else:
            token.lexer.stringbuf += token.value
        token.lexer.string_backslashed = False
    else:
        if token.value != '\\':
            token.lexer.stringbuf += token.value
        else:
            token.lexer.string_backslashed = True


t_STRING_ignore = ''


def t_STRING_error(token):
    token.lexer.string_containsNull = True
    token.lexer.string_nullrow = token.lineno
    token.lexer.string_nullcol = find_column(token.lexer.lexdata, token) - 1


t_COMMENT_ignore = ''


def t_COMMENT_error(token):
    token.lexer.counter = 0
    token.lexer.star = False
    token.lexer.lparen = False


def t_newline(token):
    r'\n+'
    token.lexer.lineno += len(token.value)


def t_ATTRIBUTEID(token):
    r'[a-z][a-zA-Z_0-9]*'
    if reserved.get(token.value.lower()) is None:
        token.type = 'ATTRIBUTEID'
    else:
        token.type = reserved.get(token.value.lower())
    token.colno = find_column(token.lexer.lexdata, token)
    return token


def t_CLASSID(token):
    r'[A-Z][a-zA-Z_0-9]*'
    if reserved.get(token.value.lower()) is None or reserved.get(token.value.lower()) == 'TRUE' or reserved.get(
            token.value.lower()) == 'FALSE':
        token.type = 'CLASSID'
    else:
        token.type = reserved.get(token.value.lower())
    token.colno = find_column(token.lexer.lexdata, token)
    return token


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(token):
    global errors
    if not (token.value[0] == '$' and token.lexpos + 1 == len(token.lexer.lexdata)):
        errors.append('(%s, %s) - LexicographicError: ERROR "%s"' % (token.lineno, find_column(token.lexer.lexdata, token), token.value[0]))
    token.lexer.skip(1)


def make_lexer(data):
    newData = ""
    global errors
    errors = []
    i = 0
    while i < len(data):
        if data[i] == '(' and i < len(data) and data[i + 1] == '*':
            counter = 0
            j = i + 2
            paster = ""
            matched = False
            while j < len(data) - 1:
                if data[j] == '(' and data[j + 1] == '*':
                    counter += 1
                    j += 1
                if data[j] == '*' and data[j + 1] == ')':
                    if counter == 0:
                        matched = True
                        break
                    else:
                        counter -= 1
                if data[j] == '\n':
                    paster += '\n'
                j += 1
            if matched:
                newData += paster
                i = j + 2
                continue
        newData += data[i]
        i += 1

    newData = newData + '$'
    lexer.input(newData)
    while True:
        tok = lexer.token()
        if not tok:
            break
    lexer.lineno = 1
    return lexer, errors


lexer = lex.lex()
