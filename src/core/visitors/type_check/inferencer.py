from .utils import *
from ...visitors import visitor
from .checker import TypeChecker
from ...cmp import CoolUtils as cool
from ...cmp.utils import InferenceSets
from ...cmp import SemanticError, AutoType, SelfType

# Type Inference Visitor
class InferenceVisitor(TypeChecker):
    def __init__(self, context, errors=[]):
        super().__init__(context, errors)
        self.variable = {}

    def inference(self, node, ntype, conforms=True):
        try:
            self.variable[node].add(ntype, conforms)
        except KeyError:
            self.variable[node] = InferenceSets().add(ntype, conforms)

    @visitor.on('node')
    def context_update(self, node, ntype):
        pass

    @visitor.when(cool.Node)
    def context_update(self, node, ntype):
        pass

    @visitor.when(cool.Param)
    def context_update(self, node, ntype):
        node.method_types[node.idx] = ntype
        try: node.method.param_types[node.idx] = ntype
        except AttributeError: pass
    
    @visitor.when(cool.AttrDeclarationNode)
    def context_update(self, node, ntype):
        try: node.attr_type = ntype
        except AttributeError: pass
        try: node.branch_type = ntype
        except AttributeError: pass
        try: node.attr.type = ntype
        except AttributeError: pass

    @visitor.when(cool.FuncDeclarationNode)
    def context_update(self, node, ntype):
        node.ret_type = ntype
        try: node.method.return_type = ntype
        except AttributeError: pass

    @visitor.on('node')
    def update(self, node, scope, ntype):
    	pass

    @visitor.when(cool.AssignNode)
    def update(self, node, scope, ntype):
        self.update(node.expr, scope, ntype)

    @visitor.when(cool.CaseOfNode)
    def update(self, node, scope, ntype):
        for branch in node.branches:
            if isinstance(branch.computed_type, AutoType):
                self.update(branch, scope, ntype)

    @visitor.when(cool.CaseExpressionNode)
    def update(self, node, scope, ntype):
        self.update(node.expr, node.scope, ntype)

    @visitor.when(cool.LetInNode)
    def update(self, node, scope, ntype):
        self.update(node.in_body, node.scope, ntype)

    @visitor.when(cool.IfThenElseNode)
    def update(self, node, scope, ntype):
        if isinstance(node.if_body.computed_type, AutoType):
            self.update(node.if_body, scope, ntype)
        if isinstance(node.else_body.computed_type, AutoType):
            self.update(node.else_body, scope, ntype)

    @visitor.when(cool.BlockNode)
    def update(self, node, scope, ntype):
        self.update(node.exprs[-1], scope, ntype)

    @visitor.when(cool.FunctionCallNode)
    def update(self, node, scope, ntype):
        self.inference(node.obj_method.ret_node, ntype)

    @visitor.when(cool.MemberCallNode)
    def update(self, node, scope, ntype):
        self.inference(node.obj_method.ret_node, ntype)

    @visitor.when(cool.IdNode)
    def update(self, node, scope, ntype):
        self.inference(scope.find_variable(node.lex).node, ntype)

    # Visit
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(cool.Node)
    def visit(self, node, scope):
        if not issubclass(node.__class__, cool.BinaryNode):
            super().visit(node, scope)

    @visitor.when(cool.ProgramNode)
    def visit(self, node, scope=None):
        scope = super().visit(node, scope) 

        infered = 0
        pending = []
        OBJ = self.context.get_type('Object')
        for (auto, sets) in self.variable.items():
            try:
                if (len(sets.D) + len(sets.S) == 1):
                    pending.append(auto)
                    continue
                ok, D1 = check_path(sets.D, OBJ)
                assert ok
                if len(sets.S) and not isinstance(D1, SelfType):
                    candidate = LCA(sets.S)
                    assert LCA([candidate, D1]) == D1
                    D1 = candidate
                auto.type = D1.name
                self.context_update(auto, D1)
                infered += 1
            except AssertionError:
                self.errors.append((SemanticError(f'Bad use of AUTO_TYPE detected'), auto.ttype))
        if not infered:
            for auto in pending:
                auto.type = OBJ.name
                self.context_update(auto, OBJ)
        self.variable.clear()
        return infered, scope
    
    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.attr_type, AutoType):
            self.inference(node, self.context.get_type('Object'))

        if not node.expr:
            return

        expr, rtype = node.info
        if update_condition(rtype, expr):
            self.inference(node, expr, False)
        if update_condition(expr, rtype):
            self.update(node.expr, scope, rtype)			

    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node, scope):
        super().visit(node, scope)   

        body, rtn = node.info
        OBJ = self.context.get_type('Object')
        if isinstance(rtn, AutoType):
            self.inference(node, OBJ)
        for ptype, pnode in zip(node.arg_types, node.arg_nodes):
            if isinstance(ptype, AutoType):
                self.inference(pnode, OBJ)
        if update_condition(rtn, body):
            self.inference(node, body, False)
        if update_condition(body, rtn):
            self.update(node.body, scope, rtn)
    
    @visitor.when(cool.AssignNode)
    def visit(self, node, scope):
        super().visit(node, scope)
        
        node_type, var = node.info
        if update_condition(var, node_type):
            self.inference(scope.find_variable(node.id).node, node_type, False)
        if update_condition(node_type, var):
            self.update(node.expr, scope, var)

    @visitor.when(cool.CaseExpressionNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.branch_type, AutoType):
            self.inference(node, self.context.get_type('Object'))

    @visitor.when(cool.LetAttributeNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.attr_type, AutoType):
            self.inference(node, self.context.get_type('Object'))

        if not node.expr:
            return

        expr, rtype = node.info
        if update_condition(rtype, expr):
            self.inference(scope.find_variable(node.id).node, expr, False)
        if update_condition(expr, rtype):
            self.update(node.expr, scope, rtype)			

    @visitor.when(cool.IfThenElseNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.cond_type, AutoType):
            self.update(node.condition, scope, OBJ = self.context.get_type('Bool'))
        
    @visitor.when(cool.WhileLoopNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.cond_type, AutoType):
            self.update(node.condition, scope, self.context.get_type('Bool'))
    
    @visitor.when(cool.FunctionCallNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        args, real = node.info
        if not real:
            return

        for idx, (atype, rtype) in enumerate(zip(args, real)):
            if update_condition(rtype, atype):
                self.inference(node.obj_method.nodes[idx], atype, False)
            if update_condition(atype, rtype):
                self.update(node.args[idx], scope, rtype)

    @visitor.when(cool.MemberCallNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        args, real = node.info
        if not real:
            return

        for idx, (atype, rtype) in enumerate(zip(args, real)):
            if update_condition(rtype, atype):
                self.inference(node.obj_method.nodes[idx], atype, False)
            if update_condition(atype, rtype):
                self.update(node.args[idx], scope, rtype)

    @visitor.when(cool.BinaryNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        left, right = node.info
        INT = self.context.get_type('Int')
        if isinstance(left, AutoType):
            self.update(node.left, scope, INT)
        if isinstance(right, AutoType):
            self.update(node.right, scope, INT)
        
    @visitor.when(cool.ComplementNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.expr_type, AutoType):
            self.update(node.expr, scope, self.context.get_type('Int'))

    @visitor.when(cool.NotNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.expr_type, AutoType):
            self.update(node.expr, scope, self.context.get_type('Bool'))
   
    @visitor.when(cool.EqualNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        left, right = node.info
        INT = self.context.get_type('Int')
        BOOL = self.context.get_type('Bool')
        STRING = self.context.get_type('String')
        if update_condition(left, right) and right in [INT, BOOL, STRING]:
            self.update(node.left, scope, right)
        if update_condition(right, left) and left in [INT, BOOL, STRING]:
            self.update(node.right, scope, left)
    