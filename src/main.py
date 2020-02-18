from cl_lexer import CoolLexer
from cl_parser import CoolParser

import sys

def main():
    program = open(sys.argv[1]).read()
    lex = CoolLexer()
    parser = CoolParser()
    # lex.input(program)
    # while True:
        # tok = lex.token()
        # if not tok:
            # break
    ast = parser.parse(program, lexer=lex.lexer)

if __name__ == "__main__":
    main()
    exit(1) # temporal