import ply.yacc as yacc
from cool_grammar import *
from lexer import CoolLexer

class CoolParser:
    def __init__(self, lexer=None):
        if lexer is None:
            self.lexer = CoolLexer()
        else:
            self.lexer = lexer
        self.parser = yacc.yacc(start='program', outputdir='output_parser')

    def parse(self, program, debug=False):
        return self.parser.parse(program, self.lexer.lexer, debug=debug)


if __name__ == "__main__":   
    s = '''
    class A {
        ackermann ( m : AUTO_TYPE , n : AUTO_TYPE ) : AUTO_TYPE {
            if ( m = 0 ) then n + 1 else
                if ( n = 0 ) then ackermann ( m - 1 , 1 ) else
                ackermann ( m - 1 , ackermann ( m , n - 1 ) )
                fi
            fi
        } ;
    } ;
    '''
    parser = CoolParser()
    result = parser.parse(s)
    print(result)