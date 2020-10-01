import sys
from argparse import ArgumentParser
from coolcmp.cmp.lexer import Lexer
from coolcmp.cmp.parser import Parser
from coolcmp.cmp.errors import *
from coolcmp.cmp.source_code import SourceCode
from pathlib import Path

args = ArgumentParser(description="Cool compiler programmed in Python.")
args.add_argument("--ast", dest="ast", action="store_true", help="Print AST.")
args.add_argument("--cil_ast", dest="cil_ast", action="store_true", help="Print CIL AST.")
args.add_argument('--tab_size', dest='tab_size', default=4, type=int, help='Tab size to convert tabs to spaces.')
args.add_argument('--no_mips', dest='no_mips', action='store_true', help='Dont generate mips file')
args.add_argument("file_path", help="Path to cool file to compile.")
args = args.parse_args()

path = Path(args.file_path)

if not path.exists():
    raise Exception(f'File {path} doesnt exists')

with open(path) as file:
    content = file.read()

source_code = SourceCode(content, args.tab_size)

try:
    lexer = source_code.lexicalAnalysis()
    root = source_code.syntacticAnalysis(lexer)

    if args.ast:
        from coolcmp.cmp.print_ast import PrintAst
        PrintAst(root)

    source_code.semanticAnalysis(root)
    source_code.runTypeChecker()
    cil_root = source_code.genCILCode()

    if args.cil_ast:
        from coolcmp.cmp.print_ast import PrintAst
        PrintAst(cil_root)

    mips_code = source_code.genMIPSCode(cil_root)
    
    if not args.no_mips:
        with open(f'{path.stem}.mips', 'w') as f:
            print(mips_code, file=f)

except CmpErrors as err:
    print(err)
    exit(1)