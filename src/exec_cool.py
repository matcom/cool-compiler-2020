from lexer import CoolLexer
import sys

file = open(sys.argv[1], 'r')
cool_lexer = CoolLexer()
cool_lexer.build()
tokens, errors_lexer = cool_lexer.test(file.read())

if len(errors_lexer) > 0:
    for error in errors_lexer:
        print(error)
    exit(1)