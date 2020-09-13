from coolcmp.cmp_utils.lexer import Lexer
from coolcmp.cmp_utils.parser import Parser
from coolcmp.cmp_utils.semantics import SemanticAnalyzer
from coolcmp.cmp_utils.my_ast import Class, Type
from coolcmp.cmp_utils.errors import LexicographicError
from coolcmp.cmp_utils.type_checker import TypeChecker

class SourceCode:
    def __init__(self, code, tab_size=4):
        self.code = ''

        for c in code:
            if c == '\t':
                self.code += ' ' * tab_size

            else: self.code += c

        self._inject_native_classes()

    def _inject_native_classes(self):
        self.native_classes = [
            Class(Type('Object'), None),
            Class(Type('Int'), None, can_inherit=False),
            Class(Type('String'), None, can_inherit=False),
            Class(Type('Bool'), None, can_inherit=False),
            Class(Type('IO'), None)
        ]

        self.root = self.native_classes[0]  #reference to root of inheritance tree

    def lexicalAnalysis(self):
        lex = Lexer()
        lex.build()
        lex.lexer.input(self.code)

        for _ in lex.lexer: pass

        if lex.lexer.errors:
            raise LexicographicError('\n'.join(lex.lexer.errors))

        return lex

    def syntacticAnalysis(self, lexer):
        lexer.build()

        p = Parser()
        p.build(self.code, lexer.tokens)

        return p.parser.parse(self.code)

    def semanticAnalysis(self, ast_root):
        semantics = SemanticAnalyzer(ast_root)
        
        self.cls_refs = semantics.build_inheritance_tree(self.native_classes)
        semantics.check_cycles()

    def runTypeChecker(self):
        chk = TypeChecker(self.root, self.cls_refs)