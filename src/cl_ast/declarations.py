from .astNode import ASTNode

class ClassDeclarationNode(ASTNode):
    def __init__(self,idx,features,parent = None):
        self.id = idx
        self.parent = parent
        self.features = features

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