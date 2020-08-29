import visitor
import ast_nodes as AST
from semantic import SemanticError
from semantic import Attribute, Method, Type, IntType, StringType, IOType, BoolType, ObjectType
from semantic import ErrorType
from semantic import Context

WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'


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
            self.visit(klass)

    @visitor.when(AST.Class)
    def visit(self, node):
        try:
            self.context.create_type(node.name)
        except SemanticError as e:
            self.errors.append(e.text)


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(AST.Program)
    def visit(self, node):
        for c in node.classes:
            self.visit(c)

    @visitor.when(AST.Class)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.name)
            if node.parent:
                self.current_type.set_parent(
                    self.context.get_type(node.parent))
                self.context.graph[node.parent].append(node.name)

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
                param_types.append(self.context.get_type(p.param_type))
            return_type = self.context.get_type(node.return_type)
            self.current_type.define_method(
                node.name, param_names, param_types, return_type)
        except SemanticError as e:
            self.errors

    @visitor.when(AST.AttributeInit)
    def visit(self, node):
        try:
            self.current_type.define_attribute(
                node.name, self.context.get_type(node.type))
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(AST.AttributeDef)
    def visit(self, node):
        try:
            self.current_type.define_attribute(
                node.name, self.context.get_type(node.type))
        except SemanticError as e:
            self.errors.append(e)

class InheritanceChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
        self.visited = {} #types visited in the graph by the DFS
        for t in self.context.graph.keys():
            self.visited[t] = False

    def detect_cycles(self):
        self.visit_component('Object')
        for t in self.visited.keys():
            if not self.visited[t]: # type t is part of another component in the graph 
                self.errors.append("The graph of types is not a tree")
                return
                
    def visit_component(self, node):
        if not self.visited[node]: 
            self.visited[node] = True
            for t in self.context.graph[node]:
                    self.visit_component(t)
       
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(AST.Program)
    def visit(self, node):
        scope = Scope()
        self.detect_cycles()
        for c in node.classes:
            self.visit(c, scope.create_child())

    @visitor.when(AST.Class)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.name)
        pass
        


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
    
        pass

    @visitor.when(AST.AttributeInit)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.AttributeDef)
    def visit(self, node, scope):
        pass

    @visitor.when(AST.ClassMethod)
    def visit(self, node, scope):
        # self.current_method
        pass

    @visitor.when(AST.FormalParameter)
    def visit(self, node, scope):
        pass

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
        print(context)

        #'=============== CHECKING INHERITANCE ============='
        checker1 = InheritanceChecker(context, self.errors)
        checker1.detect_cycles()
        
       



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
