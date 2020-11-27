from typing import List, Any, Optional
import abstract.tree as coolAst
from abstract.semantics import Method, ObjectType, SemanticError, Type, Context
from functools import singledispatchmethod

INHERITABLES = ("Int", "Bool", "String", "AUTO_TYPE")


class TypeBuilder:
    def __init__(self, context: Context, errors=[]):
        self.context: Context = context
        self.errors: List[Any] = errors
        self.current_type: Optional[Type] = None

    @singledispatchmethod
    def visit(self, node):
        pass

    @visit.register
    def _(self, node: coolAst.ProgramNode):  # noqa: F811
        for class_ in node.class_list:
            self.visit(class_)

    @visit.register
    def _(self, node: coolAst.ClassDef):
        self.current_type = self.context.get_type(node.idx)
        parent = self.context.get_type(node.parent)

        # No se puede heredar de Int ni de BOOL ni de AutoType ni de String
        if parent.name in INHERITABLES:
            self.errors.append(f"Cannot inherit from builtin {parent.name}")
            return

        # Detectar dependencias circulares
        if parent.conforms_to(self.current_type):
            self.errors.append(
                f"Circular dependency: class {self.current_type.name} cannot inherit from {parent.name}"
            )
        else:
            self.current_type.set_parent(parent)

            # Definir los atributos y metodos del padre
            for attrib in parent.attributes:
                self.current_type.attributes.append(attrib)

            # self.current_type.methods.update(parent.methods)

            for feature in node.features:
                self.visit(feature)

    @visit.register
    def _(self, node: coolAst.AttributeDef):
        # Detectar si el atributo que vamos a crear
        # redefine algun atributo heredado definido
        # anteriormente
        try:
            # Extraer el tipo del atributo del contexto
            attr_type = (
                self.context.get_type(node.typex)
                if isinstance(node.typex, str)
                else node.typex
            )

            # Definir el atributo en el tipo actual
            self.current_type.define_attribute(
                node.idx, attr_type, node.line, node.column
            )
        except SemanticError as e:
            self.errors.append(e.text)

    @visit.register
    def _(self, node: coolAst.MethodDef):
        params = [param.id for param in node.param_list]
        try:
            params_type = [
                self.context.get_type(param.type)
                if isinstance(param.type, str)
                else param.type
                for param in node.param_list
            ]
            try:
                return_type = (
                    self.context.get_type(node.return_type)
                    if isinstance(node.return_type, str)
                    else node.return_type
                )
                try:
                     # Manejar la redefinicion de metodos
                    try:
                        m = self.current_type.parent.get_method(node.idx)
                        redefined = True
                    except SemanticError:
                        redefined = False

                    if redefined:
                        # verificar la cantidad de parametros
                        if len(node.param_list) != len(m.param_types):
                            raise SemanticError(f"({node.line}, {node.column}) - SemanticError: Incompatible number of formal parameters in redefined method {node.idx}.")
                        # Verificar el tipo de los parametros
                        for param, parent_param in zip(
                            node.param_list,
                            m.param_types,
                        ):
                            if param.type != parent_param.name:
                                raise SemanticError(
                                    f"({param.line}, {param.column}) - SemanticError: In redefined method {node.idx}, parameter type {param.type} is different from original type {parent_param.name}."
                                )
                        # Verificar el tipo de retorno
                        if (
                            return_type.name
                            != m.return_type.name
                        ):
                            raise SemanticError(
                                f"({node.line}, {node.ret_col}) - SemanticError: In redefined method {node.idx}, return type {return_type.name} is different from original return type {m.return_type.name}"
                            )
                    self.current_type.define_method(
                        node.idx,
                        params,
                        params_type,
                        return_type,
                        node.line,
                        node.column,
                    )
                except SemanticError as e:
                    self.errors.append(e.text)

            except SemanticError as e:
                self.errors.append(f"({node.line}, {node.ret_col}) - TypeError: Undefined return type {node.return_type} in method {node.idx}.")

        except SemanticError as e:
            for param in node.param_list:
                if isinstance(param.type, str):
                    try:
                        self.context.get_type(param.type)
                    except:
                        self.errors.append(f"({param.line}, {param.column + len(param.id) + 2}) - TypeError: Class {param.type} of formal parameter {param.id} is undefined")
