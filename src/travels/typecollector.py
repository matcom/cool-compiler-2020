import abstract.tree as coolAst
from abstract.semantics import SemanticError, VoidType, IntegerType, StringType, ObjectType, Context, BoolType, AutoType
from functools import singledispatchmethod


class TypeCollector:
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @singledispatchmethod
    def visit(self, node):
        pass

    @visit.register  # type: ignore
    def _(self, node: coolAst.ProgramNode):  # noqa: F811
        self.context = Context()
        OBJECT, INTEGER, STRING, BOOL, VOID = ObjectType(), IntegerType(
        ), StringType(), BoolType(), VoidType()
        INTEGER.set_parent(OBJECT)
        STRING.set_parent(OBJECT)
        BOOL.set_parent(OBJECT)
        self.context.types['Object'] = OBJECT
        self.context.types['Int'] = INTEGER
        self.context.types['String'] = STRING
        self.context.types['Bool'] = BOOL
        self.context.types['Void'] = VOID
        self.context.types['AUTO_TYPE'] = AutoType()

        for class_ in node.class_list:
            self.visit(class_)

    @visit.register
    def _(self, node: coolAst.ClassDef):  # noqa: F811
        try:
            self.context.create_type(node.idx)
        except SemanticError as e:
            self.errors.append(e.text)
