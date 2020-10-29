from codegen.cil_ast import ParamNode, LocalNode, FunctionNode, TypeNode, DataNode
from semantic.tools import VariableInfo, Scope, Context
from semantic.types import Type, StringType, ObjectType, IOType, Method, Attribute
from codegen import cil_ast as cil
from utils.ast import BinaryNode, UnaryNode, AssignNode

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type: Type = None
        self.current_method: Method = None
        self.current_function = None
        self.context: Context = context
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property 
    def instructions(self):
        return self.current_function.instructions
    
    def register_param(self, vinfo):
        param_node = ParamNode(vinfo.name)
        vinfo.name = f'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        self.params.append(param_node)
        return vinfo.name
    
    def register_local(self, vinfo):
        name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = LocalNode(name)
        self.localvars.append(local_node)
        return name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_attr_name(self, attr_name, type_name):
        return f'attribute_{attr_name}_{type_name}'

    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_{type_name}'
    
    def register_function(self, function_name):
        function_node = FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name):
        type_node = TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = DataNode(vname, value)
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

    def initialize_attr(self, constructor, attr: Attribute):
        if attr.expr:
            constructor.body.expr_list.append(AssignNode(attr.name, attr.expr))
        elif attr.type == 'Int':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantNumNode(0)))
        elif attr.type == 'Bool':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantBoolNode(False)))
        elif attr.type == 'String':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantStrNode("")))


    ###### TODO: Esto es lo de los métodos nativos que no creo que funcione ######
    def native_methods(self, typex: Type, name: str, *args):
        if typex == StringType():
            return self.string_methods(name, *args)
        elif typex == ObjectType():
            return self.object_methods(name, *args)
        elif typex == IOType():
            return self.io_methods(name, *args)

    def string_methods(self, name, *args):
        result = self.define_internal_local()
        if name == 'length':
            self.register_instruction(cil.LengthNode(result, *args))
        elif name == 'concat':
            self.register_instruction(cil.ConcatNode(result, *args))
        elif name == 'substr':
            self.register_instruction(cil.SubstringNode(result, *args))
        return result

    def object_methods(self, name, result, *args):
        if name == 'abort':
            pass
        elif name == 'type_name':
            pass
        elif name == 'copy':
            pass

    def io_methods(self, name, result, *args):
        # ? Not sure of the difference between string and int
        if name == 'out_string':
            self.register_instruction(cil.PrintNode(*args))
        elif name == 'out_int':
            aux = self.define_internal_local()
            self.register_instruction(cil.ToStrNode(aux, *args))
            self.register_instruction(cil.PrintNode(aux))
        elif name == 'in_string':
            result = self.define_internal_local()
            self.register_instruction(cil.ReadNode(result))
            return result
        elif name == 'in_int':
            result = self.define_internal_local()
            self.register_instruction(cil.ReadNode(result))
            return result
