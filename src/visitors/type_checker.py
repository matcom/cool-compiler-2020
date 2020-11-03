from semantic import *

import visitors.visitor as visitor
from pipeline import State
from cl_ast import *

class TypeChecker(State):
    def __init__(self, name):
        super().__init__(name)
        self.context = None
        self.current_type = None
        self.current_method = None

    def run(self, inputx):
        ast, context, scope = inputx
        self.context = context
        self.visit(ast, scope)
        return ast, context, scope

    # Checker Auxiliar Functions (TODO: Combine in the Context)

    def _get_type(self, typex):
        try:
            return self.context.get_type(typex)
        except SemanticError as e:
            self.errors.append(e.text)
            return ErrorType()

    def _get_method(self, typex, name):
        if typex is ErrorType():
            return
        
        try:
            return typex.get_method(name)
        except SemanticError as e:
            self.errors.append(e.text)
            return MethodError(name, [], [], ErrorType())

    def _check_args(self, meth, scope, args):
        arg_types = [ self.visit(arg, scope) for arg in args ]
        
        if len(arg_types) > len(meth.param_types):
            self.errors.append(TOO_MANY_ARGUMENTS % meth.name)
        
        elif len(arg_types) < len(meth.param_types):
            for arg in meth.param_names[len(arg_types):]:
                self.errors.append(MISSING_PARAMETER % (arg, meth.name))

        for atype, ptype in zip(arg_types, meth.param_types):
            if not atype.conforms_to(ptype):
                self.errors.append(INCOMPATIBLE_TYPES % (ptype.name, atype.name))

    def _join_types(self, ltypes):
        import itertools as itt

        def path_to_objet(typex):
            path = []
            c_type = typex

            while c_type:
                path = [c_type] + path
                c_type = c_type.parent

            return path

        paths = [path_to_objet(typex) for typex in ltypes]
        tuples = zip(*paths)
    
        jtype = None

        for t in tuples:
            nxt = t[0]
            if all(nxt == l for l in t):
                jtype = nxt

        return jtype

    # Visitor Functions

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        for dec in node.declarations:
            self.visit(dec, scope.cls_scopes[dec.id])

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        for feature in node.features:
            self.visit(feature, scope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        ascope = scope.attr_scopes[node.id]
        vinfo = scope.get_attribute(node.id)
        if node.expr:
            etype = self.visit(node.expr, ascope)
            if not etype.conforms_to(vinfo.type):
                self.errors.append(INCOMPATIBLE_TYPES %(etype.name, vinfo.type.name))
                return ErrorType()
            return etype
        try:
            return self.context.get_type(node.type)
        except:
            return ErrorType()

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        fscope = scope.func_scopes[node.id]
        parent = self.current_type.parent
        ptypes = [param[1] for param in node.params]

        self.current_method = meth = self.current_type.get_method(node.id)

        while parent:
            try:
                old_meth = parent.get_method(node.id)
                if old_meth.return_type.name != meth.return_type.name and node.type != 'SELF_TYPE':
                    self.errors.append(WRONG_SIGNATURE % (node.id, parent.name))
                elif any(type1.name != type2.name for name, type1, type2 in zip(ptypes, meth.param_types, old_meth.param_types)):
                    self.errors.append(WRONG_SIGNATURE % (node.id, parent.name))
                break
            except SemanticError:
                parent = parent.parent
        
        res = self.visit(node.body, fscope)

        if not res.conforms_to(meth.return_type):
            self.errors.append(INCOMPATIBLE_TYPES %(meth.return_type.name, res.name))

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        vinfo = scope.find_variable(node.id)
        vtype = vinfo.type

        if node.expr:
            etype = self.visit(node.expr, scope)
            if not etype.conforms_to(vtype):
                self.errors.append(INCOMPATIBLE_TYPES %(vtype.name, etype.name))
            return etype

        return vtype

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        vinfo = scope.find_variable(node.id)
        vtype = vinfo.type
        
        rtype = self.visit(node.expr, scope)

        if not rtype.conforms_to(vtype):
            self.errors.append(INCOMPATIBLE_TYPES %(vtype.name, rtype.name))

        return rtype

    @visitor.when(ExprCallNode)
    def visit(self, node, scope):
        otype = self.visit(node.obj, scope)

        meth = self._get_method(otype, node.id)
        self._check_args(meth, scope, node.args)
        return meth.return_type

    @visitor.when(ParentCallNode)
    def visit(self, node, scope):
        otype = self.visit(node.obj, scope)
        ptype = self._get_type(node.type)

        if not otype.conforms_to(ptype):
            self.errors.append(INCOMPATIBLE_TYPES % (otype.name, ptype.name))
            return ErrorType()
        
        meth = self._get_method(ptype, node.id)
        self._check_args(meth, scope, node.args)
        return meth.return_type

    @visitor.when(SelfCallNode)
    def visit(self, node, scope):
        stype = self.current_type

        meth = self._get_method(stype, node.id)
        self._check_args(meth, scope, node.args)
        return meth.return_type

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        ctype = self.visit(node.cond, scope)

        if ctype.name != 'Bool':
            self.errors.append(INCORRECT_TYPE %(ctype.name, 'Bool'))
        
        self.visit(node.expr, scope)
        
        return ObjectType()

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        ctype = self.visit(node.cond, scope)

        if ctype.name != 'Bool':
            self.errors.append(INCORRECT_TYPE %(ctype.name, 'Bool'))

        ttype = self.visit(node.stm, scope)
        ftype = self.visit(node.else_stm, scope)

        return self._join_types([ttype, ftype])

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        vtype = None
        
        for expr in node.expr_list:
            vtype = self.visit(expr, scope)

        return vtype        

    @visitor.when(CaseNode)
    def visit(self, node, scope):
        etype = self.visit(node.expr, scope)
        new_scope = scope.expr_dict[node]

        types = [self.visit(opt, c_scp) for opt, c_scp in zip(node.case_list, new_scope.children)]
        
        return self._join_types([t[0] for t in types])
        
    @visitor.when(OptionNode)
    def visit(self, node, scope):
        var_info = scope.find_variable(node.id)
        typex = self.visit(node.expr, scope)
        return typex, var_info.type

    @visitor.when(LetNode)
    def visit(self, node, scope):
        child_scope = scope.expr_dict[node]
        
        iscope = child_scope
        
        for init in node.init_list:
            self.visit(init, iscope)
            iscope = iscope.children[0]

        return self.visit(node.expr, iscope)

    @visitor.when(LetDeclarationNode)
    def visit(self, node, scope):
        vinfo = scope.find_variable(node.id)
        vtype = vinfo.type

        if node.expr:
            etype = self.visit(node.expr, scope)
            if not etype.conforms_to(vtype):
                self.errors.append(INCOMPATIBLE_TYPES %(vtype.name, etype.name))
            return etype

        return vtype

    @visitor.when(BinaryArithOperationNode)
    def visit(self, node, scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if ltype != rtype != IntType():
            self.errors.append(BOPERATION_NOT_DEFINED %('Arithmetic', ltype.name, rtype.name))
            return ErrorType()

        return IntType()

    @visitor.when(LessEqualNode)
    def visit(self, node, scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if ltype != rtype != IntType():
            self.errors.append(BOPERATION_NOT_DEFINED %('Comparison', ltype.name, rtype.name))
            return ErrorType()

        return BoolType()

    @visitor.when(LessNode)
    def visit(self, node, scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if ltype != rtype != IntType():
            self.errors.append(BOPERATION_NOT_DEFINED %('Comparison', ltype.name, rtype.name))
            return ErrorType()

        return BoolType()

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)

        if ltype in [IntType(), StringType(), BoolType()] and ltype != rtype:
            self.errors.append(f'Invalid comparison operation between {ltype.name} and {rtype.name}')

        return BoolType()

    @visitor.when(NotNode)
    def visit(self, node, scope):
        ltype = self.visit(node.expr, scope)
        if ltype != BoolType():
            self.errors.append(UOPERATION_NOT_DEFINED %('Logical', ltype.name))
            return ErrorType()

        return BoolType()

    @visitor.when(BitNotNode)
    def visit(self, node, scope):
        ltype = self.visit(node.expr, scope)
        if ltype != IntType():
            self.errors.append(UOPERATION_NOT_DEFINED %('Arithmetic', ltype.name))
            return ErrorType()

        return IntType()

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        return BoolType()

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        return scope.find_variable(node.id).type
    
    @visitor.when(NewNode)
    def visit(self, node, scope):
        return self._get_type(node.type)

    @visitor.when(IntegerNode)
    def visit(self, node, scope):
        return IntType()

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        return BoolType()
   
    @visitor.when(StringNode)
    def visit(self, node, scope):
        return StringType()