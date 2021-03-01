from ...cmp import AutoType, SelfType, ErrorType

WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined.'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
CONDITION_NOT_BOOL = '"%s" conditions return type must be Bool not "%s".'
INVALID_PARAMETER = 'Formal parameter "%s" cannot have type SELF_TYPE.'
INVALID_BRANCH = 'Identifier "%s" declared with type SELF_TYPE in case branch.'
DUPLICATED_BRANCH = 'Duplicate branch "%s" in case statement.'

ST, AT = ['SELF_TYPE', 'AUTO_TYPE']
sealed = ['Int', 'String', 'Bool', 'SELF_TYPE', 'AUTO_TYPE']
built_in_types = [ 'Int', 'String', 'Bool', 'Object', 'IO', 'SELF_TYPE', 'AUTO_TYPE']

def fixed_type(cur_type):
    try: return cur_type.fixed
    except AttributeError: return cur_type

def update_condition(target, value):
    c1 = isinstance(target, AutoType)
    c2 = (not isinstance(value, AutoType)) and value
    return c1 and c2

# Compute the Lowest Common Ancestor in
# the type hierarchy tree
def LCA(type_list):
    counter = {}

    def check(target):
        return [isinstance(t, target) for t in type_list]

    if all(check(SelfType)):
        return SelfType(type_list[0].fixed)
    if any(check(AutoType)):
        return AutoType()
    if any(check(ErrorType)):
        return ErrorType()
    type_list = [fixed_type(t) for t in type_list]
    for typex in type_list:
        node = typex
        while True:
            try:
                counter[node.name] += 1
            except KeyError:
                counter[node.name] = 1
            if counter[node.name] == len(type_list):
                return node
            if not node.parent:
                break
            node = node.parent

def check_path(D, ans):
    if any([(t.name == ST) for t in D]):
        return True, SelfType()
    for t in D:
        l = [ans, t]
        lca = LCA(l)
        try: l.remove(lca)
        except ValueError:
            return False, None
        ans = l[0]
    return True, ans
