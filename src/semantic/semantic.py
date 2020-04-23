from errors import add_semantic_error
from lexer_parser.ast import *
from .types import *


class Visitor:
    def __init__(self, method_env, object_env, current_class):
        self.MethodEnv = method_env
        self.ObjectEnv = object_env
        self.CurrentClass = current_class

    def visit(self, node):
        pass


def __check_type_declaration__(node: ProgramNode):
    for c in node.classes:
        if c.type in Types:
            add_semantic_error(0, 0, f'duplicated declaration of type {c.type}')
            return False
        else:
            Types.append(c.type)
    return True


def __check_type_hierarchy__(node: ProgramNode):
    for c in node.classes:
        if c.parent_type:
            if c.parent_type in Types:
                TypesHierarchy[c.type] = c.parent_type
            else:
                add_semantic_error(0, 0, f'unknown parent type {c.parent_type}')
                return False
        else:
            TypesHierarchy[c.type] = ObjectType
    return True


class ProgramVisitor(Visitor):
    def __init__(self):
        super().__init__({}, {}, None)

    def visit(self, node: ProgramNode):
        if not (__check_type_declaration__(node) and __check_type_hierarchy__(node)):
            return
        # Initialize MethodEnv
        for c in node.classes:
            className = c.type
            for f in c.feature_nodes:
                if type(f) is DefFuncNode:
                    functionName = f.id
                    functionArgsType = [a[1] for a in f.params]
                    self.MethodEnv[className, functionName] = functionArgsType

        # Visit each class inside
        for c in node.classes:
            c.accept(DefClassVisitor(self.MethodEnv))


class DefClassVisitor(Visitor):
    def __init__(self, method_env):
        super().__init__(method_env, {}, None)

    def visit(self, node: DefClassNode):
        # Set current class name
        self.CurrentClass = node.type
        # Initialize ObjectEnv
        for feature in node.feature_nodes:
            if type(feature) is DefAttrNode:
                self.ObjectEnv[feature.id] = feature.type
        # Check all features
        for feature in node.feature_nodes:
            if type(feature) is DefAttrNode:
                feature.accept(DefAttrVisitor(self.MethodEnv, self.ObjectEnv, self.CurrentClass))
            if type(feature) is DefFuncNode:
                feature.accept(DefFuncVisitor(self.MethodEnv, self.ObjectEnv, self.CurrentClass))


class DefAttrVisitor(Visitor):
    def __init__(self, method_env, object_env, current_class):
        super().__init__(method_env, object_env, current_class)

    def visit(self, node: DefAttrNode):
        if node.expr:
            expr_type = node.expr.accept(DefExpressionVisitor(self.MethodEnv, self.ObjectEnv, self.CurrentClass))
            if expr_type != self.ObjectEnv[node.id]:
                add_semantic_error(0, 0, f'Invalid type {expr_type}')


class DefFuncVisitor(Visitor):
    def __init__(self, method_env, object_env, current_class):
        super().__init__(method_env, object_env, current_class)

    def visit(self, node: DefFuncNode):
        pass


class DefExpressionVisitor(Visitor):
    def __init__(self, method_env, object_env, current_class):
        super().__init__(method_env, object_env, current_class)

    def visit(self, node):
        if type(node) is IntNode:
            return IntType
        if type(node) is StringNode:
            return StringType


def semantic_check(node):
    if type(node) is ProgramNode:
        node.accept(ProgramVisitor())
