import cil.nodes as nodes
from abstract.semantics import VariableInfo

class BaseCoolToCilVisitor:

    def __init__(self, context):
        self.dot_types = []
        self.dot_data = []
        self.dot_code = []
        self.context = context
        self.current_type = None
        self.current_method = None
        self.current_function = None

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self):
        return self.current_function.instructions

    def register_params(self, vinfo):
        vinfo.name = f'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        param_node = nodes.ParamNode(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def register_local(self, vinfo):
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = nodes.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        self.register_local(vinfo)

    def to_function_name(self, method_name, type_name):
        return f"function_{method_name}_at_{type_name}"

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction

    def register_function(self, function_name):
        function_node = nodes.FunctionNode(function_name, [], [], [])
        self.dot_code.append(function_node)
        return function_node

    def register_type(self, name):
        type_node = nodes.TypeNode(name)
        self.dot_types.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dot_data)}'
        data_node = nodes.DataNode(vname, value)
        self.dot_data.append(data_node)
        return data_node


