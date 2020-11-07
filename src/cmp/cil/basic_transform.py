from .ast import ProgramNode, TypeNode, FunctionNode, ParamNode, LocalNode, AssignNode, PlusNode \
    , MinusNode, StarNode, DivNode, AllocateNode, TypeOfNode, StaticCallNode, DynamicCallNode    \
    , ArgNode, ReturnNode, ReadNode, PrintNode, LoadNode, LengthNode, ConcatNode, PrefixNode     \
    , SubstringNode, ToStrNode, GetAttribNode, SetAttribNode, LabelNode, GotoNode, GotoIfNode    \
    , DataNode, LessNode, LessEqNode, ComplementNode, IsVoidNode, EqualNode, ConformNode         \
    , CleanArgsNode, ErrorNode, CopyNode, TypeNameNode
from .utils import Scope


class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype

class BASE_COOL_CIL_TRANSFORM:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        self.label_count = 0
        self.build_basics()
    
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
        self.params.append(param_node)
        return vinfo.name
    
    def register_local(self, vinfo):
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
        ###############################
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'

    def to_label_name(self, label_name):
        self.label_count += 1
        return f'label_{label_name}{self.label_count}_at_{self.current_function.name[9:]}'
    
    def register_function(self, function_name):
        function_node = FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        data_node = None
        for data in self.dotdata:
            if data.value == value:
                data_node = data
                break
        else:
            vname = f'data_{len(self.dotdata)}'
            data_node = DataNode(vname, value)
            self.dotdata.append(data_node)
        return data_node

    ###################################

    def build_basics(self):
        self.build_basic_object()

    def build_basic_object(self):
        self.current_type = self.context.get_type('Object')
        type_node = self.register_type('Object')
        type_node.attributes = [ attr.name for attr in self.current_type.get_all_attributes() ]
        type_node.methods = [ (method.name, self.to_function_name(method.name, typex.name))  for method, typex in self.current_type.get_all_methods() ]
        ### abort function
        func_scope = Scope()
        self.current_method = self.current_type.get_method('abort')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        func_scope.define_var('self', self_local)
        for param_name in self.current_method.param_names:
            param_local = self.register_param(VariableInfo(param_name, None))
            func_scope.define_var(param_name, param_local)
        self.register_instruction(ErrorNode(0))
        self.current_method = self.current_function = None
        ### copy function
        func_scope = Scope()
        self.current_method = self.current_type.get_method('copy')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        func_scope.define_var('self', self_local)
        for param_name in self.current_method.param_names:
            param_local = self.register_param(VariableInfo(param_name, None))
            func_scope.define_var(param_name, param_local)
        copy_inst = self.define_internal_local()
        self.register_instruction(CopyNode(copy_inst, self_local))
        self.register_instruction(ReturnNode(copy_inst))
        self.current_method = self.current_function = None
        ### type_name
        func_scope = Scope()
        self.current_method = self.current_type.get_method('type_name')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        func_scope.define_var('self', self_local)
        for param_name in self.current_method.param_names:
            param_local = self.register_param(VariableInfo(param_name, None))
            func_scope.define_var(param_name, param_local)
        obj_type = self.define_internal_local()
        type_name_inst = self.define_internal_local()
        self.register_instruction(TypeOfNode(self_local, obj_type))
        self.register_instruction(TypeNameNode(type_name_inst, obj_type))
        self.register_instruction(ReturnNode(type_name_inst))
        self.current_method = self.current_function = None
        self.current_type = None
