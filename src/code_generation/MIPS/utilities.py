

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
    return len(type.attributes) + 1
