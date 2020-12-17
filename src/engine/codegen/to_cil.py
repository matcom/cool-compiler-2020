from typing import List
from engine import parser as cool
from engine.cp.semantic import Context
from .cil_ast import *
from ..cp import visitor
from ..cp.semantic import VariableInfo, Scope
from .cil import BASE_COOL_CIL_TRANSFORM


class COOL_TO_CIL(BASE_COOL_CIL_TRANSFORM):

    def define_binary_node(self, node: cool.BinaryNode, scope, cil_node: Node):
        result = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil_node(result, left, right))
        return result

    def define_unary_node(self, node: cool.UnaryNode, scope, cil_node: Node):
        result = self.define_internal_local()
        expr = self.visit(node.expression, scope)
        self.register_instruction(cil_node(result, expr))
        return result

    def sort_class_declar(self, program: cool.ProgramNode):
        self.context:  Context
        program.declarations = sorted(
            (
                declaration
                for declaration in program.declarations
                if isinstance(declaration, cool.ClassDeclarationNode)
            ),
            # reverse=True,
            key=lambda cd: self.context.inheritance_deep(cd.id.lex),
        )

    def save_attr_initializations(self, node: cool.ProgramNode, scope):
        self.attr_declarations = dict()
        self.attr_declarations['Object'] = []
        self.attr_declarations['IO'] = []
        self.attr_declarations['Int'] = [
            cool.AttrDeclarationNode("value")
        ]
        self.attr_declarations['String'] = [
            cool.AttrDeclarationNode("value")
        ]
        self.attr_declarations['Bool'] = [
            cool.AttrDeclarationNode("value")
        ]

        for built_in in ['IO', 'Int', 'String', 'Bool', 'Object']:
            self.create_constructor(self.attr_declarations[built_in], built_in)

        for declaration in node.declarations:
            self.attr_declarations[declaration.id.lex] = []
            if declaration.parent and not declaration.parent.lex in ['IO', 'Int', 'String', 'Bool', 'Object']:
                self.attr_declarations[declaration.id.lex] += self.attr_declarations[declaration.parent.lex]
            self.attr_declarations[declaration.id.lex] += [
                feature for feature in declaration.features
                if isinstance(feature, cool.AttrDeclarationNode)
            ]
            self.create_constructor(
                self.attr_declarations[declaration.id.lex], declaration.id.lex
            )

    def create_constructor(self, attr_declarations: List[cool.AttrDeclarationNode], type_name):
        self.current_function = self.register_function(f'ctor_{type_name}')
        self.current_type = self.context.get_type(type_name)
        instance = self.register_param(VariableInfo('self', self.current_type))

        scope = Scope()
        instance = scope.define_variable('self', self.current_type)

        self_instance_name = instance.name
        for attr in attr_declarations:
            result = None
            if attr.expression:
                result = self.visit(attr.expression, scope)
            elif attr.type == 'String':
                result = self.register_data("").name
            else:
                result = self.define_internal_local()
                self.register_instruction(VoidNode(result))

            self.register_instruction(
                SetAttribNode(self_instance_name, attr.id.lex, result, type_name))

        self.register_instruction(ReturnNode(self_instance_name))

        self.current_type = None
        self.current_function = None

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope=None):
        scope = Scope()
        self.sort_class_declar(node)
        self.save_attr_initializations(node, scope)
        # entry
        self.current_function = self.register_function('entry')
        # call Constructor
        instance = self.define_internal_local()
        self.current_type = self.context.get_type('Main')
        self.register_instruction(
            AllocateNode(instance, self.current_type.name)
        )
        self.register_instruction(ArgNode(instance))
        self.register_instruction(
            StaticCallNode(f'ctor_{self.current_type.name}', instance))
        self.register_instruction(EmptyArgs(1))

        # call Main.main
        result = self.define_internal_local()
        self.register_instruction(ArgNode(instance))
        name = self.to_function_name('main', 'Main')
        self.register_instruction(StaticCallNode(name, result))
        self.register_instruction(EmptyArgs(1))
        self.current_function = None

        classes = [
            declaration
            for declaration in node.declarations
            if isinstance(declaration, cool.ClassDeclarationNode)
        ]
        for declaration in classes:
            self.visit(declaration, scope.create_child())

        return ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id.lex)
        type_node = self.register_type(node.id.lex)
        type_node.attributes = [(attr.name)
                                for attr in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(
            method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
        type_node.features = type_node.attributes + type_node.methods
        fun_declarations = (f for f in node.features if isinstance(
            f, cool.FuncDeclarationNode))
        for feature in fun_declarations:
            self.visit(feature, scope)

        self.current_type = None

    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node: cool.FuncDeclarationNode, scope: Scope):
        fun_scope = scope.create_child()
        self.current_method = self.current_type.get_method(node.id.lex)
        type_name = self.current_type.name

        self.current_function = self.register_function(
            self.to_function_name(node.id.lex, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        fun_scope.define_variable('self', self_local)
        for param_name, param_type in node.params:
            fun_scope.define_variable(param_name.lex, param_type.lex)
            self.register_param(VariableInfo(param_name.lex, param_type.lex))

        body = self.visit(node.body, fun_scope)

        self.register_instruction(ReturnNode(body))
        self.current_method = None

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node: cool.AttrDeclarationNode, scope: Scope, typex):
        result = None
        if node.expression:
            result = self.visit(node.expression, scope)
        elif node.type == 'String':
            result = self.register_data("").name
        else:
            result = self.define_internal_local()
            self.register_instruction(VoidNode(result))
        self_inst = scope.find_variable('self').name
        self.register_instruction(
            SetAttribNode(self_inst, node.id.lex, result, typex))

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope):
        result = None
        for expr in node.expressions:
            result = self.visit(expr, scope)
        # self.register_instruction(AssignNode(result, val))
        return result

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        expr = self.visit(node.expression, scope)
        var_info = scope.find_variable(node.id.lex)
        if not var_info:
            selfx = scope.find_variable('self').name
            self.register_instruction(SetAttribNode(
                selfx, node.id.lex, expr, self.current_type.name))
        else:
            var_info = var_info.real_name
            self.register_instruction(AssignNode(var_info, expr))
        return 0

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope):
        new_local = self.define_internal_local()
        typex = self.context.get_type(node.type.lex)
        self.register_instruction(AllocateNode(new_local, typex.name))
        self.register_instruction(ArgNode(new_local))
        self.register_instruction(
            StaticCallNode(f'ctor_{typex.name}', new_local))
        self.register_instruction(EmptyArgs(1))
        return new_local

    @visitor.when(cool.IfThenElseNode)
    def visit(self, node: cool.IfThenElseNode, scope):
        label_counter = self.label_counter_gen()
        cond = self.visit(node.condition, scope)
        child_scope = scope.create_child()
        true_label = LabelNode(f'TRUE_{label_counter}')
        end_label = LabelNode(f'END_{label_counter}')
        result = self.define_internal_local()
        self.register_instruction(IfGotoNode(
            cond, true_label.label))
        label_counter += 1
        false_expr = self.visit(node.else_body, child_scope)
        self.register_instruction(AssignNode(result, false_expr))
        self.register_instruction(
            GotoNode(end_label.label))
        self.register_instruction(true_label)

        true_expr = self.visit(node.if_body, child_scope)
        self.register_instruction(AssignNode(result, true_expr))
        self.register_instruction(end_label)
        label_counter = self.label_counter_gen()

        return result

    @visitor.when(cool.WhileLoopNode)
    def visit(self, node: cool.WhileLoopNode, scope):
        while_scope = scope.create_child()
        label_counter = self.label_counter_gen()
        start_label = LabelNode(f'START_{label_counter}')
        continue_label = LabelNode(f'CONTINUE_{label_counter}')
        end_label = LabelNode(f'END_{label_counter}')

        self.register_instruction(start_label)

        cond = self.visit(node.condition, scope)
        self.register_instruction(IfGotoNode(cond, continue_label.label))
        self.register_instruction(GotoNode(end_label.label))
        self.register_instruction(continue_label)
        self.visit(node.body, while_scope)
        label_counter = self.label_counter_gen()
        self.register_instruction(GotoNode(start_label.label))
        self.register_instruction(end_label)

        return 0

    @visitor.when(cool.CaseOfNode)
    def visit(self, node: cool.CaseOfNode, scope: Scope):
        label_counter = self.label_counter_gen()
        expr = self.visit(node.expression, scope)
        result = self.define_internal_local()
        exp_type = self.define_internal_local()
        end_label = LabelNode(f'END_{label_counter}')
        error_label = LabelNode(f'ERROR_CASE_{label_counter}')
        # TODO: Label error logic if is void
        self.register_instruction(TypeOfNode(expr, exp_type))

        case_expressions = self.sort_case_list(node.branches)

        for i, case in enumerate(case_expressions):
            next_branch_label = LabelNode(f'CASE_{case.id.lex}_{i}')
            child_scope = scope.create_child()
            expr_i = self.visit(
                case, child_scope,
                expr=expr,
                expr_type=exp_type,
                next_label=next_branch_label,
            )
            self.register_instruction(AssignNode(result, expr_i))
            self.register_instruction(GotoNode(end_label.label))
            self.register_instruction(next_branch_label)

        self.register_instruction(error_label)
        # TODO: specify the message error here [ i think :/ ]
        self.register_instruction(ErrorNode())
        self.register_instruction(end_label)

        return result

    @visitor.when(cool.CaseActionExpression)
    def visit(self, node: cool.CaseActionExpression, scope: Scope, expr=None, expr_type=None, next_label=None):
        test_res = self.define_internal_local()

        matching_label = LabelNode(f'CASE_MATCH_{node.id.lex}_{node.type.lex}')
        self.register_instruction(ConformsNode(test_res, expr, node.type.lex))
        self.register_instruction(IfGotoNode(expr, matching_label.label))
        self.register_instruction(
            GotoNode(next_label.label)
        )
        self.register_instruction(matching_label)
        l_var = self.define_internal_local()
        typex = self.context.get_type(node.type.lex)
        scope.define_variable(l_var, typex)
        self.register_instruction(AssignNode(l_var, expr))

        case_action_expr = self.visit(node.expression, scope)
        return case_action_expr

    @visitor.when(cool.LetInNode)
    def visit(self, node: cool.LetInNode, scope: Scope):
        let_scope = scope.create_child()
        for var_decl in node.let_body:
            self.visit(var_decl, let_scope)

        result = self.visit(node.in_body, let_scope)
        return result

    @visitor.when(cool.LetVariableDeclaration)
    def visit(self, node: cool.LetVariableDeclaration, scope: Scope):
        var_info = scope.define_variable(node.id.lex, node.type)
        var_info.real_name = self.register_local(var_info)
        value = self.visit(node.expression, scope)

        self.register_instruction(AssignNode(var_info.real_name, value))
        return var_info.real_name

    @visitor.when(cool.FunctionCallNode)
    def visit(self, node: cool.FunctionCallNode, scope):
        name = None
        if not (node.type):
            typex = self.context.get_type(node.obj.static_type.name).name
        else:
            typex = node.type.lex
            name = self.to_function_name(node.id.lex, typex)
        result = self.define_internal_local()
        obj = self.visit(node.obj, scope)
        rev_args = []
        for arg in node.args:
            arg_value = self.visit(arg, scope)
            rev_args = [arg_value] + rev_args
        for arg_value in rev_args:
            self.register_instruction(ArgNode(arg_value))
        self.register_instruction(ArgNode(obj))
        if name:
            self.register_instruction(StaticCallNode(name, result))
        else:
            self.register_instruction(
                DynamicCallNode(obj, typex, node.id.lex, result))

        self.register_instruction(EmptyArgs(len(node.args) + 1))

        return result

    @visitor.when(cool.MemberCallNode)
    def visit(self, node: cool.MemberCallNode, scope: Scope):
        type_name = self.current_type.name
        result = self.define_internal_local()
        rev_args = []
        for arg in node.args:
            arg_value = self.visit(arg, scope)
            rev_args = [arg_value] + rev_args
        for arg_value in rev_args:
            self.register_instruction(ArgNode(arg_value))
        self_inst = scope.find_variable('self').name
        self.register_instruction(ArgNode(self_inst))
        self.register_instruction(
            DynamicCallNode(self_inst, type_name, node.id.lex, result))

        self.register_instruction(EmptyArgs(len(node.args) + 1))
        return result

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope):
        return self.define_binary_node(node, scope, PlusNode)

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope):
        return self.define_binary_node(node, scope, MinusNode)

    @visitor.when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope):
        return self.define_binary_node(node, scope, StarNode)

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope):
        return self.define_binary_node(node, scope, DivNode)

    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope):
        return self.define_binary_node(node, scope, LessNode)

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope):
        return self.define_binary_node(node, scope, LessEqNode)

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()

        if node.left.static_type == self.context.get_type('String'):
            self.register_instruction(StringEqualNode(result, left, right))
        else:
            self.register_instruction(EqualNode(result, left, right))
        return result

    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope):
        return self.define_unary_node(node, scope, IsVoidNode)

    @visitor.when(cool.NotNode)
    def visit(self, node: cool.NotNode, scope):
        return self.define_unary_node(node, scope, NotNode)

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope):
        return self.define_unary_node(node, scope, ComplementNode)

    @visitor.when(cool.IdNode)
    def visit(self, node: cool.IdNode, scope: Scope):
        nvar = scope.find_variable(node.token.lex)
        if not nvar:
            selfx = scope.find_variable('self').name
            nvar = self.define_internal_local()
            self.register_instruction(
                GetAttribNode(nvar, selfx, node.token.lex, self.current_type.name))
        else:
            nvar = nvar.real_name
        return nvar

    @visitor.when(cool.BoolNode)
    def visit(self, node: cool.BoolNode, scope):
        value = 1 if node.token.lex else 0
        bool_inst = self.define_internal_local()
        self.register_instruction(BoxNode(bool_inst, value))
        return bool_inst

    @visitor.when(cool.IntegerNode)
    def visit(self, node: cool.IntegerNode, scope):
        value = int(node.token.lex)
        int_inst = self.define_internal_local()
        self.register_instruction(BoxNode(int_inst, value))
        return int_inst

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope):
        string = self.register_data(node.token.lex)
        dest = self.define_internal_local()
        self.register_instruction(LoadNode(dest, string.name))
        return dest
