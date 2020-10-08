import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILTypesCollector:
    def __init__(self, cil_ast, context):
        self.cil_ast = cil_ast
        self.context = context
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(COOL_AST.Program)
    def visit(self, node):
        for name, type in self.context.types.items():
            x = 0
        # pass