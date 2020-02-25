import ply.lex as lex
from tools.tokens import tokens, reserved, Token
from pprint import pprint 
from tools.errors import LexicographicError
from utils.utils import find_column

class CoolLexer:
    def __init__(self, **kwargs):
        # TODO: las palabras reservadas, excepto true y false son case insensitive
        self.reserved = reserved 
        self.tokens = tokens
        self.errors = []
        self.lexer = lex.lex(module=self, **kwargs)

    
    states = (
        ('comments', 'exclusive'),
        ('strings', 'exclusive')
    )

    #Comments
    def t_comments(self,t):
        r'\(\*'
        t.lexer.level = 1
        t.lexer.begin('comments')
    
    def t_comments_open(self,t):
        r'\(\*'
        t.lexer.level += 1
        
    def t_comments_close(self,t):
        r'\*\)'
        t.lexer.level -= 1

        if t.lexer.level == 0:
            t.lexer.begin('INITIAL')

    def t_comments_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_comments_ignore = '  \t\f\r\t\v'

    def t_comments_error(self,t):
        t.lexer.skip(1)

    def t_comments_eof(self,t):
        
        if t.lexer.level > 0:
            error_text = LexicographicError.EOF_COMMENT 
            line = t.lineno
            column = find_column(self.lexer, t)
            self.errors.append(LexicographicError(error_text, line, column))
    
    #Strings
    def t_strings(self,t):
        r'\"'
        t.lexer.str_start = t.lexer.lexpos
        t.lexer.myString = ''
        t.lexer.backslash = False
        t.lexer.begin('strings')

    def t_strings_end(self,t):
        r'\"'
        if t.lexer.backslash : 
            t.lexer.myString += '"'
            t.lexer.backslash = False
        else:
            t.value = t.lexer.myString 
            t.type = 'string'
            t.lexer.begin('INITIAL')           
            return t

    def t_strings_newline(self,t):
        r'\n'
        t.lexer.lineno += 1
        if not t.lexer.backslash:
            error_text = LexicographicError.UNDETERMINATED_STRING
            line = t.lineno
            column = find_column(self.lexer, t)
            self.errors.append(LexicographicError(error_text, line, column))
            t.lexer.begin('INITIAL')

    def t_strings_nill(self,t):
        r'\0'
        error_text = LexicographicError.NULL_STRING
        line = t.lineno
        column = find_column(self.lexer, t)
        self.errors.append(LexicographicError(error_text, line, column))

    def t_strings_consume(self,t):
        r'[^\n]'

        if t.lexer.backslash :
            if t.value == 'b':
                t.lexer.myString += '\b'
            
            elif t.value == 't':
                t.lexer.myString += '\t'

            
            elif t.value == 'f':
                t.lexer.myString += '\f'

            
            elif t.value == 'n':
                t.lexer.myString += '\n'
            
            elif t.value == '\\':
                t.lexer.myString += '\\'
            else:
                t.lexer.myString += t.value
            t.lexer.backslash = False
        else:
            if t.value != '\\':
                t.lexer.myString += t.value
            else:
                t.lexer.backslash = True 

    def t_strings_error(self,t):
        pass

    t_strings_ignore = ''

    def t_strings_eof(self,t):
        error_text = LexicographicError.EOF_STRING
        line = t.lineno
        column = find_column(self.lexer, t) 
        self.errors.append(LexicographicError(error_text, line, column))


    # Regular expressions for simple tokens
    # t_ignore_COMMENT = r'--.* | \*(.)*\*'
    # A string containing ignored characters 
    t_ignore = '  \t\f\r\t\v'
    
    t_semi = r';'
    t_colon = r':'
    t_comma = r','
    t_dot = r'\.'
    t_opar = r'\('
    t_cpar = r'\)'
    t_ocur = r'\{'
    t_ccur = r'\}'
    t_larrow = r'<-'
    t_arroba = r'@'
    t_rarrow = r'=>'
    t_nox = r'~'
    t_equal = r'='
    t_plus = r'\+'
    t_of = r'of'
    t_minus = r'-'
    t_star = r'\*'
    t_div = r'/'
    t_less = r'<'
    t_lesseq = r'<='
    t_inherits = r'inherits'

    def t_type(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'type')
        return t

    # Check for reserved words:
    def t_id(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'id')
        return t


    # Get Numbers
    def t_num(self, t):
        r'\d+(\.\d+)? '
        t.value = float(t.value)
        return t

    def t_comment(self, t):
        r'--.*($|\n)'
        t.lexer.lineno += 1
        pass

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        error_text = LexicographicError.UNKNOWN_TOKEN % t.value[0]
        line = t.lineno
        column = find_column(self.lexer, t)
        
        self.errors.append(LexicographicError(error_text, line, column))
        t.lexer.skip(1)
        #t.lexer.skip(len(t.value))
    
    def tokenize_text(self, text):
        self.lexer.input(text)
        tokens = []
        for tok in self.lexer:
            col = find_column(self.lexer, tok)
            tokens.append(Token(tok.type, tok.value, tok.lineno, col))
        self.lexer.lineno = 0
        return tokens


if __name__ == "__main__":
    lexer = CoolLexer()

    data = open('string4.cl',encoding='utf-8')
    data = data.read()
    res = lexer.tokenize_text(data)
    #pprint(res)
    pprint(lexer.errors)
