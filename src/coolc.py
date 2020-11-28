import argparse

from cmp.cil import CIL_FORMATTER, CIL_TO_MIPS, COOL_TO_CIL_VISITOR
from cmp.cool_lang.lexer import COOL_LEXER
from cmp.cool_lang.parser import COOL_PARSER
from cmp.cool_lang.semantics import COOL_CHECKER

parser = argparse.ArgumentParser(description="COOL Compiler")
parser.add_argument(
    "INPUT_FILE",
    help="file to compile.",
    type=str,
)
parser.add_argument(
    "OUTPUT_FILE",
    help="compiled file.",
    type=str,
)
parser.add_argument(
    "-v",
    "--verbose",
    help="execute in verbose mode.",
    action="store_true",
)
parser.add_argument(
    "--cil",
    help="compile to cil file.",
    action="store_true",
)

args = parser.parse_args()

INPUT_FILE = args.INPUT_FILE
OUTPUT_FILE = args.OUTPUT_FILE
VERBOSE = args.verbose
GEN_CIL = args.cil

code = open(INPUT_FILE, encoding="utf8").read()

clexer = COOL_LEXER()
if not clexer.tokenize(code):
    for error in clexer.errors:
        print(error)
    exit(1)

if not list(filter(lambda x: x.type != "COMMENT", clexer.result)):
    print("(0, 0) - SyntacticError: ERROR at or near EOF")
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

ctc = COOL_TO_CIL_VISITOR(cchecker.context)
cil_ast = ctc.visit(program)

if GEN_CIL:
    with open(OUTPUT_FILE[:-4] + "cil", "w") as out_fd:
        out_fd.write(CIL_FORMATTER().visit(cil_ast))

ctm = CIL_TO_MIPS(cchecker.context)
ctm.visit(cil_ast)
mips_code = ctm.mips.compile()

open(OUTPUT_FILE, "w", encoding="utf8").write(mips_code)


exit(0)
