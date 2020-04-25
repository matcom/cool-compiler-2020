import sys
from pprint import pprint
from lexer.lexer import CoolLexer
from parser.parser import CoolParser
from semantic.semantic import run_pipeline
from utils.errors import CompilerError, SyntaticError


input_ = sys.argv[1]
# input_ = f'//media/loly/02485E43485E359F/_Escuela/__UH/4to/CC/Compiler/cool-compiler-2020/tests/parser/program1.cl' 
# output_ = args.output


try:
    with open(input_) as f:
        text = f.read()

    lexer = CoolLexer()

    # tokens = lexer.tokenize_text(text)
    # if lexer.errors:
    #     for error in lexer.errors:
    #         print(error)
    #     raise Exception()
    tokens = lexer.run(text)

    parser = CoolParser(lexer)

    ast = parser.parse(text, debug=True)
    if parser.errors:
        raise Exception()
    
    # run_pipeline(ast)

except FileNotFoundError:
    error_text = CompilerError.UNKNOWN_FILE % input_
    print(CompilerError(error_text, 0, 0))
    