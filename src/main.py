import sys
from argparse import ArgumentParser
from cmp.lexer import Cool_Lexer
from cmp.parser import Parser

args = ArgumentParser(description="Cool compiler programmed in Python.")
args.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode.")
args.add_argument("file_path", help="Path to cool file to compile.")
args = args.parse_args()

def lexical_analysis(content):
    lex = Cool_Lexer()
    lex.build()

    lex = lex.lexer
    lex.input(content)

    token_list = []
    for token in lex:
        token_list.append(token)

    if args.verbose:
        print("Lexical Analysis Tokens")

        for token in token_list:
            print(token)

    if len(lex.errors) > 0:
        print("".join(lex.errors))
        exit(1)

def syntactic_analysis(content):
    p = Parser()
    p.build()

    p.parser.parse(content)

    if len(p.errors) > 0:
        print("".join(p.errors))
        exit(1)

def main():
    content = ""

    with open(args.file_path) as file:
        content = file.read()

    lexical_analysis(content)
    syntactic_analysis(content)

if __name__ == "__main__":
    main()
