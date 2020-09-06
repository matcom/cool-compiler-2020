from coolcmp.cmp_utils.lexer import Lexer
from coolcmp.cmp_utils.parser import Parser

class SourceCode:
    def __init__(self, code):
        self.code = code

    def lexicalAnalysis(self):
        lex = Lexer()
        lex.build()
        lex.lexer.input(self.code)

        for _ in lex.lexer: pass

        return lex

    def syntacticAnalysis(self, lexer):
        lexer.build()

        p = Parser()
        p.build(lexer.tokens)

        return p.parser.parse(self.code)
