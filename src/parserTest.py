import lexer_rules
import parser_rules
import sys

from ply.lex import lex
from ply.yacc import yacc

def run(addr):
    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    with open(addr, encoding = "utf-8") as f:
        text = f.read()

    parser.parse(text, lexer)


    if parser_rules.my_bool:
        print(parser_rules.result)
        exit(1)
