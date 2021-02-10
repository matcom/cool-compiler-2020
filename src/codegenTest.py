import lexer_rules
import parser_rules
import sys

from ply.lex import lex
from ply.yacc import yacc
from semantic_rules import Semantic
import cool_to_cil, cil_to_mips

def run(addr):
    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)
    sem = Semantic()

    with open(addr, encoding = "utf-8") as f:
        text = f.read()

    ast = parser.parse(text, lexer)
    sem.visit(ast)

    cil = cool_to_cil.Build_CIL(ast, sem)

    mips = cil_to_mips.Build_Mips(cil.astCIL)

    out_file = addr.split(".")
    out_file[-1] = "mips"
    out_file = ".".join(out_file)

    mips_code = ''
    for line in mips.lines:
            mips_code += line + '\n'
    
    with open(out_file, 'w') as f:
        f.write(mips_code)
        f.close()
    exit(0)
