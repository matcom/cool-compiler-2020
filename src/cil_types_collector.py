import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILTypesCollector:
    def __init__(self, cil_ast):
        self.cil_ast = cil_ast