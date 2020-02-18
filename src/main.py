from cl_lexer import CoolLexer
from cl_parser import CoolParser

import sys

def main():
    program = open(sys.argv[1]).read()
    lex = CoolLexer()
    lex.input(program)
    while True:
        tok = lex.token()
        if not tok:
            break

if __name__ == "__main__":
    main()
    exit(1) # temporal
