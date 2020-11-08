class SemanticException(Exception):
    @property
    def text(self):
        return self.args[0]

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type
    
    def is_override(self, omethod): # check if self is an override of omethod
        valid = False
        if omethod.name == self.name:
            if self.return_type.is_subtype(omethod.return_type):
                if len(self.param_names) == len(omethod.param_names):
                    for ptype, optype in zip(self.param_types, omethod.param_types):
                        if not ptype == optype:
                            break
                    else:
                        valid = True
        return valid

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = {}
        self.parent = None
        self.children = []
        self.finish_time = 0
        self._visited = False

    def compute_finish_time_recursively(self, ref_int):
        for child in self.children:
            child.compute_finish_time_recursively(ref_int)
        self.finish_time = ref_int['value']
        ref_int['value'] += 1

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticException(f'Parent type is already set for type {self.name}.')
        if parent.name in ['Int', 'String', 'Bool']:
            raise SemanticException(f'Cannot inherit from basic type {parent.name}.')
        self.parent = parent
        if all(map(lambda x: x.name != self.name, parent.children)):
            parent.children.append(self)

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticException(f'Attribute "{name}" is not defined in type {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticException:
                raise SemanticException(f'Attribute "{name}" is not defined in type {self.name}.')

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticException:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticException(f'Attribute "{name}" is already defined in type {self.name}.')

    def get_method(self, name:str):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                raise SemanticException(f'Method "{name}" is not defined in type {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticException:
                raise SemanticException(f'Method "{name}" is not defined in type {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        try:
            method = self.get_method(name)
        except SemanticException:
            pass
        else:
            if name in self.methods.keys(): # duplicate?
                raise SemanticException(f'Method "{name}" already defined in type {self.name}.')
            else: # override?
                new_method = Method(name, param_names, param_types, return_type)
                if not new_method.is_override(method): # override check is different from the manual, check method if something goes wrong here
                    raise SemanticException(f'Invalid override of method "{name}" in type {self.name}.')
        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

    def get_all_attributes(self):
        if self.parent:
            for attr in self.parent.get_all_attributes():
                yield attr
        for attr in self.attributes:
            yield attr

    def get_all_methods(self):
        if self.parent:
            for tup in self.parent.get_all_methods():
                yield tup
        for method in self.methods.values():
            yield (method, self)

    def is_subtype(self, otype): # check if self is subtype of otype
        actual = self
        while True:
            if actual == otype:
                return True
            if actual.parent == None:
                return False
            actual = actual.parent

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods.values())
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def is_subtype(self, otype):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def __eq__(self, other):
        return isinstance(other, VoidType)

def find_common_ancestor(type1:Type, type2:Type):
    if type1 is ErrorType or type2 is ErrorType:
        return ErrorType()

    ancestor_t1 = []
    actual = type1
    while actual:
        ancestor_t1.append(actual)
        actual = actual.parent

    actual = type2
    while actual:
        if actual in ancestor_t1:
            return actual
        actual = actual.parent
    

class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticException(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticException(f'Type "{name}" is not defined.')

    def compute_finish_time(self):
        root = self.types['Object']
        root.compute_finish_time_recursively({'value': 0})

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class Var:
    def __init__(self, idx, typex):
        self.id = idx
        self.type = typex

    def __str__(self):
        return f'[var] {self.id}: {self.type.name}'

    def __repr__(self):
        return str(self)

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}

    def define_var(self, name, typex):
        if name in self.vars:
            raise SemanticException(f'Variable {name} already defined in current context.')
        var = self.vars[name] = Var(name, typex)
        return var
    
    def get_var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            if not self.parent is None:
                try:
                    return self.parent.get_var(name)
                except SemanticException as e:
                    raise e
            raise SemanticException(f'Variable {name} is not defined.')

    def __str__(self):
        return '{\n' + ('\t' if self.parent is None else 'Parent:\n' + f'{self.parent}\n\t') + '\n\t'.join(str(x) for x in self.vars.values()) + '\n}'

    def __repr__(self):
        return str(self)
