from AST import *

class Defaults:
    def ObjectClass():
        identifier=AttributeNode("type#","Int",IntegerNode(0))
        abort=MethodNode("abort",[],"Object",[])
        typename=MethodNode("type_name",[],"String",[])
        copy=MethodNode("copy",[],"SELF_TYPE",[])

        clase=ClassNode("Object",None,[identifier,abort,typename,copy])

        return clase
    
    def IOClass():
        identifier=AttributeNode("type#","Int",IntegerNode(1))
        out_string=MethodNode("out_string",[ParameterNode("x","String"),"SELF_TYPE",[]],"SELF_TYPE",[])
        out_int=MethodNode("out_int",[ParameterNode("x","Int")],"SELF_TYPE",[])
        in_string=MethodNode("in_string",[],"String",[])
        in_int=MethodNode("in_int",[],"Int",[])

        clase=ClassNode("IO","Object",[identifier,out_string,out_int,in_string,in_int])

        return clase