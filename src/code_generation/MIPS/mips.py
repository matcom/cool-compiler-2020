from code_generation.CIL import ast as cil

def program_to_mips_visitor(program:cil.ProgramNode):
    data_section=[f'{d.id}: .asciiz \"{d.val}\"' for d in program.data].join('\n')
    
        