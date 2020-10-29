import visitor
import ast_nodes as AST
from semantic import SemanticException, ErrorSemantic
from semantic import Attribute, Method, Type, IntType, StringType, IOType, BoolType, ObjectType
from semantic import ErrorType
from semantic import Context
from semantic import Scope


WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
PARAM_ALREADY_DEFINED = 'Parameter "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined.'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
WRONG_TYPE = 'Type %s expected'
INVALID_SELF_TYPE = 'Invalid use of SELF_TYPE'

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
                error = ErrorSemantic("Is an error redefine a builint type", klass.line, klass.column)
                self.errors.append(error)
            else:
                self.visit(klass)

    @visitor.when(AST.Class)
    def visit(self, node):
        try:
            self.context.create_type(node)
        except SemanticException as e:
            error = ErrorSemantic(e.text, node.line, node.column)
            self.errors.append(error)


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
        self.sort = []  # topologic sort for all types defined
        self.visited = {key: False for key in self.context.graph.keys()} # types visited in the graph by the DFS

    def visit_component(self, actual_type):
        self.sort.append(actual_type)
        self.visited[actual_type] = True
        for children in self.context.graph[actual_type]:
            self.visit_component(children)

    def topologic_sort(self):
        indeg = {key: 0 for key in self.context.graph.keys()}
        for u in self.context.graph.keys():
            for v in self.context.graph[u]:
                indeg[v] += 1

        roots = [key for key in indeg.keys() if indeg[key] == 0]
        if len(roots) > 1:
            error = ErrorSemantic("The graph of types is not a tree", 0, 0)
            self.errors.append(error)
        for v in roots:
            self.visit_component(v)
        
        for t in self.visited:
            if not self.visited[t] and not t in BUILTIN_TYPES:
                class_node = self.context.classes[t]
                error = ErrorSemantic("Exist a cycle that start in type {}".format(t), class_node.line, class_node.column)
                self.errors.append(error)
                break
               

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
                    pass
                else:
                    self.visit(class_node)
        if not self.context.types.__contains__('Main'):
            error = ErrorSemantic("The class Main is not defined", 0, 0)
            self.errors.append(error)
        else:
            if not self.context.types['Main'].methods.__contains__('main'):
                main_node = self.context.classes['Main']
                error = ErrorSemantic("The main method is not defined in class Main", main_node.line, main_node.column)
                self.errors.append(error)


    @visitor.when(AST.Class)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.name)
            if node.parent:
                try:
                    parent = self.context.get_type(node.parent)
                except SemanticException as e:
                    error = ErrorSemantic(e.text, node.line, node.column)
                    self.errors.append(error)
                    parent = ErrorType()
                    self.current_type.set_parent(parent)
                else:
                    if parent.name in ['Int', 'String', 'Bool']:
                        parent = ErrorType()
                        error = ErrorSemantic("Type {} inherits from a builint type".format(node.name), node.line, node.column)
                        self.errors.append(error)
                    self.current_type.set_parent(parent)

            for f in node.features:
                self.visit(f)
        except SemanticException as e:
            error = ErrorSemantic(e.text, node.line, node.column)
            self.errors.append(error)

    @visitor.when(AST.ClassMethod)
    def visit(self, node):
        try:
            param_names = []
            param_types = []
            for p in node.params:
                param_names.append(p.name)
                try:
                    param_type = self.context.get_type(p.param_type)
                except SemanticException:
                    param_type = ErrorType()
                    error = ErrorSemantic("The type of param {} in method {} not exist, in the class {}.".format(
                        p.name, node.name, self.current_type.name), node.line, node.column)
                    self.errors.append(error)
                    
                param_types.append(param_type)

            try:
                return_type = self.context.get_type(node.return_type)
            except SemanticException:
                return_type = ErrorType()
                error = ErrorSemantic("The return type {} in method {} not exist, in the class {}.".format(
                    node.return_type, node.name, self.current_type.name), node.line, node.column)
                self.errors.append(error)

            self.current_type.define_method(
                node.name, param_names, param_types, return_type)
        except SemanticException as e:
            error = ErrorSemantic(e.text, node.line, node.column)
            self.errors.append(error)

    @visitor.when(AST.AttributeInit)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticException:
            attr_type = ErrorType()
            error = ErrorSemantic("The type of attr {} in class {} not exist.".format(
                node.name, self.current_type.name), node.line, node.column)
            self.errors.append(error)

        self.current_type.define_attribute(node.name, attr_type)

    @visitor.when(AST.AttributeDef)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticException:
            attr_type = ErrorType()
            error = ErrorSemantic("The type of attr {} in class {} not exist.".format(
                node.name, self.current_type.name), node.line, node.column)
            self.errors.append(error)

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
        return scope

    @visitor.when(AST.Class)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.name)
        scope.define_variable('self', self.current_type)

        attributes = self.current_type.get_all_attributes()
        for attr in attributes:
            if attr.type.name == 'SELF_TYPE':
                scope.define_variable(attr.name, self.current_type)
            else:
                scope.define_variable(attr.name, attr.type)

        for feature in node.features:
            self.visit(feature, scope)

    @visitor.when(AST.AttributeInit)
    def visit(self, node, scope):
        try:
            node_type = self.current_type.get_attribute(node.name).type
        except SemanticException as ex:
            node_type = ErrorType()
            error =  ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)
         
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type

        if not expr_type.conforms_to(node_type):
            error = ErrorSemantic(INCOMPATIBLE_TYPES.replace(
                '%s', expr_type.name, 1).replace('%s', node_type.name, 1), node.line, node.column)
            self.errors.append(error)

    @visitor.when(AST.AttributeDef)
    def visit(self, node, scope):
        try:
            self.current_type.get_attribute(node.name)
        except SemanticException as ex:
            error = ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)

    @visitor.when(AST.ClassMethod)
    def visit(self, node, scope):
        try:
            self.current_method = self.current_type.get_method(node.name)
        except SemanticException as ex:
            error = ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)
        
        method_scope = scope.create_child()

        for param in node.params:
            self.visit(param, method_scope)

        self.visit(node.expr, method_scope)

        expr_type = node.expr.computed_type

        return_type = self.current_method.return_type

        if expr_type.name == 'SELF_TYPE':
            if not self.current_type.conforms_to(return_type):
                error = ErrorSemantic(INCOMPATIBLE_TYPES.replace(
                    '%s', expr_type.name, 1).replace('%s', self.current_type.name, 1), node.line, node.column)
                self.errors.append(error)
        elif not expr_type.conforms_to(return_type):
            error = ErrorSemantic(INCOMPATIBLE_TYPES.replace(
                '%s', expr_type.name, 1).replace('%s', return_type.name, 1), node.line, node.column)
            self.errors.append(error)


    @visitor.when(AST.FormalParameter)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.param_type)
            if node_type.name == 'SELF_TYPE':
                node_type = ErrorType()
                error = ErrorSemantic(INVALID_SELF_TYPE, node.line, node.column)
                self.errors.append(error)
               
        except SemanticException as ex:
            node_type = ErrorType()
            error = ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)

        if not scope.is_local(node.name):
            scope.define_variable(node.name, node_type)
        else:
            error = ErrorSemantic(PARAM_ALREADY_DEFINED.replace(
                '%s', node.name, 1).replace('%s', self.current_method.name, 1), node.line, node.column)
            self.errors.append(error)

    @visitor.when(AST.DynamicCall)
    def visit(self, node, scope):
        self.visit(node.instance, scope)
        instance_type = node.instance.computed_type

        if instance_type.name == 'SELF_TYPE':
            instance_type = scope.find_variable('self').type
        try:
            instance_method = instance_type.get_method(node.method)

            if len(node.args) == len(instance_method.param_types):
                for arg, param_type in zip(node.args, instance_method.param_types):
                    self.visit(arg, scope)
                    arg_type = arg.computed_type

                    if not arg_type.conforms_to(param_type):
                        error = ErrorSemantic(INCOMPATIBLE_TYPES.replace(
                            '%s', arg_type.name, 1).replace('%s', param_type.name, 1), node.line, node.column)
                        self.errors.append(error)
            else:
                error = ErrorSemantic(f'Method "{instance_method.name}" of "{instance_type.name}" only accepts {len(instance_method.param_types)} argument(s)', node.line, node.column)
                self.errors.append(error)

            if instance_method.return_type.name == 'SELF_TYPE':
                node_type = instance_type
            node_type = instance_method.return_type

        except SemanticException as ex:
            node_type = ErrorType()
            error = ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)
            
        node.computed_type = node_type

    @visitor.when(AST.StaticCall)
    def visit(self, node, scope):
        self.visit(node.instance, scope)
        instance_type = node.instance.computed_type

        try:
            static_type = self.context.get_type(node.static_type)
        except SemanticException as ex:
            static_type = ErrorType()
            error = ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)
         
        if not instance_type.conforms_to(static_type):
            error = ErrorSemantic(INCOMPATIBLE_TYPES.replace(
                '%s', instance_type.name, 1).replace('%s', static_type.name, 1). node.line. node.column)
            self.errors.append(error)

        try:
            method = static_type.get_method(node.method)

            if len(node.args) == len(method.param_types):
                for arg, param_type in zip(node.args, method.param_types):
                    self.visit(arg, scope)
                    arg_type = arg.computed_type

                    if not arg_type.conforms_to(param_type):
                        error = ErrorSemantic(INCOMPATIBLE_TYPES.replace(
                            '%s', arg_type.name, 1).replace('%s', param_type.name, 1), node.line, node.column)
                        self.errors.append(error)
            else:
                error = ErrorSemantic( f'Method "{method.name}" of "{static_type.name}" only accepts {len(method.param_types)} argument(s)', node.line, node.column)
                self.errors.append(error)

            if method.return_type.name == 'SELF_TYPE':
                node_type = instance_type
            node_type = method.return_type

        except SemanticException as ex:
            error = ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.AssignExpr)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node_type = node.expr.computed_type

        if scope.is_defined(node.name):
            var = scope.find_variable(node.name)

            if var.name == 'self':
                error = ErrorSemantic(SELF_IS_READONLY, node.line, node.column)
                self.errors.append(error)
                node_type = ErrorType()
            elif not node_type.conforms_to(var.type):
                error = ErrorSemantic(INCOMPATIBLE_TYPES.replace(
                    '%s', node_type.name, 1).replace('%s', var.type.name, 1), node.line, node.column)
                self.errors.append(error)
                node_type = ErrorType()
        else:
            error = ErrorSemantic(VARIABLE_NOT_DEFINED.replace(
                '%s', node.name, 1), node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.Case)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        action_expr_types = []
        var_declared = []

        for action in node.actions:
            var_type = action.action_type
            if not var_type in var_declared:
                var_declared.append(var_type)
            else:
                error = ErrorSemantic("The type {} is declared in another branch".format(var_type), node.line, node.column)
                self.errors.append(error)
            self.visit(action, scope.create_child())
            action_expr_types.append(action.computed_type)

        t_0 = action_expr_types.pop(0)
        node_type = t_0.multiple_join(action_expr_types)
       
        node.computed_type = node_type

    @visitor.when(AST.Action)
    def visit(self, node, scope):
        try:
            action_type = self.context.get_type(node.action_type)
        except SemanticException as ex:
            error = ErrorSemantic(ex.text, node.line, node.column )
            self.errors.append(error)
            action_type = ErrorType()

        scope.define_variable(node.name, action_type)

        self.visit(node.body, scope)
        node.computed_type = node.body.computed_type

    @visitor.when(AST.If)
    def visit(self, node, scope):
        self.visit(node.predicate, scope)
        predicate_type = node.predicate.computed_type

        if predicate_type.name != 'Bool':
            error = ErrorSemantic(WRONG_TYPE.replace('%s', 'Bool', 1), node.line, node.column)
            self.errors.append(error)

        self.visit(node.then_body, scope)
        then_type = node.then_body.computed_type
        self.visit(node.else_body, scope)
        else_type = node.else_body.computed_type

        node.computed_type = then_type.join(else_type)
  

    @visitor.when(AST.While)
    def visit(self, node, scope):
        self.visit(node.predicate, scope)
        predicate_type = node.predicate.computed_type

        if predicate_type.name != 'Bool':
            error = ErrorSemantic(WRONG_TYPE.replace('%s', 'Bool', 1), node.line, node.column)
            self.errors.append(error)

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
            if node_type.name == 'SELF_TYPE':
                node_type = scope.find_variable('self').type
        except SemanticException as ex:
            error = ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type

        if not expr_type.conforms_to(node_type):
            error = ErrorSemantic(INCOMPATIBLE_TYPES.replace(
                '%s', expr_type.name, 1).replace('%s', node_type.name, 1), node.line, node.column)
            self.errors.append(error)

        if scope.is_local(node.name):
            scope.remove_local(node.name)

        scope.define_variable(node.name, node_type)

    @visitor.when(AST.LetVarDef)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
            if node_type.name == 'SELF_TYPE':
                node_type = scope.find_variable('self').type
        except SemanticException as ex:
            error = ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        if scope.is_local(node.name):
            scope.remove_local(node.name)

        scope.define_variable(node.name, node_type)

    @visitor.when(AST.NewType)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
            if node_type.name == 'SELF_TYPE':
                node_type = scope.find_variable('self').type
        except SemanticException as ex:
            error = ErrorSemantic(ex.text, node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.IsVoid)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.computed_type = self.context.get_type('Bool')

    @visitor.when(AST.ArithmeticBinOp)
    def visit(self, node, scope):
        node_type = self.context.get_type('Int')

        self.visit(node.left, scope)
        left_type = node.left.computed_type

        if left_type.name != 'Int':
            error = ErrorSemantic(WRONG_TYPE.replace('%s', 'Int', 1), node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        self.visit(node.right, scope)
        right_type = node.right.computed_type

        if right_type.name != 'Int':
            error = ErrorSemantic(WRONG_TYPE.replace('%s', 'Int', 1), node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.LogicBinOp)
    def visit(self, node, scope):
        node_type = self.context.get_type('Bool')

        self.visit(node.left, scope)
        left_type = node.left.computed_type

        if left_type.name != 'Int':
            error = ErrorSemantic(WRONG_TYPE.replace('%s', 'Int', 1), node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        self.visit(node.right, scope)
        right_type = node.right.computed_type

        if right_type.name != 'Int':
            error = ErrorSemantic(WRONG_TYPE.replace('%s', 'Int', 1), node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.Not)
    def visit(self, node, scope):
        node_type = self.context.get_type('Bool')

        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type

        if expr_type.name != 'Bool':      
            error = ErrorSemantic(WRONG_TYPE.replace('%s', 'Bool', 1), node.line, node.column)      
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.LogicalNot)
    def visit(self, node, scope):
        node_type = self.context.get_type('Int')

        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type

        if expr_type.name != 'Int':
            error = ErrorSemantic(WRONG_TYPE.replace('%s', 'Int', 1), node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.Equals)
    def visit(self, node, scope):
        node_type = self.context.get_type('Bool')

        self.visit(node.left, scope)
        left_type = node.left.computed_type

        self.visit(node.right, scope)
        right_type = node.right.computed_type

        if (left_type.name in ['Int', 'Bool', 'String'] or right_type.name in ['Int', 'Bool', 'String']) and left_type.name != right_type.name:
            error = ErrorSemantic(WRONG_TYPE.replace('%s', left_type.name, 1), node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.Identifier)
    def visit(self, node, scope):
        if scope.is_defined(node.name):
            node_type = scope.find_variable(node.name).type
        else:
            error = ErrorSemantic(VARIABLE_NOT_DEFINED.replace(
                '%s', node.name, 1), node.line, node.column)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(AST.INTEGER)
    def visit(self, node, scope):
        node.computed_type = self.context.get_type('Int')

    @visitor.when(AST.STRING)
    def visit(self, node, scope):
        node.computed_type = self.context.get_type('String')

    @visitor.when(AST.Boolean)
    def visit(self, node, scope):
        node.computed_type = self.context.get_type('Bool')


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
        checker = TypeChecker(context, self.errors)
        scope = checker.visit(self.ast)

        return context, scope


if __name__ == '__main__':
    import sys
    from cparser import Parser

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
            exit(1)
