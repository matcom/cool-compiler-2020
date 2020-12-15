from .astNode import ASTNode

class ClassDeclarationNode(ASTNode):
    def __init__(self, row, col, idx, features, parent = "Object"):
        super().__init__(row, col)
        self.id = idx
        self.parent = parent
        self.features = self._sort_features(features)
        self.parent_pos = (0, 0)

    def _sort_features(self, features):
        sort_f = []
        fmeth = []
        fattr = []
        for f in features:
            if isinstance(f, AttrDeclarationNode):
                fattr.append(f)
            else:
                fmeth.append(f)
        return fattr + fmeth

class AttrDeclarationNode(ASTNode):
    def __init__(self, row, col, idx, typex, expr=None):
        super().__init__(row, col)
        self.id = idx
        self.type = typex
        self.expr = expr
        self.type_pos = (0, 0)

class FuncDeclarationNode(ASTNode):
    def __init__(self, row, col, idx, params, return_type, body):
        super().__init__(row, col)
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
        self.type_pos = (0, 0)

class FormalParamNode(ASTNode):
    def __init__(self, row, col, idx, typex):
        super().__init__(row, col)
        self.id = idx
        self.type = typex
        self.type_pos = (0, 0)

class VarDeclarationNode(ASTNode):
    def __init__(self, row, col, idx, typex, expr=None):
        super().__init__(row, col)
        self.id = idx
        self.type = typex
        self.expr = expr