from .cil_ast import *
from ..cp.semantic import VariableInfo, Scope


class BASE_COOL_CIL_TRANSFORM:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        self.attr_declarations = {}
        self._label_counter = 0
        self.define_object_type()
        self.define_string_type()
        self.define_io_type()
        self.define_int_type()
        self.define_bool_type()

    def label_counter_gen(self):
        self._label_counter += 1
        return self._label_counter

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

    def register_function(self, function_name):
        function_node = FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name):
        type_node = TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        for data in self.dotdata:
            if value == data.value:
                return data
        vname = f'data_{len(self.dotdata)}'
        data_node = DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def sort_case_list(self, case_expressions):
        return sorted(case_expressions, reverse=True,
                      key=lambda x: self.context.inheritance_deep(x.type.lex))

        ###################################

    def define_int_type(self):
        self.current_type = self.context.get_type('Int')
        type_node = self.register_type('Int')
        type_node.attributes = [(attr.name)
                                for attr in self.current_type.all_attributes()]
        type_node.attributes.append('value')
        type_node.methods = [(method.name, self.to_function_name(
            method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]

    def define_bool_type(self):
        self.current_type = self.context.get_type('Bool')
        type_node = self.register_type('Bool')
        type_node.attributes = [(attr.name)
                                for attr in self.current_type.all_attributes()]
        type_node.attributes.append('value')
        type_node.methods = [(method.name, self.to_function_name(
            method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]

    def define_string_type(self):
        self.current_type = self.context.get_type('String')
        type_node = self.register_type('String')
        type_node.attributes = [(attr.name)
                                for attr in self.current_type.all_attributes()]
        type_node.attributes.append('value')
        type_node.methods = [(method.name, self.to_function_name(
            method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
        type_node.features = type_node.attributes + type_node.methods

        self.current_method = self.current_type.get_method('length')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        self_param = self.register_param(VariableInfo('self', None))
        dest = self.define_internal_local()
        self.register_instruction(LengthNode(dest, self_param))
        self.register_instruction(ReturnNode(dest))
        self.current_method = self.current_function = None

        self.current_method = self.current_type.get_method('concat')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        self_param = self.register_param(VariableInfo('self', None))
        str_param = self.register_param(VariableInfo('string', None))
        dest = self.define_internal_local()
        self.register_instruction(ConcatNode(dest, self_param, str_param))
        self.register_instruction(ReturnNode(dest))
        self.current_method = self.current_function = None

        self.current_method = self.current_type.get_method('substr')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        self_param = self.register_param(VariableInfo('self', None))
        start = self.register_param(VariableInfo('start', None))
        length = self.register_param(VariableInfo('length', None))
        dest = self.define_internal_local()
        result_msg = self.define_internal_local()
        length_var = self.define_internal_local()
        zero = self.define_internal_local()
        sum_var = self.define_internal_local()
        cmp_var1 = self.define_internal_local()
        cmp_var2 = self.define_internal_local()
        cmp_var3 = self.define_internal_local()
        no_error_label1 = LabelNode("error1")
        no_error_label2 = LabelNode("error2")
        no_error_label3 = LabelNode("error3")
        self.register_instruction(BoxNode(zero, 0))
        self.register_instruction(LengthNode(length_var, self_param))
        eol = self.register_data('\\n').name
        msg_eol = self.define_internal_local()

        self.register_instruction(LessEqNode(cmp_var1, zero, start))
        self.register_instruction(IfGotoNode(cmp_var1, no_error_label1.label))
        error_msg = self.register_data("Invalid substring start").name
        self.register_instruction(ConcatNode(msg_eol, error_msg, eol))
        self.register_instruction(PrintStrNode(msg_eol))
        self.register_instruction(ErrorNode())
        self.register_instruction(no_error_label1)

        self.register_instruction(LessEqNode(cmp_var2, zero, length))
        self.register_instruction(IfGotoNode(cmp_var2, no_error_label2.label))
        error_msg = self.register_data("Invalid substring length").name
        self.register_instruction(ConcatNode(msg_eol, error_msg, eol))
        self.register_instruction(PrintStrNode(msg_eol))
        self.register_instruction(ErrorNode())
        self.register_instruction(no_error_label2)

        self.register_instruction(PlusNode(sum_var, start, length))
        self.register_instruction(LessEqNode(cmp_var3, sum_var, length_var))
        self.register_instruction(IfGotoNode(cmp_var3, no_error_label3.label))
        error_msg = self.register_data("Invalid substring").name
        self.register_instruction(ConcatNode(msg_eol, error_msg, eol))
        self.register_instruction(PrintStrNode(msg_eol))
        self.register_instruction(ErrorNode())
        self.register_instruction(no_error_label3)
        self.register_instruction(SubstringNode(
            dest, self_param, start, length))
        self.register_instruction(ReturnNode(dest))
        self.current_method = self.current_function = None

        self.current_type = None

    def define_io_type(self):
        self.current_type = self.context.get_type('IO')
        type_node = self.register_type('IO')
        type_node.attributes = [(attr.name)
                                for attr in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(
            method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
        type_node.features = type_node.attributes + type_node.methods

        self.current_method = self.current_type.get_method('out_string')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo("self", None))
        str_val = self.register_param(VariableInfo('str_val', None))
        self.register_instruction(PrintStrNode(str_val))
        self.register_instruction(ReturnNode(self_local))
        self.current_method = self.current_function = None

        self.current_method = self.current_type.get_method('in_string')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        dest = self.define_internal_local()
        self.register_instruction(ReadStrNode(dest))
        self.register_instruction(ReturnNode(dest))
        self.current_method = self.current_function = None

        self.current_method = self.current_type.get_method('out_int')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo("self", None))
        int_val = self.register_param(VariableInfo('int_val', None))
        self.register_instruction(PrintIntNode(int_val))
        self.register_instruction(ReturnNode(self_local))
        self.current_method = self.current_function = None

        self.current_method = self.current_type.get_method('in_int')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        dest = self.define_internal_local()
        self.register_instruction(ReadIntNode(dest))
        self.register_instruction(ReturnNode(dest))
        self.current_method = self.current_function = None
        self.current_type = None

    def define_object_type(self):
        self.current_type = self.context.get_type('Object')
        type_node = self.register_type('Object')
        type_node.attributes = [(attr.name)
                                for attr in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(
            method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
        type_node.features = type_node.attributes + type_node.methods

        self.current_method = self.current_type.get_method('abort')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        type_name = self.define_internal_local()
        abort_msg = self.register_data("Abort called from class ").name
        eol = self.register_data('\\n').name
        msg = self.define_internal_local()
        msg_eol = self.define_internal_local()
        self.register_instruction(TypeNameNode(type_name, self_local))
        self.register_instruction(ConcatNode(msg, abort_msg, type_name))
        self.register_instruction(ConcatNode(msg_eol, msg, eol))
        self.register_instruction(PrintStrNode(msg_eol))
        self.register_instruction(AbortNode())
        self.current_method = self.current_function = None

        self.current_method = self.current_type.get_method('copy')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        copy_inst = self.define_internal_local()
        self.register_instruction(CopyNode(copy_inst, self_local))
        self.register_instruction(ReturnNode(copy_inst))
        self.current_method = self.current_function = None

        self.current_method = self.current_type.get_method('type_name')
        type_name = self.current_type.name
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        type_name_inst = self.define_internal_local()
        obj_type = self.define_internal_local()
        self.register_instruction(TypeOfNode(self_local, obj_type))
        self.register_instruction(TypeNameNode(type_name_inst, obj_type))
        self.register_instruction(ReturnNode(type_name_inst))
        self.current_method = self.current_function = None
        self.current_type = None
