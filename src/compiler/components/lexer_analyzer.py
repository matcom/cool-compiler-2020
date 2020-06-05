import ply.lex as lex
from ply.lex import Token
from ply.lex import TOKEN
from ..utils.errors import error

tokens = [
    # Identifiers
    "ID", "TYPE",

    # Primitive Types
    "INTEGER", "STRING", "BOOLEAN",

    # Literals
    "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COLON", "COMMA", "DOT", "SEMICOLON", "AT",

    # Operators
    "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQ", "LT", "LTEQ", "ASSIGN", "INT_COMP", "NOT",

    # Special Operators
    "ARROW"
]

reserved = {
    'new':'NEW',
    'of':'OF',
    'if' : 'IF',
    'let':'LET',
    'in' : 'IN',
    'fi':'FI',
    'else' : 'ELSE',
    'while':'WHILE',
    'case':'CASE',
    'then' : 'THEN',
    'esac':'ESAC',
    'pool':'POOL',
    'class':'CLASS',
    'loop':'LOOP',
    'true':'TRUE',
    'inherits':'INHERITS',
    'isvoid':'ISVOID',
    'false':'FALSE',
    "self": "SELF",
}

tokens += list(reserved.values())

#Simple rules
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQ = r'\='
t_LT = r'\<'
t_LTEQ = r'\<\='
t_ASSIGN = r'\<\-'
t_INT_COMP = r'~'
t_NOT = r'not'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r'\:'
t_COMMA = r'\,'
t_DOT = r'\.'
t_SEMICOLON = r'\;'
t_AT = r'\@'
t_ARROW = r'\=\>'
#complex rules

@TOKEN(r"(true|false)")
def t_BOOLEAN(token):
    token.value = True if token.value == "true" else False
    return token

@TOKEN(r"\d+")
def t_INTEGER(token):
    token.value = int(token.value)
    return token

@TOKEN(r"[A-Z][A-Za-z0-9_]*")
def t_TYPE(token):
    token.type = reserved.get(token.value, 'TYPE')
    return token

@TOKEN(r"[a-z][A-Za-z0-9_]*")
def t_ID(token):
    token.type = reserved.get(token.value, "ID")
    return token

# Utility definitions
@TOKEN(r'\n+')
def t_newline(t):
    global readjust_col    
    readjust_col = t.lexpos + len(t.value)
    t.lexer.lineno += len(t.value)

def t_error(token):
    global readjust_col
    errors.append(error(error_type="LexicographicError", row_and_col= (token.lineno, token.lexpos - readjust_col + 1), message='ERROR "%s"' % (token.value[:1])))
    token.lexer.skip(1)

t_ignore  = ' \t'
t_ignore_COMMENTLINE = r"\-\-[^\n]*"


#Global states
states = (
    ("STRING", "exclusive"),
    ("COMMENT", "exclusive")
)

#The string states
@TOKEN(r'\"')
def t_start_string(token):
    token.lexer.push_state("STRING")
    token.lexer.string_backslashed = False
    token.lexer.stringbuf = ""

@TOKEN(r'\n')
def t_STRING_newline(token):
    global readjust_col
    token.lexer.lineno += 1
    if not token.lexer.string_backslashed:
        errors.append(error(error_type="LexicographicError", row_and_col= (token.lineno, token.lexpos - readjust_col + 1),
                                        message= "Unterminated string constant"))
        token.lexer.pop_state()
    else:
        token.lexer.string_backslashed = False
    readjust_col = token.lexpos + len(token.value)

@TOKEN('\0')
def t_STRING_null(token):
    errors.append(error(error_type="LexicographicError", row_and_col= (token.lineno, token.lexpos - readjust_col + 1), message='Null character in string'))
    token.lexer.skip(1)

@TOKEN(r'\"')
def t_STRING_end(token):
    if not token.lexer.string_backslashed:
        token.lexer.pop_state()
        token.value = token.lexer.stringbuf
        token.type = "STRING"
        return token
    else:
        token.lexer.stringbuf += '"'
        token.lexer.string_backslashed = False

@TOKEN(r"[^\n]")
def t_STRING_anything(token):
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
        else:
            token.lexer.stringbuf += token.value
        token.lexer.string_backslashed = False
    else:
        if token.value != '\\':
            token.lexer.stringbuf += token.value
        else:
            token.lexer.string_backslashed = True

def t_STRING_error(token):
    token.lexer.skip(1)
    errors.append(error(error_type="LexicographicError",  
                row_and_col= (token.lineno, token.lexpos - readjust_col + 1),
                message= 'ERROR at or near '))

def t_STRING_eof(token):
    errors.append(error(error_type="LexicographicError", row_and_col= (token.lineno, token.lexpos - readjust_col + 1), message='EOF in string constant'))
    token.lexer.pop_state()

t_STRING_ignore = ''

# The comment state

@TOKEN(r"\(\*")
def t_start_comment(token):
    token.lexer.push_state("COMMENT")
    token.lexer.comment_count = 0

@TOKEN(r"\(\*")
def t_COMMENT_startanother(token):
    token.lexer.comment_count += 1

@TOKEN(r"\n+")
def t_COMMENT_newline(token):
    global readjust_col
    readjust_col = token.lexpos + len(token.value)
    token.lexer.lineno += len(token.value)

@TOKEN(r"\*\)")
def t_COMMENT_end(token):
    if token.lexer.comment_count == 0:
        token.lexer.pop_state()
    else:
        token.lexer.comment_count -= 1


def t_COMMENT_error(token):
    token.lexer.skip(1)
    
def t_COMMENT_eof(token):
    global readjust_col
    errors.append(error(error_type="LexicographicError", row_and_col= (token.lineno, token.lexpos - readjust_col + 1), message= "EOF in comment"))
    token.lexer.pop_state()

t_COMMENT_ignore = ''
errors = []


lexer = lex.lex()
def tokenizer(stream_input):
    global readjust_col
    readjust_col = 0
    lexer.input(stream_input)
    token_list = []
    real_col = {}
    for tok in lexer:
        real_col.update({ str(tok): tok.lexpos - readjust_col + 1 })  
        token_list.append(tok)

    return errors, token_list, real_col

