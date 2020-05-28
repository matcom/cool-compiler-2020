

__TYPES_CODES__ = {}


def init_types_codes(types):
    for i, t in enumerate(types):
        __TYPES_CODES__[t] = i


def get_type_code(type):
    try:
        return __TYPES_CODES__[type]
    except KeyError:
        return None
