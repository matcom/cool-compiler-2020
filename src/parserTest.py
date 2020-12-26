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

    # temp = parser_rules.result.split(':')
    # s = temp[0]
    # parser_rules.result = ''
    # return s

    if parser_rules.my_bool:
        print(parser_rules.result)
        parser_rules.result = ''
        exit(1)


# lexer = lex(module=lexer_rules)
# parser = yacc(module=parser_rules)

# text = ""
# lexer = lex(module=lexer_rules)

# fpath = "C:/Users/Eziel/Desktop/ejemplos/cool-compiler-jj-christian-alberto-hector-c411/src/test/TestCases/Semantics/success/"
# fpath = fpath + 'binary_tree.cl'

# with open(fpath, encoding = "utf-8") as file:
#     text = file.read()

# parser.parse(text, lexer)