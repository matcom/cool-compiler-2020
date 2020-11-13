 
from cil_ast import * 


f1_params = [ParamNode("self")]
f1_localVars = [LocalNode("f1_self")]
f1_intructions = [AssignNode(f1_localVars[0],f1_params[0]),ExitNode(),ReturnNode(f1_localVars[0])]
f1 = FunctionNode("function_abort_Object",f1_params,f1_localVars,f1_intructions)

f2_params = [ParamNode("self")]
f2_localVars = [LocalNode("f2_result")]
f2_intructions = [TypeOfNode(f2_params[0],f2_localVars[0]),ReturnNode(f2_localVars[0])]
f2 = FunctionNode("function_typeOf_Object",f2_params,f2_localVars,f2_intructions)

f3_params = [ParamNode("self")]
f3_localVars = [LocalNode("f3_result")]
f3_intructions = [CopyNode(f3_localVars[0],f3_params[0]),ReturnNode(f3_localVars[0])]
f3 = FunctionNode("function_copy_Object",f3_params,f3_localVars,f3_intructions)

f4_params = [ParamNode("self"),ParamNode("word")]
f4_localVars = [LocalNode("f4_self"),LocalNode("f4_word")]
f4_intructions = [AssignNode(f4_localVars[0],f4_params[0]),LoadNode(f4_localVars[1],f4_params[1]),OutStringNode(f4_localVars[1]),ReturnNode(f4_localVars[0])]
f4 = FunctionNode("function_outString_IO",f4_params,f4_localVars,f4_intructions)

f5_params = [ParamNode("self"),ParamNode("number")]
f5_localVars = [LocalNode("f5_self")]
f5_intructions = [AssignNode(f5_localVars[0],f5_params[0]),OutIntNode(f5_params[1]),ReturnNode(f5_localVars[0])]
f5 = FunctionNode("function_outInt_IO",f5_params,f5_localVars,f5_intructions)

f6_params = [ParamNode("self")]
f6_localVars = [LocalNode("f6_result")]
f6_intructions = [ReadIntNode(f6_localVars[0]),ReturnNode(f6_localVars[0])]
f6 = FunctionNode("function_inInt_IO",f6_params,f6_localVars,f6_intructions)

f7_params = [ParamNode("self")]
f7_localVars = [LocalNode("f7_result")]
f7_intructions = [ReadStringNode(f7_localVars[0]),ReturnNode(f7_localVars[0])]
f7 = FunctionNode("function_inString_IO",f7_params,f7_localVars,f7_intructions)

f8_params = [ParamNode("self")]
f8_localVars = [LocalNode("f8_word"),LocalNode("f8_result")]
f8_intructions = [LoadNode(f8_localVars[0],f8_params[0]),LengthNode(f8_localVars[1],f8_localVars[0]),ReturnNode(f8_localVars[1])]
f8 = FunctionNode("function_length_String",f8_params,f8_localVars,f8_intructions)

f9_params = [ParamNode("self"),ParamNode("word")]
f9_localVars = [LocalNode("f9_word"),LocalNode("f9_word1"),LocalNode("f9_result")]
f9_intructions = [LoadNode(f9_localVars[0],f9_params[0]),LoadNode(f9_localVars[1],f9_params[1]),ConcatNode(f9_localVars[2],f9_localVars[0],f9_localVars[1]),ReturnNode(f9_localVars[2])]
f9 = FunctionNode("function_concat_String",f9_params,f9_localVars,f9_intructions)

f10_params = [ParamNode("self"),ParamNode("begin"),ParamNode("end")]
f10_localVars = [LocalNode("f10_word"),LocalNode("f10_result")]
f10_intructions = [LoadNode(f10_localVars[0],f10_params[0]), SubstringNode(f10_localVars[1],f10_localVars[0],f10_params[1],f10_params[2])]
f10 = FunctionNode("function_substr_String",f10_params,f10_localVars,f10_intructions)


_data = []

_code = [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10]

_types = [TypeNode("Object",[],[f1,f2,f3]) , TypeNode("IO" , [],[f4,f5,f6,f7]) , TypeNode("String", [],[f8,f9,f10])]