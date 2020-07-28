from ..utils.visitors_definitions import TypeCheckVisitor
from ..utils.AST_definitions import NodeProgram


class semanticAnalyzer:
    def __init__(self, ast: NodeProgram):
        self.ast = ast
        self.typeChecker = TypeCheckVisitor()

    def run_visits(self : NodeProgram):
        self.programContext, self.programErrors = self.typeChecker.visit(self.ast)
        
