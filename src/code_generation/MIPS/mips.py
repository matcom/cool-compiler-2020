from code_generation.CIL import ast as cil
from . import ast as mips

__METHOD_MAPPING__={}
__ADDRS__= {}

def save_caller_registers():
    pass

def save_callee_registers():
    pass

def restore_caller_registers():
    pass

def restore_callee_registers():
    pass

def push_stack(src):
    pass
    
    

def program_to_mips_visitor(program:cil.ProgramNode):
    global __METHOD_MAPPING__
    
    #filling method mapping
    for t in program.types:
        for m in t.methods:
            __METHOD_MAPPING__[(t,m)]=t.methods[m]
            
    data_section=[f'{d.id}: .asciiz \"{d.val}\"' for d in program.data].join('\n')
    #continue
    
def vcall_to_mips_visitor(vcall:cil.VCAllNode):
    return save_caller_registers() + [mips.JalNode(__METHOD_MAPPING__[(vcall.type, vcall.method)])] + restore_caller_registers() + [mips.Move('v0',__ADDRS__[vcall.result])]
