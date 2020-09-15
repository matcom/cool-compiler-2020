from coolcmp.cmp_utils.errors import *
from coolcmp.cmp_utils.environment import Environment
from coolcmp.cmp_utils.my_ast import Id, Type, Attribute, Class, SELF_TYPE
from coolcmp.cmp_utils.utils import init_logger

class TypeChecker:
    def __init__(self, root, cls_refs):
        self.logger = init_logger('TypeChecker')

        self.root = root
        self.cls_refs = cls_refs
        self._t = 0
        self._dfs(root, Environment())

        self.cur_env = None
        self.cur_cls = None

    def _dfs(self, u, env):
        self._t += 1
        u.td = self._t

        for name, ref in u.methods.items():
            old = env.get(name)

            if old and old.get_signature() != ref.get_signature():
                raise SemanticError(ref.id.line, ref.id.col, f'{ref} of {u} is not compatible to {old} for inheritance')

            env.define(name, ref)

            for formal in ref.formal_list:
                if formal.type.value == 'SELF_TYPE':
                    raise SemanticError(formal.type.line, formal.type.col, f'Tried to declare a formal with {formal.type}')

                formal.set_static_type(self._get_correct_type(formal, u.self_type))  #precalculate static type of formals before doing visitor

        for v in u.children:
            v.parent = u
            v.level = u.level + 1

            self._dfs(v, Environment(env))
        
        u.tf = self._t

        self.logger.debug(f'{u}, td={u.td}, tf={u.tf}, level={u.level}, parent={u.parent}')

    def _conforms(self, u, v):  #Does u conforms with v?
        return v.td <= u.td <= v.tf

    def _lca(self, u, v):
        self.logger.debug(f'LCA query between {u} and {v}')

        while u.type.value != v.type.value:
            if u.level > v.level:
                u = u.parent

            else: v = v.parent

        self.logger.debug(f'LCA is: {u}')

        return u

    def _dispatch(self, u, name):
        while u and name not in u.methods:
            u = u.parent

        return u.methods[name] if u else None

    def _get_correct_type(self, node, default_type):
        if node.type.value == 'SELF_TYPE':
            return default_type

        if node.type.value not in self.cls_refs:
            raise SemanticError(node.type.line, node.type.col, f'{Class(node.type)} doesnt exists')

        return self.cls_refs[node.type.value]

    def visit(self, node):
        self.logger.debug(f'On {node}')

        fn = getattr(self, 'visit_' + node.__class__.__name__)
        res = fn(node)

        if hasattr(node, 'static_type'):
            self.logger.debug(f'{node}, static_type: {node.static_type}')

        return res

    def visit_Class(self, node):
        old_env = self.cur_env
        self.cur_env = Environment(old_env)

        old_cls = self.cur_cls
        self.cur_cls = node

        self.cur_env.define('self', Attribute(Id('self'), Type('SELF_TYPE'), None))

        self.logger.info(f'{node} Created new environment with self')

        for feature in node.feature_list:
            if isinstance(feature, Attribute):
                if self.cur_env.get(feature.id.value):
                    raise SemanticError(feature.id.line, feature.id.col, f'Tried to redefine {feature} by inheritance')

                self.cur_env.define(feature.id.value, feature)
                self.logger.info(f'{node} defined {feature}')

        for feature in node.feature_list:
            self.visit(feature)
            
        for cls in node.children:
            self.visit(cls)

        self.cur_env = old_env
        self.cur_cls = old_cls

        self.logger.info(f'{node} Restoring previous environment')

    def visit_SELF_TYPE(self, node): pass  #For SELF_TYPE(C) classes, for consistency

    def visit_Formal(self, node):
        if node.id.value == 'self':
            raise SemanticError(node.id.line, node.id.col, f'Tried to assign to {node.id}')

        if node.id.value in self.cur_env.map:  #check that is not defined on current env only!
            raise SemanticError(node.id.line, node.id.col, f'Tried to redefine {node}')

        self.cur_env.define(node.id.value, node)

        self.visit(node.id)
        node.set_static_type(node.id.static_type)

    def visit_Method(self, node):
        old_env = self.cur_env
        self.cur_env = Environment(old_env)

        for formal in node.formal_list:
            self.visit(formal)

        self.visit(node.expr)

        _static_type = self._get_correct_type(node, self.cur_cls.self_type)

        self.logger.debug(f'{node} static type: {_static_type}')

        if not self._conforms(node.expr.static_type, _static_type):
            raise TypeError(node.expr.line, node.expr.col, f'{node.expr} with {node.expr.static_type} doesnt conform to {node} with {_static_type}')

        self.cur_env = old_env

    def visit_Attribute(self, node):
        self.visit(node.id)
        node.set_static_type(node.id.static_type)

        if node.opt_expr_init:
            self.logger.info(f'{node} has expr')

            expr = node.opt_expr_init
            self.visit(expr)

            if not self._conforms(expr.static_type, node.static_type):
                raise TypeError(expr.line, expr.col, f'{expr} with {expr.static_type} doesnt conform to {node} with {node.static_type}')

    def visit_Dispatch(self, node):
        for expr in node.expr_list:
            self.visit(expr)

        self.visit(node.expr)
        cls = None

        if node.opt_type:  #static dispatch
            if node.opt_type.value == 'SELF_TYPE':
                raise SemanticError(node.opt_type.line, node.opt_type.col, f'Cant perform static dispatch on {node.opt_type}')

            if node.opt_type.value not in self.cls_refs:
                raise SemanticError(node.opt_type.line, node.opt_type.col, f'{Class(node.opt_type, None)} doesnt exists')

            cls = self.cls_refs[node.opt_type.value]

            if not self._conforms(node.expr.static_type, cls):
                raise SemanticError(node.line, node.col, f'Dispatch failed, {node.expr} with {node.expr.static_type} doenst conform to {cls}')

        else:
            cls = node.expr.static_type

            #Assert that static type of node.expr is one of the nodes of the tree and NEVER a declared SELF_TYPE
            #It can be SELF_TYPE(C) though
            assert node.expr.static_type.td > 0

            if isinstance(node.expr.static_type, SELF_TYPE):
                cls = self.cur_cls

        self.logger.debug(f'{node}: finding method {node.id} on class {cls} or some ancestor')

        method = self._dispatch(cls, node.id.value)

        if not method:
            raise AttributeError(node.line, node.col, f'Dispatch failed: couldnt find a method with {node.id} in {cls} or any ancestor')
        
        self.logger.debug(f'{node}, found {method}')

        formals = list(method.formal_list)

        if len(node.expr_list) != len(formals):
            raise SemanticError(node.line, node.col, (f'Dispatch failed, number of arguments of dispatch is {len(node.expr_list)}, '
                                                        f'number of formals is {len(formals)}'))

        for expr, formal in zip(node.expr_list, formals):
            self.logger.debug(f'Checking conformance of {expr} and {formal}')

            if not self._conforms(expr.static_type, formal.static_type):
                raise TypeError(expr.line, expr.col, f'{expr} with {expr.static_type} doesnt conform to {formal} with {formal.static_type}')

        node.set_static_type(self._get_correct_type(method, node.expr.static_type))

    def visit_Assignment(self, node):
        if node.id.value == 'self':
            raise SemanticError(node.id.line, node.id.col, f'Tried to assign to {node.id}')

        self.visit(node.id)
        self.visit(node.expr)

        if not self._conforms(node.expr.static_type, node.id.static_type):
            raise TypeError(node.expr.line, node.expr.col, f'{node.expr} with {node.expr.static_type} doesnt conform to {node.id} with {node.id.static_type}')

        node.set_static_type(node.expr.static_type)

    def visit_Block(self, node):
        for expr in node.expr_list:
            self.visit(expr)

        node.set_static_type(node.expr_list[-1].static_type)

    def visit_New(self, node):
        node.set_static_type(self._get_correct_type(node, self.cur_cls.self_type))

    def visit_If(self, node):
        self.visit(node.predicate)

        _static_type = node.predicate.static_type

        if _static_type.type.value != 'Bool':
            raise TypeError(node.predicate.line, node.predicate.col, f'{node} predicate must have {self.cls_refs["Bool"]}, not {_static_type}')

        self.visit(node.if_branch)
        self.visit(node.else_branch)

        node.set_static_type(self._lca(node.if_branch.static_type, node.else_branch.static_type))

    def visit_Plus(self, node):
        self.visit(node.left)
        self.visit(node.right)

        if node.left.static_type.type.value != 'Int' or node.right.static_type.type.value != 'Int':
            raise TypeError(node.line, node.col, f'{node.left} and {node.right} must both have {self.cls_refs["Int"]}')

        node.set_static_type(self.cls_refs['Int'])

    def visit_Minus(self, node):
        self.visit_Plus(node)
    
    def visit_Mult(self, node):
        self.visit_Plus(node)
    
    def visit_Div(self, node):
        self.visit_Plus(node)

    def visit_Eq(self, node):
        self.visit(node.left)
        self.visit(node.right)

        types = ['Int', 'String', 'Bool']

        lft_type = node.left.static_type.type.value
        rgt_type = node.right.static_type.type.value

        if lft_type in types or rgt_type in types:
            if lft_type != rgt_type:
                raise TypeError(node.line, node.col, f'{node.left} with {node.left.static_type} and {node.right} with {node.right.static_type} must both have the same type')

        node.set_static_type(self.cls_refs['Bool'])

    def visit_Less(self, node):
        self.visit(node.left)
        self.visit(node.right)

        if node.left.static_type.type.value != 'Int' or node.right.static_type.type.value != 'Int':
            raise TypeError(node.line, node.col, f'{node.left} and {node.right} must both have {self.cls_refs["Int"]}')

        node.set_static_type(self.cls_refs['Bool'])

    def visit_LessEq(self, node):
        self.visit_Less(node)

    def visit_IntComp(self, node):
        self.visit(node.expr)

        if node.expr.static_type.type.value != 'Int':
            raise TypeError(node.line, node.col, f'{node.expr} must have {self.cls_refs["Int"]}')

        node.set_static_type(self.cls_refs['Int'])

    def visit_Not(self, node):
        self.visit(node.expr)

        if node.expr.static_type.type.value != 'Bool':
            raise TypeError(node.line, node.col, f'{node.expr} must have {self.cls_refs["Bool"]}')

        node.set_static_type(self.cls_refs['Bool'])

    def visit_IsVoid(self, node):
        node.set_static_type(self.cls_refs['Bool'])

    def visit_Id(self, node):
        ref = self.cur_env.get(node.value)

        if not ref:
            raise NameError(node.line, node.col, f'{node} doesnt exists in this environment')

        self.logger.info(f'{node}, asked for reference, got {ref} with declared type : {ref.type}')

        node.set_static_type(self._get_correct_type(ref, self.cur_cls.self_type))

    def visit_Int(self, node):
        node.set_static_type(self.cls_refs['Int'])

    def visit_Bool(self, node):
        node.set_static_type(self.cls_refs['Bool'])

    def visit_String(self, node):
        node.set_static_type(self.cls_refs['String'])