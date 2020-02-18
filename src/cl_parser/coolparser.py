import ply.yacc as yacc
import cl_parser.config
from cl_lexer import CoolLexer

class CoolParser(object):
    def __init__(self, *args, **kwargs):
        self.parser = yacc.yacc(module=cl_parser.config, **kwargs)

    def parse(self, data, lexer=CoolLexer()):
        return self.parser.parse(data, lexer=lexer)
        