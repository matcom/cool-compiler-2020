import lexer_rules
import parser_rules
import sys

from ply.lex import lex
from ply.yacc import yacc

lexer = lex(module=lexer_rules)
parser = yacc(module=parser_rules)


lexer = lex(module=lexer_rules)
with open(sys.argv[1], encoding = "utf-8") as f:
    text = f.read()


parser.parse(text, lexer)

if parser_rules.my_bool:
    exit(1)
