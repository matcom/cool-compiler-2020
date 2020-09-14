from coolcmp.cmp_utils.errors import *
from coolcmp.cmp_utils.environment import Environment
from coolcmp.cmp_utils.my_ast import Id, Type, Attribute, Class
from coolcmp.cmp_utils.utils import init_logger

class TypeChecker:
    def __init__(self, root, cls_refs):
        self.logger = init_logger('TypeChecker')

        self.root = root
        self.cls_refs = cls_refs
        self._t = 0
        self._dfs(root, Environment())

        self.cur_env = Environment()
        self.cur_cls = self.cls_refs['Object']

    def _dfs(self, u, env):
        self._t += 1
        u.td = self._t

        for name, ref in u.methods.items():
            old = env.get(name)

            if old and old.get_signature() != ref.get_signature():
                raise SemanticError(ref.id.line, ref.id.col, f'{ref} of {u} is not compatible to {old} for inheritance')

            env.define(name, ref)

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

        _static_type = self.cur_cls if node.type.value == 'SELF_TYPE' else self.cls_refs[node.type.value]

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

    def visit_Assignment(self, node):
        if node.id.value == 'self':
            raise SemanticError(node.id.line, node.id.col, f'Tried to assign to {node.id}')

        self.visit(node.id)
        self.visit(node.expr)

        if not self._conforms(node.expr.static_type, node.id.static_type):
            raise TypeError(node.expr.line, node.expr.col, f'{node.expr} with {node.expr.static_type} doesnt conform to {node.id} with {node.id.static_type}')

        node.set_static_type(node.expr.static_type)

    def visit_Id(self, node):
        ref = self.cur_env.get(node.value)

        if not ref:
            raise NameError(node.line, node.col, f'{node} doesnt exists in this environment')

        self.logger.info(f'{node}, asked for reference, got {ref} with declared type : {ref.type}')
        
        if ref.type.value not in self.cls_refs:
            raise SemanticError(ref.type.line, ref.type.col, f'{Class(ref.type, None)} doesnt exists')

        if ref.type.value == 'SELF_TYPE':
            node.set_static_type(self.cur_cls)

        else: node.set_static_type(self.cls_refs[ref.type.value])

    def visit_Int(self, node):
        node.set_static_type(self.cls_refs['Int'])

    def visit_Bool(self, node):
        node.set_static_type(self.cls_refs['Bool'])

    def visit_String(self, node):
        node.set_static_type(self.cls_refs['String'])