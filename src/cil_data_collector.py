import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILDataCollector:
    def __init__(self, cil_ast, context):
        self.cil_ast = cil_ast
        self.context = context

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(COOL_AST.Program)
    def visit(self, node):
        self.cil_ast.data["Object"] = "object_type_name"
        
        for klass in node.classes:
            self.visit(klass)
    
    @visitor.when(COOL_AST.Class)
    def visit(self, node):
        for feature in node.features:
            self.visit(feature)
    
    @visitor.when(COOL_AST.AttributeInit)
    def visit(self, node):
        self.visit(node.expr)
    
    @visitor.when(COOL_AST.ClassMethod)
    def visit(self, node):
        self.visit(node.expr)

    @visitor.when(COOL_AST.DynamicCall)
    def visit(self, node):
        for arg in node.args:
            self.visit(arg)
    
    @visitor.when(COOL_AST.STRING)
    def visit(self, node):
        if node.value not in self.cil_ast.data:
            self.cil_ast.data[node.value] = f's{len(self.cil_ast.data)}'