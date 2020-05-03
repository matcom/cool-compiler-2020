from  .cil import ast_to_cil
from .code import cil_to_code

def generate_code(ast):
    cil_ast=ast_to_cil(ast)
    return cil_to_code(cil_ast)
    