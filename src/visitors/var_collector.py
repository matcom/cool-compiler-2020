from semantic import *
from tools.cmp_errors import * 

import visitors.visitor as visitor
from pipeline import State
from cl_ast import *

class VarCollector(State):
    def __init__(self, name):
        super().__init__(name)
        self.context = None
        self.current_type = None
        self.current_method = None 

    def run(self, inputx):
        ast, context = inputx
        self.context = context
        scope = self.visit(ast)
        return ast, context, scope

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope(context=self.context)
        for dec in node.declarations:
            self.visit(dec, scope.cls_scopes[dec.id])
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        
        # visit features
        for feature in node.features:
            self.visit(feature, scope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        ascope = scope.attr_scopes[node.id]
        self.current_method = self.current_type.get_attribute(node.id)
        self.visit(node.expr, ascope)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)
        func_scope = scope.func_scopes[node.id]

        for param in node.params:
            try:
                if param.id == 'self':
                    raise ScopeError(FORMAL_ERROR_SELF)
                func_scope.define_variable(param.id, self.context.get_type(param.type))
            except ScopeError as e:
                self.errors.append(CSemanticError(param.row, param.col, e.text))

        self.visit(node.body, func_scope)        

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        if scope.is_defined(node.id) and scope.find_variable(node.id).type is not ErrorType():
            self.errors.append(CSemanticError(node.row, node.col, LOCAL_ALREADY_DEFINED %(node.id, self.current_method.name)))

        else:
            try:
                vtype = self.context.get_type(node.type)
                scope.define_variable(node.id, vtype)
            except ScopeError as e:
                scope.define_variable(node.id, ErrorType())
                self.errors.append(CSemanticError(node.row, node.col, e.text))

            if node.expr is not None:
                self.visit(node.expr, scope)

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        vinfo = scope.find_variable(node.id)
        if vinfo.name == 'self':
            self.errors.append(CSemanticError(node.row, node.col, SELF_IS_READONLY))            

        if vinfo is None:
            self.errors.append(CNameError(node.row, node.col, VARIABLE_NOT_DEFINED %(node.id, self.current_method.name)))
            scope.define_variable(node.id, ErrorType())

        self.visit(node.expr, scope)

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.expr_list:
            self.visit(expr, scope)

    @visitor.when(LetNode)
    def visit(self, node, scope):
        new_scope = scope.create_child()
        scope.expr_dict[node] = new_scope

        iscope = new_scope

        for init in node.init_list:
            self.visit(init, iscope)
            iscope = iscope.create_child()

        self.visit(node.expr, iscope)

    @visitor.when(LetDeclarationNode)
    def visit(self, node, scope):
        try:
            vtype = self.context.get_type(node.type)
            scope.redefine_variable(node.id, vtype)
        except ScopeError as e:
            self.errors.append(CSemanticError(node.type_pos[0], node.type_pos[1], e.text))

        if node.expr is not None:
            self.visit(node.expr, scope)

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        if not scope.is_defined(node.id):
            self.errors.append(CNameError(node.row, node.col, VARIABLE_NOT_DEFINED %(node.id, self.current_method.name)))
            scope.define_variable(node.id, ErrorType())

    @visitor.when(CaseNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)

        new_scope = scope.create_child()
        scope.expr_dict[node] = new_scope

        for case in node.case_list:
            self.visit(case, new_scope.create_child())

    @visitor.when(OptionNode)
    def visit(self, node, scope):
        typex = self.context.get_type(node.typex)
        
        self.visit(node.expr, scope)
        scope.define_variable(node.id, typex)

    @visitor.when(BinaryOperationNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
    
    @visitor.when(UnaryOperationNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        self.visit(node.cond, scope)
        self.visit(node.expr, scope)

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        self.visit(node.cond, scope)
        self.visit(node.stm, scope)
        self.visit(node.else_stm, scope)
    
    @visitor.when(ExprCallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope)

        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(ParentCallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope)

        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(SelfCallNode)
    def visit(self, node, scope):
        for arg in node.args:
            self.visit(arg, scope)