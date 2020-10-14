from Cool_Type import *
from AST import *

class Scope:
    def __init__(self, class_name, parent=None, local=False):
        self.parent = parent
        self.class_name = class_name
        self.cool_types = {}
        self.variables = {}
        self.attributes = {}
        self.methods = {}
        if not parent:
            self.cool_types = {cool_type.name: cool_type for cool_type in get_basic_types()}

    def get_type(self, type_name: str):
        scope = self
        while scope:
            if type_name in self.cool_types:
                return self.cool_types[type_name]
            scope = scope.parent
        return None
    
    def exists_type(self, type_name: str):
        if type_name in self.cool_types:
            return True
        if not self.parent is None:
            return self.parent.exists_attribute(attribute)
        return False

    def create_type(self, cool_type: Cool_Type):
        if exists_type(cool_type.name):
            return False
        self.cool_types[cool_type.name] = cool_type
        return True

    def exists_variable(self, variable: str):
        if variable == 'self':
            return True
        ct = self
        while ct.class_name:
            if variable in ct.variables:
                return True
            if variable in ct.attributes:
                return True
            ct = ct.parent
        False


    def define_variable(self, var_name: str, cool_type: Cool_Type, override=False, value=None):
        scope = self
        if variable == 'self':
            return False
        if not override and var_name in scope.variables:
            return False        
        self.variables[var_name] = {
            'type': cool_type,
            'value': value
        }
        return True
     
    def get_variable_type(self, variable: str):
        if variable == 'self':
            return self.get_type("SELF_TYPE")
        ct = self
        while ct.class_name:
            if variable in ct.variables:
                return ct.variables[variable]['type']
            if variable in ct.attributes:
                return ct.attributes[variable].type
            ct = ct.parent
     
    
    def get_types(self):
        return self.cool_types
    
    def set_types(self, new_types):
        self.cool_types = new_types

    def exists_attribute(self, attribute: str):
        if attribute in self.attributes:
            return True
        if not self.parent is None:
            return self.parent.exists_attribute(attribute)
        return False
    
    def define_attribute(self, attribute: str, cool_type: Cool_Type, value=None):
        if not self.exists_attribute(attribute):
            return False
        self.attributes[attribute] = {
            AttributeNode(name = attribute, attr_type = cool_type, value = value)
        }

    def exists_method(self, method: str):
        if method in self.methods:
            return True
        if not self.parent is None:
            return self.parent.exists_method(method)
        return False
    
    def define_method(self, method: str, parameters:list, cool_type: Cool_Type, body=None):
        if not self.exists_method(method):
            return False
        self.methods[method] = {
            MethodNode(name = method, parameters = parameters, return_type = cool_type, body = body)
        }
    
    def join(self, ctype: Cool_Type, other: Cool_Type):
        first = ctype 
        while first:
            if other < first:
                return first
            first = self.get_type(first.parent)