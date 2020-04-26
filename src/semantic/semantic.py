from errors import add_semantic_error
from lexer_parser.ast import *
from .types import *


class Visitor:
    def __init__(self, current_class):
        self.CurrentClass = current_class

    def visit(self, node):
        pass


def __check_type_declaration__(node: ProgramNode):
    for c in node.classes:
        try:
            _ = TypesByName[c.type]
            add_semantic_error(0, 0, f'duplicated declaration of type {c.type}')
            return False
        except KeyError:
            TypesByName[c.type] = CoolType(c.type, None)
    return True


def __check_type_hierarchy__(node: ProgramNode):
    for c in node.classes:
        cType = TypesByName[c.type]
        if c.parent_type:
            try:
                cType.parent = TypesByName[c.parent_type]
            except KeyError:
                add_semantic_error(0, 0, f'unknown parent type {c.parent_type}')
                return False
        else:
            cType.parent = ObjectType
    return True


def __check_inherits__(type_a: CoolType, type_b: CoolType):
    """
    Return True if type_a <= typeB
    """
    current = type_a
    while current != type_b:
        if current is None:
            return False
        current = current.parent
    return True


class ProgramVisitor(Visitor):
    def __init__(self):
        super().__init__(None)

    def visit(self, node: ProgramNode):
        if not (__check_type_declaration__(node) and __check_type_hierarchy__(node)):
            return
        # Check Main class exists
        try:
            TypesByName['Main']
        except KeyError:
            add_semantic_error(0, 0, f'Main class undeclared')
            return
        # Initialize MethodEnv
        for c in node.classes:
            classType = TypesByName[c.type]
            for f in c.feature_nodes:
                if type(f) is DefFuncNode:
                    # Add all functions to types
                    functionArgsTypeNames = [a[1] for a in f.params]
                    functionArgsType = []
                    for type_name in functionArgsTypeNames:
                        # Check all argument types
                        try:
                            functionArgsType.append(TypesByName[type_name])
                        except KeyError:
                            add_semantic_error(0, 0, f'unknown type {type_name}')
                            return
                    # Check returned type
                    try:
                        returnType = TypesByName[f.return_type]
                    except KeyError:
                        add_semantic_error(0, 0, f'unknown type {f.return_type}')
                        return
                    try:
                        _ = classType.methods[f.id]
                        # Duplicated method declaration in same class, not overload allowed
                        add_semantic_error(0, 0, f'method {f.id} already declared in class {classType.name}')
                    except KeyError:
                        classType.methods[f.id] = CoolTypeMethod(f.id, functionArgsType, returnType)
                elif type(f) is DefAttrNode:
                    # Add all attributes to types
                    try:
                        _ = classType.attributes[f.id]
                        add_semantic_error(0, 0, f'attribute {f.id} already declared')
                    except KeyError:
                        try:
                            attrType = TypesByName[f.type]
                        except KeyError:
                            add_semantic_error(0, 0, f'unknown type {f.type}')
                            return
                        classType.attributes[f.id] = CoolTypeAttribute(f.id, attrType)

        # Visit each class inside
        for c in node.classes:
            c.accept(DefClassVisitor())


class DefClassVisitor(Visitor):
    def __init__(self):
        super().__init__(None)

    def visit(self, node: DefClassNode):
        self.CurrentClass = TypesByName[node.type]
        # Check all features
        for feature in node.feature_nodes:
            if type(feature) is DefAttrNode:
                feature.accept(DefAttrVisitor(self.CurrentClass))
            if type(feature) is DefFuncNode:
                feature.accept(DefFuncVisitor(self.CurrentClass))


class DefAttrVisitor(Visitor):
    def __init__(self, current_class):
        super().__init__(current_class)

    def visit(self, node: DefAttrNode):
        if node.expr:
            expr_type = node.expr.accept(DefExpressionVisitor(self.CurrentClass))
            attr_type = self.CurrentClass.attributes[node.id].attrType
            if not __check_inherits__(expr_type, attr_type):
                add_semantic_error(0, 0, f'Invalid type {expr_type}')
            else:
                return attr_type


class DefFuncVisitor(Visitor):
    def __init__(self, current_class):
        super().__init__(current_class)

    def visit(self, node: DefFuncNode):
        body_type = node.expressions.accept(DefExpressionVisitor(self.CurrentClass))
        return_type = TypesByName[node.return_type]
        if __check_inherits__(body_type, return_type):
            return return_type
        elif body_type is not None:
            add_semantic_error(0, 0, f'invalid returned type {body_type}')


class DefExpressionVisitor(Visitor):
    def __init__(self, current_class):
        super().__init__(current_class)

    def visit(self, node):
        if type(node) is IntNode:
            return IntType
        if type(node) is StringNode:
            return StringType
        if type(node) is BoolNode:
            return BoolType
        if type(node) is VarNode:
            try:
                return self.CurrentClass.attributes[node.id].attrType
            except KeyError:
                add_semantic_error(0, 0, f'invalid variable {node.id}')
                return None
        if type(node) is AssignNode:
            try:
                varType = self.CurrentClass.attributes[node.id].attrType
            except KeyError:
                add_semantic_error(0, 0, f'invalid variable {node.id}')
                return None
            expressionType = node.accept(DefExpressionVisitor(self.CurrentClass))
            if __check_inherits__(expressionType, varType):
                return varType
            else:
                return None


def semantic_check(node):
    if type(node) is ProgramNode:
        node.accept(ProgramVisitor())
