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
        exit(1)

# text = ""
# lexer = lex(module=lexer_rules)
# fpath = "C:/Users/Eziel/Downloads/Telegram Desktop/cool-compiler-2020/tests/"
# fpath += "parser/"
# fpath += "assignment1"
# fpath += ".cl"
# with open(fpath, encoding = "utf-8") as file:
#     text = file.read()
#     lexer.input(text)

# token = lexer.token()

# while token is not None:
#     token = lexer.token()