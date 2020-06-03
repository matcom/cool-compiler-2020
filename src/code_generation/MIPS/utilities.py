from code_generation.MIPS import ast as mips


__TYPES__ = {}


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
    for i in range(8):
        code += push_stack(f'$s{i}', (7-i)*4)
    code += push_stack('$fp', 4)
    code += push_stack('$ra')
    return code


def save_caller_registers():
    code = allocate_stack(40)
    for i in range(10):
        code += push_stack(f'$t{i}', (9-i)*4)

    return code


def restore_callee_registers():
    code = []
    for i in range(8):
        code += peek_stack(f'$s{i}', (7-i)*4)
    code += peek_stack('$fp', 4)
    code += peek_stack('$ra')
    code += restore_stack(40)
    return code


def restore_caller_registers():
    code = []
    for i in range(10):
        code += peek_stack(f'$t{i}', (9-i)*4)
    code += restore_stack(40)
    return code


def restore_stack(bytes):
    return [mips.AdduInstruction('$sp', '$sp', bytes)]


def allocate_stack(bytes):
    return [mips.SubuInstruction('$sp', '$sp', bytes)]


def push_stack(src, pos=0):
    code = []
    if src[0] != '$':
        code = peek_stack('$t0', src)
        if pos:
            return code+[mips.SwInstruction('$t0', f'{pos}($sp)')]
        return code+[mips.SwInstruction('$t0', '($sp)')]
    else:
        if pos:
            return code+[mips.SwInstruction(src, f'{pos}($sp)')]
        return code+[mips.SwInstruction(src, '($sp)')]


def peek_stack(src, pos=0):
    if pos:
        return [mips.LwInstruction(src, f'{pos}($sp)')]
    return [mips.LwInstruction(src, '($sp)')]


def get_address(dict, key):
    if type(key) is int:
        return key, True
    try:
        if type(key) is str:
            return dict[key], False
        return dict[key.id], False
    except:
        raise Exception('Local not found in stack')
