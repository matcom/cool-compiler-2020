from typing import List
import abstract.tree as coolAst
from abstract.semantics import (
    IoType,
    Method,
    SelfType,
    SemanticError,
    Type,
    VoidType,
    IntegerType,
    StringType,
    ObjectType,
    Context,
    BoolType,
    AutoType,
)
from functools import singledispatchmethod

BUILTINS = ("Int", "Bool", "Object", "String", "IO", "AUTO_TYPE")


def bootstrap_string(obj: StringType, intType: IntegerType):
    def length() -> Method:
        method_name = "length"
        param_names = []
        params_types = []
        return_type = intType

        return Method(method_name, param_names, params_types, return_type)

    def concat() -> Method:
        method_name = "concat"
        param_names = ["s"]
        params_types: List[Type] = [StringType()]
        return_type = obj

        return Method(method_name, param_names, params_types, return_type)

    def substr() -> Method:
        method_name = "substr"
        param_names = ["i", "l"]
        params_types: List[Type] = [IntegerType(), IntegerType()]
        return_type = obj

        return Method(method_name, param_names, params_types, return_type)

    obj.methods["length"] = length()
    obj.methods["concat"] = concat()
    obj.methods["substr"] = substr()


def bootstrap_io(io: IoType, strType: StringType, selfType: SelfType, intType: IntegerType):
    def out_string() -> Method:
        method_name = "out_string"
        param_names = ["x"]
        param_types: List[Type] = [StringType()]
        return_type = selfType

        return Method(method_name, param_names, param_types, return_type)

    def out_int() -> Method:
        method_name = "out_int"
        param_names = ["x"]
        params_types: List[Type] = [IntegerType()]
        return_type = selfType

        return Method(method_name, param_names, params_types, return_type)

    def in_string() -> Method:
        method_name = "in_string"
        param_names = []
        params_types = []
        return_type = strType

        return Method(method_name, param_names, params_types, return_type)

    def in_int() -> Method:
        method_name = "in_int"
        param_names = []
        params_types = []
        return_type = intType

        return Method(method_name, param_names, params_types, return_type)

    # Crear el metodo out_string
    io.methods["out_string"] = out_string()
    io.methods["out_int"] = out_int()
    io.methods["in_string"] = in_string()
    io.methods["in_int"] = in_int()


def bootstrap_object(obj: ObjectType, strType: StringType):
    def abort() -> Method:
        method_name = "abort"
        param_names = []
        params_types = []
        return_type = obj

        return Method(method_name, param_names, params_types, return_type)

    def type_name() -> Method:
        method_name = "type_name"
        param_names = []
        params_types = []
        return_type = strType

        return Method(method_name, param_names, params_types, return_type)

    def copy() -> Method:
        method_name = "copy"
        param_names = []
        params_types = []
        return_type = SelfType()

        return Method(method_name, param_names, params_types, return_type)

    obj.methods["abort"] = abort()
    obj.methods["type_name"] = type_name()
    obj.methods["copy"] = copy()


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
        OBJECT, INTEGER, STRING, BOOL, VOID, SELF_TYPE = (
            ObjectType(),
            IntegerType(),
            StringType(),
            BoolType(),
            VoidType(),
            SelfType(),
        )
        ioType = IoType()

        INTEGER.set_parent(OBJECT)
        STRING.set_parent(OBJECT)
        BOOL.set_parent(OBJECT)
        ioType.set_parent(OBJECT)

        # Agregar los metodos builtin
        bootstrap_string(STRING, INTEGER)
        bootstrap_io(ioType, STRING, SELF_TYPE, INTEGER)
        bootstrap_object(OBJECT, STRING)

        # Agregar al objeto IO los metodos de OBJECT
        ioType.methods.update(OBJECT.methods)

        self.context.types["Object"] = OBJECT
        self.context.types["Int"] = INTEGER
        self.context.types["String"] = STRING
        self.context.types["Bool"] = BOOL
        self.context.types["Void"] = VOID
        self.context.types["AUTO_TYPE"] = AutoType()
        self.context.types["IO"] = ioType
        self.context.types["SELF_TYPE"] = SELF_TYPE

        for class_ in node.class_list:
            self.visit(class_)

    @visit.register
    def _(self, node: coolAst.ClassDef):
        try:
            if node.idx in BUILTINS:
                raise SemanticError(
                f"{node.line, node.column} - SemanticError: Redefinition of basic class {node.idx}."
            )
            self.context.create_type(node.idx)
        except SemanticError as e:
            raise SemanticError(f"{node.line, node.column - 2} - SemanticError: Classes may not be redefined")
