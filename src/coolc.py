import argparse

from cmp.cool_lang.lexer import COOL_LEXER
from cmp.cool_lang.parser import COOL_PARSER
from cmp.cool_lang.semantics import COOL_CHECKER
from cmp.cil.cool_to_cil import COOL_TO_CIL_VISITOR


parser = argparse.ArgumentParser(description='COOL Compiler')
parser.add_argument('INPUT_FILE', help='file to compile.', type=str)
parser.add_argument('OUTPUT_FILE', help='compiled file.', type=str)
parser.add_argument('-v', '--verbose', help='execute in verbose mode', action="store_true")

args = parser.parse_args()

INPUT_FILE = args.INPUT_FILE
OUTPUT_FILE = args.OUTPUT_FILE
VERBOSE = args.verbose

code = open(INPUT_FILE, encoding="utf8").read()

clexer = COOL_LEXER()
if not clexer.tokenize(code):
    for error in clexer.errors:
        print(error)
    exit(1)

if not list(filter(lambda x: x.type != 'COMMENT', clexer.result)):
    print('(0, 0) - SyntacticError: ERROR at or near EOF')
    exit(1)

cparser = COOL_PARSER()
if not cparser.parse(clexer):
    for error in cparser.errors:
        print(error)
    exit(1)

program = cparser.result
cchecker = COOL_CHECKER()
if not cchecker.check_semantics(program, verbose=VERBOSE):
    for error in cchecker.errors:
        print(error)
    exit(1)

exit(0)
