import ply.lex as lex
import re

from ..cmp import Token
from ..cmp.cool import grammar as G

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
        "CLASS":              G.classx,
        "ELSE":               G.elsex,
        "FI":                 G.fi,
        "IF":                 G.ifx,
        "IN":                 G.inx,
        "INHERITS":           G.inherits,
        "ISVOID":             G.isvoid,
        "LET":                G.let,
        "LOOP":               G.loop,
        "POOL":               G.pool,    
        "THEN":               G.then,    
        "WHILE":              G.whilex,
        "CASE":               G.case,    
        "ESAC":               G.esac,    
        "NEW":                G.new,     
        "OF":                 G.of,      
        "NOT":                G.notx,
        "OBJECTIDENTIFIER":   G.idx,
        "TYPEIDENTIFIER":     G.typex,
        "LCBRA":              G.ocur,
        "RCBRA":              G.ccur,
        "LPAREN":             G.opar,
        "RPAREN":             G.cpar,
        "COLON":              G.colon,
        "SEMICOLON":          G.semi, 
        "NUMBER":             G.integer,    
        "eof":                G.eof,
        "PLUS":               G.plus,
        "MINUS":              G.minus,
        "DIVIDE":             G.div,
        "TIMES":              G.star,
        "LESS":               G.less,
        "LESSEQ":             G.leq,
        "EQUALS":             G.equal,
        "TRUE":               G.boolx,
        "FALSE":              G.boolx,  
        "COMPLEMENT":         G.compl,
        "RARROW":             G.rarrow,
        "LARROW":             G.larrow,
        "COMMA":              G.comma,
        "DOT":                G.dot,
        "AT":                 G.at,
        "STRING":             G.string,
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

    t_ignore = ' \t\f\r\t\v'
    t_comments_ignore = ''

    def __init__(self):
        self.build()
        
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, errorlog=lex.NullLogger(), **kwargs)
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
        self.add_line_column(t)
        return t

    def t_strings_newline1(self, t):
        r'\\n'
        self.string += '\n'
    
    def t_strings_newline2(self, t):
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
        self.add_line_column(t)
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
        self.add_line_column(t)
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
        self.add_line_column(t)
        return t

    def t_TYPEIDENTIFIER(self, t):
        r'[A-Z][a-zA-Z0-9|_]*'
        l_value = t.value.lower()
        if l_value == "false" or l_value == "true":
            if t.value[0] != "f" and t.value[0] != 't':
                self.add_line_column(t)
                return t
        t.type = CoolLexer.reserved.get(l_value, "TYPEIDENTIFIER")
        self.add_line_column(t)
        return t

    def t_OBJECTIDENTIFIER(self,t):
        r'[a-z][a-zA-Z0-9|_]*'
        l_value = t.value.lower()
        if l_value == "false" or l_value == "true":
            if t.value[0] != "f" and t.value[0] != 't':
                self.add_line_column(t)
                return t
        t.type = CoolLexer.reserved.get(l_value, "OBJECTIDENTIFIER")
        self.add_line_column(t)
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        self.add_line_column(t)
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
        self.add_line_column(t)
        return t

    def compute_column(self, token):
        line_start = self.text.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def t_LARROW(self, t):
        r'<-'
        self.add_line_column(t)
        return t

    def t_LESSEQ(self, t):
        r'<='
        self.add_line_column(t)
        return t
        
    def t_RARROW(self, t):
        r'=>'
        self.add_line_column(t)
        return t

    def t_EQUALS(self, t):
        r'='
        self.add_line_column(t)
        return t

    def t_PLUS(self, t):
        r'\+'
        self.add_line_column(t)
        return t

    def t_MINUS(self, t):
        r'-'
        self.add_line_column(t)
        return t

    def t_TIMES(self, t):
        r'\*'
        self.add_line_column(t)
        return t

    def t_DIVIDE(self, t):
        r'/'
        self.add_line_column(t)
        return t

    def t_LPAREN(self, t):
        r'\('
        self.add_line_column(t)
        return t

    def t_RPAREN(self, t):
        r'\)'
        self.add_line_column(t)
        return t

    def t_LESS(self, t):
        r'<'
        self.add_line_column(t)
        return t
       
    def t_LCBRA(self, t):
        r'{'
        self.add_line_column(t)
        return t

    def t_RCBRA(self, t):
        r'}'
        self.add_line_column(t)
        return t

    def t_COLON(self, t):
        r':'
        self.add_line_column(t)
        return t

    def t_SEMICOLON(self, t):
        r';'
        self.add_line_column(t)
        return t

    def t_COMPLEMENT(self, t):
        r'~'
        self.add_line_column(t)
        return t

    def t_COMMA(self, t):
        r','
        self.add_line_column(t)
        return t

    def t_DOT(self, t):
        r'\.'
        self.add_line_column(t)
        return t

    def t_AT(self, t):   
        r'@' 
        self.add_line_column(t)  
        return t  

    def t_error(self, t):
        line = t.lexer.lineno
        column = self.compute_column(t)
        error_text = t.value[0]
        t.lexer.skip(1)
        t.type = "ERROR"
        t.value = f"({line},{column}) - LexicographicError: \"{error_text}\""
        self.add_line_column(t)
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
            tokens[-1].row = token.row
            tokens[-1].column = token.column
        EOF = Token('$', G.eof)
        EOF.row, EOF.column = self.lexer.eof
        return tokens + [EOF]

    def add_line_column(self, t):
        t.row = t.lexer.lineno
        t.column = self.compute_column(t)
        