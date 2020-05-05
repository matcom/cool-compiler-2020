import sys

import errors as err
from lexer_parser import lexer, parser
from semantic import semantic_check
from code_generation import generate_code


def exit_with_error(error):
    print(f'CompilerError: {error}')
    exit(1)


def main():
    if len(sys.argv) != 2:
        exit_with_error("invalid number of arguments")

    input_data = ""
    input_file = sys.argv[1]
    try:
        with open(input_file) as f:
            input_data = f.read()
    except FileNotFoundError:
        exit_with_error(f'file {sys.argv[1]} not found')

    ast = parser.parse(input_data, lexer, tracking=True)
    if err.LEXER_ERRORS:
        for e in err.LEXER_ERRORS:
            print(e)
        exit(1)
    if err.PARSER_ERRORS:
        for e in err.PARSER_ERRORS:
            print(e)
        exit(1)

    semantic_check(ast)
    if err.SEMANTIC_ERRORS:
        for e in err.SEMANTIC_ERRORS:
            print(e)
        exit(1)
        
    cil_code=generate_code(ast)
    output_file = input_file[0:-2] + 'cli'

    with open(output_file,"w") as output:
        output.write(cil_code)

if __name__ == "__main__":
    main()
