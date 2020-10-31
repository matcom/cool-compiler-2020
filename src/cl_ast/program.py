from .astNode import ASTNode

class ProgramNode(ASTNode):
    def __init__(self, row, col, declarations):
        super().__init__(row, col)
        self.declarations = declarations
    
