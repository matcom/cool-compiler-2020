from ..cool_lang import ast as cool

from .ast import ProgramNode, TypeNode, FunctionNode, ParamNode, LocalNode, AssignNode, PlusNode \
    , MinusNode, StarNode, DivNode, AllocateNode, TypeOfNode, StaticCallNode, DynamicCallNode    \
    , ArgNode, ReturnNode, ReadNode, PrintNode, LoadNode, LengthNode, ConcatNode, PrefixNode     \
    , SubstringNode, ToStrNode, GetAttribNode, SetAttribNode, LabelNode, GotoNode, GotoIfNode    \
    , DataNode, LessNode, LessEqNode, ComplementNode, IsVoidNode, EqualNode
from .utils import Scope
from .basic_transform import BASE_COOL_CIL_TRANSFORM, VariableInfo
from .utils import when, on


class COOL_TO_CIL_VISITOR(BASE_COOL_CIL_TRANSFORM):
    @on('node')
    def visit(self, node, scope:Scope):
        pass
    
    def build_attr_init(self, node:cool.ProgramNode):
        self.attr_init = dict()
        for classx in node.classes:
            self.attr_init[classx.id] = []
            if classx.parent:
                self.attr_init[classx.id] += self.attr_init[classx.parent]
            for feature in classx.features:
                if type(feature) is cool.AttrDeclarationNode:
                    self.attr_init[classx.id].append(feature)

    @when(cool.ProgramNode)
    def visit(self, node:cool.ProgramNode=None, scope:Scope=None):
        scope = Scope()
        self.build_attr_init(node)
        self.current_function = self.register_function('main')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(AllocateNode(instance, 'Main'))
        self.register_instruction(ArgNode(instance))
        self.register_instruction(StaticCallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(ReturnNode(0))
        self.current_function = None

        for classx in node.classes:
            self.visit(classx, scope)
        
        return ProgramNode(self.dottypes, self.dotdata, self.dotcode)
        
    @when(cool.ClassDeclarationNode)
    def visit(self, node:cool.ClassDeclarationNode, scope:Scope):
        self.current_type = self.context.get_type(node.id)

        type_node = self.register_type(node.id)
        type_node.attributes = [ attr.name for attr in self.current_type.get_all_attributes() ]
        type_node.methods = [ (method.name, self.to_function_name(method.name, typex.name))  for method, typex in self.current_type.get_all_methods() ]

        for feature in node.features:
            if isinstance(feature, cool.FuncDeclarationNode):
                self.visit(feature, scope)

        self.current_type = None

    @when(cool.AttrDeclarationNode)
    def visit(self, node:cool.AttrDeclarationNode, scope:Scope):
        pass                                        

    @when(cool.FuncDeclarationNode)
    def visit(self, node:cool.FuncDeclarationNode, scope:Scope):
        func_scope = Scope(parent=scope)
        self.current_method = self.current_type.get_method(node.id)
        type_name = self.current_type.name

        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        func_scope.define_var('self', self_local)
        for param_name in self.current_method.param_names:
            param_local = self.register_param(VariableInfo(param_name, None))
            func_scope.define_var(param_name, param_local)
        
        body = self.visit(node.expression, func_scope)
        self.register_instruction(ReturnNode(body))

        self.current_method = self.current_function = None


    @when(cool.IfThenElseNode)
    def visit(self, node:cool.IfThenElseNode, scope:Scope):
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
    def visit(self, node:cool.WhileLoopNode, scope:Scope):
        while_scope = Scope(parent=scope)
        loop_label = self.to_label_name('loop')
        body_label = self.to_label_name('body')
        end_label  = self.to_label_name('pool')
        self.register_instruction(LabelNode(loop_label))
        condition = self.visit(node.condition, scope)
        self.register_instruction(GotoIfNode(condition, body_label))
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(LabelNode(body_label))
        self.visit(node.body, while_scope)
        self.register_instruction(LabelNode(end_label))

        return 0


    @when(cool.BlockNode)
    def visit(self, node:cool.BlockNode, scope:Scope):
        result = None
        for expr in node.expressions:
            result = self.visit(expr, scope)
        
        return result


    @when(cool.LetNode)
    def visit(self, node:cool.LetNode, scope:Scope):
        var_name = self.register_local(VariableInfo(node.id, None))
        scope.define_var(node.id, var_name)
        result = self.visit(node.expression, scope)

        self.register_instruction(AssignNode(var_name, result))
        
    @when(cool.LetInNode)
    def visit(self, node:cool.LetInNode, scope:Scope):
        let_scope = Scope(parent=scope)
        for let in node.let_body:
            self.visit(let, let_scope)

        result = self.visit(node.in_body, let_scope)
        return result

    @when(cool.CaseNode)
    def visit(self, node:cool.CaseNode, scope:Scope):
        pass

    @when(cool.CaseOfNode)
    def visit(self, node:cool.CaseOfNode, scope:Scope):
        pass

    @when(cool.AssignNode)
    def visit(self, node:cool.AssignNode, scope:Scope):
        value = self.visit(node.expression, scope)
        pvar = scope.get_var(node.id)
        if not pvar:
            selfx = scope.get_var('self')
            self.register_instruction(SetAttribNode(selfx, node.id, value))
        
        return 0
    
    @when(cool.MemberCallNode)
    def visit(self, node:cool.MemberCallNode, scope:Scope):
        pass

    @when(cool.FunctionCallNode)
    def visit(self, node:cool.FunctionCallNode, scope:Scope):
        pass

    @when(cool.NewNode)
    def visit(self, node:cool.NewNode, scope:Scope): # Remember attributes initialization
        pass

    @when(cool.IsVoidNode)
    def visit(self, node:cool.IsVoidNode, scope:Scope):
        body = self.visit(node.expression, scope)
        result = self.define_internal_local()
        
        self.register_instruction(IsVoidNode(result, body))
        return result

    @when(cool.NotNode)
    def visit(self, node:cool.NotNode, scope:Scope):
        value = self.visit(node.expression, scope)
        result = self.define_internal_local()

        self.register_instruction(ComplementNode(result, value))
        return result

    @when(cool.ComplementNode)
    def visit(self, node:cool.ComplementNode, scope:Scope):
        value = self.visit(node.expression, scope)
        result = self.define_internal_local()

        self.register_instruction(ComplementNode(result, value))
        return result

    @when(cool.PlusNode)
    def visit(self, node:cool.PlusNode, scope:Scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()

        self.register_instruction(PlusNode(result, left, right))
        return result

    @when(cool.MinusNode)
    def visit(self, node:cool.MinusNode, scope:Scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()

        self.register_instruction(MinusNode(result, left, right))
        return result

    @when(cool.StarNode)
    def visit(self, node:cool.StarNode, scope:Scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()

        self.register_instruction(StarNode(result, left, right))
        return result

    @when(cool.DivNode)
    def visit(self, node:cool.DivNode, scope:Scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()

        self.register_instruction(DivNode(result, left, right))
        return result

    @when(cool.EqualNode)
    def visit(self, node:cool.EqualNode, scope:Scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()

        self.register_instruction(EqualNode(result, left, right))
        return result

    @when(cool.LessNode)
    def visit(self, node:cool.LessNode, scope:Scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()

        self.register_instruction(LessNode(result, left, right))
        return result

    @when(cool.LessEqualNode)
    def visit(self, node:cool.LessEqualNode, scope:Scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        result = self.define_internal_local()

        self.register_instruction(LessEqNode(result, left, right))
        return result
        
    @when(cool.IdNode)
    def visit(self, node:cool.IdNode, scope:Scope):
        pvar = scope.get_var(node.token)
        if not pvar:
            selfx = scope.get_var('self')
            pvar = self.define_internal_local()

            self.register_instruction(GetAttribNode(pvar, selfx, node.token)) # Perhaps GetAttribNode could need info about self type, this is know in self.current_type variable
        
        return pvar

    @when(cool.BoolNode)
    def visit(self, node:cool.BoolNode, scope:Scope):
       return 1 if node.token.lower() == 'true' else 0

    @when(cool.IntegerNode)
    def visit(self, node:cool.IntegerNode, scope:Scope):
        return int(node.token)

    @when(cool.StringNode)
    def visit(self, node:cool.StringNode, scope:Scope):
        string = self.register_data(node.token[1:-1])
        return string.name
