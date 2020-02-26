from lexer import CoolLexer
from Parser import CoolParser
import sys

file = open(sys.argv[1], 'r')
cool_lexer = CoolLexer()
errors_lexer = cool_lexer.tokenize(file.read())
# errors_lexer = cool_lexer.tokenize('''''')

if len(errors_lexer) > 0:
    for error in errors_lexer:
        print(error)
    exit(1)

parser = CoolParser()
errors_parser = parser.parse(cool_lexer)

if len(errors_parser) > 0:
    for error in errors_parser:
        print(error)
    exit(1)