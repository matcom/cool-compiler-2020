from pprint import pprint
from lexer import CoolLexer
from parser import CoolParser
import os

cwd = os.getcwd()

# input_ = sys.argv[1]
input_ = f'{cwd}/tests/parser/program3.cl' 
# output_ = args.output


try:
    with open(input_) as f:
        data = f.read()

    lexer = CoolLexer()

    parser = CoolParser(lexer)
    if lexer.errors:
        print(lexer.errors)
        # raise Exception()

    ast = parser.parse(data)
    # if parser.errors:
    #     raise Exception()
    # print(ast)

except FileNotFoundError:
    print(f'No se pude encontrar el fichero {input_}')
    