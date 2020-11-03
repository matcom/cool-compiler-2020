"""Contains Definitions for Semantic Types"""

from .error import SemanticError
from .features import *
from tools.utils import Singleton

class Type:
    def __init__(self, name:str):
        if name == 'ObjectType':
            return ObjectType()
        self.name = name
        self.attributes = []
        self.methods = {}
        self.parent = ObjectType()

    def set_parent(self, parent):
        if self.parent != ObjectType() and self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if not self.parent:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        if name == 'self':
            raise SemanticError(f'\'self\' cannot be the name of an attribute')
        
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
            if not self.parent:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name == 'self':
            raise SemanticError(f'\'self\' cannot be the name of an method')
        
        if name in self.methods:
            raise SemanticError(f'Method "{name}" already defined in {self.name}')
        
        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

    def change_type(self, method, nparm, newtype):
        idx = method.param_names.index(nparm)
        method.param_types[idx] = newtype
                
    def conforms_to(self, other):
        return self == other or self.parent is not None and self.parent.conforms_to(other)

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

class SELF_TYPE(Type):
    def __init__(self):
        Type.__init__(self, 'SELF_TYPE')

    # not check conforms with self_type
    def conforms_to(self, other):
        return True

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<Error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, ErrorType)

    def __ne__(self, other):
        return not isinstance(other, ErrorType)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, 'Void')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class BoolType(Type):
    def __init__(self):
        Type.__init__(self, 'Bool')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)
    
    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, BoolType)


class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'Int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, IntType)

class StringType(Type, metaclass=Singleton):
    def __init__(self):
        Type.__init__(self, 'String')

        self.methods = { }

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, StringType)

class IOType(Type, metaclass=Singleton):
    def __init__(self):
        Type.__init__(self, 'IO')

        self.methods = { }

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IOType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, IOType)

class ObjectType(Type, metaclass=Singleton):
    def __init__(self):
        self.name = 'Object'
        self.attributes = []
        self.methods = { }
        self.parent = None

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, ObjectType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, ObjectType)