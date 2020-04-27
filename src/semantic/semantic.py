from errors import add_semantic_error
from lexer_parser.ast import *
from .types import *


class Visitor:
    def __init__(self, current_class):
        self.CurrentClass = current_class

    def visit(self, node):
        pass


class ProgramVisitor(Visitor):
    def __init__(self):
        super().__init__(None)

    def visit(self, node: ProgramNode):
        if not (check_type_declaration(node) and check_type_hierarchy(node)):
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
                    result, msg = classType.add_method(f.id, f.params, f.return_type)
                    if not result:
                        add_semantic_error(0, 0, msg)
                elif type(f) is DefAttrNode:
                    # Add all attributes to types
                    result, msg = classType.add_attr(f.id, f.type)
                    if not result:
                        add_semantic_error(0, 0, msg)
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
            if not check_inherits(expr_type, attr_type):
                add_semantic_error(0, 0, f'Invalid type {expr_type}')
            else:
                return attr_type


class DefFuncVisitor(Visitor):
    def __init__(self, current_class):
        super().__init__(current_class)

    def visit(self, node: DefFuncNode):
        body_type = node.expressions.accept(DefExpressionVisitor(self.CurrentClass))
        return_type = type_by_name(node.return_type, self.CurrentClass.name)
        if check_inherits(body_type, return_type):
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
            if check_inherits(expressionType, varType):
                return varType
            else:
                return None
        print(f'Not rule for {type(node)} in DefExpressionVisitor')


def semantic_check(node):
    if type(node) is ProgramNode:
        node.accept(ProgramVisitor())
