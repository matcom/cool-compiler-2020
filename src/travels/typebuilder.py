from typing import List, Any, Optional
import abstract.tree as coolAst
from abstract.semantics import SemanticError, Type, Context
from functools import singledispatchmethod

INHERITABLES = ('Int', 'Bool', 'String', 'AUTO_TYPE')


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
    def _(self, node: coolAst.ClassDef):  # noqa: F811
        self.current_type = self.context.get_type(node.idx)
        parent = self.context.get_type(node.parent)

        # No se puede heredar de Int ni de BOOL ni de AutoType ni de String
        if parent.name in INHERITABLES:
            self.errors.append(f"Cannot inherit from builtin {parent.name}")
            return

        # Detectar dependencias circulares
        if parent.conforms_to(self.current_type):
            self.errors.append(
                f'Circular dependency: class {self.current_type.name} cannot inherit from {parent.name}'
            )
        else:
            self.current_type.set_parent(parent)

            for feature in node.features:
                self.visit(feature)

    @visit.register
    def _(self, node: coolAst.AttributeDef):
        # Detectar si el atributo que vamos a crear
        # redefine algun atributo heredadoo definido
        # anteriormente
        try:
            self.current_type.get_attribute(node.idx)
            self.errors.append(f"Can not redefine {node.idx} attribute")
        except SemanticError:  # Al lanzar la excepcion indica que el atributo no se ha definido
            try:
                # Extraer el tipo del atributo del contexto
                attr_type = self.context.get_type(node.typex) if isinstance(
                    node.typex, str) else node.typex

                # Definir el atributo en el tipo actual
                self.current_type.define_attribute(node.idx, attr_type)
            except SemanticError as e:
                self.errors.append(e.text)

    @visit.register
    def _(self, node: coolAst.MethodDef):  # noqa: F811
        params = [param.id for param in node.param_list]
        try:
            params_type = [
                self.context.get_type(param.type) if isinstance(
                    param.type, str) else param.type
                for param in node.param_list
            ]
            try:
                return_type = self.context.get_type(
                    node.return_type) if isinstance(node.return_type,
                                                    str) else node.return_type
                try:
                    self.current_type.define_method(node.idx, params,
                                                    params_type, return_type)
                except SemanticError as e:
                    self.errors.append(e.text)

            except SemanticError as e:
                self.errors.append(e.text)

        except SemanticError as e:
            self.errors.append(e.text)
