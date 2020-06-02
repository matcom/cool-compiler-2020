from .CIL.cil import ast_to_cil
from .MIPS.mips import program_to_mips_visitor


def generate_code(ast):
    cil_ast = ast_to_cil(ast)
    mips_program = program_to_mips_visitor(cil_ast)
    return str(mips_program)
