import sys
from argparse import ArgumentParser
from cmp.lexer import Cool_Lexer
from cmp.parser import Parser

def lexical_analysis(content):
    lex = Cool_Lexer()
    lex.build()

    lex = lex.lexer

    lex.input(content)

    for token in lex:
        pass

    return lex.errors

def syntactic_analysis(content):
    p = Parser()
    p.build()

    p.parser.parse(content)

    return p.errors

def output_errors(*errors):
    for e in errors:
        if len(e) > 0:
            print("".join(e))
            exit(1)

args = ArgumentParser(description="Cool compiler programmed in Python.")
args.add_argument("-c", choices=["lexer", "parser"], dest="comp", default="all", help="Show output of single components of compiler. Default is all components.", type=str)
args.add_argument("path_file", help="Path to cool file to compile.")
args = args.parse_args()

content = ""

with open(args.path_file) as file:
    content = "".join(file.readlines())

lex_errors = lexical_analysis(content)
par_errors = syntactic_analysis(content)

if args.comp == "lexer":
    output_errors(lex_errors)

elif args.comp == "parser":
    output_errors(par_errors)

else: output_errors(lex_errors, par_errors)
