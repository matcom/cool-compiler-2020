import cil
from semantic import VariableInfo, Scope

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = [ cil.DataNode('_empty', '')]
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    @property
    def labels(self):
        return self.current_function.labels

    def register_param(self, vinfo):
        vinfo.cilName = vinfo.name # f'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        param_node = cil.ParamNode(vinfo.cilName)
        self.params.append(param_node)
        return vinfo.cilName
    
    def register_local(self, vinfo):
        vinfo.cilName = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.cilName)
        self.localvars.append(local_node)
        return vinfo.cilName
    
    def register_label(self):
        name = f'label_{self.current_function.name[9:]}_{len(self.labels)}'
        self.labels.append(name)
        return name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def to_attribute_name(self, attr_name, attr_type):
        return f'attribute_{attr_type}_{attr_name}'

    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        for dataNode in self.dotdata:
            if dataNode.value == value:
                return dataNode
    
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node