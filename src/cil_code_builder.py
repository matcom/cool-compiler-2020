import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILCodeBuilder:
    def __init__(self, cil_ast, context):
        self.cil_ast = cil_ast
        self.context = context

