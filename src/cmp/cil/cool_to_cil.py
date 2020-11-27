from ..cool_lang import ast as cool
from ..cool_lang.semantics.semantic_utils import Attribute

from .ast import ProgramNode, TypeNode, FunctionNode, ParamNode, LocalNode, AssignNode, PlusNode, MinusNode, StarNode, DivNode, AllocateNode, TypeOfNode, StaticCallNode, DynamicCallNode, ArgNode, ReturnNode, LengthNode, ConcatNode, PrefixNode, SubstringNode, GetAttribNode, SetAttribNode, LabelNode, GotoNode, GotoIfNode, DataNode, LessNode, LessEqNode, ComplementNode, IsVoidNode, EqualNode, ConformNode, CleanArgsNode, ErrorNode, StringEqualNode
from .utils import Scope
from .basic_transform import BASE_COOL_CIL_TRANSFORM, VariableInfo
from .utils import when, on


class COOL_TO_CIL_VISITOR(BASE_COOL_CIL_TRANSFORM):
    @on('node')
    def visit(self, node, scope: Scope):
        pass

    def order_caseof(self, node: cool.CaseOfNode):
        ini_dict = {case.type: case for case in node.cases}
        list_types = list()
        set_types = set()
        queue = [self.context.get_type(case.type) for case in node.cases]
        while queue:
            item = queue.pop(0)
            if item.name not in set_types:
                set_types.add(item.name)
                list_types.append(item)
            queue += item.children
        list_types_for_sorted = [(item.finish_time, item)
                                 for item in list_types]
        list_types_for_sorted.sort()
        list_types_for_sorted = [item for _, item in list_types_for_sorted]
        result = []
        for item in list_types_for_sorted:
            node = item
            while True:
                assert node is not None, "Error in case of node generator"
                if node.name in ini_dict:
                    case = ini_dict[node.name]
                    new_case = cool.CaseNode(
                        case.id,
                        item.name,
                        case.expression,
                        case.line,
                        case.column,
                    )
                    result.append(new_case)
                    break
                node = node.parent
        return result

    def find_type_name(self, typex, func_name):
        if func_name in typex.methods:
            return typex.name
        return self.find_type_name(typex.parent, func_name)

    def init_class_attr(self, scope: Scope, class_id, self_inst):
        attr_nodes = self.attr_init[class_id]
        for attr in attr_nodes:
            attr_scope = Scope(parent=scope)
            attr_scope.define_var('self', self_inst)
            self.visit(attr, attr_scope)

    def build_attr_init(self, node: cool.ProgramNode):
        self.attr_init = dict()
        for classx in node.classes:
            self.attr_init[classx.id] = []
            if classx.parent and not classx.parent in ['IO', 'Object']:
                self.attr_init[classx.id] += self.attr_init[classx.parent]
            for feature in classx.features:
                if type(feature) is cool.AttrDeclarationNode:
                    self.attr_init[classx.id].append(feature)

    @when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode = None, scope: Scope = None):
        scope = Scope()
        self.build_attr_init(node)
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(AllocateNode(instance, 'Main'))
        self.init_class_attr(scope, 'Main', instance)
        self.register_instruction(ArgNode(instance))
        self.register_instruction(StaticCallNode(
            self.to_function_name('main', 'Main'), result))
        self.register_instruction(CleanArgsNode(1))
        # self.register_instruction(ReturnNode(0))
        self.current_function = None

        for classx in node.classes:
            self.visit(classx, scope)

        return ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id)

        type_node = self.register_type(node.id)
        type_node.name_dir = self.register_data(node.id).name
        type_node.attributes = [
            attr.name for attr in self.current_type.get_all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(
            method.name, typex.name)) for method, typex in self.current_type.get_all_methods()]
        type_node.features = [feature.name if isinstance(feature, Attribute) else (feature[0].name, self.to_function_name(
            feature[0].name, feature[1].name)) for feature in self.current_type.get_all_features()]

        for feature in node.features:
            if isinstance(feature, cool.FuncDeclarationNode):
                self.visit(feature, scope)

        self.current_type = None

    @when(cool.AttrDeclarationNode)
    def visit(self, node: cool.AttrDeclarationNode, scope: Scope):
        result = None
        if node.expression:
            result = self.visit(node.expression, scope)
        else:
            result = self.define_internal_local()
            self.register_instruction(AllocateNode(result, "Int"))
            self.register_instruction(SetAttribNode(result, "value", 0, "Int"))
        self_inst = scope.get_var('self').local_name
        self.register_instruction(SetAttribNode(self_inst, node.id, result, self.current_type.name))

    @when(cool.FuncDeclarationNode)
    def visit(self, node: cool.FuncDeclarationNode, scope: Scope):
        func_scope = Scope(parent=scope)
        self.current_method = self.current_type.get_method(node.id)
        type_name = self.current_type.name

        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        func_scope.define_var('self', self_local)
        for param_name in self.current_method.param_names:
            param_local = self.register_param(VariableInfo(param_name, None))
            func_scope.define_var(param_name, param_local)

        body = self.visit(node.expression, func_scope)
        self.register_instruction(ReturnNode(body))

        self.current_method = self.current_function = None

    @when(cool.IfThenElseNode)
    def visit(self, node: cool.IfThenElseNode, scope: Scope):
        if_scope = Scope(parent=scope)
        cond_result = self.visit(node.condition, scope)
        result = self.define_internal_local()
        true_label = self.to_label_name('if_true')
        end_label = self.to_label_name('end_if')
        self.register_instruction(GotoIfNode(cond_result, true_label))
        false_result = self.visit(node.else_body, if_scope)
        self.register_instruction(AssignNode(result, false_result))
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(LabelNode(true_label))
        true_result = self.visit(node.if_body, if_scope)
        self.register_instruction(AssignNode(result, true_result))
        self.register_instruction(LabelNode(end_label))

        return result

    @when(cool.WhileLoopNode)
    def visit(self, node: cool.WhileLoopNode, scope: Scope):
        while_scope = Scope(parent=scope)
        loop_label = self.to_label_name('loop')
        body_label = self.to_label_name('body')
        end_label = self.to_label_name('pool')
        self.register_instruction(LabelNode(loop_label))
        condition = self.visit(node.condition, scope)
        self.register_instruction(GotoIfNode(condition, body_label))
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(LabelNode(body_label))
        self.visit(node.body, while_scope)
        self.register_instruction(LabelNode(end_label))

        return 0

    @when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        result = None
        for expr in node.expressions:
            result = self.visit(expr, scope)

        return result

    @when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        var_name = self.register_local(VariableInfo(node.id, None))
        scope.define_var(node.id, var_name)
        result = self.visit(node.expression, scope) if node.expression else 0

        self.register_instruction(AssignNode(var_name, result))

    @when(cool.LetInNode)
    def visit(self, node: cool.LetInNode, scope: Scope):
        let_scope = Scope(parent=scope)
        for let in node.let_body:
            self.visit(let, let_scope)

        result = self.visit(node.in_body, let_scope)
        return result

    @when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope: Scope, typex=None, result_inst=None, end_label=None):
        cond = self.define_internal_local()
        not_cond = self.define_internal_local()
        case_label = self.to_label_name(f'case_{node.type}')
        self.register_instruction(EqualNode(cond, typex, node.type))
        self.register_instruction(ComplementNode(not_cond, cond))
        self.register_instruction(GotoIfNode(not_cond, case_label))
        case_scope = Scope(parent=scope)
        case_var = self.register_local(VariableInfo(node.id, None))
        case_scope.define_var(node.id, case_var)
        case_result = self.visit(node.expression, case_scope)
        self.register_instruction(AssignNode(result_inst, case_result))
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(LabelNode(case_label))

    @when(cool.CaseOfNode)
    def visit(self, node: cool.CaseOfNode, scope: Scope):
        order_cases = self.order_caseof(node)
        end_label = self.to_label_name('end')
        error_label = self.to_label_name('error')
        result = self.define_internal_local()
        type_inst = self.define_internal_local()
        is_void = self.define_internal_local()
        obj_inst = self.visit(node.expression, scope)
        self.register_instruction(IsVoidNode(is_void, obj_inst))
        self.register_instruction(GotoIfNode(is_void, error_label))
        self.register_instruction(TypeOfNode(obj_inst, type_inst))
        for case in order_cases:
            self.visit(case, scope, type_inst, result, end_label)
        self.register_instruction(LabelNode(error_label))
        self.register_instruction(ErrorNode())
        self.register_instruction(LabelNode(end_label))

        return result

    @when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        value = self.visit(node.expression, scope)
        pvar = scope.get_var(node.id)
        if not pvar:
            selfx = scope.get_var('self').local_name
            self.register_instruction(SetAttribNode(selfx, node.id, value, self.current_type.name))
        else:
            pvar = pvar.local_name
            self.register_instruction(AssignNode(pvar, value))
        return 0

    @when(cool.MemberCallNode)
    def visit(self, node: cool.MemberCallNode, scope: Scope):
        type_name = self.current_type.name
        result = self.define_internal_local()
        rev_args = []
        for arg in node.args:
            arg_value = self.visit(arg, scope)
            rev_args = [arg_value] + rev_args
        for arg_value in rev_args:
            self.register_instruction(ArgNode(arg_value))
        self_inst = scope.get_var('self').local_name
        self.register_instruction(ArgNode(self_inst))
        self.register_instruction(DynamicCallNode(self_inst, type_name, node.id, result))
        self.register_instruction(CleanArgsNode(len(node.args)+1))

        return result

    @when(cool.FunctionCallNode)
    def visit(self, node: cool.FunctionCallNode, scope: Scope):
        typex = None if not node.type else self.context.get_type(node.type)
        type_name = self.find_type_name(typex, node.id) if typex else ''
        func_name = self.to_function_name(
            node.id, type_name) if type_name else ''
        result = self.define_internal_local()
        rev_args = []
        for arg in node.args:
            arg_value = self.visit(arg, scope)
            rev_args = [arg_value] + rev_args
        for arg_value in rev_args:
            self.register_instruction(ArgNode(arg_value))
        obj_inst = self.visit(node.obj, scope)
        self.register_instruction(ArgNode(obj_inst))
        self.register_instruction(StaticCallNode(func_name, result)) if func_name else self.register_instruction(
            DynamicCallNode(obj_inst,node.obj.static_type.name, node.id, result))
        self.register_instruction(CleanArgsNode(len(node.args)+1))

        return result

    @when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope): 
        result = self.define_internal_local() # TODO: attributes initialization
        self.register_instruction(AllocateNode(result, node.type))
        self.init_class_attr(scope, node.type, result)
        return result

    @when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        body = self.visit(node.expression, scope)
        result_raw = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(IsVoidNode(result_raw, body))
        self.register_instruction(AllocateNode(result, "Bool"))
        self.register_instruction(SetAttribNode(result, "value", result_raw, "Bool"))
        return result

    @when(cool.NotNode)
    def visit(self, node: cool.NotNode, scope: Scope):
        value_result = self.visit(node.expression, scope)
        result_raw = self.define_internal_local()
        value = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(GetAttribNode(value, value_result, "value", "Bool"))
        self.register_instruction(ComplementNode(result_raw, value))
        self.register_instruction(AllocateNode(result, "Bool"))
        self.register_instruction(SetAttribNode(result, "value", result_raw, "Bool"))
        return result

    @when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        value_result = self.visit(node.expression, scope)
        result_raw = self.define_internal_local()
        value = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(GetAttribNode(value, value_result, "value", "Int"))
        self.register_instruction(ComplementNode(result_raw, value))
        self.register_instruction(AllocateNode(result, "Int"))
        self.register_instruction(SetAttribNode(result, "value", result_raw, "Int"))
        return result

    @when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        left = self.define_internal_local()
        right = self.define_internal_local()
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        self.register_instruction(GetAttribNode(left, left_result, "value", "Int"))
        self.register_instruction(GetAttribNode(right, right_result, "value", "Int"))
        result_raw = self.define_internal_local()
        result = self.define_internal_local()

        self.register_instruction(PlusNode(result_raw, left, right))
        self.register_instruction(AllocateNode(result, "Int"))
        self.register_instruction(SetAttribNode(result, "value", result_raw, "Int"))
        return result

    @when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        left = self.define_internal_local()
        right = self.define_internal_local()
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        self.register_instruction(GetAttribNode(left, left_result, "value", "Int"))
        self.register_instruction(GetAttribNode(right, right_result, "value", "Int"))
        result_raw = self.define_internal_local()
        result = self.define_internal_local()

        self.register_instruction(MinusNode(result_raw, left, right))
        self.register_instruction(AllocateNode(result, "Int"))
        self.register_instruction(SetAttribNode(result, "value", result_raw, "Int"))
        return result

    @when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope: Scope):
        left = self.define_internal_local()
        right = self.define_internal_local()
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        self.register_instruction(GetAttribNode(left, left_result, "value", "Int"))
        self.register_instruction(GetAttribNode(right, right_result, "value", "Int"))
        result_raw = self.define_internal_local()
        result = self.define_internal_local()

        self.register_instruction(StarNode(result_raw, left, right))
        self.register_instruction(AllocateNode(result, "Int"))
        self.register_instruction(SetAttribNode(result, "value", result_raw, "Int"))
        return result

    @when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        left = self.define_internal_local()
        right = self.define_internal_local()
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        self.register_instruction(GetAttribNode(left, left_result, "value", "Int"))
        self.register_instruction(GetAttribNode(right, right_result, "value", "Int"))
        result_raw = self.define_internal_local()
        result = self.define_internal_local()

        self.register_instruction(DivNode(result_raw, left, right))
        self.register_instruction(AllocateNode(result, "Int"))
        self.register_instruction(SetAttribNode(result, "value", result_raw, "Int"))
        return result

    @when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        left = self.define_internal_local()
        right = self.define_internal_local()
        result_raw = self.define_internal_local()
        result = self.define_internal_local()

        if node.left.static_type == self.context.get_type('String'):
            self.register_instruction(GetAttribNode(left, left_result, "value", "String"))
            self.register_instruction(GetAttribNode(right, right_result, "value", "String"))
            self.register_instruction(StringEqualNode(result_raw, left, right))
        else:
            self.register_instruction(GetAttribNode(left, left_result, "value", "Int"))
            self.register_instruction(GetAttribNode(right, right_result, "value", "Int"))
            self.register_instruction(EqualNode(result_raw, left, right))
        self.register_instruction(AllocateNode(result, "Bool"))
        self.register_instruction(SetAttribNode(result, "value", result_raw, "Bool"))
        return result

    @when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):
        left = self.define_internal_local()
        right = self.define_internal_local()
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        self.register_instruction(GetAttribNode(left, left_result, "value", "Int"))
        self.register_instruction(GetAttribNode(right, right_result, "value", "Int"))
        result_bool = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(LessNode(result_bool, left, right))
        self.register_instruction(AllocateNode(result, "Bool"))
        self.register_instruction(SetAttribNode(result, "value", result_bool, "Bool"))
        return result

    @when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        left = self.define_internal_local()
        right = self.define_internal_local()
        left_result = self.visit(node.left, scope)
        right_result = self.visit(node.right, scope)
        self.register_instruction(GetAttribNode(left, left_result, "value", "Int"))
        self.register_instruction(GetAttribNode(right, right_result, "value", "Int"))
        result_bool = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(LessEqNode(result_bool, left, right))
        self.register_instruction(AllocateNode(result, "Bool"))
        self.register_instruction(SetAttribNode(result, "value", result_bool, "Bool"))
        return result

    @when(cool.IdNode)
    def visit(self, node: cool.IdNode, scope: Scope):
        pvar = scope.get_var(node.token)
        if not pvar:
            selfx = scope.get_var('self').local_name
            pvar = self.define_internal_local()
            self.register_instruction(GetAttribNode(pvar, selfx, node.token, self.current_type.name))
        else:
            pvar = pvar.local_name
        return pvar

    @when(cool.BoolNode)
    def visit(self, node: cool.BoolNode, scope: Scope):
        value = 1 if node.token.lower() == 'true' else 0
        bool_inst = self.define_internal_local()
        self.register_instruction(AllocateNode(bool_inst, "Bool"))
        self.register_instruction(SetAttribNode(bool_inst, "value", value, "Bool"))
        return bool_inst

    @when(cool.IntegerNode)
    def visit(self, node: cool.IntegerNode, scope: Scope):
        value = int(node.token)
        int_inst = self.define_internal_local()
        self.register_instruction(AllocateNode(int_inst, "Int"))
        self.register_instruction(SetAttribNode(int_inst, "value", value, "Int"))
        return int_inst

    @when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        string = self.register_data(node.token[1:-1])
        value = string.name
        string_inst = self.define_internal_local()
        self.register_instruction(AllocateNode(string_inst, "String"))
        self.register_instruction(SetAttribNode(string_inst, "value", value, "String"))
        return string_inst
