from code_generation.MIPS import ast as mips


__TYPES__ = {}
__ADDRS__ = {}


def init_types(types):
    """
    Objects in MIPS code are memory space (size_mips), therefore we need to know the type 
    of this object. But we cannot save the type name, therefore, we configure 
    a unique number for each type which will be identified in MIPS (code_mips)\n

    """
    for i, t in enumerate(types):
        t.code_mips = i
        t.size_mips = (len(t.attributes) + 1) * 4
        t.size_vt = (len(t.methods) + 1) * 4
        t.attr_index_mips = {}
        for i, a in enumerate(t.attributes):
            t.attr_index_mips[a] = i + 1
        __TYPES__[t.type] = t


def get_type(name):
    try:
        return __TYPES__[name]
    except KeyError:
        return None


def save_callee_registers():
    code = allocate_stack(40)
    n = 8
    for i in range(n):
        pos = (n-1-i)*4
        if pos:
            code += push_stack(f'$s{i}', f'{pos}($sp)')
        else:
            code += push_stack(f'$s{i}', '($sp)')
    code += push_stack('$fp', f'4($sp)')
    code += push_stack('$ra', '($sp)')
    return code


def save_caller_registers():
    code = allocate_stack(40)
    n = 10
    for i in range(n):
        pos = (n-1-i)*4
        if pos:
            code += push_stack(f'$t{i}', f'{pos}($sp)')
        else:
            code += push_stack(f'$t{i}', '($sp)')

    return code


def restore_callee_registers():
    code = []
    n = 8
    for i in range(n):
        pos = (n-1-i)*4
        if pos:
            code += peek_stack(f'$s{i}', f'{pos}($sp)')
        else:
            code += peek_stack(f'$s{i}', '($sp)')
    code += peek_stack('$fp', '4($sp)')
    code += peek_stack('$ra', '($sp)')
    code += restore_stack(40)
    return code


def restore_caller_registers():
    code = []
    n = 10
    for i in range(n):
        pos = (n-1-i)*4
        code += peek_stack(f'$t{i}', f'{pos}($sp)')
    code += restore_stack(40)
    return code


def restore_stack(bytes):
    return [mips.AdduInstruction('$sp', '$sp', bytes)]


def allocate_stack(bytes):
    return [mips.SubuInstruction('$sp', '$sp', bytes)]


def push_stack(src, pos):
    code = []
    if src[0] != '$':
        code = peek_stack('$t0', src)
        return code+[mips.SwInstruction('$t0', pos)]
    else:
        return code+[mips.SwInstruction(src, pos)]


def peek_stack(src, pos):
    return [mips.LwInstruction(src, pos)]


def restore_addresses():
    __ADDRS__ = {}


def get_address(key):
    try:
        if type(key) is str:
            return __ADDRS__[key]
        return __ADDRS__[key.id]
    except:
        raise Exception('Local not found in stack')


def save_address(key, value):
    if type(value) is int:
        if value:
            __ADDRS__[key] = f'{value}($sp)'
        else:
            __ADDRS__[key] = f'($sp)'

    __ADDRS__[key] = value
