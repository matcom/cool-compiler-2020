import sys
from argparse import ArgumentParser
from coolcmp.cmp_utils.lexer import Lexer
from coolcmp.cmp_utils.parser import Parser
from coolcmp.cmp_utils.errors import SyntacticError
from coolcmp.cmp_utils.source_code import SourceCode

args = ArgumentParser(description="Cool compiler programmed in Python.")
args.add_argument("--ast", dest="ast", action="store_true", help="Print AST.")
args.add_argument("file_path", help="Path to cool file to compile.")
args = args.parse_args()

with open(args.file_path) as file:
    content = file.read()

source_code = SourceCode(content)

lexer = source_code.lexicalAnalysis()

if lexer.lexer.errors:
    print('\n'.join(lexer.lexer.errors))
    exit(1)

try:
    root = source_code.syntacticAnalysis(lexer)
except SyntacticError as err:
    print(err)
    exit(1)

if args.ast:
    from coolcmp.cmp_utils.print_ast import PrintAst
    PrintAst(root)
