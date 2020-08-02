from typing import List, Any, Optional
import abstract.tree as coolAst
from abstract.semantics import SemanticError, Type, Context
from functools import singledispatchmethod


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
    def _(self, node: coolAst.AttributeDef):  # noqa: F811
        try:
            attr_type = self.context.get_type(node.typex) if isinstance(
                node.typex, str) else node.typex
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
