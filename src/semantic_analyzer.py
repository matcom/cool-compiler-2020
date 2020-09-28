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
BUILINT_TYPES = ['Object', 'Int', 'String', 'Bool', 'IO']

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
            if klass.name in BUILINT_TYPES:
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
        self.sort = []  #topologic sort for all types defined 
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

    def topologic_sort(self, actual_type):
        self.sort.append(actual_type)
        for children in self.context.graph[actual_type]:
            self.topologic_sort(children)


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(AST.Program)
    def visit(self, node):
        self.detect_cycles()
        self.topologic_sort('Object')
        for t in self.sort:
            if t not in BUILINT_TYPES:
                class_node = self.context.classes[t]
                self.visit(class_node)
              
    @visitor.when(AST.Class)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.name)
            if node.parent: #TODO:no heredar de builint excepto IO
                print("current type", node.name, "has parent", node.parent)
                try:
                    parent = self.context.get_type(node.parent)
                except SemanticError:
                    parent = ErrorType()
                    self.current_type.set_parent(parent)
                else: 
                    if parent.name in ['Int', 'String', 'Bool']:
                        parent = ErrorType()
                        self.errors.append("Type {} inherits from a builint type".format(node.name))
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
                param_types.append(self.context.get_type(p.param_type))
            return_type = self.context.get_type(node.return_type)
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
            self.current_type.define_attribute(node.name, attr_type)
            self.errors.append("The type of attr {} in class {} not exist.".format(node.name, self.current_type.name))
        else:
            self.current_type.define_attribute(node.name, attr_type)

    @visitor.when(AST.AttributeDef)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError:
            attr_type = ErrorType()
            self.current_type.define_attribute(node.name, attr_type)
            self.errors.append("The type of attr {} in class {} not exist.".format(node.name, self.current_type.name))
        else:
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
        print(builder.sort)
      

        #'=============== CHECKING INHERITANCE ============='
        # checker1 = InheritanceChecker(context, self.errors)
        # checker1.detect_cycles()
       
        
       



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
