from __future__ import annotations
from typing import List, Optional, Tuple, Union

from abstract.semantics import SemanticError


class Node:
    pass


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    def __init__(self, line, column) -> None:
        self.line = line
        self.column = column


class ProgramNode(Node):
    def __init__(self, class_list):
        self.class_list: List[ClassDef] = class_list

    def check_semantics(self, deep=1):
        from travels import typecollector, typebuilder, inference

        # recolectar los tipos
        type_collector = typecollector.TypeCollector()
        try:
            type_collector.visit(self)
        except SemanticError as e:
            type_collector.errors.append(e.text)

        if type_collector.errors:
            return type_collector.errors, type_collector.context, None

        # Construir los tipos detectados en el contexto
        assert type_collector.context is not None
        type_builder = typebuilder.TypeBuilder(
            type_collector.context, type_collector.errors
        )
        try:
            type_builder.visit(self)
        except SemanticError as e:
            type_builder.errors.append(e.text)

        # Garantizar que exista un tipo Main que contenga un
        # metodo main
        context = type_builder.context
        try:
            context.get_type("Main")
            context.get_type("Main").methods["main"]
        except SemanticError as e:
            type_builder.errors.append(str(e))
        except KeyError:
            type_builder.errors.append(f"Main class must contain a main method.")

        errors = type_builder.errors
        scope = None
        if not errors:
            try:
                inferer = inference.TypeInferer(type_builder.context, errors=errors)
                for d in range(1, deep + 1):
                    scope = inferer.visit(self, scope=scope, deep=d)
            except SemanticError as e:
                errors.append(e.text)
        # reportar los errores
        return errors, type_builder.context, scope


class Param(DeclarationNode):
    def __init__(self, idx, typex, line, column):
        self.id, self.type = idx, typex
        self.line = line
        self.column = column - len(idx)

    def __eq__(self, o: Param) -> bool:
        return self.id == o.id


class MethodDef(DeclarationNode):
    def __init__(
        self,
        idx: str,
        param_list: List[Param],
        return_type: str,
        line,
        column,
        statements: ExpressionNode,
        ret_col
    ):
        self.idx: str = idx
        self.param_list: List[Param] = param_list
        self.return_type: str = return_type
        self.statements: ExpressionNode = statements
        self.line = line
        self.column = column - len(self.idx)
        self.ret_col = ret_col


class AttributeDef(DeclarationNode):
    def __init__(self, idx: str, typex: str, line, column, default_value=None):
        self.idx: str = idx
        self.typex: str = typex
        self.default_value: Optional[ExpressionNode] = default_value
        self.line = line
        self.column = column - len(idx)


class VariableDeclaration(ExpressionNode):
    def __init__(self, var_list, line, column, block_statements=None):
        self.var_list: List[Tuple[str, str, Optional[ExpressionNode]]] = var_list
        self.block_statements: Optional[ExpressionNode] = block_statements
        self.line = line
        self.column = column


class BinaryNode(ExpressionNode):
    def __init__(self, left, right, line, column):
        self.left: ExpressionNode = left
        self.right: ExpressionNode = right
        self.line = line
        self.column = column


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex


class IfThenElseNode(ExpressionNode):
    def __init__(self, cond, expr1, expr2, line, column):
        self.cond: ExpressionNode = cond
        self.expr1: ExpressionNode = expr1
        self.expr2: ExpressionNode = expr2
        self.line = line
        self.column = column


class PlusNode(BinaryNode):
    def __init__(self, left, right, line, column):
        super(PlusNode, self).__init__(left, right, line, column)


class DifNode(BinaryNode):
    def __init__(self, left, right, line, column):
        super(DifNode, self).__init__(left, right, line, column)


class MulNode(BinaryNode):
    def __init__(self, left, right, line, column):
        super(MulNode, self).__init__(left, right, line, column)


class DivNode(BinaryNode):
    def __init__(self, left, right, line, column):
        super(DivNode, self).__init__(left, right, line, column)


class FunCall(ExpressionNode):
    def __init__(self, obj, idx, arg_list, line, column):
        self.obj: Union[str, ExpressionNode] = obj
        self.id: str = idx
        self.args: List[ExpressionNode] = arg_list
        self.line = line
        self.column = column


