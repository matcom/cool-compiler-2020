from coolcmp.cmp_utils.visitor import Visitor
from coolcmp.cmp_utils.errors import *
from coolcmp.cmp_utils.environment import Environment

class TypeChecker(Visitor):
    def __init__(self, root, cls_refs):
        self.root = root
        self.cls_refs = cls_refs
        self._t = 0
        self._dfs(root, Environment())

    def _dfs(self, u, env):
        self._t += 1
        u.td = self._t

        for name, ref in u.methods.items():
            old = env.get(name)

            if old and old.get_signature() != ref.get_signature():
                raise SemanticError(ref.id.line, ref.id.col, (
                        f'The signature of method "{ref.id.value}" in class "{u.type.value}" is '
                        f'different from signature of inherited method "{old.id.value}". '
                        f'Expected {old.get_signature()}, found {ref.get_signature()}'))

            env.define(name, ref)

        for v in u.children:
            v.parent = u
            v.level = u.level + 1

            self._dfs(v, Environment(env))
        
        u.tf = self._t

    def _conforms(self, u, v):  #Does u conforms with v?
        return v.td <= u.td <= v.tf

    def _lca(self, u, v):
        while u.type.value != v.type.value:
            if u.level > v.level:
                u = u.parent

            else: v = v.parent

        return u

    def visit_Int(self, node):
        node.set_static_type(self.cls_refs['Int'])

    def visit_Bool(self, node):
        node.set_static_type(self.cls_refs['Bool'])

    def visit_String(self, node):
        node.set_static_type(self.cls_refs['String'])