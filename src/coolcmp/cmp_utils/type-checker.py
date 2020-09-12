from coolcmp.cmp_utils.visitor import Visitor

class TypeChecker(Visitor):
    def __init__(self, root):
        self.root = root
        self.cls_refs = {}
        self._t = 0
        self._dfs(root)

    def _dfs(self, u):
        self._t += 1
        
        u.td = self._t
        self.cls_refs[u.type.value] = u

        for v in u.children:
            v.parent = u
            v.level = u.level + 1
            self._dfs(v)
        
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

    