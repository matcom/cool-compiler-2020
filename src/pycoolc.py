from build.compiler_struct import LEXER, PARSER
from comments import find_comments
from argparse import ArgumentParser
import sys


def pipeline(program: str) -> None:
    try:
        program = find_comments(program)
    except AssertionError as e:
        print(e)
        sys.exit(1)

    # Right now, program has no comments, so is safe to pass it to the LEXER
    try:
        tokens = LEXER(program)
    except Exception as e:
        print(e)
        sys.exit(1)

    # Parse the tokens to obtain a derivation tree
    try:
        parse = PARSER(tokens)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()
    with open(args.file, "r") as f:
        program = f.read()
        pipeline(program)
        sys.exit(0)
