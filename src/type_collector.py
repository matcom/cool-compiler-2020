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
    def visit(self, node):
        self.Context = context.Context(None)

        for _class in node.classes:
            self.visit(_class)

    @visitor.when(ast_hierarchy.ClassNode)
    def visit(self, node):
        ans = self.Context.DefineType(node.typeName, node.fatherTypeName)
        if ans is None:
            #lanzar error   
            pass         

