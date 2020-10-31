from typing import List, Optional, Tuple, Union

from abstract.semantics import SemanticError


class Node:
    pass


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class ProgramNode(Node):
    def __init__(self, class_list):
        self.class_list: List[ClassDef] = class_list

    def check_semantics(self, deep=1):
        from travels import typecollector, typebuilder, inference
        # recolectar los tipos
        type_collector = typecollector.TypeCollector()
        type_collector.visit(self)

        # Construir los tipos detectados en el contexto
        assert type_collector.context is not None
        type_builder = typebuilder.TypeBuilder(type_collector.context,
                                               type_collector.errors)
        type_builder.visit(self)

        # Garantizar que exista un tipo Main que contenga un
        # metodo main
        context = type_builder.context
        try:
            context.get_type('Main')
            context.get_type('Main').methods['main']
        except SemanticError as e:
            type_builder.errors.append(str(e))
        except KeyError:
            type_builder.errors.append(
                f"Main class must contain a main method.")

        errors = type_builder.errors
        scope = None
        if not errors:
            inferer = inference.TypeInferer(type_builder.context,
                                            errors=errors)
            for d in range(1, deep + 1):
                scope = inferer.visit(self, scope=scope, deep=d)
        # reportar los errores
        return errors, type_builder.context, scope


class Param(DeclarationNode):
    def __init__(self, idx, typex):
        self.id, self.type = idx, typex


class MethodDef(DeclarationNode):
    def __init__(self, idx: str, param_list: List[Param], return_type: str,
                 statements: List[ExpressionNode]):
        self.idx: str = idx
        self.param_list: List[Param] = param_list
        self.return_type: str = return_type
        self.statements: List[ExpressionNode] = statements


class AttributeDef(DeclarationNode):
    def __init__(self, idx: str, typex: str, default_value=None):
        self.idx: str = idx
        self.typex: str = typex
        self.default_value: Optional[ExpressionNode] = default_value


class VariableDeclaration(ExpressionNode):
    def __init__(self, var_list, block_statements=None):
        self.var_list: List[Tuple[str, str,
                                  Optional[ExpressionNode]]] = var_list
        self.block_statements: Optional[ExpressionNode] = block_statements


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left: ExpressionNode = left
        self.right: ExpressionNode = right


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex


class IfThenElseNode(ExpressionNode):
    def __init__(self, cond, expr1, expr2):
        self.cond: ExpressionNode = cond
        self.expr1: ExpressionNode = expr1
        self.expr2: ExpressionNode = expr2


class PlusNode(BinaryNode):
    def __init__(self, left, right):
        super(PlusNode, self).__init__(left, right)


class DifNode(BinaryNode):
    def __init__(self, left, right):
        super(DifNode, self).__init__(left, right)


class MulNode(BinaryNode):
    def __init__(self, left, right):
        super(MulNode, self).__init__(left, right)


class DivNode(BinaryNode):
    def __init__(self, left, right):
        super(DivNode, self).__init__(left, right)


class FunCall(ExpressionNode):
    def __init__(self, obj, idx, arg_list):
        self.obj: Union[str, ExpressionNode] = obj
        self.id: str = idx
        self.args: List[ExpressionNode] = arg_list


class ParentFuncCall(ExpressionNode):
    def __init__(self, obj, parent_type, idx, arg_list):
        self.obj: ExpressionNode = obj
        self.parent_type: str = parent_type
        self.idx: str = idx
        self.arg_list: List[ExpressionNode] = arg_list


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.idx: str = idx
        self.expr: ExpressionNode = expr


class IntegerConstant(AtomicNode):
    def __init__(self, lex):
        super(IntegerConstant, self).__init__(int(lex))


class StringConstant(AtomicNode):
    def __init__(self, lex):
        super(StringConstant, self).__init__(lex)


class TypeNode(AtomicNode):
    def __init__(self, lex):
        super(TypeNode, self).__init__(lex)


class BoleanNode(TypeNode):
    def __init__(self, val):
        self.val = True if val == 'true' else False


class FalseConstant(AtomicNode):
    def __init__(self):
        super(FalseConstant, self).__init__('False')


class TrueConstant(AtomicNode):
    def __init__(self):
        super(TrueConstant, self).__init__('True')


class StringTypeNode(TypeNode):
    def __init__(self):
        super(StringTypeNode, self).__init__('String')


class IntegerTypeNode(TypeNode):
    def __init__(self):
        super(IntegerTypeNode, self).__init__('Int')


class ObjectTypeNode(TypeNode):
    def __init__(self):
        super(ObjectTypeNode, self).__init__('Object')


class VoidTypeNode(TypeNode):
    def __init__(self):
        super(VoidTypeNode, self).__init__('Void')


class ClassDef(DeclarationNode):
    def __init__(self, idx, features, parent='Object'):
        self.idx: str = idx
        self.features: List[Union[MethodDef, AttributeDef]] = features
        self.parent: str = parent


class VariableCall(ExpressionNode):
    def __init__(self, idx):
        self.idx: str = idx


class GreaterThanNode(BinaryNode):
    def __init__(self, left, right):
        super(GreaterThanNode, self).__init__(left, right)


class LowerThanNode(BinaryNode):
    def __init__(self, left, right):
        super(LowerThanNode, self).__init__(left, right)


class EqualToNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class LowerEqual(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class GreaterEqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class NotNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)


class NegNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)


class InstantiateClassNode(ExpressionNode):
    def __init__(self, type_, args=None):
        self.type_: str = type_
        self.args = args


class WhileBlockNode(ExpressionNode):
    def __init__(self, cond, statements):
        self.cond: ExpressionNode = cond
        self.statements: ExpressionNode = statements


class ActionNode(ExpressionNode):
    def __init__(self, idx, typex, expresion):
        self.actions: ExpressionNode = expresion
        self.idx: str = idx
        self.typex: str = typex


class CaseNode(ExpressionNode):
    def __init__(self, expression, actions):
        self.expression: ExpressionNode = expression
        self.actions: List[ActionNode] = actions


class BlockNode(ExpressionNode):
    def __init__(self, expressions):
        self.expressions: List[ExpressionNode] = expressions


class IsVoidNode(ExpressionNode):
    def __init__(self, expr):
        self.expr: ExpressionNode = expr


class SelfNode(ExpressionNode):
    pass