import codegen.cil_ast as cil
from codegen.visitors.base_cil_visitor import BaseCOOLToCILVisitor
from utils.ast import *
from semantic.tools import Scope, VariableInfo
from semantic.types import *
from utils import visitor
from utils.utils import get_type, get_common_basetype

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Scope):
        self.current_function = self.register_function('entry')
        idx = self.index
        instance = self.define_internal_local()
        result = self.define_internal_local()

        self.register_instruction(cil.AllocateNode('Main', instance)) 
        typex = self.context.get_type('Main', (0,0))
        if typex.all_attributes():
            self.register_instruction(cil.StaticCallNode(typex.name, typex.name, None, [cil.ArgNode(instance)], typex.name))
        
        name = self.to_function_name('main', 'Main')
        self.register_instruction(cil.StaticCallNode('Main', 'main', result, [cil.ArgNode(instance)], 'Object'))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None

        self.void_data = self.register_data(VOID_NAME).name

        self.create_built_in()
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode, idx)
    

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id, node.pos)
        
        cil_type = self.register_type(node.id)
 
        attrs = self.current_type.all_attributes()
        if len(attrs) > 0:
            # Si hay atributos creo el constructor, en otro caso no
            constructor = FuncDeclarationNode(node.token, [], node.token, BlockNode([], node.token))
            # definiendo el constructor en el tipo para analizar
            func_declarations = [constructor]
            self.constructors.append(node.id)
            self.current_type.define_method(self.current_type.name, [], [], self.current_type, node.pos)
            scopes = [scope] + list(scope.functions.values())
        else:
            func_declarations = []
            scopes = list(scope.functions.values())
            
        for attr, a_type in attrs:
            cil_type.attributes.append((attr.name, self.to_attr_name(attr.name, a_type.name)))
            self.initialize_attr(constructor, attr, scope)            ## add the initialization code in the constructor
        if attrs:
            # Append like the last expression self type
            constructor.body.expr_list.append(SelfNode())


        for method, mtype in self.current_type.all_methods():
            cil_type.methods.append((method.name, self.to_function_name(method.name, mtype.name)))


        func_declarations += [f for f in node.features if isinstance(f, FuncDeclarationNode)] 
        for feature, child_scope in zip(func_declarations, scopes):
            self.visit(feature, child_scope)


    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):
        self.current_method = self.current_type.get_method(node.id, node.pos)
        
        name = self.to_function_name(node.id, self.current_type.name)
        self.current_function = self.register_function(name)
     
        # Handle PARAMS
        self.register_param('self', self.current_type.name)
        for p_name, p_type in node.params:
            self.register_param(p_name, p_type.value)
        
        value, typex = self.visit(node.body, scope)
        if not isinstance(value, str):
            result = self.define_internal_local()
            self.register_instruction(cil.AssignNode(result, value))
        else:
            result = value

        # Boxing if necessary
        if (typex.name == 'Int' or typex.name == 'String' or typex.name == 'Bool') and self.current_method.return_type.name == 'Object':
            self.register_instruction(cil.BoxingNode(result, typex.name))

        # Handle RETURN
        self.register_instruction(cil.ReturnNode(result)) 
        self.current_method = None


    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope):
        var_info = scope.find_variable(node.id)
        vtype = get_type(var_info.type, self.current_type)
        local_var = self.register_local(var_info.name)

        value, typex = self.visit(node.expr, scope)
        if vtype.name == 'Object' and typex.name in ['String', 'Int', 'Bool']:
            self.register_instruction(cil.BoxingNode(local_var, typex.name))
        else:
            self.register_instruction(cil.AssignNode(local_var, value))
        return local_var, vtype


    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        var_info = scope.find_local(node.id)
        value, typex = self.visit(node.expr, scope)
        if var_info is None:
            var_info = scope.find_attribute(node.id)
            attributes = [attr.name for attr, a_type in self.current_type.all_attributes()]
            if var_info.type.name == 'Object' and typex.name in ['String', 'Bool', 'Int']:
                value = self.define_internal_local()
                self.register_instruction(cil.BoxingNode(value, typex.name))
            self.register_instruction(cil.SetAttribNode('self', var_info.name, self.current_type.name, value))
        else:
            local_name = self.to_var_name(var_info.name)
            if var_info.type.name == 'Object' and typex.name in ['String', 'Bool', 'Int']:
                self.register_instruction(cil.BoxingNode(local_name, typex.name))
            else:
                self.register_instruction(cil.AssignNode(local_name, value))
        return value, typex

    def _return_type(self, typex: Type, node):
        meth = typex.get_method(node.id, node.pos)
        return get_type(meth.return_type, self.current_type)

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        obj, otype = self.visit(node.obj, scope)
        
        meth = otype.get_method(node.id, node.pos)
        args_node = [cil.ArgNode(obj, self.index)] + self.handle_arguments(node.args, scope, meth.param_types)

        rtype = meth.return_type
        result = None if isinstance(rtype, VoidType) else self.define_internal_local()
       
        continue_label = cil.LabelNode(f'continue__{self.index}') 
        isvoid = self.check_void(obj)
        self.register_instruction(cil.GotoIfFalseNode(isvoid, continue_label.label))
        self.register_instruction(cil.ErrorNode('dispatch_error'))
        self.register_instruction(continue_label)

        if otype in [StringType(), IntType(), BoolType()]:
            self.register_instruction(cil.StaticCallNode(otype.name, node.id, result, args_node, rtype.name))
        else:
            self.register_instruction(cil.DynamicCallNode(otype.name, obj, node.id, result, args_node, rtype.name))
        return result, self._return_type(otype, node)

    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope: Scope):
        obj, otype = self.visit(node.obj, scope)

        meth = otype.get_method(node.id, node.pos)
        args_node = [cil.ArgNode(obj, self.index)] + self.handle_arguments(node.args, scope, meth.param_types)

        rtype = meth.return_type
        result = None if isinstance(rtype, VoidType) else self.define_internal_local()
        
        continue_label = cil.LabelNode(f'continue__{self.index}') 
        isvoid = self.check_void(obj)
        self.register_instruction(cil.GotoIfFalseNode(isvoid, continue_label.label))
        self.register_instruction(cil.ErrorNode('dispatch_error'))
        self.register_instruction(continue_label)
        
        self.register_instruction(cil.StaticCallNode(node.type, node.id, result, args_node, rtype.name))
        return result, self._return_type(otype, node)

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode, scope: Scope):
        meth = self.current_type.get_method(node.id, node.pos)
        args_node = [cil.ArgNode('self', self.index)] + self.handle_arguments(node.args, scope, meth.param_types)

        rtype = meth.return_type
        if isinstance(rtype, VoidType):
            result = None
        else: 
            result = self.define_internal_local()

        self.register_instruction(cil.DynamicCallNode(self.current_type.name, 'self', node.id, result, args_node, rtype.name))
        return result, self._return_type(self.current_type, node)

    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope: Scope):
        return int(node.lex), IntType()

    @visitor.when(ConstantBoolNode)
    def visit(self, node: ConstantBoolNode, scope: Scope):
        return 1 if node.lex  == 'true' else 0, BoolType()
   
    @visitor.when(ConstantStrNode)
    def visit(self, node: ConstantStrNode, scope: Scope):
        data = self.register_data(node.lex)
        result = self.define_internal_local()
        self.register_instruction(cil.LoadNode(result, data.name))
        return result, StringType()

    @visitor.when(ConstantVoidNode)
    def visit(self, node: ConstantVoidNode, scope: Scope):
        result = self.register_local(node.lex)
        void = cil.VoidConstantNode(result)
        self.register_instruction(void)
        return result, VoidType() 

    @visitor.when(SelfNode)
    def visit(self, node: SelfNode, scope: Scope):
        return 'self', self.current_type

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        try:
            typex = scope.find_local(node.lex).type
            name = self.to_var_name(node.lex)
            return name, get_type(typex, self.current_type)
        except:
            var_info = scope.find_attribute(node.lex)
            local_var = self.register_local(var_info.name)
            self.register_instruction(cil.GetAttribNode('self', var_info.name, self.current_type.name, local_var, var_info.type.name))
            return local_var, get_type(var_info.type, self.current_type)

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, scope: Scope):
        instance = self.define_internal_local()
        typex = self.context.get_type(node.lex, node.pos)
        typex = get_type(typex, self.current_type)
        self.register_instruction(cil.AllocateNode(typex.name, instance))
        
        # calling the constructor to load all attributes
        # Si tiene atributos entonces tendrá constructor (esto se deberia optimizar mas)
        if typex.all_attributes():
            self.register_instruction(cil.StaticCallNode(typex.name, typex.name, instance, [cil.ArgNode(instance)], typex.name))
        
        return instance, typex


    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        '''
        LABEL start
        IF NOT <cond> GOTO end
        res = <expr>
        GOTO start
        LABEL end
        '''
        start_label = cil.LabelNode(f'start__{self.idx}')
        end_label = cil.LabelNode(f'end__{self.idx}')
        
        result = self.define_internal_local()
        self.register_instruction(cil.VoidConstantNode(result))
        self.register_instruction(start_label)

        cond, _ = self.visit(node.cond, scope)
        self.register_instruction(cil.GotoIfFalseNode(cond, end_label.label))
        expr, typex = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(result, expr))
        self.register_instruction(cil.GotoNode(start_label.label))
        self.register_instruction(end_label)
        
        return result, ObjectType()

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope):
        '''
        IF cond GOTO true
        result = <false.expr>
        GOTO end
        LABEL true
        result = <true.expr>
        LABEL end
        '''
        cond, _ = self.visit(node.cond, scope)

        true_label = cil.LabelNode(f"true__{self.idx}")
        end_label = cil.LabelNode(f"end__{self.idx}")

        result = self.define_internal_local()
        self.register_instruction(cil.GotoIfNode(cond, true_label.label))

        false_expr, ftypex = self.visit(node.else_stm, scope)
        self.register_instruction(cil.AssignNode(result, false_expr))
        self.register_instruction(cil.GotoNode(end_label.label))
        self.register_instruction(true_label)
        
        true_expr, ttypex = self.visit(node.stm, scope)
        self.register_instruction(cil.AssignNode(result, true_expr))
        self.register_instruction(end_label)
        return result, get_common_basetype([ttypex, ftypex])

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        value = None
        for exp in node.expr_list:
            value, typex = self.visit(exp, scope)
        result = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result, value))
        return result, typex

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        child_scope = scope.expr_dict[node]
        for init in node.init_list:
            self.visit(init, child_scope)
        
        expr, typex = self.visit(node.expr, child_scope)
        return expr, typex


    @visitor.when(CaseNode) 
    def visit(self, node: CaseNode, scope: Scope):
        expr, typex = self.visit(node.expr, scope)
        
        result = self.define_internal_local()
        end_label = cil.LabelNode(f'end__{self.idx}')
        error_label = cil.LabelNode(f'error__{self.idx}')
     
        isvoid = self.check_void(expr)
        self.register_instruction(cil.GotoIfNode(isvoid, error_label.label))

        try:
            new_scope = scope.expr_dict[node]
        except:
            new_scope = scope
        sorted_case_list = self.sort_option_nodes_by_type(node.case_list)
        for i, case in enumerate(sorted_case_list):
            next_label = cil.LabelNode(f'next__{self.idx}_{i}')
            expr_i = self.visit(case, new_scope.create_child(), expr, next_label, typex)
            self.register_instruction(cil.AssignNode(result, expr_i))
            self.register_instruction(cil.GotoNode(end_label.label))
            self.register_instruction(next_label)
        # Si llegó aquí es porque no matcheó nunca
        self.register_instruction(cil.ErrorNode('case_error'))
        self.register_instruction(error_label)
        self.register_instruction(cil.ErrorNode('case_void_error'))
        self.register_instruction(end_label)
        return result, typex

    @visitor.when(OptionNode)
    def visit(self, node: OptionNode, scope:Scope, expr, next_label, type_e):
        aux = self.define_internal_local()
        self.register_instruction(cil.ConformsNode(aux, expr, node.typex))
        self.register_instruction(cil.GotoIfFalseNode(aux, next_label.label))
        
        local_var = self.register_local(node.id)
        typex = self.context.get_type(node.typex, node.type_pos)
        scope.define_variable(node.id, typex)
        if typex.name == 'Object' and type_e.name in ['String', 'Int', 'Bool']:
            self.register_instruction(cil.BoxingNode(local_var, type_e.name))
        else:
            self.register_instruction(cil.AssignNode(local_var, expr))
        expr_i, type_expr = self.visit(node.expr, scope)
        return expr_i

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        return self._define_unary_node(node, scope, cil.LogicalNotNode)

    @visitor.when(BinaryNotNode)
    def visit(self, node: BinaryNotNode, scope: Scope):
        return self._define_unary_node(node, scope, cil.NotNode)


    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope: Scope):
        expr, _ = self.visit(node.expr, scope)
        result = self.check_void(expr)
        return result, BoolType()

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: Scope):
        return self._define_binary_node(node, scope, cil.PlusNode)

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        return self._define_binary_node(node, scope, cil.MinusNode)

    @visitor.when(StarNode)
    def visit(self, node: StarNode, scope: Scope):
        return self._define_binary_node(node, scope, cil.StarNode)

    @visitor.when(DivNode)
    def visit(self, node: DivNode, scope: Scope):
        return self._define_binary_node(node, scope, cil.DivNode)

    @visitor.when(LessNode)
    def visit(self, node: LessNode, scope: Scope):
        return self._define_binary_node(node, scope, cil.LessNode)
        
    @visitor.when(LessEqNode)
    def visit(self, node: LessEqNode, scope: Scope):
        return self._define_binary_node(node, scope, cil.LessEqNode)

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        return self._define_binary_node(node, scope, cil.EqualNode)
