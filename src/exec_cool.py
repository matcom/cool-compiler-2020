from lexer import CoolLexer
from Parser import CoolParser
from semantic import CoolSemantic
import sys

file = open("F:/cool-compiler-2020/src/test.cl", 'r')
cool_lexer = CoolLexer()
errors_lexer = cool_lexer.tokenize(file.read())
# errors_lexer = cool_lexer.tokenize('''''')

if len(errors_lexer) > 0:
    for error in errors_lexer:
        print(error) 
    exit(1)

parser = CoolParser()
ast , errors_parser = parser.parse(cool_lexer)

if len(errors_parser) > 0:
    for error in errors_parser:
        print(error)
        exit(1)

cool_sematic= CoolSemantic(ast)
semantics_error = cool_sematic.check_semantics()

if len(semantics_error) > 0:
    for error in semantics_error:gi
        print(error.text)
    exit(1)