from ply.lex import TOKEN
my_bool = False
<<<<<<< HEAD
=======
result = ''
>>>>>>> semantic_work

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
<<<<<<< HEAD
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
=======

		"class": "CLASS",
        #"Class": "CLASS",
        #"CLaSS": "CLASS",

		#"eLSe": "ELSE",
        "else": "ELSE",
        #"elsE": "ELSE",
        #"ElsE": "ELSE",

		"esac": "ESAC",

		"fi": "FI",
        #"Fi": "FI",
        #"fI": "FI",

		"if": "IF",
        #"If": "IF",
        #"iF": "IF",

		"in": "IN",

		"inherits": "INHERITS",
        #"iNHeRiTS": "INHERITS",

>>>>>>> semantic_work
		"isvoid": "ISVOID",
		"let": "LET",
		"loop": "LOOP",
		"new": "NEW",
		"of": "OF",
		"pool": "POOL",
<<<<<<< HEAD
		"then": "THEN",
        "THeN": "THEN",
        "tHen": "THEN",
=======

		"then": "THEN",
        #"THeN": "THEN",
        #"tHen": "THEN",

>>>>>>> semantic_work
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

def find_column(t):
    line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
    return t.lexpos - line_start + 1

<<<<<<< HEAD

=======
>>>>>>> semantic_work
@TOKEN(r"\d+")
def t_INTEGER(token):
    token.value = int(token.value)
    return token

@TOKEN(r"[A-Z][a-zA-Z_0-9]*")
def t_TYPE(token):
<<<<<<< HEAD
	token.type = reserved_keywords.get(token.value, 'TYPE')
	return token

@TOKEN(r"[a-z][a-zA-Z_0-9]*")
def t_ID(token):
	token.type = reserved_keywords.get(token.value, 'ID')
	return token
=======
    tempL = str.lower(token.value)
    if reserved_keywords.keys().__contains__(tempL):
        token.value = tempL
    token.type = reserved_keywords.get(token.value, 'TYPE')
    return token

@TOKEN(r"[a-z][a-zA-Z_0-9]*")
def t_ID(token):
    tempL = str.lower(token.value)
    if reserved_keywords.keys().__contains__(tempL):
        token.value = tempL
    token.type = reserved_keywords.get(token.value, 'ID')
    return token
>>>>>>> semantic_work

def t_NEWLINE(token):
    r"\n+"
    token.lexer.lineno += len(token.value)

# LEXER STATES
def states():
    return (
        ("STRING", "exclusive"),
        ("COMMENT", "exclusive")
    )
states = states()

<<<<<<< HEAD
###
=======

>>>>>>> semantic_work
# THE STRING STATE
@TOKEN(r"\"")
def t_start_string(token):
    token.lexer.push_state("STRING")
    token.lexer.string_backslashed = False
    token.lexer.stringbuf = ""


@TOKEN(r"\n")
def t_STRING_newline(token):
    global my_bool
<<<<<<< HEAD
=======
    global result
>>>>>>> semantic_work
    token.lexer.lineno += 1
    if not token.lexer.string_backslashed:
        token.lexer.skip(1)
        token.lexer.pop_state()
<<<<<<< HEAD
        print(f'({token.lineno}, {find_column(token)}) - LexicographicError: Unterminated string constant')
=======
        #print(f'({token.lineno}, {find_column(token)}) - LexicographicError: Unterminated string constant')
        if result == '':
            result = f'({token.lineno}, {find_column(token)}) - LexicographicError: Unterminated string constant'
>>>>>>> semantic_work
        my_bool = True
    else:
        token.lexer.string_backslashed = False

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

<<<<<<< HEAD

@TOKEN('\0')
def t_STRING_null(t):
    global my_bool
    print(f'({t.lexer.lineno}, {find_column(t)}) - LexicographicError: String contains null character')
=======
@TOKEN('\0')
def t_STRING_null(t):
    global my_bool
    global result
    #print(f'({t.lexer.lineno}, {find_column(t)}) - LexicographicError: String contains null character')
    if result=='':
        result = f'({t.lexer.lineno}, {find_column(t)}) - LexicographicError: String contains null character'
>>>>>>> semantic_work
    my_bool = True

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

<<<<<<< HEAD

=======
>>>>>>> semantic_work
# STRING ignored characters
t_STRING_ignore = ''

def t_STRING_eof(t):
    global my_bool
<<<<<<< HEAD
    print(f'({t.lineno}, {find_column(t)}) - LexicographicError: EOF in string constant')
=======
    global result
    #print(f'({t.lineno}, {find_column(t)}) - LexicographicError: EOF in string constant')
    if result=='':
        result = f'({t.lineno}, {find_column(t)}) - LexicographicError: EOF in string constant'
>>>>>>> semantic_work
    my_bool = True

# STRING error handler
def t_STRING_error(token):
    global my_bool
<<<<<<< HEAD
    print("Illegal character! Line: {0}, character: {1}".format(token.lineno, token.value[0]))
=======
    global result
    if result == '':
        result = "Illegal character! Line: {0}, character: {1}".format(token.lineno, token.value[0])
    #print("Illegal character! Line: {0}, character: {1}".format(token.lineno, token.value[0]))
>>>>>>> semantic_work
    token.lexer.skip(1)
    my_bool = True


<<<<<<< HEAD
###
=======
>>>>>>> semantic_work
# THE COMMENT STATE
@TOKEN(r"\(\*")
def t_start_comment(token):
    token.lexer.push_state("COMMENT")
    token.lexer.comment_count = 0

<<<<<<< HEAD

=======
>>>>>>> semantic_work
@TOKEN(r"\(\*")
def t_COMMENT_startanother(t):
    t.lexer.comment_count += 1

<<<<<<< HEAD


=======
>>>>>>> semantic_work
@TOKEN(r"\n")
def t_COMMENT_NEWLINE(t):
    t.lexer.lineno+=1

<<<<<<< HEAD

def t_COMMENT_eof(t):
    global my_bool
    #print("(55, 46) - LexicographicError: EOF in comment")
    print(f"({t.lineno}, {find_column(t)}) - LexicographicError: EOF in comment")
    my_bool = True




=======
def t_COMMENT_eof(t):
    global my_bool
    global result
    #print(f"({t.lineno}, {find_column(t)}) - LexicographicError: EOF in comment")
    if result=='':
        result = f"({t.lineno}, {find_column(t)}) - LexicographicError: EOF in comment"
    my_bool = True

>>>>>>> semantic_work
@TOKEN(r"\*\)")
def t_COMMENT_end(token):
    if token.lexer.comment_count == 0:
        token.lexer.pop_state()
    else:
        token.lexer.comment_count -= 1

<<<<<<< HEAD

=======
>>>>>>> semantic_work
# COMMENT ignored characters
t_COMMENT_ignore = ''
t_ignore_COMMENT_LINE = r'\-\-[^\n]*'
t_ignore = ' \t\r\f'

# COMMENT error handler
def t_COMMENT_error(t):
    t.lexer.skip(1)

<<<<<<< HEAD

def t_error(t):
    global my_bool
    message = f'({t.lineno}, {find_column(t)}) - LexicographicError: ERROR "'
    message += t.value[0]
    message +='"'
    print(message)
    my_bool = True
    #(4, 2) - LexicographicError: ERROR "!"
=======
def t_error(t):
    global my_bool
    global result
    message = f'({t.lineno}, {find_column(t)}) - LexicographicError: ERROR "'
    message += t.value[0]
    message +='"'
    #print(message)
    if result =='':
        result = message
    t.lexer.skip(1)
    my_bool = True
>>>>>>> semantic_work
