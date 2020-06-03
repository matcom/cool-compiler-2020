from .astNode import ASTNode

class ClassDeclarationNode(ASTNode):
    def __init__(self, idx, features, parent = None):
        self.id = idx
        self.parent = parent
        self.features = self._sort_features(features)

    def _sort_features(self, features):
        sort_f = []
        for f in features:
            if isinstance(f, AttrDeclarationNode):
                sort_f.insert(0, f)
            else:
                sort_f.append(f)
        return sort_f

class AttrDeclarationNode(ASTNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr

class FuncDeclarationNode(ASTNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body

class VarDeclarationNode(ASTNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr