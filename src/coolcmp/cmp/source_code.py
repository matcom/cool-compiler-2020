from coolcmp.cmp.lexer import Lexer
from coolcmp.cmp.parser import Parser
from coolcmp.cmp.semantics import SemanticAnalyzer
from coolcmp.cmp.ast_cls import *
from coolcmp.cmp.errors import LexicographicError
from coolcmp.cmp.type_checker import TypeChecker
from coolcmp.cmp.gen_cil import GenCIL
from coolcmp.cmp.gen_mips import DataSegment, GenMIPS
from coolcmp.cmp.constants import TYPE_INT, TYPE_BOOL, TYPE_STRING

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
            Class(Type('Int'), reserved_attrs=[AttrIntLiteral()], can_inherit=False, type_obj=TYPE_INT),
            Class(Type('String'), reserved_attrs=[AttrStringLength(), AttrStringLiteral()], can_inherit=False, type_obj=TYPE_STRING),
            Class(Type('Bool'), reserved_attrs=[AttrBoolLiteral()], can_inherit=False, type_obj=TYPE_BOOL),
            Class(Type('IO'))
        ]

        methods = {
            'Object': [
                        Method(Id('abort'), NodeContainer(), Type('Object')),
                        Method(Id('type_name'), NodeContainer(), Type('String')),
                        Method(Id('copy'), NodeContainer(), Type('SELF_TYPE'))
                      ],

            'String': [
                        Method(Id('length'), NodeContainer(), Type('Int')),
                        Method(Id('concat'), NodeContainer([Formal(Id('s'), Type('String'))]), Type('String')),
                        Method(Id('substr'), NodeContainer([
                            Formal(Id('i'), Type('Int')),
                            Formal(Id('l'), Type('Int'))
                        ]), Type('String'))
                      ],

            'IO':     [
                        Method(Id('out_string'), NodeContainer([Formal(Id('x'), Type('String'))]), Type('SELF_TYPE')),
                        Method(Id('out_int'), NodeContainer([Formal(Id('x'), Type('Int'))]), Type('SELF_TYPE')),
                        Method(Id('in_string'), NodeContainer(), Type('String')),
                        Method(Id('in_int'), NodeContainer(), Type('Int'))
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

    def genCILCode(self):
        cil = GenCIL(self.cls_refs)
        cil.visit(self.root)

        for lst in cil.cil_code.dict_func.values():
            lst.sort(key=lambda x: x.level, reverse=True)  #sort by greater level

        return cil.cil_code

    def genMIPSCode(self, cil_code):
        data = DataSegment(cil_code)

        mips = GenMIPS(data.code, cil_code)
        mips.visit(cil_code)

        return '\n'.join(map(str, mips.code))