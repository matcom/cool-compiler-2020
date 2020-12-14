import abstract.semantics as semantics
import abstract.tree as coolAst
from functools import singledispatchmethod

# Types aliases
Context = semantics.Context
Scope = semantics.Scope

# AST aliases
ProgramNode = coolAst.ProgramNode
ClassDef = coolAst.ClassDef
AttributeDef = coolAst.AttributeDef
MethodDef = coolAst.MethodDef


class TypeChecker:
    def __init__(self, context: Context, errors=[]):
        self.current_type = None
        self.context = context
        self.AUTO_TYPE = self.context.get_type('AUTO_TYPE')
        self.errors = errors

    @singledispatchmethod
    def visit(self, node, scope):
        pass

    @visit.register
    def _(self, node: ProgramNode, scope=None):  # noqa: F811
        scope = Scope()
        for class_ in node.class_list:
            self.visit(class_, scope.create_child())

    @visit.register
    def _(self, node: ClassDef, scope: Scope):  # noqa: F811
        self.current_type = self.context.get_type(node.idx)
        for feature in node.features:
            if isinstance(feature, AttributeDef):
                self.visit(feature, scope)

        for feature in node.features:
            if isinstance(feature, MethodDef):
                self.visit(feature, scope.create_child())

    @visit.register
    def _(self, node: AttributeDef, scope: Scope):  # noqa: F811
        att = self.current_type.get_attribute(node.idx)
        if att.type == self.AUTO_TYPE:
            self.errors.append(f'Cannot infer type of attribute {att.name}')
        scope.define_variable(att.name, att.type)

    @visit.register
    def _(self, node: MethodDef, scope: Scope):  # noqa: F811
        method = self.current_type.get_method(node.idx)
