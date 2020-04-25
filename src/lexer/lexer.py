import ply.lex as lex
from pprint import pprint 

from utils.tokens import tokens, reserved, Token
from utils.errors import LexicographicError, SyntaticError
from utils.utils import find_column


class CoolLexer:
    def __init__(self, **kwargs):
        self.reserved = reserved 
        self.tokens = tokens
        self.errors = []
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.lineno = 1
        self.lexer.linestart = 0

    def _update_column(self, t):
        t.column = t.lexpos - t.lexer.linestart + 1
        

    states = (
        ('comments', 'exclusive'),
        ('strings', 'exclusive')
    )

    def t_comment(self, t):
        r'--.*($|\n)'
        t.lexer.lineno += 1
        t.lexer.linestart = t.lexer.lexpos 

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
        t.lexer.linestart = t.lexer.lexpos

    t_comments_ignore = '  \t\f\r\t\v'

    def t_comments_error(self,t):
        t.lexer.skip(1)

    def t_comments_eof(self,t):
        self._update_column(t)
        if t.lexer.level > 0:
            error_text = LexicographicError.EOF_COMMENT 
            self.errors.append(LexicographicError(error_text, t.lineno, t.column))
    
    #Strings
    def t_strings(self,t):
        r'\"'
        t.lexer.str_start = t.lexer.lexpos
        t.lexer.myString = ''
        t.lexer.backslash = False
        t.lexer.begin('strings')

    def t_strings_end(self,t):
        r'\"'
        self._update_column(t)

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
        self._update_column(t)
        
        t.lexer.linestart = t.lexer.lexpos 

        if not t.lexer.backslash:
            error_text = LexicographicError.UNDETERMINATED_STRING
            self.errors.append(LexicographicError(error_text, t.lineno, t.column))
            t.lexer.begin('INITIAL')

    def t_strings_nill(self,t):
        r'\0'
        error_text = LexicographicError.NULL_STRING
        self._update_column(t)
  
        self.errors.append(LexicographicError(error_text, t.lineno, t.column))

    def t_strings_consume(self,t):
        r'[^\n]'
        self._update_column(t)

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
        self._update_column(t)
     
        error_text = LexicographicError.EOF_STRING
        self.errors.append(LexicographicError(error_text, t.lineno, t.column))

    t_ignore = '  \t\f\r\t\v'
    
    def t_semi(self, t):
        r';'
        self._update_column(t)
        return t

    def t_colon(self, t):
        r':'
        self._update_column(t)
        return t

    def t_comma(self, t):
        r','
        self._update_column(t)
        return t

    def t_dot(self, t):
        r'\.'
        self._update_column(t)
        return t
 
    def t_opar(self, t):
        r'\('
        self._update_column(t)
        return t
    
    def t_cpar(self, t):
        r'\)'
        self._update_column(t)
        return t
    
    def t_ocur(self, t):
        r'\{'
        self._update_column(t)
        return t
 
    def t_ccur(self, t):
        r'\}'
        self._update_column(t)
        return t
 
    def t_larrow(self, t):
        r'<-'
        self._update_column(t)
        return t
    
    def t_arroba(self, t):
        r'@'
        self._update_column(t)
        return t

    def t_rarrow(self, t):
        r'=>'
        self._update_column(t)
        return t

    def t_nox(self, t):
        r'~'
        self._update_column(t)
        return
 
    def t_equal(self, t):
        r'='
        self._update_column(t)
        return t
 
    def t_plus(self, t):
        r'\+'
        self._update_column(t)
        return t
 
    def t_of(self, t):
        r'of'
        self._update_column(t)
        return t
 
    def t_minus(self, t):
        r'-'
        self._update_column(t)
        return t
 
    def t_star(self, t):
        r'\*'
        self._update_column(t)
        return t
 
    def t_div(self, t):
        r'/'
        self._update_column(t)
        return t
   
    def t_lesseq(self, t):
        r'<='
        self._update_column(t)
        return t
 
    def t_less(self, t):
        r'<'
        self._update_column(t)
        return t
 

    def t_inherits(self, t):
        r'inherits'
        self._update_column(t)
        return t

    def t_type(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'type')
        self._update_column(t)
        return t

    # Check for reserved words:
    def t_id(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'id')
        self._update_column(t)
        return t


    # Get Numbers
    def t_num(self, t):
        r'\d+(\.\d+)? '
        t.value = float(t.value)
        self._update_column(t)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self._update_column(t)
        # t.column = t.lexer.lexpos - t.lexer.linestart
        t.lexer.linestart = t.lexer.lexpos 

    # Error handling rule
    def t_error(self, t):
        self._update_column(t)
        error_text = LexicographicError.UNKNOWN_TOKEN % t.value[0]
        
        self.errors.append(LexicographicError(error_text, t.lineno, t.column))
        t.lexer.skip(1)
        #t.lexer.skip(len(t.value))
    
    def tokenize_text(self, text: str) -> list:
        self.lexer.input(text)
        tokens = []
        for tok in self.lexer:
            tokens.append(Token(tok.type, tok.value, tok.lineno, tok.column))
        self.lexer.lineno = 1
        self.lexer.linestart = 0
        return tokens

    def _check_empty_line(self, tokens: list):
        if len(tokens) == 0:
            error_text = SyntaticError.ERROR % 'EOF'
            print(SyntaticError(error_text, 0, 0))
            raise Exception()


    def run(self, text: str):
        tokens = self.tokenize_text(text)
        if self.errors:
            for error in self.errors:
                print(error)
            raise Exception()
        
        self._check_empty_line(tokens)
        return tokens

if __name__ == "__main__":
    lexer = CoolLexer()

    data = open('string4.cl',encoding='utf-8')
    data = data.read()
    res = lexer.tokenize_text(data)
    #pprint(res)
    pprint(lexer.errors)
