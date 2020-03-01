class Node:
    pass


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class ProgramNode(Node):
    def __init__(self, class_list):
        self.class_list = class_list

    def check_semantics(self, deep=1):
        from travels import typecollector, typebuilder, inference
        # recolectar los tipos
        type_collector = typecollector.TypeCollector()
        type_collector.visit(self)

        # Construir los tipos detectados en el contexto
        type_builder = typebuilder.TypeBuilder(type_collector.context,
                                               type_collector.errors)
        type_builder.visit(self)
        errors = type_builder.errors
        if not errors:
            inferer = inference.TypeInferer(type_builder.context,
                                            errors=errors)
            scope = None
            for d in range(1, deep + 1):
                print(d)
                scope = inferer.visit(self, scope=scope, deep=d)
                print(scope)
        # reportar los errores
        return errors, type_builder.context


class MethodDef(DeclarationNode):
    def __init__(self, idx, param_list, return_type, statements):
        self.idx = idx
        self.param_list = param_list
        self.return_type = return_type
        self.statements = statements


class AttributeDef(DeclarationNode):
    def __init__(self, idx, typex, default_value=None):
        self.idx = idx
        self.typex = typex
        self.default_value = default_value


class Param(DeclarationNode):
    def __init__(self, idx, typex):
        self.id, self.type = idx, typex


class VariableDeclaration(DeclarationNode):
    def __init__(self, var_list, block_statements=None):
        self.var_list = var_list
        self.block_statements = block_statements


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left, self.right = left, right


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex


class IfThenElseNode(ExpressionNode):
    def __init__(self, cond, expr1, expr2):
        self.cond = cond
        self.expr1 = expr1
        self.expr2 = expr2


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
        self.obj = obj
        self.id = idx
        self.args = arg_list


class ParentFuncCall(ExpressionNode):
    def __init__(self, obj, parent_type, idx, arg_list):
        self.obj = obj
        self.parent_type = parent_type
        self.idx = idx
        self.arg_list = arg_list


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.idx = idx
        self.expr = expr


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
        super(FalseConstant, self).__init__('false')


class TrueConstant(AtomicNode):
    def __init__(self):
        super(TrueConstant, self).__init__('true')


class StringTypeNode(TypeNode):
    def __init__(self):
        super(StringTypeNode, self).__init__('string')


class IntegerTypeNode(TypeNode):
    def __init__(self):
        super(IntegerTypeNode, self).__init__('int')


class ObjectTypeNode(TypeNode):
    def __init__(self):
        super(ObjectTypeNode, self).__init__('object')


class VoidTypeNode(TypeNode):
    def __init__(self):
        super(VoidTypeNode, self).__init__('void')


class ClassDef(DeclarationNode):
    def __init__(self, idx, features, parent='object'):
        self.idx = idx
        self.features = features
        self.parent = parent


class VariableCall(ExpressionNode):
    def __init__(self, idx):
        self.idx = idx


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
        self.type_ = type_
        self.args = args


class WhileBlockNode(ExpressionNode):
    def __init__(self, cond, statements):
        self.cond = cond
        self.statements = statements


class ActionNode(ExpressionNode):
    def __init__(self, idx, typex, expresion):
        self.actions = expresion
        self.idx = idx
        self.typex = typex


class CaseNode(ExpressionNode):
    def __init__(self, expression, actions):
        self.expression = expression
        self.actions = actions


class BlockNode(ExpressionNode):
    def __init__(self, expressions):
        self.expressions = expressions


class IsVoidNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr
