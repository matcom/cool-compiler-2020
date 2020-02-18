from cl_lexer import CoolLexer
from cl_parser import CoolParser

import sys
from utils import LEX_ERRORS, PARSER_ERRORS

def main():
    program = open(sys.argv[1]).read()
    lex = CoolLexer()
    parser = CoolParser()
    ast = parser.parse(program, lexer=lex.lexer)

    # lex.input(program)
    # while True:
        # tok = lex.token()
        # if not tok:
            # break
        # print(tok)

    #print first Lex Errors 
    for e in LEX_ERRORS:
        print(e)

    for e in PARSER_ERRORS:
        print(e)

    if LEX_ERRORS or PARSER_ERRORS:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main() # temporal