from AST import *

class Cool_Type:
    def __init__(self, name:str, parent:str=None, attributes = None, methods = None):
        self.name = name
        self.parent = parent
        self.attributes = attributes
        self.methods = methods
    
    def __eq__(self, other ):
        return  self.name == other.name #Aquí para arreglar le pondría al inicio self!=None and other !=None and




    def add_methods(self, *methods):
        for method in methods:
            self.methods.append(method)
    
    def add_attributes(self, *attributes):
        for attribute in attributes:
            self.attributes.append(attribute)
            
    def search_attribute(self, attr):
        for attribute in self.attributes:
            if attr == attribute.name:
                return attribute
        return None
    
    def exists_method(self, method_name: str):
        for method in self.methods:
            if method_name == method.name:
                return True
        return False

    def get_method(self, method_name: str):
        for method in self.methods:
            if method_name == method.name:
                return method
        return None
    
    def delete_method(self, method_name: str):
        new = []
        for method in self.methods:
            if method_name != method.name:
                new.append(method)
        self.methods = new

def get_basic_types():
    Object = Cool_Type("Object", None, [], [])
    Int = Cool_Type("Int", "Object", [], [])
    Bool = Cool_Type("Bool", "Object", [], [])
    String = Cool_Type("String", "Object", [], [])
    SelfType = Cool_Type("SELF_TYPE", None, [], [])
    IO = Cool_Type("IO", "Object", [], [])
    Object.add_methods(
        MethodNode(name = "abort", parameters = [], return_type = "Object" , body = None),
        MethodNode(name = "type_name", parameters = [], return_type = "String" , body = None),
        MethodNode(name = "copy", parameters = [], return_type = "SELF_TYPE" , body = None)
    )
    IO.add_methods(
            MethodNode(name = "out_string", parameters = [ParameterNode(name = "x_1", param_type = "String")], return_type = "SELF_TYPE" , body = None),
            MethodNode(name = "out_int", parameters = [ParameterNode(name = "x_1", param_type = "Int")], return_type = "SELF_TYPE" , body = None),
            MethodNode(name = "in_string", parameters = [], return_type = "String" , body = None),
            MethodNode(name = "in_int", parameters = [], return_type = "Int" , body = None)
    )
    String.add_methods(
            MethodNode(name = "length", parameters = [], return_type = "Int" , body = None),
            MethodNode(name = "concat", parameters = [ParameterNode(name = "x_1", param_type = "String")], return_type = "String" , body = None),
            MethodNode(name = "substr", parameters = [ParameterNode(name = "x_1", param_type = "Int"), ParameterNode(name = "x_2", param_type = "Int")], return_type = "String" , body = None)
    )
    basics = [Object, Int, Bool, String, SelfType, IO]
    return basics
    
