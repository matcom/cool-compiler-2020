import lexer_rules
import parser_rules

from ply.lex import lex
from ply.yacc import yacc

lexer = lex(module=lexer_rules)
parser = yacc(module=parser_rules)


lexer = lex(module=lexer_rules)
addr = input()
with open(addr, encoding = "utf-8") as f:
    text = f.read()


parser.parse(text, lexer)

