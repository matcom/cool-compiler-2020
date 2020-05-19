import cil.baseCilVisitor as baseCilVisitor
import typecheck.visitor as visitor
import abstract.tree as coolAst
import abstract.semantics as semantics
import cil.nodes as cil
from typing import List, Tuple

ExpressionReturn = Tuple[List[cil.InstructionNode], List[cil.LocalNode]]
Scope = semantics.Scope


class CoolToCILVisitor(baseCilVisitor.BaseCoolToCilVisitor):
    @visitor.on("node")
    def visit(self, node: coolAst.Node) -> None:
        pass

    @visitor.when(coolAst.ProgramNode)  # type: ignore
    def visit(self, node: coolAst.ProgramNode, scope: Scope, local_vm_holder: str = '') -> cil.CilProgramNode:  # noqa: F811
        # node.class_list -> [ClassDef ...]

        # Define the entry point for the program.
        self.current_function: cil.FunctionNode = self.register_function("entry")
        instance = self.define_internal_local()
        result = self.define_internal_local()

        # The first method to call need to be the method main in a Main Class

        # allocate memory for the main object
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))

        # call the main method
        self.register_instruction(cil.StaticCallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None

        for klass, child_scope in zip(node.class_list, scope.children):
            self.visit(klass, child_scope)

        return cil.CilProgramNode(self.dot_types, self.dot_data, self.dot_code)

    @visitor.when(coolAst.ClassDef)  # type: ignore
    def visit(self, node: coolAst.ClassDef, scope: Scope) -> None:  # noqa: F811
        # node.idx -> String with the Class Name
        # node.features -> [AttributeDef ... MethodDef ...] List with attributes and method declarations

        # Register the new type in .Types section
        self.current_type = self.context.get_type(node.idx)
        new_type_node = self.register_type(node.idx)

        methods: List[str] = [feature.idx for feature in node.feature if isinstance(feature, coolAst.MethodDef)]
        attributes: List[semantics.Attribute] = [feature for feature in node.feature if isinstance(feature, coolAst.AttributeDef)]

        # Handle inherited features such as attributes and methods first
        if self.current_type.parent is not None:
            for attribute in self.current_type.parent.attributes:
                new_type_node.attributes.append(attribute.name)

            for method in self.current_type.parent.methods.keys():
                # Handle methods overload
                if method not in methods:
                    new_type_node.methods.append((method, self.to_function_name(method, self.current_type.parent.name)))

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
            new_type_node.methods.append((method.idx, self.to_function_name(method.idx, node.idx)))

        # TODO: It is necessary to visit attributes?? Think so cuz they can be initialized
        # and their value could perhaps go to .DATA section

        # Visit every method for generate its code in the .CODE section
        for feature, child_scope in zip(methods, scope.children):
            self.visit(feature, child_scope)

        self.current_type = None

    @visitor.when(coolAst.MethodDef)  # type: ignore
    def visit(self, node: coolAst.MethodDef, scope: Scope) -> None:  # noqa: F811
        self.current_method = self.current_type.get_method(node.idx)

        # Register the new function in .CODE
        function_node = self.register_function(self.to_function_name(node.idx, self.current_type.name))

        # Stablish this method as the current function so we can properly set
        # names for variables and stuffs.
        self.current_function = function_node

        # Define method's params
        params: List[semantics.VariableInfo] = [scope.find_variable(param.idx) for param in node.param_list]

        # Register function's params
        for param in params:
            self.register_params(param)

        # Get the instructions that conforms the body of the method
        for exp in node.statements:
            self.visit(exp, scope)

        self.current_method = None
        self.current_function = None

    @visitor.when(coolAst.IfThenElseNode)  # type: ignore
    def visit(self, node: coolAst.IfThenElseNode, scope: Scope) -> None:  # noqa: F811
        # Create a jumping label
        false_label = self.do_label("FALSE")
        end_label = self.do_label("END")

        # Save the instructions related to the condition,
        # Each expr returns the name of the holder varaiable
        internal_cond_vm_holder = self.visit(node.cond, scope)

        # Do the check and jump if necesary
        self.register_instruction(cil.NotZeroJump(internal_cond_vm_holder, false_label))

        # Save the instructions related to the then branch
        self.visit(node.expr1, scope)

        self.register_instruction(cil.UnconditionalJump(end_label))

        # Save the instructions related to the else branch
        self.register_instruction(cil.LabelNode(false_label))
        self.visit(node.expr2, scope)

        self.register_instruction(cil.LabelNode(end_label))

    @visitor.when(coolAst.VariableDeclaration)  # type: ignore
    def visit(self, node: coolAst.VariableDeclaration, scope: Scope) -> None:  # noqa: F811
        for var_idx, var_type, var_init_expr in node.var_list:

            # Register the variables in order
            var_info = scope.find_variable(var_idx)
            local_var = self.register_local(var_info)

            # Allocate memory for the variable type and give default initialization
            self.register_instruction(cil.AllocateNode(var_info.type.name, local_var))

            # Generate the code of the initialization expr if exists
            if var_init_expr is not None:
                expr_init_vm_holder = self.visit(var_init_expr, scope)
                # assign the corresponding value to the defined local_var
                self.register_instruction(cil.AssignNode(local_var, expr_init_vm_holder))

        # Process the associated expr, if any, to the let declaration
        # A block defines a new scope, so it is important to manage it
        self.visit(node.block_statements, scope.children[0])

    @visitor.when(coolAst.BlockNode)  # type:ignore
    def visit(self, node: coolAst.BlockNode, scope: Scope) -> str:  # noqa: F811
        last = ''
        # A block is simply a list of statements, so visit each one
        for stmt in node.expressions:
            last = self.visit(stmt, scope)
        # Return value of a block is its last statement
        return last

    @visitor.when(coolAst.AssignNode)  # type:ignore
    def visit(self, node: coolAst.AssignNode, scope: Scope):  # noqa: F811
        # Assignments looks like:
        # id <- expr
        # So here we assume that a local variable named "id"
        # has already been defined

        # TODO: need to diferentiate between attributes and method vars?

        # Generate the code for the rvalue (expr)
        rvalue_vm_holder = self.visit(self, node.expr)

        # register the assignment instruction
        self.register_instruction(cil.AssignNode(node.idx, rvalue_vm_holder))

    @visitor.when(coolAst.WhileBlockNode)  # type: ignore
    def visit(self, node: coolAst.WhileBlockNode, scope: Scope):  # noqa: F811

        # First evaluate the condition and set a label
        # to return to
        while_label = self.do_label('WHILE')
        end_label = self.do_label('WHILE_END')
        self.register_instruction(cil.LabelNode(while_label))
        cond_vm_holder = self.visit(node.cond, scope)

        # Probar la condicion, si es true continuar la ejecucion, sino saltar al LABEL end
        self.register_instruction(cil.IfZeroJump(cond_vm_holder, end_label))

        # Registrar las instrucciones del cuerpo del while
        self.visit(node.statements, scope)

        # Realizar un salto incondicional al chequeo de la condicion
        self.register_instruction(cil.UnconditionalJump(while_label))
        # Registrar el LABEL final
        self.register_instruction(cil.LabelNode(end_label))

    @visitor.when(coolAst.CaseNode)  # type: ignore
    def visit(self, node: coolAst.CaseNode, scope: Scope):  # noqa: F811
        # Evalauar la expr0
        expr_vm_holder = self.visit(node.expression, scope)

        # Almacenar el tipo del valor retornado
        type_internal_local_holder = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(expr_vm_holder, type_internal_local_holder))

        # Iterar por cada accion que se toma en la expresion case
        # para generar el codigo de cada action, ademas se agrega
        # en cada accion un chequeo en runtime que indica si el branch
        # que analizamos es el LCA entre el tipo que se deduce de la expresion
        # calculada y el tipo actual que se chequea en la rama
        branch_type = self.define_internal_local()
        for i, action_node in enumerate(node.actions):
            next_i_label = self.do_label(f'NEXT{i}')
            self.register_instruction(cil.LabelNode(next_i_label))
            self.register_instruction(cil.LCANode(action_node.itype.name, type_internal_local_holder, branch_type))
            # Comparar el LCA con 
