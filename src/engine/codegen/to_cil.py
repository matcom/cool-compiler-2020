from engine import parser as cool
from .cil_ast import *
from ..cp import visitor
from ..cp.semantic import VariableInfo , Scope
from .cil import BASE_COOL_CIL_TRANSFORM


class COOL_TO_CIL(BASE_COOL_CIL_TRANSFORM):

    def define_binary_node(self, node: cool.BinaryNode, scope: Scope, cil_node: Node):
        result = self.define_internal_local()
        left, typex = self.visit(node.left, scope)
        right, typex = self.visit( node.right, scope) 
        self.register_instruction(cil_node(result, left, right)) 
        return result, typex
    
    def define_unary_node(self, node: cool.UnaryNode, scope: Scope, cil_node: Node):
        result = self.define_internal_local()
        expr ,typex = self.visit(node.expression, scope)
        self.register_instruction(cil_node(result, expr)) 
        return result, typex

    @visitor.on('node')
    def visit(self,node,scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self,node: cool.ProgramNode,scope: Scope):
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(AllocateNode('Main',instance))
        self.register_instruction(ArgNode(instance))
        name = self.to_function_name('main','Main')
        self.register_instruction(StaticCallNode(name,result))
        self.register_instruction(ReturnNode(0))
        self.current_function = None

        for declaration, child_scope in zip(node.declarations,scope.children):
            self.visit(declaration,child_scope)

        return ProgramNode(self.dottypes,self.dotdata,self.dotcode)

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self,node: cool.ClassDeclarationNode,scope: Scope):
        self.current_type = self.context.get_type(node.id)
        type_node = self.register_type(node.id)
        type_node.attributes = [(attr.name, self.to_attr_name(attr.name,atype)) for attr, atype in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
        
        fun_declarations = (f for f in node.features if isinstance(f,cool.FuncDeclarationNode))
        for feature, child_scope in zip(fun_declarations,scope.children):
            self.visit(feature,child_scope)

        self.current_type = None

    @visitor.when(cool.FuncDeclarationNode)
    def visit(self,node: cool.FuncDeclarationNode,scope: Scope):
        self.current_method = self.current_type.get_method(node.id)
        type_name = self.current_type.name
        
        self.current_function = self.register_function(self.to_function_name(node.id, type_name))
        for param_name, param_type in node.params:
            self.register_param(VariableInfo(param_name, param_type))
        
        body, _ = self.visit(node.body,scope)

        self.register_instruction(ReturnNode(body))
        self.current_method = None

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self,node: cool.AttrDeclarationNode,scope:Scope):
        attr_info = scope.find_variable(node.id)
        vtype = get_type(attr_info.type)
        local_attr = self.register_local(VariableInfo(attr_info.name,vtype))

        expr, _ = self.visit(node.expression,scope)
        self.register_instruction(AssignNode(local_attr,expr))
        return local_attr,vtype

    @visitor.when(cool.AssignNode)
    def visit(self,node: cool.AssignNode,scope: Scope):
        vinfo = scope.find_variable(node.id)
        vname = self.register_local(VariableInfo(node.id,get_type(vinfo.type)))
        expr = self.visit(node.expression,scope)
        return self.register_instruction(AssignNode(vname,expr))

    @visitor.when(cool.IfThenElseNode)
    def visit(self,node:cool.IfThenElseNode,scope: Scope):
        cond, _ = self.visit(node.condition, scope)
        true_label = LabelNode('TRUE')
        end_label = LabelNode('END')

        result = self.define_internal_local()
        self.register_instruction(IfGotoNode(cond,true_label))

        false_expr , ftype = self.visit(node.else_body, scope)
        self.register_instruction(AssignNode(result,false_expr))
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(true_label)

        true_expr , ttype = self.visit(node.if_body, scope)
        self.register_instruction(AssignNode(result,true_expr))
        self.register_instruction(end_label)

        return result, get_common_basetype([ftype,ttype]) 
        
    @visitor.when(cool.WhileLoopNode)
    def visit(self,node:cool.WhileLoopNode,scope: Scope):
        start_label = LabelNode('START')
        continue_label = LabelNode('CONTINUE')
        end_label = LabelNode('END')

        result = self.define_internal_local()
        self.register_instruction(start_label)

        cond, _ = self.visit(node.condition,scope)
        self.register_instruction(IfGotoNode(cond, continue_label))
        self.register_instruction(GotoNode(end_label))
        self.register_instruction(continue_label)
        body, btype = self.visit(node.body, scope)
        self.register_instruction(GotoNode(start_label))
        self.register_instruction(end_label)

        self.register_instruction(AssignNode(result,body))
        return result, btype

    @visitor.when(cool.BlockNode)
    def visit(self,node: cool.BlockNode,scope: Scope):
        result = self.define_internal_local()
        for expr in node.expressions:
            val, typex = self.visit(expr, scope)
        self.register_instruction(AssignNode(result,val))
        return result, typex

    @visitor.when(cool.LetInNode)
    def visit(self,node: cool.LetInNode,scope: Scope):
        let_scope = scope.create_child()
        for let in node.let_body:
            self.visit(let,let_scope)

        result = self.define_internal_local()
        expr, typex = self.visit(node.in_body,let_scope)
        self.register_instruction(AssignNode(result,expr))
        return result,typex

    @visitor.when(cool.CaseOfNode)
    def visit(self,node: cool.CaseOfNode,scope: Scope):
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

    @visitor.when(cool.PlusNode)
    def visit(self, node:cool.PlusNode, scope:Scope):
        self.define_binary_node(node,scope,PlusNode)

    @visitor.when(cool.MinusNode)
    def visit(self, node:cool.MinusNode, scope:Scope):
        self.define_binary_node(node,scope,MinusNode)

    @visitor.when(cool.StarNode)
    def visit(self, node:cool.StarNode, scope:Scope):
        self.define_binary_node(node,scope,StarNode)

    @visitor.when(cool.DivNode)
    def visit(self, node:cool.DivNode, scope:Scope):
        self.define_binary_node(node,scope,DivNode)

    @visitor.when(cool.LessNode)
    def visit(self, node:cool.LessNode, scope: Scope):
        self.define_binary_node(node,scope,MinusNode)

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        self.define_binary_node(node,scope,MinusNode)

    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        self.define_unary_node(node, scope, IsVoidNode)
    
    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        self.define_unary_node(node, scope, ComplementNode)

    @visitor.when(cool.FunctionCallNode)
    def visit(self,node,scope):
        pass

    @visitor.when(cool.MemberCallNode)
    def visit(self,node,scope):
        pass

    @visitor.when(cool.NewNode)
    def visit(self,node,scope):
        pass

    @visitor.when(cool.AtomicNode)
    def visit(self,node,scope):
        pass


    