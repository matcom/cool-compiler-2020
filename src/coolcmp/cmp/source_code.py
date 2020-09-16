from coolcmp.cmp.lexer import Lexer
from coolcmp.cmp.parser import Parser
from coolcmp.cmp.semantics import SemanticAnalyzer
from coolcmp.cmp.my_ast import *
from coolcmp.cmp.errors import LexicographicError
from coolcmp.cmp.type_checker import TypeChecker

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
            Class(Type('Object')),
            Class(Type('Int'), can_inherit=False),
            Class(Type('String'), can_inherit=False),
            Class(Type('Bool'), can_inherit=False),
            Class(Type('IO'))
        ]

        methods = {
            'Object': [
                        Method(Id('abort'), NodeContainer(), Type('Object'), Id('self')),
                        Method(Id('type_name'), NodeContainer(), Type('String'), String('""')),
                        Method(Id('copy'), NodeContainer(), Type('SELF_TYPE'), Id('self'))
                      ],

            'String': [
                        Method(Id('length'), NodeContainer(), Type('Int'), Int('0')),
                        Method(Id('concat'), NodeContainer([Formal(Id('s'), Type('String'))]), Type('String'), String('""')),
                        Method(Id('substr'), NodeContainer([
                            Formal(Id('i'), Type('Int')),
                            Formal(Id('l'), Type('Int'))
                        ]), Type('String'), String('""'))
                      ],

            'IO':     [
                        Method(Id('out_string'), NodeContainer([Formal(Id('x'), Type('String'))]), Type('SELF_TYPE'), Id('self')),
                        Method(Id('out_int'), NodeContainer([Formal(Id('x'), Type('Int'))]), Type('SELF_TYPE'), Id('self')),
                        Method(Id('in_string'), NodeContainer(), Type('String'), String('""')),
                        Method(Id('in_int'), NodeContainer(), Type('Int'), Int('0'))
                      ]
        }

        for cls in self.native_classes:
            if cls.type.value in methods:
                cls.feature_list = methods[cls.type.value]

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
        chk.visit(self.root)