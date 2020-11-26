from engine import parser as cool
from .cil_ast import *
from ..cp import visitor
from ..cp.semantic import VariableInfo , Scope
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
        expr ,typex = self.visit(node.expression, scope)
        self.register_instruction(cil_node(result, expr)) 
        return result

    def save_attr_init(self, node:cool.ProgramNode):
        self.attr_init = dict()
        for declaration in node.declarations if isinstance(declaration, cool.ClassDeclarationNode):
            self.attr_init[declaration.id.lex] = []
            if dec.parent and not classx.parent in ['IO', 'Object']:
                self.attr_init[classx.id] += self.attr_init[classx.parent]
            for feature in classx.features:
                if type(feature) is cool.AttrDeclarationNode:
                    self.attr_init[classx.id].append(feature)

    @visitor.on('node')
    def visit(self,node,scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self,node: cool.ProgramNode, scope = None):
        scope = Scope()
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(AllocateNode('Main',instance))
        self.register_instruction(ArgNode(instance))
        name = self.to_function_name('main','Main')
        self.register_instruction(StaticCallNode(name,result))
        self.register_instruction(ReturnNode(0))
        self.current_function = None

        classes = [declaration for declaration in node.declarations if isinstance(declaration, cool.ClassDeclarationNode)]:
            self.visit(declaration,scope)

        return ProgramNode(self.dottypes,self.dotdata,self.dotcode)

    @visitor.when(cool.ClassDeclarationNode) 
    def visit(self,node: cool.ClassDeclarationNode,scope):
        self.current_type = self.context.get_type(node.id.lex)
        type_node = self.register_type(node.id.lex)
        type_node.attributes = [(attr.name) for attr in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
        
        fun_declarations = (f for f in node.features if isinstance(f,cool.FuncDeclarationNode))
        for feature in fun_declarations:
            self.visit(feature,scope)

        self.current_type = None

    @visitor.when(cool.FuncDeclarationNode)
    def visit(self,node: cool.FuncDeclarationNode,scope: Scope):
        fun_scope = Scope(parent=scope)
        self.current_method = self.current_type.get_method(node.id.lex)
        type_name = self.current_type.name
        
        self.current_function = self.register_function(self.to_function_name(node.id.lex, type_name))
        self_local = self.register_param(VariableInfo('self', None))
        func_scope.define_variable('self', self_local)
        for param_name, param_type in node.params:
            self.register_param(VariableInfo(param_name, param_type))

        body = self.visit(node.body,func_scope)

        self.register_instruction(ReturnNode(body))
        self.current_method = None

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self,node: cool.AttrDeclarationNode,scope):
        result = self.visit(node.expression, scope) if node.expression else 0
        self_inst = scope.find_variable('self').name
        self.register_instruction(SetAttribNode(self_inst, node.id.lex, result))

    @visitor.when(cool.AssignNode)
    def visit(self,node: cool.AssignNode,scope):
        expr = self.visit(node.expression,scope)
        attr_info = scope.find_variable(node.id.lex)
        if not attr_info:
            selfx = scope.find_variable('self').name
            self.register_instruction(SetAttribNode(selfx, node.id.lex, expr))
        else:
            attr_info = attr_info.name
            self.register_instruction(AssignNode(attr_info, value))
        return 0

    @visitor.when(cool.NewNode)
    def visit(self,node: cool.NewNode,scope):
        new_local = self.define_internal_local()
        typex = self.context.get_type(node.type.lex)
        self.register_instruction(AllocateNode(new_local, typex))

        return new_local

    @visitor.when(cool.IfThenElseNode)
    def visit(self,node:cool.IfThenElseNode,scope):
        cond = self.visit(node.condition, scope)
        child_scope = Scope(parent=scope)
        true_label = LabelNode('TRUE')
        end_label = LabelNode('END')
        result = self.define_internal_local()
        self.register_instruction(IfGotoNode(cond,self.to_label_name(true_label.label)))
        
        false_expr = self.visit(node.else_body, child_scope)
        self.register_instruction(AssignNode(result,false_expr))
        self.register_instruction(GotoNode(self.to_label_name(end_label.label)))
        self.register_instruction(true_label)

        true_expr = self.visit(node.if_body, child_scope)
        self.register_instruction(AssignNode(result,true_expr))
        self.register_instruction(end_label)

        return result
        
    @visitor.when(cool.WhileLoopNode)
    def visit(self,node:cool.WhileLoopNode,scope):
        while_scope = Scope(parent=None)
        start_label = LabelNode('START')
        continue_label = LabelNode('CONTINUE')
        end_label = LabelNode('END')

        # result = self.define_internal_local()
        self.register_instruction(start_label)

        cond = self.visit(node.condition,scope)
        self.register_instruction(IfGotoNode(cond, continue_label))
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(continue_label)
        self.visit(node.body, while_scope)
        self.register_instruction(GotoNode(start_label))
        self.register_instruction(end_label)

        # self.register_instruction(AssignNode(result,body))
        return 0

    @visitor.when(cool.CaseOfNode)
    def visit(self,node: cool.CaseOfNode,scope):
        expr, typex = self.visit(node.expression, scope)
        result = self.define_internal_local()
        exptype = self.define_internal_local()
        end_label = LabelNode('END')
        self.register_instruction(TypeOfNode(expr,exptype))

        for i ,case, child_scope in enumerate(zip(node.branches, scope.children)):
            expr_n, type_n = self.visit(case,child_scope)
            self.register_instruction(AssignNode(result,expr_n))
            self.register_instruction(GotoNode(end_label))
            self.register_instruction(LabelNode(f'CASE_{i}'))
        self.register_instruction(end_label)

        return result, typex

    @visitor.when(cool.LetInNode)
    def visit(self,node: cool.LetInNode,scope: Scope):
        let_scope = scope.children[0]
        for let_id, let_type, let_expr in node.let_body:
            let_scope.define_variable(let_id.lex, let_type.lex)
            self.visit(let_expr,let_scope)

        result = self.define_internal_local()
        expr = self.visit(node.in_body,let_scope)
        self.register_instruction(AssignNode(result,expr))
        return result

    @visitor.when(cool.BlockNode)
    def visit(self,node: cool.BlockNode,scope):
        result = self.define_internal_local()
        for expr in node.expressions:
            val = self.visit(expr, scope)
        self.register_instruction(AssignNode(result,val))
        return result

    @visitor.when(cool.FunctionCallNode)
    def visit(self,node: cool.FunctionCallNode, scope):
        if not (node.type):
            typex = self.context.get_type(node.obj.static_type.name).name 
        else: 
            typex = node.type.lex
        name = self.to_function_name(node.id.lex, typex)
        result = self.define_internal_local()
        rev_args = []
        for arg in node.args:
            arg_value = self.visit(arg, scope)
            rev_args = [ arg_value ] + rev_args
        for arg_value in rev_args:
            self.register_instruction(ArgNode(arg_value))
        obj = self.visit(node.obj, scope)
        self.register_instruction(ArgNode(obj))
        self.register_instruction(StaticCallNode(name, result)) if name else \
        self.register_instruction(DynamicCallNode(typex, node.id.lex, result))
        
        return result

    @visitor.when(cool.MemberCallNode)
    def visit(self,node: cool.MemberCallNode, scope: Scope):
        type_name = self.current_type.name
        result = self.define_internal_local()
        rev_args = []
        for arg in node.args:
            arg_value = self.visit(arg, scope)
            rev_args = [ arg_value ] + rev_args
        for arg_value in rev_args:
            self.register_instruction(ArgNode(arg_value))
        self_inst = scope.find_variable('self').name
        self.register_instruction(ArgNode(self_inst))
        self.register_instruction(DynamicCallNode(type_name, node.id.lex, result))
        
        return result

    @visitor.when(cool.PlusNode)
    def visit(self, node:cool.PlusNode, scope):
        return self.define_binary_node(node,scope,PlusNode)

    @visitor.when(cool.MinusNode)
    def visit(self, node:cool.MinusNode, scope):
        return self.define_binary_node(node,scope,MinusNode)

    @visitor.when(cool.StarNode)
    def visit(self, node:cool.StarNode, scope):
        return self.define_binary_node(node,scope,StarNode)

    @visitor.when(cool.DivNode)
    def visit(self, node:cool.DivNode, scope):
        return self.define_binary_node(node,scope,DivNode)

    @visitor.when(cool.LessNode)
    def visit(self, node:cool.LessNode, scope):
        return self.define_binary_node(node,scope,LessNode)

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
        return self.define_unary_node(node,scope, NotNode)

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope):
        return self.define_unary_node(node, scope, ComplementNode)

    @visitor.when(cool.IdNode)
    def visit(self, node: cool.IdNode, scope: Scope):
        nvar = scope.find_variable(node.token.lex)
        if not nvar:
            selfx = scope.find_variable('self').name
            nvar = self.define_internal_local()
            self.register_instruction(GetAttribNode(nvar, selfx, node.token.lex))
        else:
            nvar = nvar.name
        return nvar

    @visitor.when(cool.BoolNode)
    def visit(self, node:cool.BoolNode, scope):
        return 1 if node.token.lex else 0

    @visitor.when(cool.IntegerNode)
    def visit(self, node:cool.IntegerNode, scope):
        return int(node.token.lex)

    @visitor.when(cool.StringNode)
    def visit(self, node:cool.StringNode, scope):
        string = self.register_data(node.token.lex)
        dest = self.define_internal_local()
        self.register_instruction(LoadNode(dest,string.name))
        return dest





    