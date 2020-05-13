from sys import argv
from cool_lang.lexer import COOL_LEXER
from cool_lang.parser import COOL_PARSER
from cool_lang.semantics import COOL_CHECKER


INPUT_FILE = argv[1]
OUTPUT_FILE = argv[2]

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
if not cchecker.check_semantics(program):
    for error in cchecker.errors:
        print(error)
    exit(1)

exit(0)
