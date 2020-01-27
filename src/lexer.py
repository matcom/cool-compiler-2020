import ply.lex as lex
from tools.tokens import tokens, reserved, Token
from pprint import pprint 
# from src.errors import LexicographicErrors

# TODO: las palabras reservadas, excepto true y false son case insensitive
# TODO: Poner la regla para los strings de q no puede contener \n
# TODO: Arreglar los comentarios

class CoolLexer:
    def __init__(self, **kwargs):
        self.reserved = reserved
        self.tokens = tokens
        self.errors = []
        self.lexer = lex.lex(module=self, **kwargs)

    # Regular expressions for simple tokens
    t_ignore_COMMENT = r'--.* | \*(.)*\*'
    # A string containing ignored characters 
    t_ignore = '  \t\f\r\t\v'
    
    t_def = r'def'
    t_print = r'print'
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

    # Check for reserved words:
    def t_id(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'id')
        return t

    # Get Numbers
    def t_num(self, t):
        r'\d+(\.\d+)? '
        t.value = float(t.value)
        return t
    
    def t_string(self, t):
        r'".*"'
        #r'\"([^\\\n]|(\\.))*?\"'
        t.value = t.value[1:-1]
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        self.errors.append(LexicographicError(LexicographicError.UNKNOWN_TOKEN % t.value))
        t.lexer.skip(len(t.value))
    

    def find_column(self, token):
        line_start = self.lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def tokenize_text(self, text):
        self.lexer.input(data)
        tokens = []
        for tok in self.lexer:
            tokens.append(Token(tok.type, tok.value, tok.lineno, self.find_column(tok)))
        return tokens


if __name__ == "__main__":
    m = CoolLexer()

    data = '''
    CLASS Cons inherits List {
        xcar : Int;
        xcdr : List;
        isNil() : Bool { false }; 
        init(hd : Int, tl : List) : Cons {
            {
                xcar <- hd;
                xcdr <- 2;
                self;
                p . translate ( 1 , 1 ) ;
            }
        }
    '''

    res = m.tokenize_text(data)
    pprint(res)
