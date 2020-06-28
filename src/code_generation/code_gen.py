"""
Copyright (c) 2020 School of Math and Computer Science, University of Havana

COOL compiler project
"""

from .CIL import ast_to_cil
from .MIPS import program_to_mips_visitor


def generate_code(ast):
    cil_ast = ast_to_cil(ast)
    mips_program = program_to_mips_visitor(cil_ast)
    return str(mips_program)
