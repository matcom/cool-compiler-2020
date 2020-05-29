from . import ast as mips

__TYPES_CODES__ = {}


def init_types_codes(types):
    """
    Objects in MIPS code are memory space, therefore we need to know the type 
    of this object. But we cannot save the type name, therefore, we configure 
    a unique number for each type which will be identified in MIPS.
    """
    for i, t in enumerate(types):
        __TYPES_CODES__[t] = i


def get_type_code(type):
    """
    If the type is valid, it returns the number that identifies that type in 
    MIPS. In other case, returns None.
    """
    try:
        return __TYPES_CODES__[type]
    except KeyError:
        return None


def get_type_size(type):
    """
    The size of the any type in memory is size of they attributes and one space
    more for save the type identifier.Each attribute needs 4 bytes of space and 
    the type identifier also.
    """
    return (len(type.attributes) + 1) * 4


def save_callee_registers():
    code=allocate_stack(40)
    for i in range(8):
        code+=push_stack(f'$s{i}', (7-i)*4)
    code+=push_stack('$fp', 4)
    code+=push_stack('$ra')
    return code  
    

def save_caller_registers():
    code=allocate_stack(40)
    for i in range(10):
        code+=push_stack(f'$t{i}', (9-i)*4)
        
    return code


def restore_callee_registers():
    code=[]
    for i in range(8):
        code+=peek_stack(f'$s{i}', (7-i)*4)
    code+=peek_stack('$fp', 4)
    code+=peek_stack('$ra')
    code+=restore_stack(40)
    return code


def restore_caller_registers():
    code=[]
    for i in range(10):
        code+=peek_stack(f'$t{i}', (9-i)*4)
    code+=restore_stack(40)
    return code


def restore_stack(bytes):
    return [mips.AdduInstruction('$sp', '$sp', bytes)]


def allocate_stack(bytes):
    return [mips.SubuInstruction('$sp', '$sp', bytes)]


def push_stack(src, pos=0):
    if pos:
        return [mips.SwInstruction(src, f'{pos}($sp)')]
    return [mips.SwInstruction(src, '($sp)')]


def peek_stack(src, pos=0):
    if pos:
        return [mips.LwInstruction(src, f'{pos}($sp)')]
    return [mips.LwInstruction(src, '($sp)')]
