"""
Copyright (c) 2020 School of Math and Computer Science, University of Havana

COOL compiler project
"""

import sys

import errors as err
from lexer_parser import lexer, parser
from semantic import semantic_check


def exit_with_error(error):
    print(f'CompilerError: {error}')
    exit(1)


def main():
    if len(sys.argv) != 2:
        exit_with_error("invalid number of arguments")

    input_data = ""
    try:
        with open(sys.argv[1]) as f:
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


if __name__ == "__main__":
    main()
