import re
from typing import Any, Union, cast

from ..cool_lang.semantics.semantic_utils import Attribute, Type
from .ast import (
    AbortNode,
    ConcatNode,
    CopyNode,
    DataNode,
    ErrorNode,
    FunctionNode,
    GetAttribNode,
    GotoIfNode,
    LabelNode,
    LengthNode,
    LessEqNode,
    LocalNode,
    ParamNode,
    PlusNode,
    PrintIntNode,
    PrintStrNode,
    ReadIntNode,
    ReadStrNode,
    ReturnNode,
    SetAttribNode,
    SubstringNode,
    TypeNameNode,
    TypeNode,
    StaticCallNode,
    SetNode
)


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

    def unpack_type_by_value(self, value: str, static_type: Union[Type, str]):
        arg = static_type if isinstance(static_type, str) else static_type.name
        if arg in ["Int", "String", "Bool"]:
            raw_value = self.define_internal_local()
            self.register_instruction(
                GetAttribNode(
                    raw_value,
                    value,
                    "value",
                    arg,
                )
            )
            return raw_value
        return value

    def pack_type_by_value(self, value: str, static_type: Union[Type, str]):
        arg = static_type if isinstance(static_type, str) else static_type.name
        if arg in ["Int", "Bool", "String"]:
            packed = self.define_internal_local()
            self.register_instruction(StaticCallNode(f'init_{arg}', packed))
            self.register_instruction(SetAttribNode(packed, "value", value, arg))
            return packed
        return value

    def register_local(self, vinfo):
        func_name = re.findall(r"^function_(.+)$", self.current_function.name)
        if func_name:
            func_name = func_name[0]
        else:
            func_name = self.current_function.name
        vinfo.name = f"local_{func_name}_{vinfo.name}_{len(self.localvars)}"
        local_node = LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo("internal", None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
        ###########

    def to_function_name(self, method_name, type_name):
        return f"function_{method_name}_at_{type_name}"

    def to_label_name(self, label_name):
        self.label_count += 1
        return (
            f"label_{label_name}{self.label_count}_at_{self.current_function.name[9:]}"
        )

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
            vname = f"data_{len(self.dotdata)}"
            data_node = DataNode(vname, value)
            self.dotdata.append(data_node)
        return data_node

    ######################################################

    def build_basics(self):
        self.build_basic_object()
        self.build_basic_int()
        self.build_basic_bool()
        self.build_basic_string()
        self.build_basic_io()

    def get_features(self):
        return [
            feature.name
            if isinstance(feature, Attribute)
            else (
                feature[0].name,
                self.to_function_name(feature[0].name, feature[1].name),
            )
            for feature in self.current_type.get_all_features()
        ]

    def build_basic_int(self):
        self.current_type = self.context.get_type("Int")
        type_node = self.register_type("Int")
        type_node.name_dir = self.register_data("Int").name
        type_node.attributes = [
            attr.name for attr in self.current_type.get_all_attributes()
        ] + ["value"]
        type_node.methods = [
            (method.name, self.to_function_name(method.name, typex.name))
            for method, typex in self.current_type.get_all_methods()
        ]
        type_node.features = self.get_features() + [cast(Any, "value")]

    def build_basic_bool(self):
        self.current_type = self.context.get_type("Bool")
        type_node = self.register_type("Bool")
        type_node.name_dir = self.register_data("Bool").name
        type_node.attributes = [
            attr.name for attr in self.current_type.get_all_attributes()
        ] + ["value"]
        type_node.methods = [
            (method.name, self.to_function_name(method.name, typex.name))
            for method, typex in self.current_type.get_all_methods()
        ]
        type_node.features = self.get_features() + [cast(Any, "value")]

    def build_basic_object(self):
        self.current_type = self.context.get_type("Object")
        type_node = self.register_type("Object")
        type_node.name_dir = self.register_data("Object").name
        type_node.attributes = [
            attr.name for attr in self.current_type.get_all_attributes()
        ]
        type_node.methods = [
            (method.name, self.to_function_name(method.name, typex.name))
            for method, typex in self.current_type.get_all_methods()
        ]
        type_node.features = self.get_features()
        # abort function
        self.current_method = self.current_type.get_method("abort")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        self_local = self.register_param(VariableInfo("self", None))
        type_name = self.define_internal_local()
        abort_msg = self.register_data("Abort called from class ").name
        eol = self.register_data("\n").name
        msg = self.define_internal_local()
        msg_eol = self.define_internal_local()
        self.register_instruction(TypeNameNode(type_name, self_local))
        self.register_instruction(ConcatNode(msg, abort_msg, type_name))
        self.register_instruction(ConcatNode(msg_eol, msg, eol))
        self.register_instruction(PrintStrNode(msg_eol))
        self.register_instruction(AbortNode())
        self.current_method = self.current_function = None
        # copy function
        self.current_method = self.current_type.get_method("copy")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        self_local = self.register_param(VariableInfo("self", None))
        copy_inst = self.define_internal_local()
        self.register_instruction(CopyNode(copy_inst, self_local))
        self.register_instruction(ReturnNode(copy_inst))
        self.current_method = self.current_function = None
        # type_name
        self.current_method = self.current_type.get_method("type_name")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        self_local = self.register_param(VariableInfo("self", None))
        type_name_inst = self.define_internal_local()
        self.register_instruction(TypeNameNode(type_name_inst, self_local))
        type_name_inst = self.pack_type_by_value(type_name_inst, "String")
        self.register_instruction(ReturnNode(type_name_inst))
        self.current_method = self.current_function = None
        self.current_type = None

    def build_basic_io(self):
        self.current_type = self.context.get_type("IO")
        type_node = self.register_type("IO")
        type_node.name_dir = self.register_data("IO").name
        type_node.attributes = [
            attr.name for attr in self.current_type.get_all_attributes()
        ]
        type_node.methods = [
            (method.name, self.to_function_name(method.name, typex.name))
            for method, typex in self.current_type.get_all_methods()
        ]
        type_node.features = self.get_features()
        # in_string
        self.current_method = self.current_type.get_method("in_string")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        _ = self.register_param(VariableInfo("self", None))
        result_msg = self.define_internal_local()
        self.register_instruction(ReadStrNode(result_msg))
        string_inst = self.pack_type_by_value(result_msg, "String")
        self.register_instruction(ReturnNode(string_inst))
        self.current_method = self.current_function = None
        # out_string
        self.current_method = self.current_type.get_method("out_string")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        self_local = self.register_param(VariableInfo("self", None))
        string_inst = self.register_param(VariableInfo("x", None))
        out_msg = self.unpack_type_by_value(string_inst, "String")
        self.register_instruction(PrintStrNode(out_msg))
        self.register_instruction(ReturnNode(self_local))
        self.current_method = self.current_function = None
        # in_int
        self.current_method = self.current_type.get_method("in_int")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        _ = self.register_param(VariableInfo("self", None))
        result_int = self.define_internal_local()
        self.register_instruction(ReadIntNode(result_int))
        result = self.pack_type_by_value(result_int, "Int")
        self.register_instruction(ReturnNode(result))
        self.current_method = self.current_function = None
        # out_int
        self.current_method = self.current_type.get_method("out_int")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        self_local = self.register_param(VariableInfo("self", None))
        int_inst = self.register_param(VariableInfo("x", None))
        out_int = self.unpack_type_by_value(int_inst, "Int")
        self.register_instruction(PrintIntNode(out_int))
        self.register_instruction(ReturnNode(self_local))
        self.current_method = self.current_function = None
        self.current_type = None

    def build_basic_string(self):
        self.current_type = self.context.get_type("String")
        type_node = self.register_type("String")
        type_node.name_dir = self.register_data("String").name
        type_node.attributes = [
            attr.name for attr in self.current_type.get_all_attributes()
        ] + ["value"]
        type_node.methods = [
            (method.name, self.to_function_name(method.name, typex.name))
            for method, typex in self.current_type.get_all_methods()
        ]
        type_node.features = self.get_features() + [cast(Any, "value")]
        # length
        self.current_method = self.current_type.get_method("length")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        self_local = self.register_param(VariableInfo("self", None))
        length_var = self.define_internal_local()
        str_raw = self.unpack_type_by_value(self_local, "String")
        self.register_instruction(LengthNode(length_var, str_raw))
        length = self.pack_type_by_value(length_var, "Int")
        self.register_instruction(ReturnNode(length))
        self.current_method = self.current_function = None
        # concat
        self.current_method = self.current_type.get_method("concat")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        self_local = self.register_param(VariableInfo("self", None))
        param_local = self.register_param(VariableInfo("s", None))
        str_raw = self.unpack_type_by_value(self_local, "String")
        str_raw2 = self.unpack_type_by_value(param_local, "String")
        result_msg = self.define_internal_local()
        self.register_instruction(ConcatNode(result_msg, str_raw, str_raw2))
        string_inst = self.pack_type_by_value(result_msg, "String")
        self.register_instruction(ReturnNode(string_inst))
        self.current_method = self.current_function = None
        # substr
        self.current_method = self.current_type.get_method("substr")
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        self_local = self.register_param(VariableInfo("self", None))
        start_parm = self.register_param(VariableInfo("i", None))
        length_param = self.register_param(VariableInfo("l", None))
        result_msg = self.define_internal_local()
        length_var = self.define_internal_local()
        zero = self.define_internal_local()
        sum_var = self.define_internal_local()
        cmp_var1 = self.define_internal_local()
        cmp_var2 = self.define_internal_local()
        cmp_var3 = self.define_internal_local()
        no_error_label1 = self.to_label_name("error1")
        no_error_label2 = self.to_label_name("error2")
        no_error_label3 = self.to_label_name("error3")
        str_raw = self.unpack_type_by_value(self_local, "String")
        # self.register_instruction(StaticCallNode("init_Int", zero))
        # zero = self.unpack_type_by_value(zero, "Int")
        self.register_instruction(SetNode(zero, 0))
        start_raw = self.unpack_type_by_value(start_parm, "Int")
        length_raw = self.unpack_type_by_value(length_param, "Int")
        # self.register_instruction(PrintIntNode(start_raw))
        # self.register_instruction(PrintIntNode(length_raw))
        self.register_instruction(LengthNode(length_var, str_raw))
        # self.register_instruction(PrintIntNode(length_var))
        eol = self.register_data("\n").name
        msg_eol = self.define_internal_local()
        # start param negative
        self.register_instruction(LessEqNode(cmp_var1, zero, start_raw))
        self.register_instruction(GotoIfNode(cmp_var1, no_error_label1))
        error_msg = self.register_data("Invalid substring start").name
        self.register_instruction(ConcatNode(msg_eol, error_msg, eol))
        self.register_instruction(PrintStrNode(msg_eol))
        self.register_instruction(ErrorNode())
        self.register_instruction(LabelNode(no_error_label1))
        # length param negative
        self.register_instruction(LessEqNode(cmp_var2, zero, length_raw))
        self.register_instruction(GotoIfNode(cmp_var2, no_error_label2))
        error_msg = self.register_data("Invalid substring length").name
        self.register_instruction(ConcatNode(msg_eol, error_msg, eol))
        self.register_instruction(PrintStrNode(msg_eol))
        self.register_instruction(ErrorNode())
        self.register_instruction(LabelNode(no_error_label2))
        # substr larger than max length
        self.register_instruction(PlusNode(sum_var, start_raw, length_raw))
        self.register_instruction(LessEqNode(cmp_var3, sum_var, length_var))
        self.register_instruction(GotoIfNode(cmp_var3, no_error_label3))
        error_msg = self.register_data("Invalid substring").name
        self.register_instruction(ConcatNode(msg_eol, error_msg, eol))
        self.register_instruction(PrintStrNode(msg_eol))
        self.register_instruction(ErrorNode())
        self.register_instruction(LabelNode(no_error_label3))
        self.register_instruction(
            SubstringNode(result_msg, str_raw, start_raw, length_raw)
        )
        string_inst = self.pack_type_by_value(result_msg, "String")
        self.register_instruction(ReturnNode(string_inst))
        self.current_method = self.current_function = None
        self.current_type = None
