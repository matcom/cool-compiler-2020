from tools.tokens import tokens
import os
import ply.yacc as yacc

from lexer import CoolLexer
from tools.tokens import tokens

class Parser:
    def __init__(self, lexer=None):
        self.lexer = lexer if lexer else CoolLexer()
        self.outputdir = 'src/output_parser'
        self.tokens = tokens
        yacc.yacc(start='program',
                  module=self, 
                  outputdir=self.outputdir)
        
   
    def parse(self, program, debug=False):
        # tokens = self.lexer.tokenize_text(program)
        return yacc.parse(program, self.lexer.lexer, debug=debug)