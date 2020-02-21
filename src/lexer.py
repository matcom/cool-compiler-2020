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
    
    # TODO: Los strings no pueden contener \n, \0, strings anidados, eof en strings
    def t_string(self, t): 
        r'"[^"]*"'
        t.value = t.value[1:-1]
        return t

    # TODO: Comentarios anidados, eof en los comentarios
    def t_comment(self, t):
        r'--.* | \(\*(.)*\*\)'
        pass

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        error_text = LexicographicError.UNKNOWN_TOKEN % t.value
        line = t.lineno
        column = find_column(self.lexer, t)
        
        self.errors.append(LexicographicError(error_text, line, column))
        t.lexer.skip(len(t.value))
    
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

    data = '''
class Main inherits IO {
	str <- "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
	main() : Object {
			{
					out_string("Enter number of numbers to multiply\n");
					out_int(prod(in_int()));
					out_string("\n");
			}
	};
	prod(i : Int) : Int {
		let y : Int <- 1 in {
			while (not (i = 0) ) loop {
				out_string("Enter Number: ");
				y <- y * in_int();
				i <- i - 1;
			}
			y;
		}
	};
}
    '''

    res = lexer.tokenize_text(data)
    pprint(res)
