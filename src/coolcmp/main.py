import sys
from argparse import ArgumentParser
from coolcmp.cmp_utils.lexer import Lexer
from coolcmp.cmp_utils.parser import Parser
from coolcmp.cmp_utils.errors import *
from coolcmp.cmp_utils.source_code import SourceCode

args = ArgumentParser(description="Cool compiler programmed in Python.")
args.add_argument("--ast", dest="ast", action="store_true", help="Print AST.")
args.add_argument('--tab_size', dest='tab_size', default=4, type=int, help='Tab size to convert tabs to spaces.')
args.add_argument("file_path", help="Path to cool file to compile.")
args = args.parse_args()

with open(args.file_path) as file:
    content = file.read()

source_code = SourceCode(content, args.tab_size)

try:
    lexer = source_code.lexicalAnalysis()
    root = source_code.syntacticAnalysis(lexer)

    if args.ast:
        from coolcmp.cmp_utils.print_ast import PrintAst
        PrintAst(root)

    source_code.semanticAnalysis(root)
    source_code.runTypeChecker()

except CmpErrors as err:
    print(err)
    exit(1)