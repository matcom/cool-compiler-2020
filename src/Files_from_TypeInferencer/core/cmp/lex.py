import ply.lex as lex
import re
from .utils import Token
from .CoolUtils import *


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