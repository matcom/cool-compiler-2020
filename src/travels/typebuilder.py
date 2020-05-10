import typecheck.visitor as visitor
from abstract.tree import *
from abstract.semantics import SemanticError, Type, VoidType, IntegerType, StringType, ObjectType, Attribute, Method, Context, BoolType

class TypeBuilder:
    def __init__(self, context: Context, errors = []):
        self.context = context
        self.errors = errors
        self.current_type = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node):
        for class_ in node.class_list:
            self.visit(class_)

    @visitor.when(ClassDef)
    def visit(self, node: ClassDef):
        self.current_type = self.context.get_type(node.idx)
        parent = self.context.get_type(node.parent)

        #Detectar dependencias circulares
        if parent.conforms_to(self.current_type):
            self.errors.append(f'Circular dependency: class {self.current_type.name} cannot inherit from {parent.name}')
        else:
            self.current_type.set_parent(parent)

            # for method in parent.methods.values():
            #     try:
            #         self.current_type.define_method(method.name, method.param_names, method.param_types, method.return_type)
            #     except SemanticError as e:
            #         self.errors.append(e.text)

            # for att in parent.attributes:
            #     try:
            #         self.current_type.define_attribute(att.name, att.type)
            #     except SemanticError as e:
            #         self.errors.append(e.text)

            for feature in node.features:
                self.visit(feature)


    @visitor.when(AttributeDef)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.typex) if isinstance(node.typex, str) else node.typex
            self.current_type.define_attribute(node.idx, attr_type)
        except SemanticError as e:
            self.errors.append(e.text)

    @visitor.when(MethodDef)
    def visit(self, node):
        params = [param.id for param in node.param_list]
        try:
            params_type = [self.context.get_type(param.type) if isinstance(param.type, str) else param.type \
                for param in node.param_list]
            try:
                return_type = self.context.get_type(node.return_type) if isinstance(node.return_type,str) else node.return_type
                try:
                    self.current_type.define_method(node.idx,params, params_type,return_type)
                except SemanticError as e:
                    self.errors.append(e.text)
            
            except SemanticError as e:
                self.errors.append(e.text)

        except SemanticError as e:
            self. errors.append(e.text)
        


