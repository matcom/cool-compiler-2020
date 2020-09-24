from utils.tokens import tokens
import os
import ply.yacc as yacc

from parser.logger import log
from lexer.lexer import CoolLexer
from utils.tokens import tokens

class Parser:
    def __init__(self, lexer=None):
        self.lexer = lexer if lexer else CoolLexer()
        self.outputdir = 'parser/output_parser'
        self.tokens = tokens
        self.errors = False
        self.parser = yacc.yacc(start='program',
                                module=self, 
                                outputdir=self.outputdir,
                                optimize=1,
                                debuglog=log,
                                errorlog=log)
        
   
    def parse(self, program, debug=False):
        self.errors = False
        # tokens = self.lexer.tokenize_text(program)
        return self.parser.parse(program, self.lexer.lexer, debug=log)