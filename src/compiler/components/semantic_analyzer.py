from ..utils.visitors_definitions import TypeCollectorVisitor, TypeBuilderVisitor, TypeInheritanceVisitor, TypeCheckerVisitor
from ..utils.AST_definitions import NodeProgram
from ..utils.context import programContext


class semanticAnalyzer:
    def __init__(self, ast: NodeProgram):
        self.ast = ast
        self.errors = []

    def run_visits(self: NodeProgram):
        typeCollectorResult= TypeCollectorVisitor().visit(self.ast)
        typeInheritanceResult= TypeInheritanceVisitor().visit(self.ast)
        typeBuilderResult= TypeBuilderVisitor().visit(self.ast)
        typeCheckerResult= TypeCheckerVisitor().visit(self.ast)
        self.errors+= typeCollectorResult + typeBuilderResult + typeInheritanceResult + typeCheckerResult
