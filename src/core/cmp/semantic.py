import itertools as itt
from collections import OrderedDict

class SemanticError(Exception):
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

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str='Object'):
        self.name = name
        self.attributes = []
        self.methods = {}
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        # //TODO: Remove the below if clause
        if name in self.methods.keys():
            raise SemanticError(f'Method "{name}" already defined in {self.name}')
        try:
            method = self.get_method(name)
        except SemanticError:
            pass
        else:
            if method.return_type != return_type or method.param_types != param_types:
                raise SemanticError(f'Method "{name}" already defined in {self.name} with a different signature.')

        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods.values():
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        if self.name == 'Object':
            return True
        return False

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

class MutableType(Type):
    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

class ErrorType(MutableType):
    def __init__(self):
        Type.__init__(self, '<error>')

    def __eq__(self, other):
        return isinstance(other, Type)

    def __bool__(self):
        return False

class AutoType(MutableType):
    def __init__(self):
        Type.__init__(self, 'AUTO_TYPE')

    def __eq__(self, other):
        return isinstance(other, AutoType)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, 'void')

    def conforms_to(self, other):
        if other.name in [ 'Int', 'String', 'Bool', 'IO']:
            return False
        return True

    def bypass(self):
        return False

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, VoidType)

class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'Int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

class StringType(Type):
    def __init__(self):
        Type.__init__(self, 'String')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)

class BoolType(Type):
    def __init__(self):
        Type.__init__(self, 'Bool')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)

class IOType(Type):
    def __init__(self):
        Type.__init__(self, 'IO')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IOType)

class SelfType(Type):
    def __init__(self, fixed=None):
        Type.__init__(self, 'SELF_TYPE')
        self.fixed = fixed

    def get_method(self, name):
        return self.fixed.get_method(name)

    def get_attribute(self, name):
        return self.fixed.get_attribute(name)

    def conforms_to(self, other):
        return Type.conforms_to(self, other) or self.fixed is not None and self.fixed.conforms_to(other)
    
    def __eq__(self, other):
        return other.name == self.name or isinstance(other, SelfType)

class Context:
    def __init__(self):
        self.types = {}

    def append_type(self, new_type):
        name = new_type.name
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = new_type
        return typex

    def create_type(self, name:str):
        return self.append_type(Type(name))

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is not None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def count_auto(self):
        num = sum([x.type.name == 'AUTO_TYPE' for x in self.locals])
        return num + sum([scp.count_auto() for scp in self.children])