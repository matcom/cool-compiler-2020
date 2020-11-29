from codegen.cil_ast import ParamNode, LocalNode, FunctionNode, TypeNode, DataNode
from semantic.tools import VariableInfo, Scope, Context
from semantic.types import Type, StringType, ObjectType, IOType, Method, Attribute
from codegen import cil_ast as cil
from utils.ast import BinaryNode, UnaryNode, AssignNode, ProgramNode
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
        # self.name_regex = re.compile('local_[^_]+_[^_]+_(.+)_\d+')
        self.constructors = []
        self.void_data = None
        self.inherit_graph = {}

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
        regex = re.compile(f'local_{self.current_function.name[9:]}_(.+)_\d+')
        for node in reversed(self.localvars):
            m = regex.match(node.name).groups()[0]
            if  m == var_name:
                return node.name
        for node in self.params:
            if node.name == var_name:
                return var_name
        return None
        
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
        else:
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantVoidNode(atrr.name)))

    def create_built_in(self):

        # ---------------------------------- Object Functions ---------------------------------- #
        f1_params = [ParamNode("self", 'Object')]
        f1_localVars = [LocalNode("local_abort_Object_self_0")]
        f1_intructions = [cil.AssignNode(f1_localVars[0].name,f1_params[0].name, self.index),
                          cil.ExitNode(f1_params[0].name, idx=self.index),
                          cil.ReturnNode(f1_localVars[0].name, self.index)]
        f1 = FunctionNode("function_abort_Object",f1_params,f1_localVars,f1_intructions)

        f2_params = [ParamNode("self", 'Object')]
        f2_localVars = [LocalNode("local_type_name_Object_result_0")]
        f2_intructions = [cil.TypeOfNode(f2_params[0].name,f2_localVars[0].name, self.index),
                          cil.ReturnNode(f2_localVars[0].name, self.index)]
        f2 = FunctionNode("function_type_name_Object",f2_params,f2_localVars,f2_intructions)

        f3_params = [ParamNode("self", 'Object')]
        f3_localVars = [LocalNode("local_copy_Object_result_0")]
        f3_intructions = [cil.CopyNode(f3_localVars[0].name,f3_params[0].name, self.index),
                          cil.ReturnNode(f3_localVars[0].name, self.index)]
        f3 = FunctionNode("function_copy_Object",f3_params,f3_localVars,f3_intructions)

        # ---------------------------------- IO Functions ---------------------------------- #
        f4_params = [ParamNode("self", 'IO'), ParamNode("word", 'String')]
        f4_localVars = [LocalNode("local_out_string_String_self_0")]
        f4_intructions = [cil.AssignNode(f4_localVars[0].name, f4_params[0].name, self.index),
                          cil.OutStringNode(f4_params[1].name, self.index),
                          cil.ReturnNode(f4_localVars[0].name, self.index)]
        f4 = FunctionNode("function_out_string_IO",f4_params,f4_localVars,f4_intructions)

        f5_params = [ParamNode("self", 'IO'),ParamNode("number", 'Int')]
        f5_localVars = [LocalNode("local_out_int_IO_self_0")]
        f5_intructions = [cil.AssignNode(f5_localVars[0].name,f5_params[0].name, self.index),
                          cil.OutIntNode(f5_params[1].name, self.index),
                          cil.ReturnNode(f5_localVars[0].name, self.index)]
        f5 = FunctionNode("function_out_int_IO",f5_params,f5_localVars,f5_intructions)

        f6_params = [ParamNode("self", 'IO')]
        f6_localVars = [LocalNode("local_in_int_IO_result_0")]
        f6_intructions = [cil.ReadIntNode(f6_localVars[0].name, self.index),
                          cil.ReturnNode(f6_localVars[0].name, self.index)]
        f6 = FunctionNode("function_in_int_IO",f6_params,f6_localVars,f6_intructions)

        f7_params = [ParamNode("self", 'IO')]
        f7_localVars = [LocalNode("local_in_string_IO_result_0")]
        f7_intructions = [cil.ReadStringNode(f7_localVars[0].name, self.index),
                          cil.ReturnNode(f7_localVars[0].name, self.index)]
        f7 = FunctionNode("function_in_string_IO",f7_params,f7_localVars,f7_intructions)

        # ---------------------------------- String Functions ---------------------------------- #
        f8_params = [ParamNode("self", 'String')]
        f8_localVars = [LocalNode("local_length_String_result_0")]
        f8_intructions = [cil.LengthNode(f8_localVars[0].name,f8_params[0].name, self.index),
                         cil.ReturnNode(f8_localVars[0].name, self.index)]
        f8 = FunctionNode("function_length_String",f8_params,f8_localVars,f8_intructions)

        f9_params = [ParamNode("self", 'String'),ParamNode("word", 'String')]
        f9_localVars = [LocalNode("local_concat_String_result_0")]
        f9_intructions = [cil.ConcatNode(f9_localVars[0].name,f9_params[0].name,f9_params[1].name, self.index),
                          cil.ReturnNode(f9_localVars[0].name, self.index)]
        f9 = FunctionNode("function_concat_String",f9_params,f9_localVars,f9_intructions)

        f10_params = [ParamNode("self", 'String'),ParamNode("begin", 'Int'),ParamNode("end", 'Int')]
        f10_localVars = [LocalNode("local_substr_String_result_0")]
        f10_intructions = [cil.SubstringNode(f10_localVars[0].name,f10_params[0].name,f10_params[1].name,f10_params[2].name, self.index), 
                           cil.ReturnNode(f10_localVars[0].name, self.index)]
        f10 = FunctionNode("function_substr_String",f10_params,f10_localVars,f10_intructions)

        f11_params = [ParamNode("self", 'String')]
        f11_localVars = [LocalNode("local_type_name_String_result_0")]
        f11_intructions = [cil.LoadNode(f11_localVars[0].name, 'type_String', self.index),
                           cil.ReturnNode(f11_localVars[0].name, self.index)]
        f11 = FunctionNode("function_type_name_String",f11_params,f11_localVars,f11_intructions)

        f12_params = [ParamNode("self", 'String')]
        f12_localVars = [LocalNode("local_copy_String_result_0")]
        f12_intructions = [cil.ConcatNode(f12_localVars[0].name, f12_params[0].name, None, self.index),
                           cil.ReturnNode(f12_localVars[0].name, self.index)]
        f12 = FunctionNode("function_copy_String",f12_params,f12_localVars,f12_intructions)

        f17_params = [ParamNode("self", 'String')]
        f17_localVars = [LocalNode('local_abort_String_msg_0')]
        f17_intructions = [cil.LoadNode(f17_params[0].name, 'string_abort'), 
                           cil.OutStringNode(f17_params[0].name, self.index),
                           cil.ExitNode(f17_params[0].name, idx=self.index)]
        f17 = FunctionNode("function_abort_String",f17_params,f17_localVars,f17_intructions)

        # ---------------------------------- Int Functions ---------------------------------- #
        f13_params = [ParamNode("self", 'Int')]
        f13_localVars = [LocalNode("local_type_name_Int_result_0")]
        f13_intructions = [cil.LoadNode(f13_localVars[0].name, 'type_Int', self.index),
                           cil.ReturnNode(f13_localVars[0].name, self.index)]
        f13 = FunctionNode("function_type_name_Int",f13_params,f13_localVars,f13_intructions)

        f14_params = [ParamNode("self", 'Int')]
        f14_localVars = [LocalNode("local_copy_Int_result_0")]
        f14_intructions = [cil.AssignNode(f14_localVars[0].name, f14_params[0].name), 
                           cil.ReturnNode(f14_localVars[0].name, self.index)]
        f14 = FunctionNode("function_copy_Int",f14_params,f14_localVars,f14_intructions)

        f18_params = [ParamNode("self", 'Int')]
        f18_localVars = [LocalNode('local_abort_Int_msg_0')]
        f18_intructions = [cil.LoadNode(f18_params[0].name, 'int_abort'), 
                           cil.OutStringNode(f18_params[0].name, self.index),
                           cil.ExitNode(f18_params[0].name, idx=self.index)]
        f18 = FunctionNode("function_abort_Int",f18_params,f18_localVars,f18_intructions)

        # ---------------------------------- Bool Functions ---------------------------------- #
        f15_params = [ParamNode("self", 'Bool')]
        f15_localVars = [LocalNode("local_type_name_Bool_result_0")]
        f15_intructions = [cil.LoadNode(f15_localVars[0].name, 'type_Bool', self.index),
                           cil.ReturnNode(f15_localVars[0].name, self.index)]
        f15 = FunctionNode("function_type_name_Bool",f15_params,f15_localVars,f15_intructions)

        f16_params = [ParamNode("self", 'Bool')]
        f16_localVars = [LocalNode("local_copy_result_Bool_0")]
        f16_intructions = [cil.AssignNode(f16_localVars[0].name, f16_params[0].name), 
                           cil.ReturnNode(f16_localVars[0].name, self.index)]
        f16 = FunctionNode("function_copy_Bool",f16_params,f16_localVars,f16_intructions)

        f19_params = [ParamNode("self", 'Bool')]
        f19_localVars = [LocalNode('local_abort_Bool_msg_0')]
        f19_intructions = [cil.LoadNode(f19_params[0].name, 'bool_abort'), 
                           cil.OutStringNode(f19_params[0].name, self.index),
                           cil.ExitNode(f19_params[0].name, idx=self.index)]
        f19 = FunctionNode("function_abort_Bool",f19_params,f19_localVars,f19_intructions)


        self.dotcode += [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11, f12, f13, f14, f15, f16, f17, f18, f19]
        object_methods = [('abort', f1.name), ('type_name', f2.name), ('copy', f3.name)]
        string_methods = [('length', f8.name), ('concat', f9.name), ('substr', f10.name), ('abort', f17.name), ('type_name', f11.name), ('copy', f12.name)]
        io_methods = [('out_string', f4.name), ('out_int', f5.name), ('in_int', f6.name), ('in_string', f7.name)]
        int_methods = [('abort', f18.name), ('type_name', f13.name), ('copy', f14.name)]
        bool_methods = [('abort', f19.name), ('type_name', f15.name), ('copy', f16.name)]

        self.dottypes += [TypeNode("Object", [], object_methods), 
                TypeNode("IO", [], object_methods + io_methods) , 
                TypeNode("String", [],  string_methods), 
                TypeNode('Int', [], int_methods),
                TypeNode('Bool', [], bool_methods)]

    def sort_option_nodes_by_type(self, case_list):
        "Sort option nodes from specific types to more general types"
        return sorted(case_list, reverse=True,
                    key=lambda x: self.context.get_depth(x.typex))

    def check_void(self, expr):
        result = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(expr, result))
        
        void_expr = self.define_internal_local()
        self.register_instruction(cil.LoadNode(void_expr, self.void_data))
        self.register_instruction(cil.EqualNode(result, result, void_expr))
        return result
        