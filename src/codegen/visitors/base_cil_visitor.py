from codegen.cil_ast import ParamNode, LocalNode, FunctionNode, TypeNode, DataNode
from semantic.tools import VariableInfo, Scope, Context
from semantic.types import Type, StringType, ObjectType, IOType, Method, Attribute
from codegen import cil_ast as cil
from utils.ast import BinaryNode, UnaryNode, AssignNode
import re

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type: Type = None
        self.current_method: Method = None
        self.current_function = None
        self.context: Context = context
        self.idx = 0
        self.name_regex = re.compile('local_.+_(.+)_\d+')
        self.constructors = []

    @property
    def index(self):
        i = self.idx
        self.idx += 1
        return i
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property 
    def instructions(self):
        return self.current_function.instructions
    
    def register_param(self, vname, vtype):
        name = f'param_{self.current_function.name[9:]}_{vname}_{len(self.params)}'
        param_node = ParamNode(vname, vtype, self.index)
        self.params.append(param_node)
        return vname
    
    def register_local(self, vname):
        name = f'local_{self.current_function.name[9:]}_{vname}_{len(self.localvars)}' 
        local_node = LocalNode(name, self.index)
        self.localvars.append(local_node)
        return name

    def define_internal_local(self):
        return self.register_local('internal')

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        instruction.index = self.index
        return instruction
    
    def to_attr_name(self, attr_name, type_name):
        return f'attribute_{attr_name}_{type_name}'

    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_{type_name}'
    
    def to_var_name(self, var_name):
        for node in self.localvars:
            m = self.name_regex.match(node.name).groups()[0]
            if  m == var_name:
                return node.name
        return ''
        
    def register_function(self, function_name):
        function_node = FunctionNode(function_name, [], [], [], self.index)
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name):
        type_node = TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = DataNode(vname, value, self.index)
        self.dotdata.append(data_node)  
        return data_node

    def _define_binary_node(self, node: BinaryNode, scope: Scope, cil_node: cil.Node):
        result = self.define_internal_local()
        left, typex = self.visit(node.left, scope)
        right, typex = self.visit(node.right, scope)
        self.register_instruction(cil_node(result, left, right))
        return result, typex

    def _define_unary_node(self, node: UnaryNode, scope: Scope, cil_node):
        result = self.define_internal_local()
        expr, typex = self.visit(node.expr, scope)
        self.register_instruction(cil_node(result, expr))
        return result, typex

    def initialize_attr(self, constructor, attr: Attribute, scope: Scope):
        if attr.expr:
            constructor.body.expr_list.append(AssignNode(attr.name, attr.expr))
        elif attr.type == 'Int':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantNumNode(0)))
        elif attr.type == 'Bool':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantBoolNode(False)))
        elif attr.type == 'String':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantStrNode("")))

    def create_built_in(self):
        f1_params = [ParamNode("self", 'Object')]
        f1_localVars = [LocalNode("local_abort_self_0")]
        f1_intructions = [cil.AssignNode(f1_localVars[0].name,f1_params[0].name, self.index),cil.ExitNode(idx=self.index),cil.ReturnNode(f1_localVars[0].name, self.index)]
        f1 = FunctionNode("function_abort_Object",f1_params,f1_localVars,f1_intructions)

        f2_params = [ParamNode("self", 'Object')]
        f2_localVars = [LocalNode("local_type_name_result_0")]
        f2_intructions = [cil.TypeOfNode(f2_params[0].name,f2_localVars[0].name, self.index),cil.ReturnNode(f2_localVars[0].name, self.index)]
        f2 = FunctionNode("function_type_name_Object",f2_params,f2_localVars,f2_intructions)

        f3_params = [ParamNode("self", 'Object')]
        f3_localVars = [LocalNode("local_copy_result_0")]
        f3_intructions = [cil.CopyNode(f3_localVars[0].name,f3_params[0].name, self.index),cil.ReturnNode(f3_localVars[0].name, self.index)]
        f3 = FunctionNode("function_copy_Object",f3_params,f3_localVars,f3_intructions)

        f4_params = [ParamNode("self", 'IO'), ParamNode("word", 'String')]
        f4_localVars = [LocalNode("local_out_string_self_0"),LocalNode("local_out_string_word_1")]
        f4_intructions = [cil.AssignNode(f4_localVars[0].name,f4_params[0].name, self.index),cil.LoadNode(f4_localVars[1].name,f4_params[1].name, self.index),cil.OutStringNode(f4_localVars[1].name, self.index),cil.ReturnNode(f4_localVars[0].name, self.index)]
        f4 = FunctionNode("function_out_string_IO",f4_params,f4_localVars,f4_intructions)

        f5_params = [ParamNode("self", 'IO'),ParamNode("number", 'Int')]
        f5_localVars = [LocalNode("local_out_int_self_0")]
        f5_intructions = [cil.AssignNode(f5_localVars[0].name,f5_params[0].name, self.index),cil.OutIntNode(f5_params[1].name, self.index),cil.ReturnNode(f5_localVars[0].name, self.index)]
        f5 = FunctionNode("function_out_int_IO",f5_params,f5_localVars,f5_intructions)

        f6_params = [ParamNode("self", 'IO')]
        f6_localVars = [LocalNode("local_in_int_result_0")]
        f6_intructions = [cil.ReadIntNode(f6_localVars[0].name, self.index),cil.ReturnNode(f6_localVars[0].name, self.index)]
        f6 = FunctionNode("function_in_int_IO",f6_params,f6_localVars,f6_intructions)

        f7_params = [ParamNode("self", 'IO')]
        f7_localVars = [LocalNode("local_in_string_result_0")]
        f7_intructions = [cil.ReadStringNode(f7_localVars[0].name, self.index),cil.ReturnNode(f7_localVars[0].name, self.index)]
        f7 = FunctionNode("function_in_string_IO",f7_params,f7_localVars,f7_intructions)

        f8_params = [ParamNode("self", 'String')]
        f8_localVars = [LocalNode("local_length_word_0"),LocalNode("local_length_result_1")]
        f8_intructions = [cil.LoadNode(f8_localVars[0].name,f8_params[0].name, self.index),cil.LengthNode(f8_localVars[1].name,f8_localVars[0].name, self.index),cil.ReturnNode(f8_localVars[1].name, self.index)]
        f8 = FunctionNode("function_length_String",f8_params,f8_localVars,f8_intructions)

        f9_params = [ParamNode("self", 'String'),ParamNode("word", 'String')]
        f9_localVars = [LocalNode("local_concat_word_0"),LocalNode("local_concat_word_1"),LocalNode("local_concat_result_2")]
        f9_intructions = [cil.LoadNode(f9_localVars[0].name,f9_params[0].name, self.index),cil.LoadNode(f9_localVars[1].name,f9_params[1].name, self.index),cil.ConcatNode(f9_localVars[2].name,f9_localVars[0].name,f9_localVars[1].name, self.index),cil.ReturnNode(f9_localVars[2].name, self.index)]
        f9 = FunctionNode("function_concat_String",f9_params,f9_localVars,f9_intructions)

        f10_params = [ParamNode("self", 'String'),ParamNode("begin", 'Int'),ParamNode("end", 'Int')]
        f10_localVars = [LocalNode("local_substr_word_0"),LocalNode("local_substr_result_1")]
        f10_intructions = [cil.LoadNode(f10_localVars[0].name,f10_params[0].name, self.index), cil.SubstringNode(f10_localVars[1].name,f10_localVars[0].name,f10_params[1].name,f10_params[2].name, self.index), cil.ReturnNode(f10_localVars[0].name)]
        f10 = FunctionNode("function_substr_String",f10_params,f10_localVars,f10_intructions)

        self.dotcode = [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10]
        self.dottypes += [TypeNode("Object", [], [('abort', f1.name), ('type_of', f2.name), ('copy', f3.name)]), 
                TypeNode("IO", [], [('out_string', f4.name), ('out_int', f5.name), ('in_int', f6.name), ('in_string', f7.name)]) , 
                TypeNode("String", [], [('length', f8.name), ('concat', f9.name), ('substr', f10.name)]), 
                TypeNode('Int'),
                TypeNode('Bool')]
