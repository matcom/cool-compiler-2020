from .type_builder import TypeBuilderVisitor 
from .type_checker import TypeCheckerVisitor
from .type_inheritance import TypeInheritanceVisitor
from .type_collector import TypeCollectorVisitor
from .AST_definitions import NodeProgram
from .context import programContext, Attribute



class semanticAnalyzer:
    def __init__(self, ast: NodeProgram,
                 programContext):
        self.ast = ast
        self.errors = []
        self.programContext= programContext

    def run_visits(self: NodeProgram):
        typeCollectorResult= TypeCollectorVisitor(self.programContext).visit(self.ast)
        if typeCollectorResult:
            self.errors += typeCollectorResult
            return
        typeBuilderResult= TypeBuilderVisitor(self.programContext).visit(self.ast)
        if typeBuilderResult:
            self.errors += typeBuilderResult
            return 
        typeInheritanceResult= TypeInheritanceVisitor(self.programContext).visit(self.ast)
        if typeInheritanceResult:
            self.errors += typeInheritanceResult
            return 
        typeCheckerResult, mapExprWithResult= TypeCheckerVisitor(self.programContext).visit(self.ast)
        if typeCheckerResult:
            self.errors += typeCheckerResult
            return
        
        self.mapExprWithResult = mapExprWithResult