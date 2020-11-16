from ast import *
from type_defined import *
from data_visitor import *
from cil_ast import *

TYPES = []
DATA = []
CODE = []

def generate_code(ast):
    cil = generate_cil(ast)
    #mips = generate_mips()
    #return cil, mips
    return cil

def generate_cil(ast):
    result = "TYPES -->\n\n"
    result += generate_cil_types(ast)
    result += "END <--\n\n"
    
    result += "DATA -->\n\n"
    result += generate_cil_data(ast)
    result += "END <--\n\n"
    
    result += "CODE -->\n\n"
    result += generate_cil_code(ast)
    result += "END <--"

    return result


def generate_cil_types(ast):
    result = ""

    for key in ast.keys():
        if key == "SELF_TYPE":
            continue
        
        attributes = ast[key].get_attribute_owner()
        methods = ast[key].get_method_owner()
        new_type = TypeNode(key, attributes, methods)
        TYPES.append(new_type)
        
        result += new_type.GetCode() + "\n\n"

    return result
        

def generate_cil_data(ast):
    result = ""
    vis = FormatVisitor()
    data = {}
    for val in ast.values():
        for attr in val.attributes.values():
            if attr.attribute_name != "self" and attr.expression:
                for s in vis.visit(attr.expression):
                    data[s] = s.lex
        for method in val.methods.values():
            if method.expression:
                for s in vis.visit(method.expression):
                    data[s] = s.lex[0:-1]

    i = 0
    for s in data.values():
        new_data = DataNode("data_" + str(i), s)
        DATA.append(new_data)
        result += new_data.GetCode() + "\n"
        i += 1

    result += "\n"  
    return result 


def generate_cil_code(ast):
    result = generate_built_in_functions()
    
    for types in ast.value():
        for method in types.methods.values():
            pass

    return result

def generate_built_in_functions():
    code = [FunctionNode("IO_out_string", [ParamNode('self'), ParamNode('str')], [], [PrintNode('str'), 
                                                                                      ReturnNode('self')]),

            FunctionNode('IO_out_int', [ParamNode('self'), ParamNode('int')], [LocalNode('str')], [StrNode('int', 'str'), 
                                                                                                   PrintNode('str'), 
                                                                                                   ReturnNode('self')]),

            FunctionNode('IO_in_string', [ParamNode('self')], [LocalNode('str')], [ReadNode('str'), 
                                                                                   ReturnNode('str')]),

            FunctionNode('IO_in_int', [ParamNode('self')], [LocalNode('int')], [ReadIntNode('int'), 
                                                                                ReturnNode('int')]),

            FunctionNode('Object_type_name', [ParamNode('self')], [LocalNode('type'), LocalNode('str')], [TypeOfNode('type', 'self'), 
                                                                                                          StrNode('type', 'str'),
                                                                                                          ReturnNode('str')]),

            FunctionNode('Object_copy', [ParamNode('self')], [LocalNode('copy')], [CopyNode('self', 'copy'), 
                                                                                   ReturnNode('copy')]),

            FunctionNode('length_String', [ParamNode('self')], [LocalNode('result')], [LengthNode('self', 'result'), 
                                                                                       ReturnNode('result')]),

            FunctionNode('concat_String', [ParamNode('self'), ParamNode('str')], [LocalNode('result')], [ConcatNode('self', 'str', 'result'), 
                                                                                                       ReturnNode('result')]),

            FunctionNode('substr_String', [ParamNode('self'), ParamNode('from'), ParamNode('to')], [LocalNode('result')], [SubStringNode('self', 'from', 'to', 'result'), 
                                                                                                                           ReturnNode('result')])
            ]

    CODE = [] + code

    result = ""
    for f in code:
        result += f.GetCode() + "\n\n"
    
    return result


def generate_mips():
    pass