from ply import lex as lex

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
             'DISPATCH'
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
t_DISPATCH = r'@'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

states = (
    ('STRING','exclusive'),
 )

def t_start_string(t):
    r'"'
    t.lexer.push_state("STRING")
    t.lexer.string_backslashed = False
    t.lexer.stringbuf = ""
    t.lexer.string_containsNull = False
    t.lexer.string_nullrow = 0
    t.lexer.string_nullcol = 0

def t_STRING_newline(t):
    r'\n'
    t.lexer.lineno += 1
    if not t.lexer.string_backslashed:
        print("(%s, %s) - LexicographicError: Unterminated string constant" % (t.lineno, find_column(t.lexer.lexdata, t)))
        t.lexer.pop_state()
    else:
        t.lexer.string_backslashed = False

def t_STRING_eof(t):
    r'\$'
    print("(%s, %s) - LexicographicError: EOF in string constant" % (t.lineno, find_column(t.lexer.lexdata, t) - 1))
    t.lexer.pop_state()

def t_STRING_end(t):
    r'"'
    if not t.lexer.string_backslashed:
        t.lexer.pop_state()
        if t.lexer.string_containsNull:
            print("(%s, %s) - LexicographicError: String contains null character" % (t.lexer.string_nullrow, t.lexer.string_nullcol))
            t.lexer.skip(1)
        else:
            t.value = t.lexer.stringbuf
            t.type = "STRING"
            return t
    else:
        t.lexer.stringbuf += '"'
        t.lexer.string_backslashed = False

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
    t.lexer.string_nullrow = t.lineno
    t.lexer.string_nullcol = find_column(t.lexer.lexdata, t) - 1

def t_BADCOMMENT(t):
    r'\(\*(.|\n)*'
    s = t.lexer.lexdata
    lineCount = s.count('\n') + 1
    posCount = 1
    i = len(s) - 1
    while i >=0 and s[i] != '\n':
        posCount += 1
        i -= 1
    print("(%s, %s) - LexicographicError: EOF in comment" % (lineCount, posCount - 1))

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

t_ignore = ' \t'
t_ignore_INLINECOMMENT = r'--.*'
def t_error(t):
    if not(t.value[0] == '$' and t.lexpos + 1 == len(t.lexer.lexdata)):
        print('(%s, %s) - LexicographicError: ERROR "%s"' % (t.lineno, find_column(t.lexer.lexdata, t), t.value[0]))
    t.lexer.skip(1)

def make_lexer(data):
    newData = ""
    i = 0
    while i < len(data):
        if data[i] == '(' and i < len(data) and data[i + 1] == '*':
            counter = 0
            j = i + 2
            paster = ""
            matched = False
            while j < len(data) - 1:
                if data[j] == '(' and data[j + 1] == '*':
                    counter +=1
                    j += 1
                if data[j] == '*' and data[j + 1] == ')':
                    if(counter == 0):
                        matched = True
                        break
                    else:
                        counter -= 1
                if data[j] == '\n':
                    paster += '\n'
                j += 1
            if(matched):
                newData += paster
                i = j + 2
                continue
        newData += data[i]
        i += 1
    newData = newData + '$'
    lexer = lex.lex()
    lexer.input(newData)
    return lexer

lexer = lex.lex()