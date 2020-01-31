import argparse
from pprint import pprint
from lexer import CoolLexer
from parser import CoolParser

# arg_parser = argparse.ArgumentParser()
# arg_parser.add_argument('input')
# arg_parser.add_argument('output')
# args = arg_parser.parse_args()

# input_ = args.input
# output_ = args.output

input_ = './tests/parser/err2.cl' 

try:
    with open(input_) as f:
        data = f.read()

    lexer = CoolLexer()
    # lexer.tokenize_text(data)

    parser = CoolParser(lexer)
    ast = parser.parse(data)
    print(lexer.errors)
    print(ast)

except FileNotFoundError:
    print(f'No se pude encontrar el fichero {input_}')
    