import visitor
import ast_hierarchy
import context


class TypeCollectorVisitor:
    def __init__(self):
        self.Context = None
        self.BasicClasses = ["Object", "IO", "Int", "String", "Bool"]

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ast_hierarchy.ProgramNode)
    def visit(self, node, errors):
        self.Context = context.Context(None)

        for _class in node.classes:
            self.visit(_class, errors)

    @visitor.when(ast_hierarchy.ClassNode)
    def visit(self, node, errors):
        if self.Context.Hierarchy.keys().__contains__(node.typeName):
            errors.append("SemanticError: Redefinition of basic class " + node.typeName + ". ") 
        else: 
            self.Context.Hierarchy[node.typeName] = self.Context.DefineType(node.typeName, node.fatherTypeName)
        