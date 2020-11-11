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
        self.build_basic_string()

    def build_basic_object(self):
        self.current_type = self.context.get_type('Object')
        type_node = self.register_type('Object')
        type_node.attributes = [ attr.name for attr in self.current_type.get_all_attributes() ]
        type_node.methods = [ (method.name, self.to_function_name(method.name, typex.name))  for method, typex in self.current_type.get_all_methods() ]
        ### abort function
        self.current_method = self.current_type.get_method('abort')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        self.register_instruction(ErrorNode(0))
        self.current_method = self.current_function = None
        ### copy function
        self.current_method = self.current_type.get_method('copy')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        copy_inst = self.define_internal_local()
        self.register_instruction(CopyNode(copy_inst, self_local))
        self.register_instruction(ReturnNode(copy_inst))
        self.current_method = self.current_function = None
        ### type_name
        self.current_method = self.current_type.get_method('type_name')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        obj_type = self.define_internal_local()
        type_name_inst = self.define_internal_local()
        self.register_instruction(TypeOfNode(self_local, obj_type))
        self.register_instruction(TypeNameNode(type_name_inst, obj_type))
        self.register_instruction(ReturnNode(type_name_inst))
        self.current_method = self.current_function = None
        self.current_type = None

    def build_basic_string(self):
        self.current_type = self.context.get_type('String')
        type_node = self.register_type('String')
        type_node.attributes = [ attr.name for attr in self.current_type.get_all_attributes() ]
        type_node.methods = [ (method.name, self.to_function_name(method.name, typex.name))  for method, typex in self.current_type.get_all_methods() ]
        ### length
        self.current_method = self.current_type.get_method('length')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        length_var = self.define_internal_local()
        self.register_instruction(LengthNode(length_var, self_local))
        self.register_instruction(ReturnNode(length_var))
        self.current_method = self.current_function = None
        ### concat
        self.current_method = self.current_type.get_method('concat')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        param_local = self.register_param(VariableInfo('s', None))
        result_msg = self.define_internal_local()
        self.register_instruction(ConcatNode(result_msg, self_local, param_local))
        self.register_instruction(ReturnNode(result_msg))
        self.current_method = self.current_function = None
        ### substr
        self.current_method = self.current_type.get_method('substr')
        type_name = self.current_type.name
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        start_parm = self.register_param(VariableInfo('i', None))
        length_param = self.register_param(VariableInfo('l', None))
        result_msg = self.define_internal_local()
        length_var = self.define_internal_local()
        sum_var = self.define_internal_local()
        cmp_var1 = self.define_internal_local()
        cmp_var2 = self.define_internal_local()
        cmp_var3 = self.define_internal_local()
        no_error_label1 = self.to_label_name('error1')
        no_error_label2 = self.to_label_name('error2')
        no_error_label3 = self.to_label_name('error3')
        self.register_instruction(LengthNode(length_var, self_local))
        # start param negative
        self.register_instruction(LessEqNode(cmp_var1, 0, start_parm))
        self.register_instruction(GotoIfNode(cmp_var1, no_error_label1))
        self.register_instruction(ErrorNode())
        self.register_instruction(LabelNode(no_error_label1))
        # length param negative
        self.register_instruction(LessEqNode(cmp_var2, 0, length_param))
        self.register_instruction(GotoIfNode(cmp_var2, no_error_label2))
        self.register_instruction(ErrorNode())
        self.register_instruction(LabelNode(no_error_label2))
        # substr larger than max length
        self.register_instruction(PlusNode(sum_var, start_parm, length_param))
        self.register_instruction(LessEqNode(cmp_var3, sum_var, length_var))
        self.register_instruction(GotoIfNode(cmp_var3, no_error_label3))
        self.register_instruction(ErrorNode())
        self.register_instruction(LabelNode(no_error_label3))
        self.register_instruction(SubstringNode(result_msg, self_local, start_parm, length_param))
        self.register_instruction(ReturnNode(result_msg))
        self.current_method = self.current_function = None
        self.current_type = None
