import ply.lex as lex
import re
from .utils import Token
from .CoolUtils import *

__lexer__ = None
__text__ = None

reserved = {
    "class":               "CLASS",          
    "else":                "ELSE",       
    "fi":                  "FI",            
    "if":                  "IF",         
    "in":                  "IN",         
    "inherits":            "INHERITS",   
    "isvoid":              "ISVOID",     
    "let":                 "LET",        
    "loop":                "LOOP",       
    "pool":                "POOL",       
    "then":                "THEN",       
    "while":               "WHILE",          
    "case":                "CASE",       
    "esac":                "ESAC",       
    "new":                 "NEW",            
    "of":                  "OF",         
    "not":                 "NOT",            
    "true":                "TRUE",
    "false":               "FALSE",        
}


tokens = [
    'NUMBER',
    'TYPEIDENTIFIER',
    'OBJECTIDENTIFIER',
    'EQUALS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'STRING',
    'LESS',
    'LESSEQ',
    'LCBRA',
    'RCBRA',
    'COLON',
    'SEMICOLON',
    
] + list(reserved.values())

t_EQUALS    = r'=' 
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LESS      = r'<'
t_LESSEQ    = r'<='
t_LCBRA      = r'{'
t_RCBRA      = r'}'
t_COLON     = r':'
t_SEMICOLON = r';'
t_ignore = ' \t\f\r\t\v'



def t_TYPEIDENTIFIER(t):
    r'[A-Z][a-zA-Z0-9|_]*'
    l_value = t.value.lower()
    if l_value == "false" or l_value == "true":
        if t.value[0] != "f" and t.value[0] != 't':
            return t
    t.type = reserved.get(l_value, "TYPEIDENTIFIER")
    return t

def t_OBJECTIDENTIFIER(t):
    r'[a-z][a-zA-Z0-9|_]*'
    l_value = t.value.lower()
    if l_value == "false" or l_value == "true":
        if t.value[0] != "f" and t.value[0] != 't':
            return t
    t.type = reserved.get(l_value, "OBJECTIDENTIFIER")
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_LINECOMMENT(t):
    r'--.*\n'
def t_COMMENT(t):
    r'\*.*\*'

def t_eof(t):
    return None

def tokenize(text):
    global __text__
    global __lexer__
    __text__ = text
    if __lexer__ is None:
        __lexer__ = lex.lex()
    __lexer__.input(text)
    original_tokens = [token for token in __lexer__]
    tokens =  [ Token(token.value, tokenType[token.type]) for token in original_tokens]
    EOF = Token('$', eof)
    return tokens + [EOF]