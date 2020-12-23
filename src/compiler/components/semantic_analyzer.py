from ..utils.visitors_definitions import TypeCollectorVisitor, TypeBuilderVisitor, TypeInheritanceVisitor, TypeCheckerVisitor
from ..utils.AST_definitions import NodeProgram
from ..utils.context import programContext


class semanticAnalyzer:
    def __init__(self, ast: NodeProgram):
        self.ast = ast
        self.errors = []

    def run_visits(self: NodeProgram):
        typeCollectorResult= TypeCollectorVisitor().visit(self.ast)
        if typeCollectorResult:
            self.errors += typeCollectorResult
            return
        typeBuilderResult= TypeBuilderVisitor().visit(self.ast)
        if typeBuilderResult:
            self.errors += typeBuilderResult
            return 
        typeInheritanceResult= TypeInheritanceVisitor().visit(self.ast)
        if typeInheritanceResult:
            self.errors += typeInheritanceResult
            return 
        typeCheckerResult= TypeCheckerVisitor().visit(self.ast)
        if typeCheckerResult:
            self.errors += typeCheckerResult
            return
        
        
