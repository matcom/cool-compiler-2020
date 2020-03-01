from ply.lex import TOKEN

tokens_collection = ( 
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
)

class keyword(str):    
    def __eq__(self, other: str):
        val = str(self)        
        if val != 'true' and val != 'false':
            return val  == other.lower()
        return val[0] == other[0] and val[1:] == other.lower()[1:]

basic_keywords = {
    "case": keyword("case"),
    "class": keyword("class"),
    "else": keyword("else"),
    "esac": keyword("esac"),
    "fi": keyword("fi"),
    "if": keyword("if"),
    "in": keyword("in"),
    "inherits": keyword("inherits"),
    "isvoid": keyword("isvoid"),
    "let": keyword("let"),
    "loop": keyword("loop"),
    "new": keyword("new"),
    "of": keyword("of"),
    "pool": keyword("pool"),
    "self": keyword("self"),
    "then": keyword("then"),
    "while": keyword("while"),
    "true": keyword("true"),
    "false": keyword("false"),
    'not' : keyword('not') 
}

#Simple rules for cool
t_LPAREN = r'\('                    # (
t_RPAREN = r'\)'                    # )   
t_LBRACE = r'\{'                    # {  
t_RBRACE = r'\}'                    # }   
t_COLON = r'\:'                     # :   
t_COMMA = r'\,'                     # ,
t_DOT = r'\.'                       # .
t_SEMICOLON = r'\;'                 # ;
t_AT = r'\@'                        # @
t_PLUS = r'\+'                      # +
t_MINUS = r'\-'                     # -
t_MULTIPLY = r'\*'                  # *
t_DIVIDE = r'\/'                    # /
t_EQ = r'\='                        # = 
t_LT = r'\<'                        # <
t_LTEQ = r'\<\='                    # <=
t_ASSIGN = r'\<\-'                  # <-          
t_INT_COMP = r'~'                   # ~
t_NOT = r'not'                      # not

#ignore spaces
t_ignore = ' \t\r\f'

simple_rules = [
    t_LPAREN,
    t_RPAREN,
    t_LBRACE,
    t_RBRACE,
    t_COLON,
    t_COMMA,
    t_DOT,
    t_SEMICOLON,
    t_AT,
    t_PLUS,
    t_MINUS,
    t_MULTIPLY,
    t_DIVIDE,
    t_EQ,
    t_LT,
    t_LTEQ,
    t_ASSIGN,
    t_INT_COMP,
    t_NOT
]


#Complex rules for cool

@TOKEN(r"(true|false)")
def t_BOOLEAN (token):
    token.value = True if token.value == basic_keywords['true'] else False
    return token

@TOKEN(r"\d+")
def t_INTEGER(token):
    token.value = int(token.value)
    return token

@TOKEN(r"[A-Z][a-zA-Z_0-9]*")
def t_TYPE(token):    
    token.type = basic_keywords.get(token.value, 'TYPE')
    return token

@TOKEN(r"\n+")
def t_newline(token):    
    token.lexer.lineno += len(token.value)


@TOKEN(r"[a-z][a-zA-Z_0-9]*")
def t_ID(token):    
    token.type = basic_keywords.get(token.value, 'ID')
    return token



#Lexer states
def states():
    return (
        ("STRING", "exclusive"),
        ("COMMENT", "exclusive")
    )

# The string states

@TOKEN(r"\"")
def t_STRING_start(token):
    token.lexer.push_state("STRING")
    token.lexer.string_backslashed = False
    token.lexer.stringbuf = ""


@TOKEN(r"\n")
def t_STRING_newline(token):
    token.lexer.lineno += 1
    if not token.lexer.string_backslashed:
        print("String newline not escaped")
        token.lexer.skip(1)
    else:
        token.lexer.string_backslashed = False


@TOKEN(r"\"")
def t_STRING_end(self, token):
    if not token.lexer.string_backslashed:
        token.lexer.pop_state()
        token.value = token.lexer.stringbuf
        token.type = "STRING"
        return token
    else:
        token.lexer.stringbuf += '"'
        token.lexer.string_backslashed = False

@TOKEN(r"[^\n]")
def t_STRING_anything(self, token):
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






# The comment states
@TOKEN(r"\(\*")
def t_COMMENT_start(self, token):
    token.lexer.push_state("COMMENT")
    token.lexer.comment_count = 0

#Comments can be recursive
@TOKEN(r"\(\*")
def t_COMMENT_startanother(self, t):
    t.lexer.comment_count += 1

@TOKEN(r"\*\)")
def t_COMMENT_end(self, token):
    if token.lexer.comment_count == 0:
        token.lexer.pop_state()
    else:
        token.lexer.comment_count -= 1

# COMMENT ignored characters
t_COMMENT_ignore = ''






#Error handlers

# STRING error handler
def t_STRING_error(self, token):
    print("Illegal character! Line: {0}, character: {1}".format(token.lineno, token.value[0]))
    token.lexer.skip(1)


# COMMENT error handler
def t_COMMENT_error(self, token):
    token.lexer.skip(1)

def t_error(self, token):
    print("Illegal character! Line: {0}, character: {1}".format(token.lineno, token.value[0]))
    token.lexer.skip(1)



#Complex rules list
complex_rules = [ 
    t_BOOLEAN,
    t_INTEGER,
    t_TYPE,
    t_newline,
    t_ID,
    #----------
    #String states rules
    t_STRING_start,
    t_STRING_newline,
    t_STRING_anything,
    t_STRING_end,
    t_STRING_ignore,
    #----------
    #Comment states rules
    t_COMMENT_start,
    t_COMMENT_startanother,
    t_COMMENT_end,
    t_COMMENT_ignore  
 ]

#Error handlers
error_handlers = [
    t_STRING_error,
    t_COMMENT_error,
    t_error
]

