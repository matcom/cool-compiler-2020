import lexer_rules
from ply.lex import lex
import sys

def run(addr):
    lexer = lex(module=lexer_rules)
    with open(addr, encoding = "utf-8") as f:
        text = f.read()
        
    lexer.input(text)
    token = lexer.token()

    while token is not None:
        try:
            token = lexer.token()
        except:
            lexer.skip(1)

    if lexer_rules.my_bool:
        print(lexer_rules.result)
        exit(1)

