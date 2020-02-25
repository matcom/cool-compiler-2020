import ply.lex as lex
import re
from .utils import Token
from .CoolUtils import *

class CoolLexer:

    states = (
        ('comments', 'exclusive'),
        ('strings', 'exclusive'),
        
    )

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

    tokenType = {
        "CLASS":        classx,
        "ELSE":         elsex,
        "FI":           fi,
        "IF":           ifx,
        "IN":           inx,
        "INHERITS":     inherits,
        "ISVOID":       isvoid,
        "LET":          let,
        "LOOP":         loop,
        "POOL":         pool,    
        "THEN":         then,    
        "WHILE":        whilex,
        "CASE":         case,    
        "ESAC":         esac,    
        "NEW":          new,     
        "OF":           of,      
        "NOT":          notx,
        "OBJECTIDENTIFIER":   idx,
        "TYPEIDENTIFIER": typex,
        "LCBRA":        ocur,
        "RCBRA":        ccur,
        "LPAREN":       opar,
        "RPAREN":       cpar,
        "COLON":        colon,
        "SEMICOLON":    semi, 
        "NUMBER":       integer,    
        "eof":          eof,
        "PLUS":         plus,
        "MINUS":        minus,
        "DIVIDE":       div,
        "TIMES":        star,
        "LESS":         less,
        "LESSEQ":       leq,
        "EQUALS":       equal,
        "TRUE":         boolx,
        "FALSE":        boolx,  
        "COMPLEMENT":   compl,
        "RARROW":       rarrow,
        "LARROW":       larrow,
        "COMMA":        comma,
        "DOT":          dot,
        "AT":           at,
        "STRING":       string,
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
        'COMPLEMENT',
        'RARROW',
        'LARROW',
        'COMMA',
        'DOT',
        'AT',
        'ERROR'
        

    ] + list(reserved.values())

    t_EQUALS        = r'=' 
    t_PLUS          = r'\+'
    t_MINUS         = r'-'
    t_TIMES         = r'\*'
    t_DIVIDE        = r'/'
    t_LPAREN        = r'\('
    t_RPAREN        = r'\)'
    t_LESS          = r'<'
    t_LESSEQ        = r'<='
    t_LCBRA         = r'{'
    t_RCBRA         = r'}'
    t_COLON         = r':'
    t_SEMICOLON     = r';'
    t_COMPLEMENT    = r'~'
    t_RARROW        = r'=>'
    t_LARROW        = r'<-'
    t_COMMA         = r','
    t_DOT           = r'\.'
    t_AT            = r'@'

    t_ignore = ' \t\f\r\t\v'
    t_comments_ignore = ''

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.eof= (1,1)
        self.comment_level = 0
        self.string = ""

    def t_comments_COMMENTOUT(self, t):
        r'\*\)'
        if self.comment_level == 0:
            self.lexer.begin('INITIAL')
        else:
            self.comment_level -= 1
        
    def t_STRINGIN(self, t):
        r'"'
        self.string = ""
        t.lexer.begin('strings')
    
    def t_strings_NULL(self, t):
        r'\0'
        line = t.lexer.lineno
        column = self.compute_column(t)
        t.type = "ERROR"
        t.value = f"({line},{column}) - LexicographicError: Null caracter in string"
        return t

    
    def t_strings_newline(self, t):
        r'\\\n'
        t.lexer.lineno+=1
        self.string += '\n'

    def t_strings_invalid_new_line(self, t):
        r'\n'
        line = t.lexer.lineno
        t.lexer.lineno+=1
        column = self.compute_column(t)
        t.lexer.begin("INITIAL")
        t.type = "ERROR"
        t.value = f"({line},{column}) - LexicographicError: Unterminated string constant"
        return t
    
    

    def t_strings_escaped_special_character(self, t):
        r'\\(b|t|f)'
        self.string+= t.value
    
    def t_strings_escaped_character(self, t):
        r'\\.'
        self.string+= t.value[1]

    def t_strings_STRINGOUT(self, t):
        r'"'
        t.lexer.begin('INITIAL')
        t.type = 'STRING'
        t.value = self.string
        return t

    def t_strings_character(self, t):
        r'.'
        self.string += t.value

    def t_strings_eof(self, t):
        line = t.lexer.lineno
        column = self.compute_column(t)
        t.type = "ERROR"
        t.value = f"({line},{column}) - LexicographicError: EOF in string constant"
        t.lexer.begin("INITIAL")
        return t

    




    def t_TYPEIDENTIFIER(self, t):
        r'[A-Z][a-zA-Z0-9|_]*'
        l_value = t.value.lower()
        if l_value == "false" or l_value == "true":
            if t.value[0] != "f" and t.value[0] != 't':
                return t
        t.type = CoolLexer.reserved.get(l_value, "TYPEIDENTIFIER")
        return t

    def t_OBJECTIDENTIFIER(self,t):
        r'[a-z][a-zA-Z0-9|_]*'
        l_value = t.value.lower()
        if l_value == "false" or l_value == "true":
            if t.value[0] != "f" and t.value[0] != 't':
                return t
        t.type = CoolLexer.reserved.get(l_value, "OBJECTIDENTIFIER")
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ANY_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_LINECOMMENT(self, t):
        r'--.*'
    
    def t_COMMENTIN(self, t):
        r'\(\*'
        self.lexer.begin('comments')
    
    def t_comments_COMMENTIN(self, t):
        r'\(\*'
        self.comment_level += 1
            
    def t_eof(self, t):
        t.lexer.eof =(t.lexer.lineno, self.compute_column(t))
        return None

    def t_comments_eof(self, t):
        line = t.lexer.lineno
        column = self.compute_column(t)
        t.type = "ERROR"
        t.value = f"({line},{column}) - LexicographicError: EOF in comment"
        t.lexer.begin("INITIAL")
        return t

    def compute_column(self, token):
        line_start = self.text.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def t_error(self, t):
        line = t.lexer.lineno
        column = self.compute_column(t)
        error_text = t.value[0]
        t.lexer.skip(1)
        t.type = "ERROR"
        t.value = f"({line},{column}) - LexicographicError: \"{error_text}\""
        return t
    
    def t_comments_error(self, t):
        t.lexer.skip(1)
    
    def tokenize(self, text):
        self.text = text
        self.lexer.input(text)
        tokens = []
        original_tokens = [token for token in self.lexer]
        for token in original_tokens:
            if token.type == "ERROR":
                tokens.append(Token(token.value, "ERROR"))
            else:
                tokens.append(Token(token.value, self.tokenType[token.type]))
        EOF = Token('$', eof)
        return tokens + [EOF]