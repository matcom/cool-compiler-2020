import visitor
import ast_hierarchy 
import context


class TypeBuilderVisitor:
    def __init__(self, context):
        self.context = context
        self.current_type = None # type(current_type) = Type

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ast_hierarchy.ProgramNode)
    def visit(self, node, errors):
        for _class in node.classes:
            self.visit(_class, errors)

    @visitor.when(ast_hierarchy.ClassNode)
    def visit(self, node, errors):

        if node.typeName in ["Bool", "Int", "String", "Object"] :
            errors.append("SemanticError: Redefinition of basic class " + node.typeName + ". ")
            return

        if node.fatherTypeName is None:
            node.fatherTypeName = 'Object'

        elif node.fatherTypeName in ["Bool", "Int", "String"]:
            errors.append("SemanticError: Class " + node.typeName + " cannot inherit class " + node.fatherTypeName + "." )
            return

        if not self.context.Hierarchy.keys().__contains__(node.fatherTypeName):
            errors.append("Undefined class")
            return
        
        if node.fatherTypeName is None and node.typeName != 'Object':
            node.fatherTypeName = 'Object'

        node.fatherTypeName = self.context.Hierarchy[node.fatherTypeName]
        self.context.Hierarchy[node.typeName].Parent = node.fatherTypeName

        self.current_type = self.context.Hierarchy[node.typeName]

        for f in node.features:
            self.visit(f, errors)


    @visitor.when(ast_hierarchy.AttributeFeatureNode)
    def visit(self, node, errors):
        #attribute can be self type?
        if node.id == 'self':
            errors.append("SemanticError: 'self' cannot be the name of an attribute.")
            return
        if not self.context.Hierarchy.keys().__contains__(node.typeName):
            errors.append("TypeError: Class " + node.typeName + " of attribute " + node.id + " is undefined.")
            return
        # if not parent is None and parent.DefineInHierarchy(node.id):
        #     errors.append("SemanticError: Attribute x is an attribute of an inherited class.")
        #     return
        ans = self.current_type.DefineAttr(node.id, self.context.Hierarchy[node.typeName])
        
        if ans is None:
            errors.append("SemanticError: Attribute " + node.id + " is multiply redefined in class " + self.current_type.Name + ".")

    @visitor.when(ast_hierarchy.FunctionFeatureNode)
    def visit(self, node, errors):
        # return can be self type?
        if self.context.Hierarchy.keys().__contains__(node.typeName):
            argument_list = []
            for parameter in node.parameters:
                if parameter.id in argument_list or parameter.id == self:
                    errors.append("Sintactic error: Formal Parameter is multiply redefined")
                    pass
                argument_list.append(parameter.id)

            argument_types = []
            for parameter in node.parameters:
                param_name = parameter.id
                param_type = parameter.typeName
                if self.context.Hierarchy.keys().__contains__(param_type):
                    argument_types.append(param_type)
                else:
                    errors.append("TypeError")

            child_context = self.context.CreateChildContext() 
            
            ans = self.current_type.DefineMeth(node.id , argument_list, argument_types, node.typeName, None, child_context)
            if ans is None:
                errors.append("SemanticError: multiply defined methd")
        else:
            errors.append("return type missing")
