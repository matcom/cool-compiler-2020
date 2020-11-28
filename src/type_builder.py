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
    def visit(self, node):
        for _class in node.classes:
            self.visit(_class)

    @visitor.when(ast_hierarchy.ClassNode)
    def visit(self, node):
        self.current_type = self.context.GetType(node.typeName)

        parent_type = self.context.GetType(node.parent)
        if parent_type is None and node.name != "Object":
            #errors.throw_error(errors.TypeError(text=f"In class '{self.current_type.name}' parent type '{node.parent}' is missing.", line=node.line, column=node.column))
            pass
        if parent_type.name in ['Int', 'String', 'Bool']:
            #errors.throw_error(errors.SemanticError(text=f"In class '{self.current_type.name}' it is an error to inherit from basic class '{node.parent}'.", line=node.line, column=node.column))
            pass 
        for f in node.features:
            self.visit(f)


    @visitor.when(ast_hierarchy.AttributeFeatureNode)
    def visit(self, node):
        #attribute can be self type?
        attribute_type = self.context.GetType(node.typeName)
        if attribute_type is None:
            #error
            pass 
        ans = self.current_type.DefineAttr(node.id, node.typeName)
        if ans is None:
            #error
            pass

    @visitor.when(ast_hierarchy.FunctionFeatureNode)
    def visit(self, node):
        # return can be self type?
        return_type = self.context.get_type(node.return_type_method)
        if return_type is not None:
            argument_list = []
            for parameter in node.parameters:
                if parameter.name in argument_list:
                    #error
                    pass
                argument_list.append(parameter.name)

            argument_types = []
            for parameter in node.parameters:
                (param_name, param_type) = parameter
                _type = self.context.GetType(param_name)
                if _type is not None:
                    argument_types.append(parameter.type_parameter)
                else:
                    pass
                    #errors.throw_error(errors.TypeError(text=f"The type of the parameter '{parameter.name}' in method '{node.name}' is missing.", line=node.line, column=node.column))
                    
            ans = self.current_type.DefineMeth(node.name , argument_list, argument_types, node.return_type_method)
            if not ans:
                pass
                #errors.throw_error(errors.SemanticError(text=f"In class '{self.current_type.name}' method '{node.name}' is defined multiple times.", line=node.line, column=node.column))             
        else:
            pass
            #errors.throw_error(errors.TypeError(text=f"In class '{self.current_type.name}' return type of method '{node.name}' is missing.", line=node.line, column=node.column))

