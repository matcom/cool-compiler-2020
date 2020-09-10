from coolcmp.cmp_utils.lexer import Lexer
from coolcmp.cmp_utils.parser import Parser
from coolcmp.cmp_utils.semantics import SemanticAnalyzer

class SourceCode:
    def __init__(self, code, tab_size=4):
        self.code = ''

        for c in code:
            if c == '\t':
                self.code += ' ' * tab_size

            else: self.code += c

    def lexicalAnalysis(self):
        lex = Lexer()
        lex.build()
        lex.lexer.input(self.code)

        for _ in lex.lexer: pass

        return lex

    def syntacticAnalysis(self, lexer):
        lexer.build()

        p = Parser()
        p.build(self.code, lexer.tokens)

        return p.parser.parse(self.code)

    def semanticAnalysis(self, root):
        semantics = SemanticAnalyzer(root)
        
        semantics.build_inheritance_tree()
        semantics.check_cycles()