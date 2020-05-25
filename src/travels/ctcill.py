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

    #  *************** IMPLEMENTACION DE LAS DEFINICIONES DE CLASES *****************

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

    # ******************  IMPLEMENTACION DE LAS DEFINICIONES DE METODOS ******************

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

    # **************   IMPLEMENTACION DE LAS EXPRESIONES CONDICIONAES (IF, WHILE, CASE) Y LAS DECLARACIONES
    #                  DE VARIABLES (let)
    # **************

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
        # La asignacion tiene la siguiente forma:
        # id <- expr
        # Aqui asumimos que una variable interna llamada id
        # ya ha sido definida

        # TODO: Es necesario diferenciar entre variable y atributo ?

        # Generar el codigo para el rvalue (expr)
        rvalue_vm_holder = self.visit(self, node.expr)

        # registrar la instruccion de asignacion
        self.register_instruction(cil.AssignNode(node.idx, rvalue_vm_holder))

    @visitor.when(coolAst.WhileBlockNode)  # type: ignore
    def visit(self, node: coolAst.WhileBlockNode, scope: Scope):  # noqa: F811
        # Evaluar la condicion y definir un LABEL al cual
        # retornar
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

        # Variables internas para almacenar resultados intermedios
        branch_type_index = self.define_internal_local()
        expr_type_index = self.define_internal_local()
        branch_type = self.define_internal_local()
        min_ = self.define_internal_local()
        tdt_result = self.define_internal_local()
        min_check_local = self.define_internal_local()

        self.register_instruction(cil.AssignNode(min_, len(self.context.types)))
        self.register_instruction(cil.GetTypeIndex(type_internal_local_holder, expr_type_index))

        for i, action_node in enumerate(node.actions):
            self.register_instruction(cil.AssignNode(branch_type, action_node.itype.name))
            # Obtener el indice del tipo en el contexto
            self.register_instruction(cil.GetTypeIndex(branch_type, branch_type_index))
            # Calcular la distancia hacia el tipo, y actualizar el minimo de ser necesario
            self.register_instruction(cil.TdtLookupNode(branch_type_index, expr_type_index, tdt_result))

            # Comparar el resultado obtenido con el minimo actual.
            self.register_instruction(cil.MinusNode(min_, tdt_result, min_check_local))
            not_min_label = self.do_label('Not_min{i}')
            self.register_instruction(cil.JumpIfGreaterThanZeroNode(min_check_local, not_min_label))

            # Si mejora el minimo, entonces actualizarlo.
            self.register_instruction(cil.AssignNode(min_, tdt_result))
            self.register_instruction(cil.LabelNode(not_min_label))

        # Ya tenemos la menor distancia entre el tipo calculado en la expr0, y todos los tipos definidos
        # en los branches del case.
        # Comprobar que tengamos una coincidencia
        self.register_instruction(cil.AssignNode(tdt_result, len(self.context.types)))
        self.register_instruction(cil.MinusNode(tdt_result, min_, type_internal_local_holder))
        error_label = self.do_label("ERROR")
        self.register_instruction(cil.IfZeroJump(type_internal_local_holder, error_label))

        end_label = self.do_label('END')

        # Procesar cada accion y ejecutar el tipo cuya distancia sea igual a min_
        for i, action_node in enumerate(node.actions):
            next_label = self.do_label(f'NEXT{i}')
            self.register_instruction(cil.AssignNode(branch_type, action_node.itype.name))
            self.register_instruction(cil.GetTypeIndex(branch_type, branch_type_index))
            self.register_instruction(cil.TdtLookupNode(branch_type_index, expr_type_index, tdt_result))
            self.register_instruction(cil.MinusNode(min_, tdt_result, min_check_local))
            self.register_instruction(cil.NotZeroJump(min_check_local, next_label))
            # Implemententacion del branch.
            # Registrar la variable <idk>
            var_info = scope.find_variable(action_node.idx)
            idk = self.register_local(var_info)
            # Asignar al identificador idk el valor de expr0
            self.register_instruction(cil.AssignNode(idk, expr_vm_holder))
            # Generar el codigo de la expresion asociada a esta rama
            self.visit(action_node.actions)
            # Generar un salto de modo que no se chequee otra rama
            self.register_instruction(cil.UnconditionalJump(end_label))
            self.register_instruction(cil.LabelNode(next_label))

        self.register_instruction(cil.LabelNode(error_label))
        # TODO: Define some form of runtime errors

        self.register_instruction(cil.LabelNode(end_label))

    # ***************   IMPLEMENTACION DE LAS EXPRESIONES ARITMETICAS
    #
    # ***************

    @visitor.when(coolAst.PlusNode)  # type: ignore
    def visit(self, node: coolAst.PlusNode, scope: Scope):  # noqa: F811
        # Definir una variable interna local para almacenar el resultado
        sum_internal_local = self.define_internal_local()

        # Obtener el resultado del primero operando
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el resultado del segundo operando
        right_vm_holder = self.visit(node.right, scope)

        # registrar la instruccion de suma
        self.register_instruction(cil.PlusNode(sum_internal_local, left_vm_holder, right_vm_holder))

        # Devolver la variable interna que contiene la suma
        return sum_internal_local

    @visitor.when(coolAst.DifNode)  # type: ignore
    def visit(self, node: coolAst.DifNode, scope: Scope):  # noqa: F811
        # Definir una variable interna local para almacenar el resultado intermedio
        minus_internal_vm_holder = self.define_internal_local()

        # Obtener el resultado del minuendo
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el resultado del sustraendo
        right_vm_holder = self.visit(node.right, scope)

        # Registrar la instruccion de resta
        self.register_instruction(cil.MinusNode(left_vm_holder, right_vm_holder, minus_internal_vm_holder))

        # Devolver la variable que contiene el resultado
        return minus_internal_vm_holder

    @visitor.when(coolAst.MulNode)  # type: ignore
    def visit(self, node: coolAst.MulNode, scope: Scope):  # noqa: F811
        # Definir una variable interna local para almacenar el resultado intermedio
        mul_internal_vm_holder = self.define_internal_local()

        # Obtener el resultado del primer factor
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el resultado del segundo factor
        right_vm_holder = self.visit(node.right, scope)

        # Registrar la instruccion de multimplicacion
        self.register_instruction(cil.StarNode(left_vm_holder, right_vm_holder, mul_internal_vm_holder))

        # Retornarl el resultado
        return mul_internal_vm_holder

    @visitor.when(coolAst.DivNode)  # type: ignore
    def visit(self, node: coolAst.DivNode, scope: Scope):  # noqa: F811
        # Definir una variable interna local para almacenar el resultado intermedio
        div_internal_vm_holder = self.define_internal_local()

        # Obtener el resultad del dividendo
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el resultado del divisor
        right_vm_holder = self.visit(node.right, scope)

        # Registrar la instruccion de division
        self.register_instruction(cil.DivNode(div_internal_vm_holder, left_vm_holder, right_vm_holder))

        # Devolver el resultado
        return div_internal_vm_holder

    # *********************  IMPLEMENTACION DE LAS CONSTANTES
    #
    # *********************

    @visitor.when(coolAst.IntegerConstant)  # type: ignore
    def visit(self, node: coolAst.IntegerConstant, scope: Scope):  # noqa: F811
        # Variable interna que guarda el valor de la constante
        int_const_vm_holder = self.define_internal_local()

        # Asignarle el valor a la variable
        self.register_instruction(cil.AssignNode(int_const_vm_holder, int(node.lex)))

        # devolver el valor
        return int_const_vm_holder

    @visitor.when(coolAst.StringConstant)  # type: ignore
    def visit(self, node: coolAst.StringConstant, scope: Scope):  # noqa: F811
        # Variable interna que apunta al string
        str_const_vm_holder = self.define_internal_local()

        # Registrar el string en la seccion de datos
        s1 = self.register_data(node.lex)

        # Cargar el string en la variable interna
        self.register_instruction(cil.LoadNode(str_const_vm_holder, s1))

        # Devolver la variable que contiene el string
        return str_const_vm_holder

    @visitor.when(coolAst.TrueConstant)  # type: ignore
    def visit(self, node: coolAst.TrueConstant, scope: Scope):  # noqa: F811
        # variable interna que devuelve el valor de la constante
        true_const_vm_holder = self.define_internal_local()
        self.register_instruction(cil.AssignNode(true_const_vm_holder), 1)
        return true_const_vm_holder

    @visitor.when(coolAst.FalseConstant)  # type: ignore
    def visit(self, node: coolAst.FalseConstant, scope: Scope):  # noqa: F811
        false_const_vm_holder = self.define_internal_local()
        self.register_instruction(cil.AssignNode(false_const_vm_holder), 0)
        return false_const_vm_holder

    # *******************  Implementacion de las comparaciones
    #
    # *******************

    @visitor.when(coolAst.EqualToNode)  # type: ignore
    def visit(self, node: coolAst.EqualToNode, scope: Scope):  # noqa: F811
        # Debemos devolver una variable que contenga 0 si los valores a comparar
        # son iguales.
        expr_result_vm_holder = self.define_internal_local()

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        # Realizar una resta y devolver el resultado
        self.register_instruction(cil.MinusNode(left_vm_holder, right_vm_holder, expr_result_vm_holder))

        # Devolver la variable con el resultado
        return expr_result_vm_holder
