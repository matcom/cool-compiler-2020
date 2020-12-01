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
        if node.fatherTypeName is None:
            node.fatherTypeName = self.Context.GetType("Object")
        else:
            node.fatherTypeName = self.Context.GetType(node.fatherTypeName)
        ans = self.Context.DefineType(node.typeName, node.fatherTypeName)
        if ans is None:
            #modificar este error
            errors.append("Error en la creación de la clase ")
            pass         

