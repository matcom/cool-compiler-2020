import ply.yacc as yacc
from cool_grammar import *
from lexer import CoolLexer
from utils.utils import find_column

class CoolParser:
    def __init__(self, lexer=None):
        if lexer is None:
            self.lexer = CoolLexer()
        else:
            self.lexer = lexer
        self.parser = yacc.yacc(start='program', outputdir='src/output_parser')

    def parse(self, program, debug=False):
        tokens = self.lexer.tokenize_text(program)
        return self.parser.parse(program, self.lexer.lexer, debug=debug)


if __name__ == "__main__":   
    s = '''
    class Main {
            main(): Object {
                    (new alpha).print()
            };

    };

    (* Class names must begin with uppercase letters *)
    class alpha inherits IO {
        print() : Object {
                out_string("reached!!\n");
        };
    }; 
    '''
    parser = CoolParser()
    result = parser.parse(s)
    print(result)