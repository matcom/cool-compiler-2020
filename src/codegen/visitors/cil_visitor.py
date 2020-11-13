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
        # self.register_instruction(cil.ArgNode(instance))

        name = self.to_function_name('main', 'Main')
        self.register_instruction(cil.StaticCallNode('Main', 'main', result, [cil.ArgNode(instance)], 'Object'))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        
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
            self.current_type.define_method(self.current_type.name, [], [], self.current_type)
            scopes = [scope] + scope.children
        else:
            func_declarations = []
            scopes = scope.children
            
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
        self.register_param('self', self.current_type)
        for p_name, p_type in node.params:
            self.register_param(p_name, p_type)
        
        value, _ = self.visit(node.body, scope)
        
        # Handle RETURN
        self.register_instruction(cil.ReturnNode(value)) 
        self.current_method = None


    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope):
        var_info = scope.find_variable(node.id)
        vtype = get_type(var_info.type, self.current_type)
        local_var = self.register_local(var_info.name)

        value, _ = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(local_var, value))
        return local_var, vtype


    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        var_info = scope.find_local(node.id)
        value, typex = self.visit(node.expr, scope)
        if var_info is None:
            var_info = scope.find_attribute(node.id)
            attributes = [attr.name for attr, a_type in self.current_type.all_attributes()]
            offset = attributes.index(var_info.name)
            self.register_instruction(cil.SetAttribNode('self', var_info.name, self.current_type.name, value))
        else:
            local_name = self.to_var_name(var_info.name)
            self.register_instruction(cil.AssignNode(local_name, value))
        return value, typex

    def _return_type(self, typex: Type, node):
        meth = typex.get_method(node.id, node.pos)
        return get_type(meth.return_type, self.current_type)

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        obj, otype = self.visit(node.obj, scope)
        
        args = [self.visit(arg, scope)[0] for arg in node.args]
        args_node = [cil.ArgNode(obj, self.index)] + [cil.ArgNode(arg, self.index) for arg in args]
 
        rtype = otype.get_method(node.id, node.pos).return_type
        if isinstance(rtype, VoidType):
            result = None
        else: 
            result = self.define_internal_local()

        # name = self.to_function_name(node.id, otype.name)
        self.register_instruction(cil.StaticCallNode(otype.name, node.id, result, args_node, rtype.name))
        return result, self._return_type(otype, node)

    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope: Scope):
        obj, otype = self.visit(node.obj, scope)
        
        args = [self.visit(arg, scope)[0] for arg in node.args]
        args_node = [cil.ArgNode(obj, self.index)] + [cil.ArgNode(arg, self.index) for arg in args]
        
        rtype = otype.get_method(node.id, node.pos).return_type
        if isinstance(rtype, VoidType):
            result = None
        else: 
            result = self.define_internal_local()
        
        # name = self.to_function_name(node.id, node.type)
        self.register_instruction(cil.StaticCallNode(node.type, node.id, result, args_node, rtype.name))
        return result, self._return_type(otype, node)

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode, scope: Scope):
        
        args = [self.visit(arg, scope)[0] for arg in node.args]
        args_node = [cil.ArgNode(VariableInfo('self', self.current_type))] + [cil.ArgNode(arg, self.index) for arg in args]
       
        name = self.to_function_name(node.id, self.current_type.name)
        rtype = self.current_type.get_method(node.id, node.pos).return_type
        if isinstance(rtype, VoidType):
            result = None
        else: 
            result = self.define_internal_local()

        self.register_instruction(cil.DynamicCallNode(self.current_type.name, node.id, result, args_node, rtype.name))
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
            # attributes = [attr.name for attr, a_type in self.current_type.all_attributes()]
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
            self.register_instruction(cil.StaticCallNode(typex.name, typex.name, None, [cil.ArgNode(instance)], typex.name))
        
        # attributes = [attr for attr, a_type in typex.all_attributes()]
        # for i, attr in enumerate(attributes):
        #     # Aquí sería más cómodo llamar al constructor de la clase, pero tendría que guardar todos los constructores
        #     if attr.expr is not None:
        #         expr, _ = self.visit(attr.expr, scope)
        #     elif attr.type.name == 'Int':
        #         expr, _ = self.visit(ConstantNumNode(0), scope)
        #     elif attr.type.name == 'Bool':
        #         expr, _ = self.visit(ConstantBoolNode(False), scope)
        #     elif attr.type.name == 'String':
        #         expr, _ = self.visit(ConstantStrNode(''), scope)
        #     # attr_name = self.to_attr_name(var_info.name, typex.name)           
        #     self.register_instruction(cil.SetAttribNode(instance, attr.name, typex.name, expr))
        return instance, typex


    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        '''
        LABEL start
        IF <cond> GOTO continue
        GOTO end
        LABEL continue
        res = <expr>
        GOTO start
        LABEL end
        '''
        start_label = cil.LabelNode('start')
        continue_label = cil.LabelNode('continue')
        end_label = cil.LabelNode('end')
        
        result = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result, 'void'))
        self.register_instruction(start_label)

        cond, _ = self.visit(node.cond, scope)
        self.register_instruction(cil.GotoIfNode(cond, continue_label.label))
        self.register_instruction(cil.GotoNode(end_label.label))
        self.register_instruction(continue_label)
        expr, typex = self.visit(node.expr, scope)
        self.register_instruction(cil.GotoNode(start_label.label))
        self.register_instruction(end_label)
        
        self.register_instruction(cil.AssignNode(result, expr))
        return result, typex

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

        true_label = cil.LabelNode("true")
        end_label = cil.LabelNode("end")

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
        result = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result, expr))
        return result, typex

    @visitor.when(CaseNode) 
    def visit(self, node: CaseNode, scope: Scope):
        expr, typex = self.visit(node.expr, scope)
        result = self.define_internal_local()
        etype = self.define_internal_local()
        end_label = cil.LabelNode('end')
        self.register_instruction(cil.TypeOfNode(expr, etype))

        new_scope = scope.expr_dict[node]
        for i, (case, c_scope) in enumerate(zip(node.case_list, new_scope.children)):
            next_label = cil.LabelNode(f'next_{i}')
            expr_i, label = self.visit(case, c_scope, expr, etype, next_label)
            self.register_instruction(cil.AssignNode(result, expr_i))
            self.register_instruction(cil.GotoNode(end_label.label))
            self.register_instruction(label)
        self.register_instruction(end_label)
        return result, typex

    @visitor.when(OptionNode)
    def visit(self, node: OptionNode, scope: Scope, expr, expr_type, next_label):
        aux = self.define_internal_local()
        # TODO: Buscar una forma de representar conforms in cil
        self.register_instruction(cil.MinusNode(aux, expr_type, node.typex))

        self.register_instruction(cil.GotoIfNode(aux, next_label.label))
        var_info = scope.find_variable(node.id)
        local_var = self.register_local(var_info.name)
        self.register_instruction(cil.AssignNode(local_var, expr))

        expr_i, typex = self.visit(node.expr, scope)
        return exp_i, next_label

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        return self._define_unary_node(node, scope, cil.NotNode)

    @visitor.when(BinaryNotNode)
    def visit(self, node: NotNode, scope: Scope):
        return self._define_unary_node(node, scope, cil.NotNode)


    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope: Scope):
        result = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(node.obj, result))
        self.register_instruction(cil.EqualNode(result, result, VoidType().name))
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
