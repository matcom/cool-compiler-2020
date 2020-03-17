import lexer_rules
import parser_rules
import sys

from ply.lex import lex
from ply.yacc import yacc

def run(addr):
    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)


    lexer = lex(module=lexer_rules)
    with open(addr, encoding = "utf-8") as f:
        text = f.read()

    parser.parse(text, lexer)


    if parser_rules.my_bool:
        exit(1)


# lexer = lex(module=lexer_rules)
# parser = yacc(module=parser_rules)

# text = ""
# lexer = lex(module=lexer_rules)
# fpath = "C:/Users/Eziel/Downloads/Telegram Desktop/cool-compiler-2020/tests/"
# fpath += "parser/"
# fpath += "operation3"
# fpath += ".cl"
# with open(fpath, encoding = "utf-8") as file:
#     text = file.read()

# parser.parse(text, lexer)