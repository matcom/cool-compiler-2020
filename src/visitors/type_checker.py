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

    def _get_type(self, node, typex):
        try:
            return self.context.get_type(typex)
        except SemanticError as e:
            self.errors.append(CSemanticError(node.row, node.col, e.text))
            return ErrorType()

    def _get_method(self, node, typex, name):
        if typex is ErrorType():
            return
        try:
            return typex.get_method(name)
        except SemanticError as e:
            self.errors.append(CNameError(node.row, node.col, e.text))
            return MethodError(name, [], [], ErrorType())

    def _check_args(self, node, meth, scope, args):
        arg_types = [ self.visit(arg, scope) for arg in args ]
        
        if len(arg_types) > len(meth.param_types):
            self.errors.append(CSemanticError(node.row, node.col, TOO_MANY_ARGUMENTS % meth.name))
        
        elif len(arg_types) < len(meth.param_types):
            for arg in meth.param_names[len(arg_types):]:
                self.errors.append(CSemanticError(node.row, node.col, MISSING_PARAMETER % (arg, meth.name)))

        for arg, atype, ptype in zip(args, arg_types, meth.param_types):
            if not atype.conforms_to(ptype):
                self.errors.append(CTypeError(arg.row, arg.col, INCOMPATIBLE_TYPES % (ptype.name, atype.name)))

    def _join_types(self, ltypes):

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
                self.errors.append(CTypeError(node.expr.row, node.expr.col, INCOMPATIBLE_TYPES %(etype.name, vinfo.type.name)))
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
        # ptypes = [param[1] for param in node.params]

        self.current_method = meth = self.current_type.get_method(node.id)

        # while parent:
        #     try:
        #         old_meth = parent.get_method(node.id)
        #         if old_meth.return_type.name != meth.return_type.name and node.type != 'SELF_TYPE':
        #             self.errors.append(CSemanticError(node.row, node.col, WRONG_SIGNATURE % (node.id, parent.name)))
        #         elif any(type1.name != type2.name for name, type1, type2 in zip(ptypes, meth.param_types, old_meth.param_types)):
        #             self.errors.append(CSemanticError(node.row, node.col, WRONG_SIGNATURE % (node.id, parent.name)))
        #         break
        #     except SemanticError:
        #         parent = parent.parent
        
        res = self.visit(node.body, fscope)

        if not res.conforms_to(meth.return_type):
            self.errors.append(CTypeError(node.body.row, node.body.col, INCOMPATIBLE_TYPES %(meth.return_type.name, res.name)))

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        vinfo = scope.find_variable(node.id)
        vtype = vinfo.type

        if node.expr:
            etype = self.visit(node.expr, scope)
            if not etype.conforms_to(vtype):
                self.errors.append(CTypeError(node.row, node.col, INCOMPATIBLE_TYPES %(vtype.name, etype.name)))
            return etype

        return vtype

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        vinfo = scope.find_variable(node.id)
        vtype = vinfo.type
        
        rtype = self.visit(node.expr, scope)

        if not rtype.conforms_to(vtype):
            self.errors.append(CTypeError(node.expr.row, node.expr.col, INCOMPATIBLE_TYPES %(vtype.name, rtype.name)))

        return rtype

    @visitor.when(ExprCallNode)
    def visit(self, node, scope):
        otype = self.visit(node.obj, scope)

        meth = self._get_method(node, otype, node.id)
        self._check_args(node, meth, scope, node.args)
        return meth.return_type

    @visitor.when(ParentCallNode)
    def visit(self, node, scope):
        otype = self.visit(node.obj, scope)
        ptype = self._get_type(node, node.type)

        if not otype.conforms_to(ptype):
            self.errors.append(CTypeError(node.obj.row, node.obj.col, INCOMPATIBLE_TYPES % (otype.name, ptype.name)))
            return ErrorType()
        
        meth = self._get_method(node, ptype, node.id)
        self._check_args(node, meth, scope, node.args)
        return meth.return_type

    @visitor.when(SelfCallNode)
    def visit(self, node, scope):
        stype = self.current_type

        meth = self._get_method(node, stype, node.id)
        self._check_args(node, meth, scope, node.args)
        return meth.return_type

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        ctype = self.visit(node.cond, scope)

        if ctype.name != 'Bool':
            self.errors.append(CTypeError(node.cond.row, node.cond.col, INCORRECT_TYPE %(ctype.name, 'Bool')))
        
        self.visit(node.expr, scope)
        
        return ObjectType()

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        ctype = self.visit(node.cond, scope)

        if ctype.name != 'Bool':
            self.errors.append(CTypeError(node.cond.row, node.cond.col, INCORRECT_TYPE %(ctype.name, 'Bool')))

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
                self.errors.append(CTypeError(node.expr.row, node.expr.col, INCOMPATIBLE_TYPES %(vtype.name, etype.name)))
            return etype

        return vtype

    @visitor.when(BinaryArithOperationNode)
    def visit(self, node, scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if rtype != IntType() or ltype != IntType():
            self.errors.append(CTypeError(node.row, node.col, BOPERATION_NOT_DEFINED %('Arithmetic', ltype.name, rtype.name)))
            return ErrorType()

        return IntType()

    @visitor.when(LessEqualNode)
    def visit(self, node, scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if rtype != IntType() or ltype != IntType():
            self.errors.append(CTypeError(node.row, node.col, BOPERATION_NOT_DEFINED %('Comparison', ltype.name, rtype.name)))
            return ErrorType()

        return BoolType()

    @visitor.when(LessNode)
    def visit(self, node, scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if rtype != IntType() or ltype != IntType():
            self.errors.append(CTypeError(node.row, node.col, BOPERATION_NOT_DEFINED %('Comparison', ltype.name, rtype.name)))
            return ErrorType()

        return BoolType()

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)

        if ltype in [IntType(), StringType(), BoolType()] and ltype != rtype:
            self.errors.append(CTypeError(node.row, node.col, f'Invalid comparison operation between {ltype.name} and {rtype.name}'))

        return BoolType()

    @visitor.when(NotNode)
    def visit(self, node, scope):
        ltype = self.visit(node.expr, scope)
        if ltype != BoolType():
            self.errors.append(CTypeError(node.row, node.col, UOPERATION_NOT_DEFINED %('Logical', ltype.name)))
            return ErrorType()

        return BoolType()

    @visitor.when(BitNotNode)
    def visit(self, node, scope):
        ltype = self.visit(node.expr, scope)
        if ltype != IntType():
            self.errors.append(CTypeError(node.row, node.col, UOPERATION_NOT_DEFINED %('Arithmetic', ltype.name)))
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
        return self._get_type(node, node.type)

    @visitor.when(IntegerNode)
    def visit(self, node, scope):
        return IntType()

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        return BoolType()
   
    @visitor.when(StringNode)
    def visit(self, node, scope):
        return StringType()