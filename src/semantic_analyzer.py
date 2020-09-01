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
WRONG_TYPE = 'Type %s expected'

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
        self.visit(node.instance, scope)
        instance_type = node.instance.computed_type

        try:
            instance_method = instance_type.get_method(node.method)

            if len(node.args) == len(instance_method.param_types):
                for arg, param_type in zip(node.args, instance_method.param_types):
                    self.visit(arg, scope)
                    arg_type = arg.computed_type

                    if not arg_type.conforms_to(param_type):
                        self.errors.append(INCOMPATIBLE_TYPES.replace(
                            '%s', arg_type.name, 1).replace('%s', param_type.name, 1))
            else:
                self.errors.append(
                    f'Method "{instance_method.name}" of "{instance_type.name}" only accepts {len(instance_method.param_types)} argument(s)')

            if instance_method.return_type == 'SELF_TYPE':
                node_type = instance_type
            else:
                try:
                    node_type = self.context.get_type(
                        instance_method.return_type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    node_type = ErrorType()

        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.StaticCall)
    def visit(self, node, scope):
        self.visit(node.instance, scope)
        instance_type = node.instance.computed_type

        try:
            static_type = self.context.get_type(node.static_type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            static_type = ErrorType()

        if not instance_type.conforms_to(static_type):
            self.errors.append(INCOMPATIBLE_TYPES.replace(
                '%s', instance_type.name, 1).replace('%s', static_type.name, 1))

        try:
            method = static_type.get_method(node.method)

            if len(node.args) == len(method.param_types):
                for arg, param_type in zip(node.args, method.param_types):
                    self.visit(arg, scope)
                    arg_type = arg.computed_type

                    if not arg_type.conforms_to(param_type):
                        self.errors.append(INCOMPATIBLE_TYPES.replace(
                            '%s', arg_type.name, 1).replace('%s', param_type.name, 1))
            else:
                self.errors.append(
                    f'Method "{method.name}" of "{static_type.name}" only accepts {len(method.param_types)} argument(s)')

            if instance_method.return_type == 'SELF_TYPE':
                node_type = instance_type
            else:
                try:
                    node_type = self.context.get_type(
                        instance_method.return_type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    node_type = ErrorType()

        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.AssignExpr)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node_type = node.expr.computed_type

        if scope.is_defined(node.name):
            var = scope.find_variable(node.name)

            if var.name == 'self':
                self.errors.append(SELF_IS_READONLY)
                node_type = ErrorType()
            elif not node_type.conforms_to(var.type):
                self.errors.append(INCOMPATIBLE_TYPES.replace(
                    '%s', node_type.name, 1).replace('%s', var.type.name, 1))
                node_type = ErrorType()

        else:
            self.errors.append(VARIABLE_NOT_DEFINED.replace(
                '%s', node.name, 1).replace('%s', self.current_method.name, 1))
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.Case)
    def visit(self, node, scope):
        action_expr_types = []
        for action in node.actions:
            self.visit(action, scope.create_child())
            action_expr_types.append(action.computed_type)
        t_0 = action_expr_types.pop(0)
        node.computed_type = t_0.multiple_join(action_expr_types)

    @visitor.when(AST.Action)
    def visit(self, node, scope):
        try:
            action_type = self.context.get_type(node.action_type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            action_type = ErrorType()

        scope.define_variable(node.name, action_type)

        self.visit(node.body)
        node.computed_type = node.body.computed_type

    @visitor.when(AST.If)
    def visit(self, node, scope):
        self.visit(node.predicate, scope)
        predicate_type = node.predicate.computed_type

        if predicate_type.name != 'Bool'
        self.errors.append(WRONG_TYPE.replace('%s', 'Bool', 1))

        self.visit(node.then_body, scope)
        then_type = node.then_body.computed_type
        self.visit(node.else_body, scope)
        else_type = node.else_body.computed_type

        node.computed_type = then_type.join(else_type)

    @visitor.when(AST.While)
    def visit(self, node, scope):
        self.visit(node.predicate, scope)
        predicate_type = node.predicate.computed_type

        if predicate_type.name != 'Bool'
        self.errors.append(WRONG_TYPE.replace('%s', 'Bool', 1))

        self.visit(node.body, scope)

        node.computed_type = self.context.get_type('Object')

    @visitor.when(AST.Block)
    def visit(self, node, scope):
        for expr in node.exprs:
            self.visit(expr, scope)

        node.computed_type = node.exprs[-1].computed_type

    @visitor.when(AST.Let)
    def visit(self, node, scope):
        let_scope = scope.create_child()

        for var in node.var_list:
            self.visit(var, let_scope)

        self.visit(node.body, let_scope)

        node.computed_type = node.body.computed_type

    @visitor.when(AST.LetVarInit)
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

        if scope.is_local(node.name):
            scope.remove_local(node.name)

        scope.define_variable(node.name, node_type)

    @visitor.when(AST.LetVarDef)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()

        if scope.is_local(node.name):
            scope.remove_local(node.name)

        scope.define_variable(node.name, node_type)

    @visitor.when(AST.NewType)
    def visit(self, node, scope):
        if node.type == 'SELF_TYPE':
            node.computed_type = scope.find_variable('self').type
        else:
            try:
                node_type = self.context.get_type(node.type)
            except SemanticError as ex:
                self.errors.append(ex.text)
                node_type = ErrorType()
            node.computed_type = node_type

    @visitor.when(AST.IsVoid)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.computed_type = self.context.get_type('Bool')

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
