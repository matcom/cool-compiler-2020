import ply.lex as lex
import cl_lexer.config

class CoolLexer(object):
    def __init__(self, *args, **kwargs):
        self.lexer = lex.lex(module=cl_lexer.config, **kwargs)

    def token(self):
        return self.lexer.token()

    def input(self, raw):
        self.lexer.input(raw)