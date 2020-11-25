from utils.errors import SemanticError, AttributesError, TypesError, NamesError
from collections import OrderedDict

class Attribute:
    def __init__(self, name, typex, index, tok=None):
        self.name = name
        self.type = typex
        self.index = index  # lugar que ocupa en el scope
        self.expr = None

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

class MethodError(Method):
    def __init__(self, name, param_names, param_types, return_types):
        super().__init__(name, param_names, param_types, return_types)

    def __str__(self):
        return f'[method] {self.name} ERROR'

class Type:
    def __init__(self, name:str, pos):
        if name == 'ObjectType':
            return ObjectType(pos)
        self.name = name
        self.attributes = {}
        self.methods = {}
        self.parent = ObjectType(pos)
        self.pos = pos

    def set_parent(self, parent):
        if type(self.parent) != ObjectType and self.parent is not None:
            error_text = TypesError.PARENT_ALREADY_DEFINED % self.name
            raise TypesError(error_text, *self.pos)
        self.parent = parent

    def get_attribute(self, name:str, pos) -> Attribute:
        try:
            return self.attributes[name] #next(attr for attr in self.attributes if attr.name == name)
        except KeyError:
            if self.parent is None:
                error_text = AttributesError.ATTRIBUTE_NOT_DEFINED % (name, self.name)
                raise AttributesError(error_text, *pos)
            try:
                return self.parent.get_attribute(name, pos)
            except AttributesError:
                error_text = AttributesError.ATTRIBUTE_NOT_DEFINED % (name, self.name)
                raise AttributesError(error_text, *pos)

    def define_attribute(self, name:str, typex, pos):
        try:
            self.attributes[name]
        except KeyError:
            try:
                self.get_attribute(name, pos)
            except SemanticError:
                self.attributes[name] = attribute = Attribute(name, typex, len(self.attributes))
                # self.attributes.append(attribute)
                return attribute
            else:    
                error_text = SemanticError.ATTR_DEFINED_PARENT % name
                raise SemanticError(error_text, *pos)
        else:
            error_text = SemanticError.ATTRIBUTE_ALREADY_DEFINED % name
            raise SemanticError(error_text, *pos)

    def get_method(self, name:str, pos) -> Method:
        try:
            return self.methods[name]
        except KeyError:
            error_text = AttributesError.METHOD_NOT_DEFINED %(name, self.name)
            if self.parent is None:
                raise AttributesError(error_text, *pos)
            try:
                return self.parent.get_method(name, pos)
            except AttributesError:
                raise AttributesError(error_text, *pos)

    def define_method(self, name:str, param_names:list, param_types:list, return_type, pos=(0, 0)):
        if name in self.methods:
            error_text = SemanticError.METHOD_ALREADY_DEFINED % name
            raise SemanticError(error_text, *pos)

        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

    def change_type(self, method, nparm, newtype):
        idx = method.param_names.index(nparm)
        method.param_types[idx] = newtype

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes.values():
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
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes.values())
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods.values())
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class ErrorType(Type):
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, '<error>', pos)

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, ErrorType)

    def __ne__(self, other):
        return not isinstance(other, ErrorType)

class VoidType(Type):
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, 'Void', pos)

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class BoolType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'Bool'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)
    
    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, BoolType)


class SelfType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'Self'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, SelfType)
    
    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, SelfType)


class IntType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'Int'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, IntType)


class StringType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'String'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos
        self.init_methods()

    def init_methods(self):
        self.define_method('length', [], [], IntType())
        self.define_method('concat', ['s'], [self], self)
        self.define_method('substr', ['i', 'l'], [IntType(), IntType()], self)

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, StringType)


class ObjectType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'Object'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos
        self.init_methods()

    def init_methods(self):
        self.define_method('abort', [], [], self)
        self.define_method('type_name', [], [], StringType())
        self.define_method('copy', [], [], SelfType())

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, ObjectType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, ObjectType)

class AutoType(Type):
    def __init__(self):
        Type.__init__(self, 'AUTO_TYPE')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, AutoType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, AutoType)


class IOType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'IO'
        self.attributes = {}
        self.methods = {}
        self.parent = ObjectType(pos)
        self.pos = pos
        self.init_methods()

    def init_methods(self):
        self.define_method('out_string', ['x'], [StringType()], SelfType())
        self.define_method('out_int', ['x'], [IntType()], SelfType())
        self.define_method('in_string', [], [], StringType())
        self.define_method('in_int', [], [], IntType())

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IOType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, IOType)
