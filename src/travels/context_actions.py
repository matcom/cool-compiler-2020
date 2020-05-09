from abstract.semantics import *


def update_attr_type(current_type_: Type, attr_name: str, new_type: Type):
    for attr in current_type_.attributes:
        attr.type = new_type if attr.name == attr_name else attr.type


def update_method_param(current_type: Type, method: str, param_name: str,
                        new_type: Type):
    m = current_type.methods[method]
    for i, (pname, ptype) in enumerate(zip(m.param_names, m.param_types)):
        if pname == param_name:
            m.param_types[i] = new_type


def update_scope_variable(vname: str,
                          new_type: Type,
                          scope: Scope,
                          index=None):
    if not index:
        index = 0
    for i in range(index, len(scope.locals)):
        if scope.locals[i].name == vname:
            scope.locals[i].type = new_type
            print(f'Changed {scope.locals[i].name} to type {new_type.name}')
            return
    if scope.parent:
        update_scope_variable(vname, new_type, scope.parent, scope.index)
