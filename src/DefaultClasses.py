from src.AST import *
from src.CIL import *

#TODO Definir en CIL algunos métodos predefinidos
class Defaults:
    def ObjectClass():
        #selfattribute=AttributeNode("self","Int",IntegerNode(0))
        # identifier=AttributeNode("type#","Int",IntegerNode(0))
        abort=MethodNode("abort",[],"Object",[])
        typename=MethodNode("type_name",[],"String",[])
        copy=MethodNode("copy",[],"SELF_TYPE",[])
        init=MethodNode("$init",[],"SELF_TYPE",[])

        clase=ClassNode("Object",None,[abort,typename,copy])

        return clase
    
    def IOClass():
        #typeString=AttributeNode("$type","String",StringNode("IO"))
        out_string=MethodNode("out_string",[ParameterNode("x","String")],"SELF_TYPE",[])
        out_int=MethodNode("out_int",[ParameterNode("x","Int")],"SELF_TYPE",[])
        in_string=MethodNode("in_string",[],"String",[])
        in_int=MethodNode("in_int",[],"Int",[])

        clase=ClassNode("IO","Object",[out_string,out_int,in_string,in_int])

        return clase

    def StringClass():
        #typeString=AttributeNode("$type","String",StringNode("String"))
        #value=AttributeNode("value", "Int", IntegerNode(0))

        length=MethodNode("length",[],"Int",[])
        concat=MethodNode("concat",[ParameterNode("s","String")],"String",[])
        substr=MethodNode("substr",[ParameterNode("i","Int"),ParameterNode("l","Int")],"String",[])

        clase=ClassNode("String","Object",[length,concat,substr])#Removed typeString,value,
        
        return clase

    # def typename_CIL():
    #     instrucciones=[CILAssign("$result",["$type"])]
    #     return CILGlobalMethod('typename',params=["self"],locals=["$result"],instrucciones=instrucciones)
    def abort_CIL():
        instrucciones=[CILAbort("$result",[])]
        return CILGlobalMethod('abort',[ParameterNode("self","SELF_TYPE")],["$result"],instrucciones)

    def copy_CIL(cantidadatributos):
        instrucciones=[CILCopy("$result",["self",cantidadatributos])]
        return CILGlobalMethod('copy',[ParameterNode("self","SELF_TYPE")],["$result"],instrucciones)

    def out_string_CIL():
        instrucciones=[CILOutString(["x"]),CILAssign("$result",["self"])]
        return CILGlobalMethod('out_string',[ParameterNode("self","SELF_TYPE"),ParameterNode("x","String")],["$result"],instrucciones)

    def out_int_CIL():
        instrucciones=[CILOutInt(["x"]),CILAssign("$result",["self"])]
        return CILGlobalMethod('out_int',[ParameterNode("self","SELF_TYPE"),ParameterNode("x","Int")],["$result"],instrucciones)

    def in_string_CIL():
        instrucciones=[CILInString("$result",[])]
        return CILGlobalMethod('in_string',[ParameterNode("self","SELF_TYPE")],["$result"],instrucciones)

    def in_int_CIL():
        instrucciones=[CILInString("$result",[])]
        return CILGlobalMethod('in_int',[ParameterNode("self","SELF_TYPE")],["$result"],instrucciones)

    def len_string_CIL():
        instrucciones=[CILStringLenght("$result",["self"])]
        return CILGlobalMethod('length',[ParameterNode("self","SELF_TYPE")],["$result"],instrucciones)

    def concat_string_CIL():
        instrucciones=[CILStringConcat("$result",["self","s"])]
        return CILGlobalMethod('concat',[ParameterNode("self","SELF_TYPE"),ParameterNode("s","String")],["$result"],instrucciones)

    def substring_string_CIL():
        instrucciones=[CILStringConcat("$result",["self","x"])]
        return CILGlobalMethod('substr',[ParameterNode("self","SELF_TYPE"),ParameterNode("x","Int")],["$result"],instrucciones)