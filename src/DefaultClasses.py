from AST import *
from CIL import *

#TODO Definir en CIL algunos métodos predefinidos
class Defaults:
    def ObjectClass():
        selfattribute=AttributeNode("self","Int",IntegerNode(0))
        typeString=AttributeNode("$type","String",StringNode("Object"))
        # identifier=AttributeNode("type#","Int",IntegerNode(0))
        abort=MethodNode("abort",[],"Object",[])
        typename=MethodNode("type_name",[],"String",[])
        copy=MethodNode("copy",[],"SELF_TYPE",[])
        init=MethodNode("$init",[],"SELF_TYPE",[])

        clase=ClassNode("Object",None,[typeString,abort,typename,copy])

        return clase
    
    def IOClass():
        typeString=AttributeNode("$type","String",StringNode("IO"))
        out_string=MethodNode("out_string",[ParameterNode("x","String")],"SELF_TYPE",[])
        out_int=MethodNode("out_int",[ParameterNode("x","Int")],"SELF_TYPE",[])
        in_string=MethodNode("in_string",[],"String",[])
        in_int=MethodNode("in_int",[],"Int",[])

        clase=ClassNode("IO","Object",[typeString,out_string,out_int,in_string,in_int])

        return clase

    def StringClass():
        typeString=AttributeNode("$type","String",StringNode("String"))
        value=AttributeNode("value", "Int", IntegerNode(0))

        length=MethodNode("length",[],"Int",[])
        concat=MethodNode("concat",[ParameterNode("s","String")],"String",[])
        substr=MethodNode("substr",[ParameterNode("i","Int"),ParameterNode("l","Int")],"String",[])

        clase=ClassNode("String","Object",[typeString,value,length,concat,substr])
        
        return clase

    def typename_CIL():
        instrucciones=[CILAssign("$result",["$type"])]
        return CILGlobalMethod('typename',params=["self"],locals=["$result"],instrucciones=instrucciones)

    def copy_CIL():
        instrucciones=[CILCopy("$result",["self"])]
        return CILGlobalMethod('copy',params=["self"],locals=["$result"],instrucciones=instrucciones)

    def out_string_CIL():
        instrucciones=[CILOutString(params=["x"]),CILAssign("$result",["self"])]
        return CILGlobalMethod('out_string',params=["self","x"],locals=["$result"],instrucciones=instrucciones)

    def out_int_CIL():
        instrucciones=[CILOutInt(params=["x"]),CILAssign("$result",["self"])]
        return CILGlobalMethod('out_int',params=["self","x"],locals=["$result"],instrucciones=instrucciones)

    def in_string_CIL():
        instrucciones=[CILInString("$result",params=[]))]
        return CILGlobalMethod('in_string',params=["self"],locals=["$result"],instrucciones=instrucciones)

    def in_int_CIL():
        instrucciones=[CILInString("$result",params=[]))]
        return CILGlobalMethod('in_int',params=["self"],locals=["$result"],instrucciones=instrucciones)

    def len_string_CIL():
        instrucciones=[CILStringLenght("$result",params=["self"]))]
        return CILGlobalMethod('length',params=["self"],locals=["$result"],instrucciones=instrucciones)

    def concat_string_CIL():
        instrucciones=[CILStringConcat("$result",params=["self","s"]))]
        return CILGlobalMethod('concat',params=["self, s"],locals=["$result"],instrucciones=instrucciones)

    def substring_string_CIL():
        instrucciones=[CILStringConcat("$result",params=["self","x"]))]
        return CILGlobalMethod('substr',params=["self, x"],locals=["$result"],instrucciones=instrucciones)