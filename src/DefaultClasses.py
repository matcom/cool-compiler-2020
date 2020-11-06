from AST import *

#TODO Definir en CIL algunos métodos predefinidos
class Defaults:
    def ObjectClass():
        selfattribute=AttributeNode("self","Int",IntegerNode(0))
        # identifier=AttributeNode("type#","Int",IntegerNode(0))
        abort=MethodNode("abort",[],"Object",[])
        typename=MethodNode("type_name",[],"String",[])
        copy=MethodNode("copy",[],"SELF_TYPE",[])
        init=MethodNode("$init",[],"SELF_TYPE",[])

        clase=ClassNode("Object",None,[identifier,abort,typename,copy])

        return clase
    
    def IOClass():
        identifier=AttributeNode("type#","Int",IntegerNode(1))
        out_string=MethodNode("out_string",[ParameterNode("x","String")],"SELF_TYPE",[])
        out_int=MethodNode("out_int",[ParameterNode("x","Int")],"SELF_TYPE",[])
        in_string=MethodNode("in_string",[],"String",[])
        in_int=MethodNode("in_int",[],"Int",[])

        clase=ClassNode("IO","Object",[identifier,out_string,out_int,in_string,in_int])

        return clase

    def StringClass():
        identifier=AttributeNode("type#","Int",IntegerNode(2))
        value=AttributeNode("value", "Int", IntegerNode(0))

        length=MethodNode("length",[],"Int",[])
        concat=MethodNode("concat",[ParameterNode("s","String")],"String",[])
        substr=MethodNode("substr",[ParameterNode("i","Int"),ParameterNode("l","Int")],"String",[])

        clase=ClassNode("String","Object",[identifier,value,length,concat,substr])