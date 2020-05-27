from .CIL.cil import ast_to_cil


def generate_code(ast):
    cil_ast = ast_to_cil(ast)
    return str(cil_ast)
