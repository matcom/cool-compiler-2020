import lexer_rules
import parser_rules
import sys

from ply.lex import lex
from ply.yacc import yacc
from semantic_rules import Semantic

def run(addr):
    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)
    sem = Semantic()

    with open(addr, encoding = "utf-8") as f:
        text = f.read()

    ast = parser.parse(text, lexer)
    sem.visit(ast)

    if len(sem.error) > 0:
        print(sem.error[0] + '\n')
        exit(1)
