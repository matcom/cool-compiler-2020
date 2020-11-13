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
            expr, _ = self.visit(attr.expr, scope)
            constructor.body.expr_list.append(AssignNode(attr.name, attr.expr))
        elif attr.type == 'Int':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantNumNode(0)))
        elif attr.type == 'Bool':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantBoolNode(False)))
        elif attr.type == 'String':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantStrNode("")))