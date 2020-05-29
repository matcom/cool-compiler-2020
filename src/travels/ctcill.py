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
    def visit(self, node: coolAst.Node, scope: Scope) -> None:
        pass

    @visitor.when(coolAst.ProgramNode)  # type: ignore
    def visit(self, node: coolAst.ProgramNode, scope: Scope) -> cil.CilProgramNode:  # noqa: F811
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

        methods: List[str] = [feature.idx for feature in node.features if isinstance(feature, coolAst.MethodDef)]
        attributes: List[semantics.Attribute] = [feature for feature in node.features if isinstance(feature, coolAst.AttributeDef)]

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
            new_type_node.methods.append((method, self.to_function_name(method, node.idx)))

        # TODO: It is necessary to visit attributes?? Think so cuz they can be initialized
        # and their value could perhaps go to .DATA section

        # Visit every method for generate its code in the .CODE section
        for feature, child_scope in zip((x for x in node.features if isinstance(x, coolAst.MethodDef)), scope.children):
            self.visit(feature, child_scope)

        self.current_type = None

    # ******************  IMPLEMENTACION DE LAS DEFINICIONES DE METODOS ******************

    @visitor.when(coolAst.MethodDef)  # type: ignore
    def visit(self, node: coolAst.MethodDef, scope: Scope) -> None:  # noqa: F811
        self.current_method = self.current_type.get_method(node.idx)

        # Registrar la nueva funcion en .CODE
        function_node = self.register_function(self.to_function_name(node.idx, self.current_type.name))

        # Establecer el metodo actual y la funcion actual en construccion
        # para poder establecer nombres de variables y otras cosas.
        self.current_function = function_node

        # Definir los parametros del metodo.
        params: List[semantics.VariableInfo] = [scope.find_variable(param.id) for param in node.param_list]

        # Establecer los parametros de la funcion.
        for param in params:
            self.register_params(param)

        # Registrar las instrucciones que conforman el cuerpo del metodo.
        last = self.visit(node.statements, scope)
        if last is not None:
            self.register_instruction(cil.ReturnNode(last))
        else:
            self.register_instruction(cil.ReturnNode())

        self.current_method = None
        self.current_function = None


    # **************   IMPLEMENTACION DE LAS EXPRESIONES CONDICIONAES (IF, WHILE, CASE) Y LAS DECLARACIONES
    #                  DE VARIABLES (let)
    # **************

    @visitor.when(coolAst.IfThenElseNode)  # type: ignore
    def visit(self, node: coolAst.IfThenElseNode, scope: Scope) -> None:  # noqa: F811
        # Crear un LABEL al cual realizar un salto.
        false_label = self.do_label("FALSE")
        end_label = self.do_label("END")

        # Salvar las instrucciones relacionadas con la condicion,
        # cada expresion retorna el nombre de la variable interna que contiene el valor ??
        internal_cond_vm_holder = self.visit(node.cond, scope)

        # Chequear y saltar si es necesario.
        self.register_instruction(cil.IfZeroJump(internal_cond_vm_holder, false_label))

        # Salvar las instrucciones relacionadas con la rama TRUE.
        self.visit(node.expr1, scope)

        self.register_instruction(cil.UnconditionalJump(end_label))

        # Registrar las instrucciones relacionadas con la rama ELSE
        self.register_instruction(cil.LabelNode(false_label))
        self.visit(node.expr2, scope)

        self.register_instruction(cil.LabelNode(end_label))

    @visitor.when(coolAst.VariableDeclaration)  # type: ignore
    def visit(self, node: coolAst.VariableDeclaration, scope: Scope) -> None:  # noqa: F811
        for var_idx, var_type, var_init_expr in node.var_list:

            # Registrar las variables en orden.
            var_info = scope.find_variable(var_idx)
            local_var = self.register_local(var_info)

            # Reservar memoria para la variable y realizar su inicializacion si tiene
            self.register_instruction(cil.AllocateNode(var_info.type.name, local_var))

            if var_init_expr is not None:
                expr_init_vm_holder = self.visit(var_init_expr, scope)
                # Assignar el valor correspondiente a la variable reservada
                self.register_instruction(cil.AssignNode(local_var, expr_init_vm_holder))

        # Process the associated expr, if any, to the let declaration
        # A block defines a new scope, so it is important to manage it
        return self.visit(node.block_statements, scope)

    @visitor.when(coolAst.VariableCall)  # type: ignore
    def visit(self, node: coolAst.VariableCall, scope: Scope):  # noqa: F811
        vinfo = scope.find_variable(node.idx)
        # Diferenciar la variable si es un parametro, un atributo o una variable local
        # en el scope actual
        if vinfo.location == "PARAM":
            for param_node in self.params:
                if vinfo.name in param_node.name:
                    return param_node.name
        if vinfo.location == "ATTRIBUTE":
            local = self.define_internal_local()
            self.register_instruction(cil.GetAttributeNode(self.current_type.name, vinfo.name, local))
            return local
        if vinfo.location == "LOCAL":
            for local_node in self.localvars:
                if vinfo.name in local_node.name:
                    return local_node.name

    @visitor.when(coolAst.InstantiateClassNode)  # type: ignore
    def visit(self, node: coolAst.InstantiateClassNode, scope: Scope):  # noqa: F811
        # Reservar una variable que guarde la nueva instancia
        type_ = self.context.get_type(node.type_)
        instance_vm_holder = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(type_, instance_vm_holder))
        return instance_vm_holder

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
            self.visit(action_node.actions, scope)
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

    # *******************  Implementacion de las comparaciones ********************
    # Todas las operaciones de comparacion devuelven 1 si el resultado es verdadero,
    # o 0 si es falso.
    # *******************

    @visitor.when(coolAst.EqualToNode)  # type: ignore
    def visit(self, node: coolAst.EqualToNode, scope: Scope):  # noqa: F811
        expr_result_vm_holder = self.define_internal_local()
        true_label = self.do_label("TRUE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        # Realizar una resta y devolver el resultado
        self.register_instruction(cil.MinusNode(left_vm_holder, right_vm_holder, expr_result_vm_holder))

        # Si la resta da 0, entonces son iguales y se devuelve 1, si no, se devuelve 0
        self.register_instruction(cil.IfZeroJump(expr_result_vm_holder, true_label))

        # si la resta no da 0, almacenar 0 y retornar
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 0))
        self.register_instruction(cil.UnconditionalJump(end_label))

        # Si la resta da 0, devolver 1
        self.register_instruction(cil.LabelNode(true_label))
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 1))

        self.register_instruction(cil.LabelNode(end_label))

        # Devolver la variable con el resultado
        return expr_result_vm_holder

    @visitor.when(coolAst.LowerThanNode)  # type: ignore
    def visit(self, node: coolAst.LowerThanNode, scope: Scope):  # noqa: F811
        expr_result_vm_holder = self.define_internal_local()
        false_label = self.do_label("FALSE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        # Comparar los resultados restando
        self.register_instruction(cil.MinusNode(left_vm_holder, right_vm_holder, expr_result_vm_holder))

        self.register_instruction(cil.JumpIfGreaterThanZeroNode(expr_result_vm_holder, false_label))
        self.register_instruction(cil.IfZeroJump(expr_result_vm_holder, false_label))

        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 1))
        self.register_instruction(cil.UnconditionalJump(end_label))

        self.register_instruction(cil.LabelNode(false_label))
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 0))
        self.register_instruction(cil.LabelNode(end_label))

        return expr_result_vm_holder

    @visitor.when(coolAst.LowerEqual)  # type: ignore
    def visit(self, node: coolAst.LowerEqual, scope: Scope):  # noqa: F811
        expr_result_vm_holder = self.define_internal_local()
        false_label = self.do_label("FALSE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        self.register_instruction(cil.MinusNode(left_vm_holder, right_vm_holder, expr_result_vm_holder))

        self.register_instruction(cil.JumpIfGreaterThanZeroNode(expr_result_vm_holder, false_label))

        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 1))
        self.register_instruction(cil.UnconditionalJump(end_label))

        self.register_instruction(cil.LabelNode(false_label))
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 0))
        self.register_instruction(cil.LabelNode(end_label))

        return expr_result_vm_holder

    @visitor.when(coolAst.GreaterThanNode)  # type: ignore
    def visit(self, node: coolAst.GreaterThanNode, scope: Scope):  # noqa: F811
        expr_result_vm_holder = self.define_internal_local()
        true_label = self.do_label("TRUE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        self.register_instruction(cil.MinusNode(left_vm_holder, right_vm_holder, expr_result_vm_holder))

        self.register_instruction(cil.JumpIfGreaterThanZeroNode(expr_result_vm_holder, true_label))

        # False Branch
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 0))
        self.register_instruction(cil.UnconditionalJump(end_label))

        # True Branch
        self.register_instruction(cil.LabelNode(true_label))
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 1))
        self.register_instruction(cil.LabelNode(end_label))

        return expr_result_vm_holder

    @visitor.when(coolAst.GreaterEqualNode)  # type: ignore
    def visit(self, node: coolAst.GreaterEqualNode, scope: Scope):  # noqa: F811
        expr_result_vm_holder = self.define_internal_local()
        true_label = self.do_label("TRUE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        self.register_instruction(cil.MinusNode(left_vm_holder, right_vm_holder, expr_result_vm_holder))

        self.register_instruction(cil.JumpIfGreaterThanZeroNode(expr_result_vm_holder, true_label))
        self.register_instruction(cil.IfZeroJump(expr_result_vm_holder, true_label))

        # False Branch
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 1))
        self.register_instruction(cil.UnconditionalJump(end_label))

        # True Branch
        self.register_instruction(cil.LabelNode(true_label))
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 1))
        self.register_instruction(cil.LabelNode(end_label))

        return expr_result_vm_holder

    # *********************  IMPLEMENTACION DE LOS METODOS DE DISPATCH  *******************
    #
    # *********************

    @visitor.when(coolAst.FunCall)  # type: ignore
    def visit(self, node: coolAst.FunCall, scope: Scope):  # noqa: F811
        type_vm_holder = self.define_internal_local()
        return_vm_holder = self.define_internal_local()
        # Evaluar la expresion a la izquierda del punto
        expr = self.visit(node.obj, scope)

        self.register_instruction(cil.TypeOfNode(expr, type_vm_holder))

        # Evaluar los argumentos
        for arg in node.args:
            arg_expr = self.visit(arg, scope)
            self.register_instruction(cil.ArgNode(arg_expr))

        self.register_instruction(cil.DynamicCallNode(type_vm_holder, node.id, return_vm_holder))

        return return_vm_holder

    @visitor.when(coolAst.ParentFuncCall)  # type: ignore
    def visit(self, node: coolAst.ParentFuncCall, scope: Scope):  # noqa: F811
        local_type_identifier = self.define_internal_local()
        return_expr_vm_holder = self.define_internal_local()
        expr = self.visit(node.obj, scope)

        # Evaluar los argumentos
        for arg in node.arg_list:
            arg_expr = self.visit(arg, scope)
            self.register_instruction(cil.ArgNode(arg_expr))

        # Asignar el tipo a una variable
        type_ = self.context.get_type(node.parent_type)
        self.register_instruction(cil.AssignNode(local_type_identifier, type_))

        self.register_instruction(cil.DynamicCallNode(local_type_identifier, node.idx, return_expr_vm_holder))

        return return_expr_vm_holder


