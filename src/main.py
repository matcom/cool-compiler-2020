from pprint import pprint
from lexer import CoolLexer
from parser import CoolParser
import sys, os

input_ = sys.argv[1]
# input_ = f'tests/codegen/atoi2.cl' 
# output_ = args.output


try:
    with open(input_) as f:
        data = f.read()

    lexer = CoolLexer()
    tokens = lexer.tokenize_text(data)
    if lexer.errors:
        for error in lexer.errors:
            print(error)
        raise Exception()

    parser = CoolParser(lexer)

    ast = parser.parse(data, debug=True)
    if parser.errors:
        raise Exception()
    # print(ast)

except FileNotFoundError:
    print(f'No se pude encontrar el fichero {input_}')
    