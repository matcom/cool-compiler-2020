from ast import *
from type_defined import *

TYPES = {}
DATA = {}
CODE = {}

def generate_code(ast):
    cil = generate_cil(ast)
    #mips = generate_mips()
    #return cil, mips
    return cil

def generate_cil(ast):
    result = "TYPES\n\n"
    result += generate_cil_types(ast)
    result += "END\n\n"
    
    #result += "DATA\n\n"
    #result += generate_cil_data(ast)
    #result += "END\n\n"
    
    #result += "CODE\n\n"
    #result += generate_cil_code(ast)
    #result += "END\n\n"

    return result


def generate_cil_types(ast):
    result = ""

    for key in ast.keys():
        if key == "SELF_TYPE":
            continue
        result += "type " + key + " {"
        
        ATTRIBUTES = ast[key].get_attribute_owner()
        METHODS = ast[key].get_method_owner()
        
        for key in ATTRIBUTES.keys():
            result += "\n\tattribute " + key + ":" + ATTRIBUTES[key]

        for key in METHODS.keys():
            result += "\n\tmethod " + key + ":" + METHODS[key]

        result += "\n}\n\n"

    return result
        

def generate_cil_data(ast):
    pass

def generate_cil_code(ast):
    pass

def generate_mips():
    pass