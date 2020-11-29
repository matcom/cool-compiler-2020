from ..cool_lang import ast as cool
from ..cool_lang.semantics.semantic_utils import Attribute
from .ast import (
    AllocateNode,
    ArgNode,
    AssignNode,
    CleanArgsNode,
    ComplementNode,
    DivNode,
    DynamicCallNode,
    EqualNode,
    ErrorNode,
    GetAttribNode,
    GotoIfNode,
    GotoNode,
    IsVoidNode,
    LabelNode,
    LessEqNode,
    LessNode,
    MinusNode,
    PlusNode,
    ProgramNode,
    ReturnNode,
    SetAttribNode,
    StarNode,
    StaticCallNode,
    StringEqualNode,
    TypeOfNode,
    VoidNode,
)
from .basic_transform import BASE_COOL_CIL_TRANSFORM, VariableInfo
from .utils import Scope, on, when


class COOL_TO_CIL_VISITOR(BASE_COOL_CIL_TRANSFORM):
    @on("node")
    def visit(self, node, scope: Scope):  # noqa:F811
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
        list_types_for_sorted = [(item.finish_time, item) for item in list_types]
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
        # print(self.attr_init)
        # print("==============================")
        attr_nodes = self.attr_init[class_id]
        for attr in attr_nodes:
            attr_scope = Scope(parent=scope)
            attr_scope.define_var("self", self_inst)
            self.visit(attr, attr_scope, class_id)

    def build_attr_init(self, node: cool.ProgramNode):
        self.attr_init = dict()
        self.attr_init["IO"] = []
        self.attr_init["Object"] = []
        self.attr_init["Int"] = [cool.AttrDeclarationNode("value", None, None, 0, 0)]
        self.attr_init["Bool"] = [cool.AttrDeclarationNode("value", None, None, 0, 0)]
        self.attr_init["String"] = [cool.AttrDeclarationNode("value", None, None, 0, 0)]
        for classx in node.classes:
            self.attr_init[classx.id] = []
            if classx.parent:
                self.attr_init[classx.id] += self.attr_init[classx.parent]
            for feature in classx.features:
                if type(feature) is cool.AttrDeclarationNode:
                    self.attr_init[classx.id].append(feature)

    @when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode = None, scope: Scope = None):  # noqa:F811
        scope = Scope()
        self.build_attr_init(node)
        self.current_function = self.register_function("entry")
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(AllocateNode(instance, "Main"))
        self.current_type = self.context.get_type("Main")
        self.init_class_attr(scope, "Main", instance)
        self.current_type = None
        self.register_instruction(ArgNode(instance))
        self.register_instruction(
            StaticCallNode(self.to_function_name("main", "Main"), result)
        )
        self.register_instruction(CleanArgsNode(1))
        # self.register_instruction(ReturnNode(0))
        self.current_function = None

        for classx in node.classes:
            self.visit(classx, scope)

        return ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):  # noqa:F811
        self.current_type = self.context.get_type(node.id)

        type_node = self.register_type(node.id)
        type_node.name_dir = self.register_data(node.id).name
        type_node.attributes = [
            attr.name for attr in self.current_type.get_all_attributes()
        ]
        type_node.methods = [
            (method.name, self.to_function_name(method.name, typex.name))
            for method, typex in self.current_type.get_all_methods()
        ]
        type_node.features = [
            feature.name
            if isinstance(feature, Attribute)
            else (
                feature[0].name,
                self.to_function_name(feature[0].name, feature[1].name),
            )
            for feature in self.current_type.get_all_features()
        ]

        for feature in node.features:
            if isinstance(feature, cool.FuncDeclarationNode):
                self.visit(feature, scope)

        self.current_type = None

    @when(cool.AttrDeclarationNode)
    def visit(  # noqa:F811
        self, node: cool.AttrDeclarationNode, scope: Scope, typex: str = None
    ):
        result = None
        if node.expression:
            result = self.visit(node.expression, scope)
        # elif typex in ["Int", "Bool", "String"]:
        #     # print("------------------------------")
        #     result = self.define_internal_local()
        #     self.register_instruction(AllocateNode(result, typex))
        #     self.register_instruction(SetAttribNode(result, "value", 0, typex))
        else:
            result = self.define_internal_local()
            self.register_instruction(VoidNode(result))
            # self.register_instruction(PrintIntNode(result))
        self_inst = scope.get_var("self").local_name
        assert typex, f"AttrDeclarationNode: {typex}"
        result = self.unpack_type_by_value(result, node.expression.static_type if node.expression else None)
        self.register_instruction(SetAttribNode(self_inst, node.id, result, typex))

    @when(cool.FuncDeclarationNode)
    def visit(self, node: cool.FuncDeclarationNode, scope: Scope):  # noqa:F811
        func_scope = Scope(parent=scope)
        self.current_method = self.current_type.get_method(node.id)
        type_name = self.current_type.name

        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name)
        )
        self_local = self.register_param(VariableInfo("self", None))
        func_scope.define_var("self", self_local)
        for param_name in self.current_method.param_names:
            param_local = self.register_param(VariableInfo(param_name, None))
            func_scope.define_var(param_name, param_local)

        body = self.visit(node.expression, func_scope)
        # print(body, type(body), node.expression, "==================================")
        self.register_instruction(ReturnNode(body))

        self.current_method = self.current_function = None

    @when(cool.IfThenElseNode)
    def visit(self, node: cool.IfThenElseNode, scope: Scope):  # noqa:F811
        if_scope = Scope(parent=scope)
        cond_result = self.visit(node.condition, scope)
        result = self.define_internal_local()
        true_label = self.to_label_name("if_true")
        end_label = self.to_label_name("end_if")
        cond_result = self.unpack_type_by_value(cond_result, node.condition.static_type)
        self.register_instruction(GotoIfNode(cond_result, true_label))
        false_result = self.visit(node.else_body, if_scope)
        # if false_result == "0" or false_result == 0:
        #     print(type(node.else_body), "IfThenElseNode")
        false_result = self.unpack_type_by_value(
            false_result, node.else_body.static_type
        )
        self.register_instruction(AssignNode(result, false_result))
        result = self.pack_type_by_value(result, node.else_body.static_type)
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(LabelNode(true_label))
        true_result = self.visit(node.if_body, if_scope)
        true_result = self.unpack_type_by_value(true_result, node.if_body.static_type)
        # if true_result == "0" or true_result == 0:
        #     print(type(node.if_body), "IfThenElseNode")
        self.register_instruction(AssignNode(result, true_result))
        result = self.pack_type_by_value(result, node.if_body.static_type)
        self.register_instruction(LabelNode(end_label))

        return result

    @when(cool.WhileLoopNode)
    def visit(self, node: cool.WhileLoopNode, scope: Scope):  # noqa:F811
        while_scope = Scope(parent=scope)
        loop_label = self.to_label_name("loop")
        body_label = self.to_label_name("body")
        end_label = self.to_label_name("pool")
        self.register_instruction(LabelNode(loop_label))
        condition = self.visit(node.condition, scope)
        condition_raw = self.unpack_type_by_value(condition, node.condition.static_type)
        # self.register_instruction(PrintIntNode(condition_raw))
        self.register_instruction(GotoIfNode(condition_raw, body_label))
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(LabelNode(body_label))
        self.visit(node.body, while_scope)
        self.register_instruction(GotoNode(loop_label))
        self.register_instruction(LabelNode(end_label))
        zero = self.define_internal_local()
        self.register_instruction(VoidNode(zero))
        return zero

    @when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):  # noqa:F811
        result = None
        assert node.expressions, "BlockNode empty"
        for expr in node.expressions:
            result = self.visit(expr, scope)
        return result

    @when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):  # noqa:F811
        var_name = self.register_local(VariableInfo(node.id, None))
        result = self.visit(node.expression, scope) if node.expression else 0
        if result == 0:
            typex = node.type
            if typex in ["Int", "String", "Bool"]:
                self.register_instruction(AllocateNode(var_name, typex))
                self.register_instruction(SetAttribNode(var_name, "value", 0, typex))
            else:
                self.register_instruction(VoidNode(var_name))
        else:
            result = self.unpack_type_by_value(result, node.expression.static_type)
            self.register_instruction(AssignNode(var_name, result))
            var_name = self.pack_type_by_value(var_name, node.expression.static_type)
        scope.define_var(node.id, var_name)

    @when(cool.LetInNode)
    def visit(self, node: cool.LetInNode, scope: Scope):  # noqa:F811
        let_scope = Scope(parent=scope)
        for let in node.let_body:
            self.visit(let, let_scope)

        result = self.visit(node.in_body, let_scope)
        return result

    @when(cool.CaseNode)
    def visit(  # noqa:F811
        self,
        node: cool.CaseNode,
        scope: Scope,
        typex=None,
        result_inst=None,
        end_label=None,
        expr_inst=None,
    ):
        cond = self.define_internal_local()
        not_cond = self.define_internal_local()
        case_label = self.to_label_name(f"case_{node.type}")
        # print(node.type, type(node.type))
        temp_type = self.define_internal_local()
        type_val = self.define_internal_local()
        # WARNING: attr initialization isn't done
        self.register_instruction(AllocateNode(temp_type, node.type))
        self.register_instruction(TypeOfNode(temp_type, type_val))
        self.register_instruction(EqualNode(cond, typex, type_val))
        self.register_instruction(ComplementNode(not_cond, cond))
        self.register_instruction(GotoIfNode(not_cond, case_label))
        case_scope = Scope(parent=scope)
        case_var = self.register_local(VariableInfo(node.id, None))
        case_scope.define_var(node.id, case_var)
        self.register_instruction(AssignNode(case_var, expr_inst))
        case_result = self.visit(node.expression, case_scope)
        # if case_result == "0" or case_result == 0:
        #     print(type(node.expression), "CaseNode")
        self.register_instruction(AssignNode(result_inst, case_result))
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(LabelNode(case_label))

    @when(cool.CaseOfNode)
    def visit(self, node: cool.CaseOfNode, scope: Scope):  # noqa:F811
        order_cases = self.order_caseof(node)
        end_label = self.to_label_name("end")
        error_label = self.to_label_name("error")
        result = self.define_internal_local()
        type_inst = self.define_internal_local()
        is_void = self.define_internal_local()
        obj_inst = self.visit(node.expression, scope)
        self.register_instruction(IsVoidNode(is_void, obj_inst))
        self.register_instruction(GotoIfNode(is_void, error_label))
        self.register_instruction(TypeOfNode(obj_inst, type_inst))
        for case in order_cases:
            self.visit(case, scope, type_inst, result, end_label, obj_inst)
        self.register_instruction(LabelNode(error_label))
        self.register_instruction(ErrorNode())
        self.register_instruction(LabelNode(end_label))

        return result

    @when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):  # noqa:F811
        value = self.visit(node.expression, scope)
        pvar = scope.get_var(node.id)
        value = self.unpack_type_by_value(value, node.expression.static_type)
        if not pvar:
            selfx = scope.get_var("self").local_name
            value_raw = self.unpack_type_by_value(value, node.expression.static_type)
            self.register_instruction(
                SetAttribNode(
                    selfx,
                    node.id,
                    value_raw,
                    self.current_type.name,
                )
            )
        else:
            pvar = pvar.local_name
            # if value == "0" or value == 0:
            #     print(type(node.expression), "AssignNode")
            self.register_instruction(AssignNode(pvar, value))
        return value

    @when(cool.MemberCallNode)
    def visit(self, node: cool.MemberCallNode, scope: Scope):  # noqa:F811
        type_name = self.current_type.name
        result = self.define_internal_local()
        rev_args = []
        for arg in node.args:
            arg_value = self.visit(arg, scope)
            rev_args = [arg_value] + rev_args
        for arg_value in rev_args:
            # arg_value = self.unpack_type_by_value(arg_value, typex)
            self.register_instruction(ArgNode(arg_value))
        self_inst = scope.get_var("self").local_name
        self.register_instruction(ArgNode(self_inst))
        self.register_instruction(
            DynamicCallNode(self_inst, type_name, node.id, result)
        )
        self.register_instruction(CleanArgsNode(len(node.args) + 1))
        return result

    @when(cool.FunctionCallNode)
    def visit(self, node: cool.FunctionCallNode, scope: Scope):  # noqa:F811
        typex = None if not node.type else self.context.get_type(node.type)
        type_name = self.find_type_name(typex, node.id) if typex else ""
        func_name = self.to_function_name(node.id, type_name) if type_name else ""
        result = self.define_internal_local()
        rev_args = []
        for arg in node.args:
            arg_value = self.visit(arg, scope)
            rev_args = [arg_value] + rev_args
        for arg_value in rev_args:
            self.register_instruction(ArgNode(arg_value))
        obj_inst = self.visit(node.obj, scope)
        self.register_instruction(ArgNode(obj_inst))
        if func_name:
            self.register_instruction(StaticCallNode(func_name, result))
        else:
            self.register_instruction(
                DynamicCallNode(
                    obj_inst,
                    node.obj.static_type.name,
                    node.id,
                    result,
                )
            )
        self.register_instruction(CleanArgsNode(len(node.args) + 1))
        return result

    @when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope):  # noqa:F811
        result = self.define_internal_local()
        self.register_instruction(AllocateNode(result, node.type))
        self.init_class_attr(scope, node.type, result)
        return result

    @when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):  # noqa:F811
        body = self.visit(node.expression, scope)
        result = self.define_internal_local()
        self.register_instruction(IsVoidNode(result, body))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.NotNode)
    def visit(self, node: cool.NotNode, scope: Scope):  # noqa:F811
        value = self.visit(node.expression, scope)
        one = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(AllocateNode(one, "Int"))
        self.register_instruction(SetAttribNode(one, "value", 1, "Int"))
        one = self.unpack_type_by_value(one, "Int")
        self.register_instruction(MinusNode(result, one, value))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):  # noqa:F811
        value = self.visit(node.expression, scope)
        value = self.unpack_type_by_value(value, node.expression.static_type)
        result = self.define_internal_local()
        self.register_instruction(ComplementNode(result, value))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):  # noqa:F811
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        left = self.unpack_type_by_value(left, node.left.static_type)
        right = self.unpack_type_by_value(right, node.right.static_type)
        result = self.define_internal_local()
        self.register_instruction(PlusNode(result, left, right))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):  # noqa:F811
        left = self.define_internal_local()
        right = self.define_internal_local()
        left = self.unpack_type_by_value(left, node.left.static_type)
        right = self.unpack_type_by_value(right, node.right.static_type)
        result = self.define_internal_local()
        self.register_instruction(MinusNode(result, left, right))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope: Scope):  # noqa:F811
        left = self.define_internal_local()
        right = self.define_internal_local()
        left = self.unpack_type_by_value(left, node.left.static_type)
        right = self.unpack_type_by_value(right, node.right.static_type)
        result = self.define_internal_local()
        self.register_instruction(StarNode(result, left, right))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):  # noqa:F811
        left = self.define_internal_local()
        right = self.define_internal_local()
        left = self.unpack_type_by_value(left, node.left.static_type)
        right = self.unpack_type_by_value(right, node.right.static_type)
        result = self.define_internal_local()
        self.register_instruction(DivNode(result, left, right))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):  # noqa:F811
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        left = self.unpack_type_by_value(left, node.left.static_type)
        right = self.unpack_type_by_value(right, node.right.static_type)
        result = self.define_internal_local()
        if node.left.static_type == self.context.get_type("String"):
            self.register_instruction(StringEqualNode(result, left, right))
        else:
            self.register_instruction(EqualNode(result, left, right))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):  # noqa:F811
        left = self.define_internal_local()
        right = self.define_internal_local()
        left = self.unpack_type_by_value(left, node.left.static_type)
        right = self.unpack_type_by_value(right, node.right.static_type)
        result = self.define_internal_local()
        self.register_instruction(LessNode(result, left, right))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):  # noqa:F811
        left = self.define_internal_local()
        right = self.define_internal_local()
        left = self.unpack_type_by_value(left, node.left.static_type)
        right = self.unpack_type_by_value(right, node.right.static_type)
        result = self.define_internal_local()
        self.register_instruction(LessEqNode(result, left, right))
        result = self.pack_type_by_value(result, node.static_type)
        return result

    @when(cool.IdNode)
    def visit(self, node: cool.IdNode, scope: Scope):  # noqa:F811
        pvar = scope.get_var(node.token)
        if not pvar:
            selfx = scope.get_var("self").local_name
            pvar = self.define_internal_local()
            self.register_instruction(
                GetAttribNode(pvar, selfx, node.token, self.current_type.name)
            )
            vattrbs = [
                item for item in self.current_type.get_all_attributes() if item.name == node.token
            ]
            assert vattrbs, "IdNode: attributes is empty"
            vattr: Attribute = vattrbs[0]
            pvar = self.pack_type_by_value(pvar, vattr.type)
        else:
            pvar = pvar.local_name
        return pvar

    @when(cool.BoolNode)
    def visit(self, node: cool.BoolNode, scope: Scope):  # noqa:F811
        value = 1 if node.token.lower() == "true" else 0
        bool_inst = self.define_internal_local()
        self.register_instruction(AllocateNode(bool_inst, "Bool"))
        self.register_instruction(SetAttribNode(bool_inst, "value", value, "Bool"))
        return bool_inst

    @when(cool.IntegerNode)
    def visit(self, node: cool.IntegerNode, scope: Scope):  # noqa:F811
        value = int(node.token)
        int_inst = self.define_internal_local()
        self.register_instruction(AllocateNode(int_inst, "Int"))
        self.register_instruction(SetAttribNode(int_inst, "value", value, "Int"))
        return int_inst

    @when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):  # noqa:F811
        string = self.register_data(node.token[1:-1])
        value = string.name
        string_inst = self.define_internal_local()
        self.register_instruction(AllocateNode(string_inst, "String"))
        self.register_instruction(SetAttribNode(string_inst, "value", value, "String"))
        return string_inst
