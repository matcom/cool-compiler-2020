from .utils import *
from ...visitors import visitor
from ...cmp import CoolUtils as cool
from ...cmp import IntType, BoolType, StringType, SemanticError, ErrorType, SelfType, Scope

# Type Checker
class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        
        scope.define_variable('self', SelfType(self.current_type))
        cur_type = self.current_type
        while True:
            for attr in cur_type.attributes:
                vtype = attr.type
                if vtype.name == ST:
                    vtype = SelfType(self.current_type)
                var = scope.define_variable(attr.name, vtype)
                var.node = attr.node
            if not cur_type.parent:
                break
            cur_type = cur_type.parent
            
        cur_type = self.current_type
        pending, count = [], 0
        for feature in node.features:
            if isinstance(feature, cool.AttrDeclarationNode):
                self.visit(feature, scope)
                if not scope.is_defined(feature.id):
                    vtype = cur_type.attributes[count].type
                    if vtype.name == ST:
                        vtype = SelfType(self.current_type)
                    var = scope.define_variable(feature.id, vtype)
                    var.node = cur_type.attributes[count].node
                count += 1
            else:
                pending.append(feature)

        for feature in pending:  
            self.visit(feature, scope.create_child())
    
    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node, scope):
        if not node.expr:
            return

        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        real_type = node.attr_type
        node.info = [expr_type, real_type]

        if not expr_type.conforms_to(real_type):
            self.errors.append((TypeError(INCOMPATIBLE_TYPES % (expr_type.name, real_type.name)),  node.arrow))
            
    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = node.id
        
        for pname, ptype, pnode in zip(node.arg_names, node.arg_types, node.arg_nodes):
            var = scope.define_variable(pname, ptype)
            var.node = pnode
            
        self.visit(node.body, scope)
            
        body_type = node.body.computed_type
        method_rtn_type = node.ret_type
        node.info = [body_type, method_rtn_type]

        if not body_type.conforms_to(method_rtn_type):
            self.errors.append((TypeError(INCOMPATIBLE_TYPES % (body_type.name, method_rtn_type.name)), node.ttype))
            
    @visitor.when(cool.AssignNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node_type = node.expr.computed_type
        var_type = None

        try:
            if not scope.is_defined(node.id):
                scope.define_variable(node.id, ErrorType())
                raise NameError(VARIABLE_NOT_DEFINED % (node.id))
            var = scope.find_variable(node.id)
            var_type = var.type
            if var.name == 'self':
                raise SemanticError(SELF_IS_READONLY)
            if not node_type.conforms_to(var.type): 
                raise TypeError(INCOMPATIBLE_TYPES % (node_type.name, var.type.name))
        except Exception as ex:
            self.errors.append((ex, node.tid))
            node_type = ErrorType()
        
        node.info = [node_type, var_type]
        node.computed_type = node_type
        
    @visitor.when(cool.CaseOfNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        
        types_list = []
        branches = set()
        for case in node.branches:
            if case.type in branches:
                # //TODO: Check this again after the Inference process
                self.errors.append((SemanticError(DUPLICATED_BRANCH % (case.type)), case.ttype))
            branches.add(case.type)
            self.visit(case, scope.create_child())
            types_list.append(case.computed_type)

        node.computed_type = LCA(types_list)

    @visitor.when(cool.CaseExpressionNode)
    def visit(self, node, scope):
        node.scope = scope
        try:
            assert node.type != ST
            branch_type = self.context.get_type(node.type)
        except TypeError as ex:
            self.errors.append((ex, node.ttype))
            branch_type = ErrorType()
        except AssertionError:
            self.errors.append((SemanticError(INVALID_BRANCH % node.id), node.ttype))
            branch_type = ErrorType()
        node.branch_type = branch_type
        
        if node.id == 'self':
            self.errors.append((SemanticError(SELF_IS_READONLY), node.id))
        else:
            var = scope.define_variable(node.id, branch_type)
            var.node = node
        self.visit(node.expr, scope)
        node.computed_type = node.expr.computed_type
            
    @visitor.when(cool.LetInNode)
    def visit(self, node, scope):
        node.scope = scope
        
        for expr in node.let_body:
            node.scope = node.scope.create_child()
            self.visit(expr, node.scope)
        
        self.visit(node.in_body, node.scope)
        node.computed_type = node.in_body.computed_type

    @visitor.when(cool.LetAttributeNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
            if node_type.name == ST:
                node_type = SelfType(self.current_type)
        except TypeError as ex:
            self.errors.append((ex, node.ttype))
            node_type = ErrorType()
        node.attr_type = node_type
        node.scope = None
        
        if node.expr:
            self.visit(node.expr, scope)
            expr_type = node.expr.computed_type
            node.info = [expr_type, node_type]

            if not expr_type.conforms_to(node_type): 
                self.errors.append((TypeError(INCOMPATIBLE_TYPES % (expr_type.name, node_type.name)), node.arrow))
        if node.id == 'self':
            self.errors.append((SemanticError(SELF_IS_READONLY), node.tid))
        else:
            var = scope.define_variable(node.id, node_type)
            var.node = node
        
    @visitor.when(cool.IfThenElseNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        node.cond_type = node.condition.computed_type

        BOOL = self.context.get_type('Bool')
        if not node.cond_type.conforms_to(BOOL):
            self.errors.append((TypeError(CONDITION_NOT_BOOL % ('If', node.cond_type.name)), node.token))

        self.visit(node.if_body, scope)
        if_type = node.if_body.computed_type

        self.visit(node.else_body, scope)
        else_type = node.else_body.computed_type
        node.computed_type = LCA([if_type, else_type])
        
    @visitor.when(cool.BlockNode)
    def visit(self, node, scope):
        for expr in node.exprs:
            self.visit(expr, scope)

        last_expr = node.exprs[-1]
        node.computed_type = last_expr.computed_type    
            
    @visitor.when(cool.WhileLoopNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        node.cond_type = node.condition.computed_type

        BOOL = self.context.get_type('Bool')
        if not node.cond_type.conforms_to(BOOL):
            self.errors.append((TypeError(CONDITION_NOT_BOOL % ('While', node.cond_type.name)), node.token))

        self.visit(node.body, scope)
        node.computed_type = self.context.get_type('Object')
    
    @visitor.when(cool.FunctionCallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope)
        obj_type = node.obj.computed_type
        
        error = False

        arg_types, real_types = [], []
        for arg in node.args:
            self.visit(arg, scope)
            arg_types.append(arg.computed_type)
        
        try:
            if node.type:
                token = node.ttype
                cast_type = self.context.get_type(node.type)
                if cast_type.name == ST:
                    raise SemanticError("Invalid use of SELF_TYPE")
                if cast_type.name == AT:
                    raise SemanticError('Is not possible to use AUTO_TYPE in a cast')
                if not obj_type.conforms_to(cast_type):
                    raise TypeError(INCOMPATIBLE_TYPES % (obj_type.name, node.type))
                obj_type = cast_type
            
            assert obj_type
            token = node.tid
            obj_method = obj_type.get_method(node.id)
            node.obj_method = obj_method
            if len(node.args) == len(obj_method.param_types):
                for idx, (arg, param_type) in enumerate(zip(arg_types, obj_method.param_types)):
                    real_types.append(param_type)

                    if not arg.conforms_to(param_type):
                        self.errors.append((TypeError(INCOMPATIBLE_TYPES % (arg.name, param_type.name + f" in the argument #{idx} of {node.id}")), token))
                        error = True
            else:
                raise SemanticError(f'Method "{obj_method.name}" of "{obj_type.name}" only accepts {len(obj_method.param_types)} argument(s)')
            assert not error
            node_type = obj_method.return_type
            if node_type.name == ST:
                node_type = obj_type
        except AssertionError:
            node_type = ErrorType()
        except Exception as ex:
            self.errors.append((ex, token))
            node_type = ErrorType()
        
        node.info = [arg_types, real_types]
        node.computed_type = node_type

    @visitor.when(cool.MemberCallNode)
    def visit(self, node, scope):
        obj_type = SelfType(self.current_type)
        
        error = False

        arg_types, real_types = [], []
        for arg in node.args:
            self.visit(arg, scope)
            arg_types.append(arg.computed_type)

        try:
            token = node.tid
            obj_method = obj_type.get_method(node.id)
            node.obj_method = obj_method
            if len(node.args) == len(obj_method.param_types):
                for arg, param_type in zip(arg_types, obj_method.param_types):
                    real_types.append(param_type)
                    
                    if not arg.conforms_to(param_type):
                        self.errors.append((TypeError(INCOMPATIBLE_TYPES % (arg.name, param_type.name + f" in the argument #{idx} of {node.id}")), token))
                        error = True
            else:
                raise SemanticError(f'Method "{obj_method.name}" of "{obj_type.name}" only accepts {len(obj_method.param_types)} argument(s)')
            assert not error
            node_type = obj_method.return_type
            if node_type.name == ST:
                node_type = obj_type
        except AssertionError:
            node_type = ErrorType()
        except Exception as ex:
            self.errors.append((ex, token))
            node_type = ErrorType()

        node.info = [arg_types, real_types] 
        node.computed_type = node_type
    
    @visitor.when(cool.BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.computed_type
        
        self.visit(node.right, scope)
        right_type = node.right.computed_type
        node.info = [left_type, right_type]
        
        INT = self.context.get_type('Int')
        BOOL = self.context.get_type('Bool')
        if not (right_type.conforms_to(INT) and left_type.conforms_to(INT)):
            self.errors.append((TypeError(INVALID_OPERATION % (left_type.name, right_type.name)), node.symbol))
            
        node.computed_type = [BOOL, INT][isinstance(node, cool.ArithmeticNode)]
    
    @visitor.when(cool.IntegerNode)
    def visit(self, node, scope):
        node.computed_type = self.context.get_type('Int')
        
    @visitor.when(cool.StringNode)
    def visit(self, node, scope):
        node.computed_type = self.context.get_type('String')
        
    @visitor.when(cool.BoolNode)
    def visit(self, node, scope):
        node.computed_type = self.context.get_type('Bool')

    @visitor.when(cool.IdNode)
    def visit(self, node, scope):
        if scope.is_defined(node.lex):
            node_type = scope.find_variable(node.lex).type       
        else:
            scope.define_variable(node.lex, ErrorType())
            self.errors.append((NameError(VARIABLE_NOT_DEFINED % (node.lex)), node.token))
            node_type = ErrorType()
        
        node.computed_type = node_type

    @visitor.when(cool.NewNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
            if node.type == ST:
                node_type = SelfType(self.current_type)
        except TypeError as ex:
            self.errors.append((ex, node.ttype))
            node_type = ErrorType()
            
        node.computed_type = node_type

    @visitor.when(cool.IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.computed_type = self.context.get_type('Bool')

    @visitor.when(cool.ComplementNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        node.expr_type = expr_type

        INT = self.context.get_type('Int')
        if not expr_type.conforms_to(INT):
            self.errors.append((TypeError("Complement works only for Int"), node.symbol))
        node.computed_type = INT

    @visitor.when(cool.NotNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        node.expr_type = expr_type
    
        BOOL = self.context.get_type('Bool')
        if not expr_type.conforms_to(BOOL):
            self.errors.append((TypeError("Not operator works only for Bool"), node.symbol))
        node.computed_type = BOOL

    @visitor.when(cool.EqualNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.computed_type
        
        self.visit(node.right, scope)
        right_type = node.right.computed_type
        node.info = [left_type, right_type]
        
        valid_types = [IntType(), BoolType(), StringType()]
        try:
            cur_types = [right_type, left_type]
            for op_type in valid_types:
                try:
                    cur_types.remove(op_type)
                    assert cur_types[0].conforms_to(op_type)
                    break
                except ValueError: pass
        except AssertionError:
            self.errors.append((TypeError(INVALID_OPERATION % (left_type.name, right_type.name)), node.symbol))
            
        node.computed_type = self.context.get_type('Bool')
