from semantic.visitors import visitor
from semantic.tools import *
from utils.utils import get_common_basetype
from utils.ast import *
from utils.errors import SemanticError, AttributesError, TypesError, NamesError


class TypeChecker:
    def __init__(self, context:Context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope:Scope):
        for declaration, new_scope in zip(node.declarations, scope.children):
            self.visit(declaration, new_scope)
    
    def _get_type(self, ntype:Type, pos):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()


    def _get_method(self, typex:Type, name:str, pos) -> Method:
        try:
            return typex.get_method(name, pos)
        except SemanticError as e:
            if type(typex) != ErrorType and type(typex) != AutoType:
                self.errors.append(e)
            return MethodError(name, [], [], ErrorType())


    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):
        self.current_type = self.context.get_type(node.id, node.pos)

        fd = [feat for feat in node.features if isinstance(feat, FuncDeclarationNode)]

        for feat in node.features:
            if isinstance(feat, AttrDeclarationNode):
                self.visit(feat, scope)

        for feat, child_scope in zip(fd, scope.children):
            self.visit(feat, child_scope)  
        

    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode, scope:Scope):
        varinfo = scope.find_variable(node.id)
        if node.expr is not None:
            typex = self.visit(node.expr, scope)
            if not typex.conforms_to(varinfo.type):
                error_text = TypesError.INCOMPATIBLE_TYPES %(typex.name, varinfo.type.name)
                self.errors.append(TypesError(error_text, node.pos))
                return ErrorType()
            return typex
        return self._get_type(node.type, node.type_pos)


        
    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode, scope:Scope):
        parent = self.current_type.parent 
        ptypes = [param[1] for param in node.params]

        self.current_method = method = self.current_type.get_method(node.id, node.pos)
        if parent is not None:
            try:
                old_meth = parent.get_method(node.id, node.pos)
                error_text = AttributesError.WRONG_SIGNATURE % (node.id, parent.name)
                if old_meth.return_type.name != method.return_type.name:
                    if node.type != 'SELF_TYPE':
                        self.errors.append(AttributesError(error_text, *node.pos))
                elif any(type1.name != type2.name for name, type1, type2 in zip(ptypes, method.param_types, old_meth.param_types)):
                    if name != 'SELF_TYPE':
                        self.errors.append(AttributesError(error_text, *node.pos))
            except SemanticError:
                pass

        result = self.visit(node.body, scope)
        
        if not result.conforms_to(method.return_type):
            error_text = TypesError.INCOMPATIBLE_TYPES %(method.return_type.name, result.name)
            self.errors.append(TypesError(error_text, *node.type_pos))

    
    @visitor.when(VarDeclarationNode)
    def visit(self, node:VarDeclarationNode, scope:Scope):

        var_info = scope.find_variable(node.id)
        vtype = var_info.type

        if node.expr != None:
            typex = self.visit(node.expr, scope)
            if not typex.conforms_to(var_info.type):
                error_text = TypesError.INCOMPATIBLE_TYPES %(vtype.name, typex.name)            
                self.errors.append(TypesError(error_text, *node.type_pos))
            return typex
        return vtype
            
        
    @visitor.when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        vinfo = scope.find_variable(node.id)
        vtype = vinfo.type
            
        typex = self.visit(node.expr, scope)

        if not typex.conforms_to(vtype):
            error_text = TypesError.INCOMPATIBLE_TYPES %(vtype.name, typex.name)            
            self.errors.append(TypesError(error_text, *node.pos))
        return typex
            

    def _check_args(self, meth:Method, scope:Scope, args, pos):
        arg_types = [self.visit(arg, scope) for arg in args]
        
        if len(arg_types) > len(meth.param_types):
            error_text = SemanticError.TOO_MANY_ARGUMENTS % meth.name
            self.errors.append(SemanticError(error_text, *pos))
        elif len(arg_types) < len(meth.param_types):
            for arg, arg_info in zip(meth.param_names[len(arg_types):], args[len(arg_types):]):
                error_text = SemanticError.MISSING_PARAMETER % (arg, meth.name)
                self.errors.append(SemanticError(error_text, *arg_info.pos))

        for atype, ptype, arg_info in zip(arg_types, meth.param_types, args):
            if not atype.conforms_to(ptype):
                error_text = TypesError.INCOMPATIBLE_TYPES % (ptype.name, atype.name)
                self.errors.append(TypesError(error_text, *arg_info.pos))
        

    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope:Scope):
        stype = self.visit(node.obj, scope)

        meth = self._get_method(stype, node.id, node.pos)
        self._check_args(meth, scope, node.args, node.pos)
        return meth.return_type


    @visitor.when(BaseCallNode)
    def visit(self, node:BaseCallNode, scope:Scope):
        obj = self.visit(node.obj, scope)
        typex = self._get_type(node.type, node.type_pos)

        if not obj.conforms_to(typex):
            error_text = TypesError.INCOMPATIBLE_TYPES % (typex.name, obj.name)
            self.errors.append(TypesError(error_text, *node.type_pos))
            return ErrorType()
        
        meth = self._get_method(typex, node.id, node.pos)
        self._check_args(meth, scope, node.args, node.pos)
        return meth.return_type


    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode, scope:Scope):
        typex = self.current_type

        meth = self._get_method(typex, node.id, node.pos)
        self._check_args(meth, scope, node.args, node.pos)
        return meth.return_type


    @visitor.when(ConstantNumNode)
    def visit(self, node:ConstantNumNode, scope:Scope):
        return IntType(node.pos)


    @visitor.when(ConstantBoolNode)
    def visit(self, node:ConstantBoolNode, scope:Scope):
        return BoolType(node.pos)

   
    @visitor.when(ConstantStrNode)
    def visit(self, node:ConstantStrNode, scope:Scope):
        return StringType(node.pos)


    @visitor.when(VariableNode)
    def visit(self, node:VariableNode, scope:Scope):
        return scope.find_variable(node.lex).type
    

    @visitor.when(InstantiateNode)
    def visit(self, node:InstantiateNode, scope:Scope):
        return self._get_type(node.lex, node.pos)

    
    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope:Scope):
        cond = self.visit(node.cond, scope)
        
        if cond.name != 'Bool':
            self.errors.append(INCORRECT_TYPE % (cond.name, 'Bool'))   
        return self.visit(node.expr, scope)


    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode, scope:Scope):
        self.visit(node.expr, scope)
        return BoolType()


    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope:Scope):
        cond = self.visit(node.cond, scope)

        if cond.name != 'Bool':
            error_text = TypesError.INCORRECT_TYPE % (cond.name, 'Bool')
            self.errors.append(TypesError(error_text, node.pos))
        
        true_type = self.visit(node.stm, scope)
        false_type = self.visit(node.else_stm, scope)
      
        if true_type.conforms_to(false_type):
            return false_type
        elif false_type.conforms_to(true_type):
            return true_type
        else:
            error_text = TypesError.INCOMPATIBLE_TYPES % (false_type.name, true_type.name)
            self.errors.append(TypesError(error_text, node.pos))
            return ErrorType()
        

    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, scope:Scope):
        value = None
        for exp in node.expr_list:
            value = self.visit(exp, scope)
        return value


    @visitor.when(LetNode)
    def visit(self, node:LetNode, scope:Scope):
        child_scope = scope.expr_dict[node]
        for init in node.init_list:
            self.visit(init, child_scope)
        return self.visit(node.expr, child_scope)

    
    @visitor.when(CaseNode) 
    def visit(self, node:CaseNode, scope:Scope):
        type_expr = self.visit(node.expr, scope)

        new_scope = scope.expr_dict[node]
        types = []
        var_types = []
        for case, c_scope in zip(node.case_list, new_scope.children):
            t, vt = self.visit(case, c_scope)
            types.append(t)
            var_types.append(vt)

        for t in var_types:
            if not type_expr.conforms_to(t):
                error_text = TypesError.INCOMPATIBLE_TYPES % (t.name, type_expr.name)
                self.errors.append(TypesError(error_text, *node.pos))
                return ErrorType()

        return get_common_basetype(types)
        

    @visitor.when(OptionNode)
    def visit(self, node:OptionNode, scope:Scope):
        var_info = scope.find_variable(node.id)
        typex = self.visit(node.expr, scope)
        return typex, var_info.type

            
    @visitor.when(BinaryArithNode)
    def visit(self, node:BinaryArithNode, scope:Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if ltype != rtype != IntType():
            error_text = TypesError.BOPERATION_NOT_DEFINED %('Arithmetic', ltype.name, rtype.name)
            self.errors.append(TypesError(error_text, *node.pos))
            return ErrorType()
        return IntType()


    @visitor.when(BinaryLogicalNode)
    def visit(self, node:BinaryLogicalNode, scope:Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if ltype != rtype != IntType():
            error_text = TypesError.BOPERATION_NOT_DEFINED %('Logical', ltype.name, rtype.name)
            self.errors.append(TypesError(error_text, *node.pos))
            return ErrorType()

        return BoolType()


    @visitor.when(UnaryLogicalNode)
    def visit(self, node:UnaryLogicalNode, scope:Scope):
        ltype = self.visit(node.expr, scope)
        if ltype != BoolType():
            error_text = TypesError.UOPERATION_NOT_DEFINED %('Logical', ltype.name)
            self.errors.append(TypesError(error_text, *node.pos))
            return ErrorType()

        return BoolType()



    @visitor.when(UnaryArithNode)
    def visit(self, node:UnaryArithNode, scope:Scope):
        ltype = self.visit(node.expr, scope)
        if ltype != IntType():
            error_text = TypesError.UOPERATION_NOT_DEFINED %('Arithmetic', ltype.name)
            self.errors.append(TypesError(error_text, *node.pos))
            return ErrorType()
        return IntType()