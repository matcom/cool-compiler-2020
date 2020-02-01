import ply.yacc as yacc
from cool_grammar import *
from lexer import CoolLexer


class CoolParser:
    def __init__(self, lexer=None):
        if lexer is None:
            self.lexer = CoolLexer()
        else:
            self.lexer = lexer
        self.parser = yacc.yacc(start='program', outputdir='src/output_parser')

    def parse(self, program, debug=False):
        # tokens = self.lexer.tokenize_text(program)
        return self.parser.parse(program, self.lexer.lexer, debug=debug)


if __name__ == "__main__":   
    s = '''class Main inherits IO {
	mod(i : Int, ) : Int {	-- Formal list must be comma separated. A comma does not terminate a list of formals.
	  i - (i/k)*k
	};
};
    '''
    parser = CoolParser()
    result = parser.parse(s)
    print(result)