class ParentFuncCall(ExpressionNode):
    def __init__(self, obj, parent_type, idx, arg_list, line, column):
        self.obj: ExpressionNode = obj
        self.parent_type: str = parent_type
        self.idx: str = idx
        self.arg_list: List[ExpressionNode] = arg_list
        self.line = line
        self.column = column


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr, line, column):
        self.idx: str = idx
        self.expr: ExpressionNode = expr
        self.line = line
        self.column = column - len(idx)


class IntegerConstant(AtomicNode):
    def __init__(self, lex):
        super(IntegerConstant, self).__init__(int(lex))


class StringConstant(AtomicNode):
    def __init__(self, lex, line, column):
        super(StringConstant, self).__init__(lex)
        self.line = line
        self.column = column


class TypeNode(AtomicNode):
    def __init__(self, lex):
        super(TypeNode, self).__init__(lex)


class BoleanNode(TypeNode):
    def __init__(self, val):
        self.val = True if val == "true" else False


class FalseConstant(AtomicNode):
    def __init__(self):
        super(FalseConstant, self).__init__("False")


class TrueConstant(AtomicNode):
    def __init__(self):
        super(TrueConstant, self).__init__("True")


class StringTypeNode(TypeNode):
    def __init__(self):
        super(StringTypeNode, self).__init__("String")


class IntegerTypeNode(TypeNode):
    def __init__(self):
        super(IntegerTypeNode, self).__init__("Int")


class ObjectTypeNode(TypeNode):
    def __init__(self):
        super(ObjectTypeNode, self).__init__("Object")


class VoidTypeNode(TypeNode):
    def __init__(self):
        super(VoidTypeNode, self).__init__("Void")


class ClassDef(DeclarationNode):
    def __init__(self, idx, features, line, colum, parent="Object"):
        self.idx: str = idx
        self.features: List[Union[MethodDef, AttributeDef]] = features
        self.parent: str = parent
        self.line = line
        self.column = colum - len(idx)


class VariableCall(ExpressionNode):
    def __init__(self, idx, line, column):
        self.idx: str = idx
        self.line = line
        self.column = column


class GreaterThanNode(BinaryNode):
    def __init__(self, left, right, line, column):
        super(GreaterThanNode, self).__init__(left, right, line, column)


class LowerThanNode(BinaryNode):
    def __init__(self, left, right, line, column):
        super(LowerThanNode, self).__init__(left, right, line, column)


class EqualToNode(BinaryNode):
    def __init__(self, left, right, line, column):
        super().__init__(left, right, line, column)


class LowerEqual(BinaryNode):
    def __init__(self, left, right, line, column):
        super().__init__(left, right, line, column)


class GreaterEqualNode(BinaryNode):
    def __init__(self, left, right, line, column):
        super().__init__(left, right, line, column)


class NotNode(AtomicNode):
    def __init__(self, lex, line, column):
        super().__init__(lex)
        self.line = line
        self.column = column


class NegNode(AtomicNode):
    def __init__(self, lex, line, column):
        super().__init__(lex)
        self.line = line
        self.column = column


class InstantiateClassNode(ExpressionNode):
    def __init__(self, type_, line, column, args=None):
        self.type_: str = type_
        self.args = args
        self.line = line
        self.column = column


class WhileBlockNode(ExpressionNode):
    def __init__(self, cond, statements):
        self.cond: ExpressionNode = cond
        self.statements: ExpressionNode = statements


class ActionNode(ExpressionNode):
    def __init__(self, idx, typex, expresion, line, column):
        self.actions: ExpressionNode = expresion
        self.idx: str = idx
        self.typex: str = typex
        self.line = line
        self.column = column


class CaseNode(ExpressionNode):
    def __init__(self, expression, actions, line, column):
        self.expression: ExpressionNode = expression
        self.actions: List[ActionNode] = actions
        self.line = line
        self.column = column


class BlockNode(ExpressionNode):
    def __init__(self, expressions, line, column):
        self.expressions: List[ExpressionNode] = expressions
        self.line = line
        self.column = column


class IsVoidNode(ExpressionNode):
    def __init__(self, expr):
        self.expr: ExpressionNode = expr


class SelfNode(ExpressionNode):
    def __init__(self, line, column) -> None:
        self.line = line
        self.column = column