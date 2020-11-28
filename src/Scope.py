from src.Cool_Type import *
from src.AST import *

class Scope:
    def __init__(self, class_name, parent=None, local=False):
        self.parent = parent
        self.class_name = class_name
        self.cool_types = {}
        self.variables = {}
        self.attributes = {}
        self.methods = {}
        self.locals=[]
        self.params={}
        self.local = local
        self.valid = True
        if not parent:
            self.cool_types = {cool_type.name: cool_type for cool_type in get_basic_types()}

    def invalidate(self):
        scope = self
        while scope:
            if not scope.parent:
                scope.valid = False
            scope = scope.parent

    def get_type(self, type_name: str):
        scope = self
        i = 1
        while scope:
            if type_name in scope.cool_types:
                return scope.cool_types[type_name]
            else:
                scope = scope.parent
        return None

    def lower_than(self, first  : Cool_Type, other : Cool_Type ):
        ct = first
        while ct:
            if ct == other:
                return True
            ct = self.get_type(ct.parent)
        return False

    def exists_type(self, type_name: str):
        if type_name in self.cool_types:
            return True
        if not self.parent is None:
            return self.parent.exists_type(type_name)
        return False

    def create_type(self, cool_type: Cool_Type):
        if self.exists_type(cool_type.name):
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
        cname = self.class_name
        ctype = self.get_type(cname)
        while ctype:
            a = ctype.search_attribute(variable)
            if a:
                return True
            ctype = self.get_type(ctype.parent)
        return False
    
    def get_attribute(self, variable: str):
        ct = self
        while ct.class_name:
            if variable in ct.attributes:
                return ct.attributes[variable] 
            ct = ct.parent
        cname = self.class_name
        ctype = self.get_type(cname)
        while ctype:
            a = ctype.search_attribute(variable)
            if a:
                return a
            ctype = self.get_type(ctype.parent)
        return None
    
    def get_method(self, variable: str):
        ct = self
        while ct.class_name:
            if variable in ct.methods:
                return ct.methods[variable] 
            ct = ct.parent
        cname = self.class_name
        ctype = self.get_type(cname)
        while ctype:
            a = ctype.get_method(variable)
            if a:
                return a
            ctype = self.get_type(ctype.parent)
        return None
    
    def get_parent_attribute(self, variable: str):
        cname = self.class_name
        ptype = self.get_type(cname)
        ctype = self.get_type(ptype.parent)
        while ctype:
            a = ctype.search_attribute(variable)
            if a:
                return a
            ctype = self.get_type(ctype.parent)
        return None

    def get_parent_method(self, variable: str):
        cname = self.class_name
        ptype = self.get_type(cname)
        ctype = self.get_type(ptype.parent)
        while ctype:
            a = ctype.get_method(variable)
            if a:
                return a
            ctype = self.get_type(ctype.parent)
        return None

    def define_variable(self, var_name: str, cool_type: Cool_Type, override=False, value=None):
        scope = self
        if var_name == 'self':
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
                return self.get_type(ct.attributes[variable].type)
            ct = ct.parent
        cname = self.class_name
        ctype = self.get_type(cname)
        while ctype:
            a = ctype.search_attribute(variable)
            if a:
                return self.get_type(a.type)
            ctype = self.get_type(ctype.parent)
     
    
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
        if self.exists_attribute(attribute):
            return False
        self.attributes[attribute] = AttributeNode(name = attribute, attr_type = cool_type, value = value)
        return True

    def exists_method(self, method: str):
        if method in self.methods:
            return True
        if not self.parent is None:
            return self.parent.exists_method(method)
        return False
    
    def exists_type_method(self,ctype: Cool_Type,method:str):
        rtype = ctype
        while rtype:
            if rtype.exists_method(method):
                return True
            rtype = self.get_type(rtype.parent)
        return False
    
    def get_type_method(self,ctype: Cool_Type,method:str):
        rtype = ctype
        while rtype:
            if rtype.exists_method(method):
                return rtype.get_method(method)
            rtype = self.get_type(rtype.parent)
        return None

    def define_method(self, method: str, parameters:list, cool_type: Cool_Type, body=None):
        if self.exists_method(method):
            return False
        self.methods[method] = MethodNode(name = method, parameters = parameters, return_type = cool_type, body = body)
        return True
    
    def join(self, ctype: Cool_Type, other: Cool_Type):
        first = ctype 
        while first:
            if self.lower_than(other, first):
                return first
            first = self.get_type(first.parent)