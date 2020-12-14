from engine.cp import SemanticError, visitor, Context, SelfType
from engine.parser import ProgramNode, ClassDeclarationNode
from engine.semantic_errors import ERROR_ON_LN_COL, CYCLIC_HERITAGE


class Collector:
    def __init__(self, errors=[]):
        self.context = Context()
        self.errors = errors
        self.parents = {}

        # Tipos especiales
        self.context.add_type(SelfType())

        # Tipos Buit-In
        self.context.create_type('Object', builtin=True)
        self.context.create_type('IO', builtin=True)
        self.context.create_type('Int', builtin=True)
        self.context.create_type('String', builtin=True)
        self.context.create_type('Bool', builtin=True)

        self.parents['Object'] = None
        self.parents['IO'] = 'Object'
        self.parents['Int'] = 'Object'
        self.parents['String'] = 'Object'
        self.parents['Bool'] = 'Object'

    def ciclic_heritage(self, name, parent):
        if parent is None:
            return False
        if name == parent:
            return True
        return self.ciclic_heritage(name, self.parents[parent])

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for class_def in node.declarations:
            self.visit(class_def)

        if not len(self.errors):
            for declaration in node.declarations:
                if declaration.id.lex not in self.parents.keys():
                    self.parents[declaration.id.lex] = 'Object' if declaration.parent == None else declaration.parent.lex
                if declaration.parent != None and declaration.parent.lex in self.parents.keys() and self.ciclic_heritage(declaration.id.lex, declaration.parent.lex):
                    self.errors.append(ERROR_ON_LN_COL % (
                        declaration.line, declaration.column) + "SemanticError: " + CYCLIC_HERITAGE % (declaration.id.lex))
                    break

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id.lex)
        except SemanticError as se:
            self.errors.append(ERROR_ON_LN_COL % (
                node.line, node.column) + "SemanticError: " + se.text)
