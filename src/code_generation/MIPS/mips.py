from code_generation.CIL import ast as cil
from . import ast as mips

__METHOD_MAPPING__ = {}
__ADDRS__ = {}


def save_callee_registers():
    allocate_stack(40)
    for i in range(8):
        push_stack(f'$s{i}', (7-i)*4)
    push_stack('$fp', 4)
    push_stack('$ra')  
    


def save_caller_registers():
    allocate_stack(40)
    for i in range(10):
        push_stack(f'$t{i}', (9-i)*4)


def restore_callee_registers():
    for i in range(8):
        push_stack(f'$s{i}', (7-i)*4)
    pop_stack('$fp', 4)
    pop_stack('$ra')
    restore_stack(40)


def restore_caller_registers():
    for i in range(10):
        pop_stack(f'$t{i}', (9-i)*4)
    restore_stack(40)

def restore_stack(bytes):
    return [mips.AdduInstruction('$sp', '$sp', bytes)]
        
def allocate_stack(bytes):
    return [mips.SubuInstruction('$sp', '$sp', bytes)]

def push_stack(src, pos=0):
    if pos:
        return [mips.SwInstruction(src, f'{pos}($sp)')]
    return [mips.SwInstruction(src, '($sp)')]

def pop_stack(src, pos=0):
    if pos:
        return [mips.LwInstruction(src, f'{pos}($sp)')]
    return [mips.LwInstruction(src, '($sp)')]
        


def program_to_mips_visitor(program: cil.ProgramNode):
    global __METHOD_MAPPING__

    # filling method mapping
    for t in program.types:
        for m in t.methods:
            __METHOD_MAPPING__[(t, m)] = t.methods[m]

    data_section = [mips.AsciizInst(d.val) for d in program.data]
    # continue


def vcall_to_mips_visitor(vcall: cil.VCAllNode):
    return save_caller_registers() + [mips.JalInstruction([__METHOD_MAPPING__[(vcall.type, vcall.method)]])] + restore_caller_registers() + [mips.MoveInstruction(['$v0', __ADDRS__[vcall.result]])]


def arg_to_mips_visitor(arg:cil.ArgNode):
    return allocate_stack(4) + push_stack(__ADDRS__[arg.val])

def param_to_mips_visitor(param:cil.ParamNode):
    return pop_stack(__ADDRS__[param.id]) + restore_stack(4)