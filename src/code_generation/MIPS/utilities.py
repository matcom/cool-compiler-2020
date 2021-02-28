from code_generation.MIPS import ast as mips
import re

__TYPES__ = {}
__ADDRS__ = {}


def init_types(types):
    """
    Objects in MIPS code are memory space (size_mips), therefore we need to know the type 
    of this object. But we cannot save the type name, therefore, we configure 
    a unique number for each type which will be identified in MIPS (code_mips)\n

    """
    size_vt=0
    for i, t in enumerate(types):
        t.code_mips = i
        t.size_mips = (len(t.attributes) + 5) * 4
        size_vt +=(len(t.methods) + 1) * 4
        t.attr_index_mips = {}
        for i, a in enumerate(t.attributes):
            t.attr_index_mips[a] = i + 1
        __TYPES__[t.type] = t
    return size_vt


def get_types():
    return __TYPES__

def get_type(name):
    try:
        return __TYPES__[name]
    except KeyError:
        return None


def allocate_stack(bytes):
    return [mips.SubuInstruction('$sp', '$sp', bytes)]


def free_stack(bytes):
    return [mips.AdduInstruction('$sp', '$sp', bytes)]


def push_stack(src, pos):
    return peek_stack('$t0', src)+[mips.SwInstruction('$t0', pos)]


def peek_stack(src, pos):
    return [mips.LwInstruction(src, pos)]


def save_address(key, value):
    
    if type(value) is int:
        if value:
            __ADDRS__[key] = f'{value}($sp)'
        else:
            __ADDRS__[key] = f'($sp)'

    __ADDRS__[key] = value


register_pattern = re.compile(r'\$v[0-1]|\$a[0-3]|\$t[0-9]|\$s[0-7]')


def is_register(addr: str):
    return register_pattern.match(addr) != None
