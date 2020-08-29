import visitor
import ast_nodes as AST
from semantic import SemanticError
from semantic import Attribute, Method, Type, IntType, StringType, IOType, BoolType, ObjectType
from semantic import ErrorType
from semantic import Context
from semantic import Scope


WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
PARAM_ALREADY_DEFINED = 'Parameter "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
BUILTIN_TYPES = ['Object', 'Int', 'String', 'Bool', 'IO']


class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(AST.Program)
    def visit(self, node):
        self.context = Context()
        self.context.create_builtin_types()
        for klass in node.classes:
            if klass.name in BUILTIN_TYPES:
                self.errors.append("Is an error redefine a builint type")
            else:
                self.visit(klass)

    @visitor.when(AST.Class)
    def visit(self, node):
        try:
            self.context.create_type(node)
        except SemanticError as e:
            self.errors.append(e.text)


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
        self.sort = []  # topologic sort for all types defined
        # types visited in the graph by the DFS
        self.visited = {key: False for key in self.context.graph.keys()}

    def visit_component(self, actual_type):
        self.sort.append(actual_type)
        for children in self.context.graph[actual_type]:
            self.visit_component(children)

    def topologic_sort(self):
        indeg = {key: 0 for key in self.context.graph.keys()}
        for u in self.context.graph.keys():
            for v in self.context.graph[u]:
                indeg[v] += 1

        roots = [key for key in indeg.keys() if indeg[key] == 0]
        if len(roots) > 1:
            self.errors.append("The graph of types is not a tree")
        for v in roots:
            self.visit_component(v)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(AST.Program)
    def visit(self, node):
        self.topologic_sort()
        for t in self.sort:
            if t not in BUILTIN_TYPES:
                try:
                    class_node = self.context.classes[t]
                except KeyError:
                    self.errors.append("The class {} not exist".format(t))
                else:
                    self.visit(class_node)

    @visitor.when(AST.Class)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.name)
            if node.parent:
                try:
                    parent = self.context.get_type(node.parent)
                except SemanticError:
                    parent = ErrorType()
                    self.current_type.set_parent(parent)
                else:
                    if parent.name in ['Int', 'String', 'Bool']:
                        parent = ErrorType()
                        self.errors.append(
                            "Type {} inherits from a builint type".format(node.name))
                    self.current_type.set_parent(parent)

            for f in node.features:
                self.visit(f)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(AST.ClassMethod)
    def visit(self, node):
        try:
            param_names = []
            param_types = []
            for p in node.params:
                param_names.append(p.name)
                try:
                    param_type = self.context.get_type(p.param_type)
                except SemanticError:
                    param_type = ErrorType()
                    self.errors.append("The type of param {} in method {} not exist, in the class {}.".format(
                        p.name, node.name, self.current_type.name))
                param_types.append(param_type)

            try:
                return_type = self.context.get_type(node.return_type)
            except SemanticError:
                return_type = ErrorType()
                self.errors.append("The return type {} in method {} not exist, in the class {}.".format(
                    node.return_type, node.name, self.current_type.name))

            self.current_type.define_method(
                node.name, param_names, param_types, return_type)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(AST.AttributeInit)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError:
            attr_type = ErrorType()
            self.errors.append("The type of attr {} in class {} not exist.".format(
                node.name, self.current_type.name))

        self.current_type.define_attribute(node.name, attr_type)

    @visitor.when(AST.AttributeDef)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError:
            attr_type = ErrorType()
            self.errors.append("The type of attr {} in class {} not exist.".format(
                node.name, self.current_type.name))

        self.current_type.define_attribute(node.name, attr_type)


class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Program)
    def visit(self, node, scope=None):
        scope = Scope()
        for c in node.classes:
            self.visit(c, scope.create_child())

    @visitor.when(AST.Class)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.name)
        scope.define_variable('self', self.current_type)

        for feature in node.features:
            self.visit(feature, scope)

    @visitor.when(AST.AttributeInit)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()

        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type

        if not expr_type.conforms_to(node_type):
            self.errors.append(INCOMPATIBLE_TYPES.replace(
                '%s', expr_type.name, 1).replace('%s', node_type.name, 1))

        scope.define_variable(node.name, node_type)

    @visitor.when(AST.AttributeDef)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()

        scope.define_variable(node.name, node_type)

    @visitor.when(AST.ClassMethod)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.name)
        method_scope = scope.create_child()

        for param in node.params:
            self.visit(param, method_scope)

        for e in node.expr:
            self.visit(e, method_scope)

        last_expr = node.expr[-1]
        last_expr_type = last_expr.computed_type

        if not last_expr_type.conforms_to(node.return_type):
            self.errors.append(INCOMPATIBLE_TYPES.replace(
                '%s', last_expr_type.name, 1).replace('%s', node.return_type.name, 1))

    @visitor.when(AST.FormalParameter)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()

        if not scope.is_local(node.name):
            scope.define_variable(node.name, node_type)
        else:
            self.errors.append(PARAM_ALREADY_DEFINED.replace(
                '%s', node.name, 1).replace('%s', self.current_method.name, 1))

    @visitor.when(AST.DynamicCall)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.StaticCall)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Arg)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Case)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Action)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.If)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.While)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Block)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Let)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.LetVarInit)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.LetVarDef)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.NewType)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.IsVoid)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Sum)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Sub)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Mult)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Div)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.LogicalNot)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.LessThan)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.LessOrEqualThan)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Equals)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Not)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Object)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.SELF)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.INTEGER)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.STRING)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.Boolean)
    def visit(self, node, scope):
        pass


class SemanticAnalyzer:
    def __init__(self, ast, *args, **kwargs):
        self.ast = ast
        self.errors = []

    def analyze(self):
        #'============== COLLECTING TYPES ==============='
        collector = TypeCollector(self.errors)
        collector.visit(self.ast)
        context = collector.context

        # #'=============== BUILDING TYPES ================'
        builder = TypeBuilder(context, self.errors)
        builder.visit(self.ast)

        #'=============== CHECKING TYPES ================'
        # checker = TypeChecker(context, self.errors)
        # scope = checker.visit(self.ast)


if __name__ == '__main__':
    import sys
    from parser import Parser

    parser = Parser()

    if len(sys.argv) > 1:

        input_file = sys.argv[1]
        with open(input_file, encoding="utf-8") as file:
            cool_program_code = file.read()

        parse_result = parser.parse(cool_program_code)

        if parser.errors:
            print(parser.errors[0])
            exit(1)

        semantic_analyzer = SemanticAnalyzer(parse_result)
        semantic_analyzer.analyze()

        for e in semantic_analyzer.errors:
            print(e)
