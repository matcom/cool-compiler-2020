import cil.baseCilVisitor as baseCilVisitor
import typecheck.visitor as visitor
import abstract.tree as coolAst
import cil.nodes as cil


class CoolToCILVisitor(baseCilVisitor.BaseCoolToCilVisitor):
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(coolAst.ProgramNode)
    def visit(self, node, scope):
        # node.class_list -> [ClassDef ...]

        # Define the entry point for the program.
        self.current_function = self.register_function("entry")
        instance = self.define_internal_local()
        result = self.define_internal_local()

        # The first method to call need to be the method main in a Main Class

        # allocate memory for the main object
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))

        # call the main method
        self.register_instruction(
            cil.StaticCallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None

        for klass, child_scope in zip(node.class_list, scope.children):
            self.visit(klass, child_scope)

        return cil.CilProgramNode(self.dot_types, self.dot_data, self.dot_code)

    @visitor.when(coolAst.ClassDef)
    def visit(self, node, scope):
        # node.idx -> String with the Class Name
        # node.features -> [AttributeDef ... MethodDef ...] List with attributes and method declarations

        # Register the new type in .Types section
        self.current_type = self.context.get_type(node.idx)
        new_type_node = self.register_type(node.idx)

        methods = (feature.idx for feature in node.feature
                   if isinstance(feature, coolAst.MethodDef))
        attributes = (feature for feature in node.feature
                      if isinstance(feature, coolAst.AttributeDef))

        # Handle inherited features such as attributes and methods first
        if self.current_type.parent is not None:
            for attribute in self.current_type.parent.attributes:
                new_type_node.attributes.append(attribute.name)

            for method in self.current_type.parent.methods.keys():
                # Handle methods overload
                if method not in methods:
                    new_type_node.methods.append(
                        (method,
                         self.to_function_name(method,
                                               self.current_type.parent.name)))

        # Register every attribute and method for this type
        # so the .Type section must look like:
        #####################################################################
        # .TYPES                                                            #
        # type A {                                                          #
        #      attribute x;                                                 #
        #      method f : function_f_at_A;                                  #
        # }                                                                 #
        #####################################################################
        for attribute in attributes:
            new_type_node.attributes.append(attribute.idx)
        for method in methods:
            new_type_node.methods.append(
                (method.idx, self.to_function_name(method.idx, node.idx)))

        # TODO: It is necessary to visit attributes?? Think so cuz they can be initialized
        # and their value could perhaps go to .DATA section

        # Visit every method for generate its code in the .CODE section
        for feature, child_scope in zip(methods, scope.children):
            self.visit(feature, child_scope)

        self.current_type = None

    @visitor.when(coolAst.MethodDef)
    def visit(self, node, scope):
        # node.idx -> String with the method name
        # node.param_list -> [Param ... ] params of the method
        # node.return_type -> Type: method's return type
        # node.statements -> ExpressionList with the body of the method

        self.current_method = self.current_type.get_method(node.idx)

        # Register the new function in .CODE
        function_node = self.register_function(
            self.to_function_name(node.idx, self.current_type.name))

        # Define the method params
        function_node.params = [
            cil.ParamNode(param.idx) for param in node.param_list
        ]

        # Get the instructions that conforms the body of the method
        for exp, child_scope in zip(node.statements, scope.children):
            # every exp return a tuple: the instruction set and the localvars
            # needed
            instructions, local_vars = self.visit(exp, child_scope)
            function_node.instructions += instructions
            function_node.localvars += local_vars

        self.current_method = None