class CilDisplayFormatter:
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cil.CilProgramNode)  # type: ignore
    def visit(self, node: cil.CilProgramNode):  # noqa: F811
        # Primero imprimir la seccion .TYPES
        dottypes = '\n'.join(self.visit(type_) for type_ in node.dottypes)

        # Imprimir la seccion .DATA
        dotdata = '\n'.join(self.visit(data) for data in node.dotdata)

        # Imprimir la seccion .CODE
        dotcode = '\n'.join(self.visit(code) for code in node.dotcode)

        return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

    @visitor.when(cil.TypeNode)  # type: ignore
    def visit(self, node: cil.TypeNode):  # noqa: F811
        attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
        methods = '\n\t'.join(f'method {x}: {y}' for x, y in node.methods)

        return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

    @visitor.when(cil.FunctionNode)  # type: ignore
    def visit(self, node: cil.FunctionNode):  # noqa: F811
        params = '\n\t'.join(self.visit(x) for x in node.params)
        localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
        instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

        return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

    @visitor.when(cil.ParamNode)  # type: ignore
    def visit(self, node: cil.ParamNode):  # noqa : F811
        return f'PARAM {node.name}'

    @visitor.when(cil.LocalNode)  # type: ignore
    def visit(self, node: cil.LocalNode):  # noqa: F811
        return f'LOCAL {node.name}'

    @visitor.when(cil.AssignNode)  # type: ignore
    def visit(self, node: cil.AssignNode):  # noqa: F811
        return f'{node.dest} = {node.source}'

    @visitor.when(cil.PlusNode)  # type: ignore
    def visit(self, node: cil.PlusNode):  # noqa: F811
        return f'{node.dest} = {node.left} + {node.right}'

    @visitor.when(cil.MinusNode)  # type: ignore
    def visit(self, node: cil.MinusNode):  # noqa: F811
        return f'{node.dest} = {node.x} - {node.y}'

    @visitor.when(cil.StarNode)  # type: ignore
    def visit(self, node: cil.StarNode):  # noqa: F811
        return f'{node.dest} = {node.x} * {node.y}'

    @visitor.when(cil.DivNode)  # type: ignore
    def visit(self, node: cil.DivNode):  # noqa: F811
        return f'{node.dest} = {node.left} / {node.right}'

    @visitor.when(cil.AllocateNode)  # type: ignore
    def visit(self, node: cil.AllocateNode):  # noqa: F811
        return f'{node.dest} = ALLOCATE {node.itype}'

    @visitor.when(cil.TypeOfNode)  # type: ignore
    def visit(self, node: cil.TypeOfNode):  # noqa: F811
        return f'{node.dest} = TYPEOF {node.variable}'

    @visitor.when(cil.DynamicCallNode)  # type: ignore
    def visit(self, node: cil.DynamicCallNode):  # noqa: F811
        return f'{node.dest} = VCALL {node.xtype} {node.method}'

    @visitor.when(cil.StaticCallNode)  # type: ignore
    def visit(self, node: cil.StaticCallNode):  # noqa: F811
        return f'{node.dest} = CALL {node.function}'

    @visitor.when(cil.ArgNode)  # type: ignore
    def visit(self, node: cil.ArgNode):  # noqa: F811
        return f'ARG {node.name}'

    @visitor.when(cil.ReturnNode)  # type: ignore
    def visit(self, node: cil.ReturnNode):  # noqa: F811
        return f'RETURN {node.value if node.value is not None else ""}'

    @visitor.when(cil.DataNode)  # type: ignore
    def visit(self, node: cil.DataNode):  # noqa: F811
        if isinstance(node.value, str):
            return f'{node.name} = "{node.value}" ;'
        elif isinstance(node.value, list):
            data = "\n\t".join(str(x) for x in node.value)
            return f'{node.name} = {data}'
        elif isinstance(node.value, int):
            return f'{node.name} = {node.value}'

    @visitor.when(cil.GetTypeIndex)  # type: ignore
    def visit(self, node: cil.GetTypeIndex):  # noqa: F811
        return f'{node.dest} = GETTYPEINDEX {node.itype}'

    @visitor.when(cil.TdtLookupNode)  # type: ignore
    def visit(self, node: cil.TdtLookupNode):  # noqa: F811
        return f'{node.dest} = TYPE_DISTANCE {node.i} {node.j}'

    @visitor.when(cil.IfZeroJump)  # type: ignore
    def visit(self, node: cil.IfZeroJump):  # noqa: F811
        return f'IF_ZERO {node.variable} GOTO {node.label}'

    @visitor.when(cil.UnconditionalJump)  # type: ignore
    def visit(self, node: cil.UnconditionalJump):  # noqa: F811
        return f'GOTO {node.label}'

    @visitor.when(cil.JumpIfGreaterThanZeroNode)  # type: ignore
    def visit(self, node: cil.JumpIfGreaterThanZeroNode):  # noqa: F811
        return f'IF_GREATER_ZERO {node.variable} GOTO {node.label}'

    @visitor.when(cil.LabelNode)  # type: ignore
    def visit(self, node: cil.LabelNode):  # noqa: F811
        return f'{node.label}:'

    def __call__(self, node):
        return self.visit(node)
