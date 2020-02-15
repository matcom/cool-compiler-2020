from .astNode import ASTNode

class ProgramNode(ASTNode):
    def __init__(self, declarations):
        self.declarations = declarations
    
