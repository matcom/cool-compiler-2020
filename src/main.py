from pprint import pprint
from lexer import CoolLexer
from parser import CoolParser
from tools.errors import CompilerError, SyntaticError
import sys, os

input_ = sys.argv[1]
# input_ = f'tests/parser/program1.cl' 
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
    
    if len(tokens) == 0:
        error_text = SyntaticError.ERROR % 'EOF'
        print(SyntaticError(error_text, 0, 0))
        raise Exception()


    parser = CoolParser(lexer)

    ast = parser.parse(data, debug=True)
    if parser.errors:
        raise Exception()
    # print(ast)

except FileNotFoundError:
    error_text = CompilerError.UNKNOWN_FILE % input_
    print(CompilerError(error_text, 0, 0))
    