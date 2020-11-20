from .cil_ast import *
from ..cp.semantic import VariableInfo , Scope

class BASE_COOL_CIL_TRANSFORM:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        self.define_object_type()
        self.define_string_type()
        self.define_io_type()
        
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
        # vinfo.name = f'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
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
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'

    def to_attr_name(self, attr_name, type_name):
        return f'attribute_{attr_name}_at_{type_name}'
    
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

    ###################################

    def define_string_type(self):
        self.current_type = self.context.get_type('String')
        type_node = self.register_type(node.id)
        type_node.attributes = [(attr.name, self.to_attr_name(attr.name,atype)) for attr, atype in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
        
        self.current_method = self.current_type.get_method('length')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name,type_name))
        self_param = self.register_param(VariableInfo('self',None))
        dest = self.define_internal_local()
        self.register_instruction(LengthNode(dest,self_param))
        self.register_instruction(ReturnNode(dest))
        self.current_method = self.current_function = None
        self.current_type = None

        self.current_method = self.current_type.get_method('concat')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name,type_name))
        self_param = self.register_param(VariableInfo('self',None))
        str_param = self.register_param(VariableInfo('string',None))
        dest = self.define_internal_local()
        self.register_instruction(ConcatNode(dest,self_param,str_param))
        self.register_instruction(ReturnNode(dest))
        self.current_method = self.current_function = None

        self.current_method = self.current_type.get_method('substr')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name,type_name))
        self_param = self.register_param(VariableInfo('self',None))
        start = self.register_param(VariableInfo('start',None))
        length = self.register_param(VariableInfo('length',None))
        dest = self.define_internal_local()
        self.register_instruction(SubstringNode(dest,self_param,start,length))
        self.register_instruction(ReturnNode(dest))
        self.current_method = self.current_function = None
        
        self.current_method = self.current_type.get_method('prefix')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name,type_name))
        self_param = self.register_param(VariableInfo('self',None))
        length = self.register_param(VariableInfo('length',None))
        dest = self.define_internal_local()
        self.register_instruction(ConcatNode(dest,self_param,length))
        self.register_instruction(ReturnNode(dest))
        self.current_method = self.current_function = None
        self.current_type = None

    def define_io_type(self):
        self.current_type = self.context.get_type('IO')
        type_node = self.register_type('IO')
        type_node.attributes = [(attr.name, self.to_attr_name(attr.name,atype)) for attr, atype in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
        
        self.current_method = self.current_type.get_method('print')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name,type_name))
        str_val = self.define_internal_local()
        self.current_method = self.current_function = None
        self.register_instruction(PrintNode(str_val))

        self.current_method = self.current_type.get_method('read')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name,type_name))
        dest = self.define_internal_local()
        self.current_method = self.current_function = None
        self.register_instruction(ReadNode(dest))

        self.current_method = self.current_type.get_method('str')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name,type_name))
        dest = self.define_internal_local()
        str_val = self.register_param(VariableInfo('value',None))
        self.register_instruction(ToStrNode(dest,str_val))
        self.current_method = self.current_function = None
        self.current_type = None

    def define_object_type(self):
        self.current_type = self.context.get_type('Object')
        type_node = self.register_type('Object')
        type_node.attributes = [(attr.name, self.to_attr_name(attr.name,atype)) for attr, atype in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
        
        self.current_method = self.current_type.get_method('abort')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name,type_name))
        self.current_method = self.current_function = None
