from ply.lex import TOKEN
my_bool = False

tokens = [
# Identifiers
'ID', 'TYPE',

# Primitive Types
'INTEGER', 'STRING', 'TRUE', 'FALSE',

# Literals
'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'TDOTS', 'COMMA', 'DOT', 'SEMICOLON', 'AT',

# Operators
'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQ', 'LT', 'LTEQ', 'ASSIGN', 'INT_COMP',

# Special Operators
'ARROW',

# reserved_keywords
'CASE', 'CLASS', 'ELSE', 'ESAC', 'FI', 'IF', 'IN', 'INHERITS', 'ISVOID', "LET",
"LOOP", "NEW", "OF", "POOL", "THEN", "WHILE", "NOT"

]

reserved_keywords = {
		"case": "CASE",
		"class": "CLASS",
        "CLaSS": "CLASS",
		"eLSe": "ELSE",
        "else": "ELSE",
        "elsE": "ELSE",
        "ElsE": "ELSE",
		"esac": "ESAC",
		"fi": "FI",
        "Fi": "FI",
        "fI": "FI",
		"if": "IF",
        "If": "IF",
        "iF": "IF",
		"in": "IN",
		"inherits": "INHERITS",
        "iNHeRiTS": "INHERITS",
		"isvoid": "ISVOID",
		"let": "LET",
		"loop": "LOOP",
		"new": "NEW",
		"of": "OF",
		"pool": "POOL",
		"then": "THEN",
        "THeN": "THEN",
        "tHen": "THEN",
		"while": "WHILE",
		"not": "NOT",
        "true":"TRUE",
        "false":"FALSE"
	}

reserved = reserved_keywords.keys()  # ply reserved keywords map


# Simple tokens
t_LPAREN = r'\('        # (
t_RPAREN = r'\)'        # )
t_LBRACE = r'\{'        # {
t_RBRACE = r'\}'        # }
t_TDOTS = r'\:'         # :
t_COMMA = r'\,'         # ,
t_DOT = r'\.'           # .
t_SEMICOLON = r'\;'     # ;
t_AT = r'\@'            # @
t_MULTIPLY = r'\*'      # *
t_DIVIDE = r'\/'        # /
t_PLUS = r'\+'          # +
t_MINUS = r'\-'         # -
t_INT_COMP = r'~'       # ~
t_LT = r'\<'            # <
t_EQ = r'\='            # =
t_LTEQ = r'\<\='        # <=
t_ASSIGN = r'\<\-'      # <-
t_ARROW = r'\=\>'       # =>

t_ignore_WHITESPACES = r"[ \t]+"
#t_ignore = " \t"
#t_ID = r"[a-zA-Z_][a-zA-Z0-9_]*"

# @TOKEN(r"\d+")
# def t_NUMBER(token):
#     token.value = int(token.value)
# 	return token

def find_column(t):
    line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
    return t.lexpos - line_start + 1


@TOKEN(r"\d+")
def t_INTEGER(token):
    #r"[1-9][0-9]*"
    token.value = int(token.value)
    return token

# def t_ID(token):
#     r"[a-zA-Z_][a-zA-Z0-9_]*"
#     token.value =
#     return token

@TOKEN(r"[A-Z][a-zA-Z_0-9]*")
def t_TYPE(token):
	token.type = reserved_keywords.get(token.value, 'TYPE')
	return token

@TOKEN(r"[a-z][a-zA-Z_0-9]*")
def t_ID(token):
	token.type = reserved_keywords.get(token.value, 'ID')
	return token

# @TOKEN(r"(true|false)")
# def t_BOOLEAN(token):
# 	token.value = True if token.value == "true" else False
# 	return token

def t_NEWLINE(token):
    r"\n+"
    token.lexer.lineno += len(token.value)

# def t_null(t):
#     r"\0"
#     print(f'({t.lineno} ,{find_column(t)}) - LexicographicError: String contains null character')


# LEXER STATES
def states():
    return (
        ("STRING", "exclusive"),
        ("COMMENT", "exclusive")
    )
states = states()

###
# THE STRING STATE
@TOKEN(r"\"")
def t_start_string(token):
    token.lexer.push_state("STRING")
    token.lexer.string_backslashed = False
    token.lexer.stringbuf = ""


@TOKEN(r"\n")
def t_STRING_newline(token):
    token.lexer.lineno += 1
    if not token.lexer.string_backslashed:
        #print("String newline not escaped")
        token.lexer.skip(1)
        token.lexer.pop_state()
        print(f'({token.lineno}, {find_column(token)}) - LexicographicError: Unterminated string constant')
        my_bool = True
    else:
        token.lexer.string_backslashed = False

# @TOKEN(r"0")
# def t_STRING_null(t):
#     print('-------------------------------------------------------------------------------------')
#     if token.lexer.stringbuf == "\":
#         t.lexer.skip(1)
#         t.lexer.pop_state()
#         print(f'({t.lineno} ,{find_column(t)}) - LexicographicError: String contains null character')


@TOKEN(r"\"")
def t_STRING_end(token):
    if not token.lexer.string_backslashed:
        token.lexer.pop_state()
        token.value = token.lexer.stringbuf
        token.type = "STRING"
        return token
    else:
        token.lexer.stringbuf += '"'
        token.lexer.string_backslashed = False


@TOKEN('\0')
def t_STRING_null(t):
    print(f'({t.lexer.lineno}, {find_column(t)}) - LexicographicError: String contains null character')

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


# STRING ignored characters
t_STRING_ignore = ''

def t_STRING_eof(t):
    print(f'({t.lineno}, {find_column(t)}) - LexicographicError: EOF in string constant')
    my_bool = True

# STRING error handler
def t_STRING_error(token):
    print("Illegal character! Line: {0}, character: {1}".format(token.lineno, token.value[0]))
    token.lexer.skip(1)
    my_bool = True


###
# THE COMMENT STATE
@TOKEN(r"\(\*")
def t_start_comment(token):
    token.lexer.push_state("COMMENT")
    token.lexer.comment_count = 0


@TOKEN(r"\(\*")
def t_COMMENT_startanother(t):
    t.lexer.comment_count += 1



@TOKEN(r"\n")
def t_COMMENT_NEWLINE(t):
    t.lexer.lineno+=1


def t_COMMENT_eof(t):
    #print("(55, 46) - LexicographicError: EOF in comment")
    print(f"({t.lineno}, {find_column(t)}) - LexicographicError: EOF in comment")
    my_bool = True




@TOKEN(r"\*\)")
def t_COMMENT_end(token):
    if token.lexer.comment_count == 0:
        token.lexer.pop_state()
    else:
        token.lexer.comment_count -= 1


# COMMENT ignored characters
t_COMMENT_ignore = ''
t_ignore_COMMENT_LINE = r'\-\-[^\n]*'
t_ignore = ' \t\r\f'

# COMMENT error handler
def t_COMMENT_error(t):
    t.lexer.skip(1)


def t_error(t):
    message = f'({t.lineno}, {find_column(t)}) - LexicographicError: ERROR "'
    message += t.value[0]
    message +='"'
    print(message)
    my_bool = True
    #(4, 2) - LexicographicError: ERROR "!"
