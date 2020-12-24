import lexer_rules
from ply.lex import lex
import sys

<<<<<<< HEAD
<<<<<<< HEAD
#ww
=======
>>>>>>> semantic_work
=======
#ww
>>>>>>> semantic_work
def run(addr):
    lexer = lex(module=lexer_rules)
    with open(addr, encoding = "utf-8") as f:
        text = f.read()
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> semantic_work
=======
        
>>>>>>> semantic_work
    lexer.input(text)
    token = lexer.token()

    while token is not None:
        try:
            token = lexer.token()
        except:
            lexer.skip(1)

    if lexer_rules.my_bool:
<<<<<<< HEAD
<<<<<<< HEAD
=======
        print(lexer_rules.result)
>>>>>>> semantic_work
=======
>>>>>>> semantic_work
        exit(1)

