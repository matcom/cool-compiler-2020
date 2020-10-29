from cloudpickle.cloudpickle import instance
from abstract.tree import AssignNode
import cil.baseCilVisitor as baseCilVisitor
import abstract.tree as coolAst
import abstract.semantics as semantics
import cil.nodes as cil
from typing import List, Optional, Tuple
from functools import singledispatchmethod

from cil.nodes import CilNode, LocalNode, ParamNode, ReturnNode

ExpressionReturn = Tuple[List[cil.InstructionNode], List[cil.LocalNode]]
Scope = semantics.Scope


class CoolToCILVisitor(baseCilVisitor.BaseCoolToCilVisitor):
    @singledispatchmethod
    def visit(self, node, scope: Scope) -> CilNode:
        # Devolver un nodo vacio, al final este metodo no
        # se debe llamar nunca.
        return CilNode()

    @visit.register
    def _(self, node: coolAst.ProgramNode,
          scope: Scope) -> cil.CilProgramNode:  # noqa: F811

        # Definir el punto de entrada del programa.
        self.current_function = self.register_function("entry")
        instance = self.define_internal_local()
        result = self.define_internal_local()

        # El primer metodo que se invoca es el metodo main de la clase Main

        # Reservar memoria para el objeto Main
        main_type = self.context.get_type('Main')
        self.register_instruction(cil.AllocateNode(main_type, instance))
        self.register_instruction(cil.ArgNode(instance))

        # Llamar al metodo main
        self.register_instruction(
            cil.StaticCallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None

        for klass, child_scope in zip(node.class_list, scope.children):
            self.visit(klass, child_scope)

        return cil.CilProgramNode(self.dot_types, self.dot_data, self.dot_code)

    #  *************** IMPLEMENTACION DE LAS DEFINICIONES DE CLASES *****************

    @visit.register
    def _(self, node: coolAst.ClassDef, scope: Scope) -> None:  # noqa: F811
        # Registrar el tipo que creamos en .Types section
        self.current_type = self.context.get_type(node.idx)
        new_type_node = self.register_type(node.idx)

        methods = self.current_type.methods
        attributes = self.current_type.attributes

        # Manejar los features heredados como atributos y metodos
        if self.current_type.parent is not None:
            for attribute in self.current_type.parent.attributes:
                new_type_node.attributes.append(attribute)

            for method in self.current_type.parent.methods.keys():
                # Manejar la redefinicion de metodos
                if method not in methods:
                    new_type_node.methods.append(
                        (method,
                         self.to_function_name(method,
                                               self.current_type.parent.name)))

        # Registrar cada atributo y metodo para este tipo
        # la seccion .Type debe tener la siguiente forma:
        #####################################################################
        # .TYPES                                                            #
        # type A {                                                          #
        #      attribute x;                                                 #
        #      method f : function_f_at_A;                                  #
        # }                                                                 #
        #####################################################################
        for attribute in attributes:
            new_type_node.attributes.append(attribute)

        for method in methods:
            new_type_node.methods.append(
                (method, self.to_function_name(method, node.idx)))

        # Visitar los atributos definidos en la clase para generar sus funciones
        # de inicializacion
        for feature in node.features:
            if isinstance(feature, coolAst.AttributeDef):
                self.visit(feature, scope)

        # Visitar cada metodo para generar su codigo en la seccion .CODE
        for feature, child_scope in zip(
            (x for x in node.features if isinstance(x, coolAst.MethodDef)),
                scope.children):
            self.visit(feature, child_scope)

        self.current_type = None

    # ******************  IMPLEMENTACION DE LAS DEFINICIONES DE METODOS ******************

    @visit.register
    def _(self, node: coolAst.AttributeDef, scope: Scope) -> None:
        self.current_function = self.register_function(
            f"__attrib__{node.idx}__init")
        if node.default_value is not None:
            # Generar el codigo de la expresion de inicializacion
            # y devolver el valor de esta
            value = self.visit(node.default_value, scope)
            self.register_instruction(ReturnNode(value))

        else:
            # Si no tiene expresion de inicializacion entonces devolvemos
            # 0 en caso de que sea Int, Bool u otro tipo excepto String
            # (0 = false y 0 = void)
            attribute_type = self.context.get_type(node.typex)
            if attribute_type.name == "String":
                self.register_instruction(ReturnNode(self.null.name))
            else:
                self.register_instruction(ReturnNode(0))

    @visit.register
    def _(self, node: coolAst.MethodDef, scope: Scope) -> None:  # noqa: F811
        self.current_method = self.current_type.get_method(node.idx)

        # Registrar la nueva funcion en .CODE
        function_node = self.register_function(
            self.to_function_name(node.idx, self.current_type.name))

        # Establecer el metodo actual y la funcion actual en construccion
        # para poder establecer nombres de variables y otras cosas.
        self.current_function = function_node

        # Definir los parametros del metodo.
        params: List[Optional[semantics.VariableInfo]] = [
            scope.find_variable(param.id) for param in node.param_list
        ]

        # Establecer los parametros de la funcion.
        for param in params:
            if param:
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

    @visit.register
    def _(self, node: coolAst.IfThenElseNode,
          scope: Scope) -> None:  # noqa: F811
        # Crear un LABEL al cual realizar un salto.
        false_label = self.do_label("FALSE")
        end_label = self.do_label("END")

        # Salvar las instrucciones relacionadas con la condicion,
        # cada expresion retorna el nombre de la variable interna que contiene el valor ??
        internal_cond_vm_holder = self.visit(node.cond, scope)

        # Chequear y saltar si es necesario.
        assert isinstance(internal_cond_vm_holder, LocalNode)
        self.register_instruction(
            cil.IfZeroJump(internal_cond_vm_holder, false_label))

        # Salvar las instrucciones relacionadas con la rama TRUE.
        self.visit(node.expr1, scope)

        self.register_instruction(cil.UnconditionalJump(end_label))

        # Registrar las instrucciones relacionadas con la rama ELSE
        self.register_instruction(cil.LabelNode(false_label))
        self.visit(node.expr2, scope)

        self.register_instruction(cil.LabelNode(end_label))

    @visit.register
    def _(self, node: coolAst.VariableDeclaration,
          scope: Scope) -> CilNode:  # noqa: F811
        for var_idx, var_type, var_init_expr in node.var_list:

            # Registrar las variables en orden.
            var_info = scope.find_variable(var_idx)
            assert var_info is not None
            local_var = self.register_local(var_info)

            # Reservar memoria para la variable y realizar su inicializacion si tiene
            assert var_info.type is not None

            # Si la variable es int, string o boolean, su valor por defecto es 0
            if var_info.type.name not in ("String", "Int", "Bool"):
                self.register_instruction(
                    cil.AllocateNode(var_info.type, local_var))
            else:
                # Si la variable tiene una expresion de inicializacion
                # entonces no es necesario ponerle valor por defecto
                if var_init_expr is None:
                    self.register_instruction(cil.AssignNode(local_var, 0))

            if var_init_expr is not None:
                expr_init_vm_holder = self.visit(var_init_expr, scope)
                # Assignar el valor correspondiente a la variable reservada
                self.register_instruction(
                    cil.AssignNode(local_var, expr_init_vm_holder))

        # Process the associated expr, if any, to the let declaration
        # A block defines a new scope, so it is important to manage it
        return self.visit(node.block_statements, scope)

    @visit.register
    def _(self, node: coolAst.VariableCall, scope: Scope):  # noqa: F811
        vinfo = scope.find_variable(node.idx)
        # Diferenciar la variable si es un parametro, un atributo o una variable local
        # en el scope actual
        if vinfo.location == "PARAM":
            for param_node in self.params:
                if vinfo.name in param_node.name:
                    return param_node
        if vinfo.location == "ATTRIBUTE":
            local = self.define_internal_local()
            assert self.current_type is not None
            self.register_instruction(
                cil.GetAttributeNode(self.current_type, vinfo.name, local))
            return local
        if vinfo.location == "LOCAL":
            for local_node in self.localvars:
                if vinfo.name in local_node.name:
                    return local_node

    @visit.register
    def _(self, node: coolAst.InstantiateClassNode, scope: Scope) -> LocalNode:
        # Reservar una variable que guarde la nueva instancia
        type_ = self.context.get_type(node.type_)
        instance_vm_holder = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(type_, instance_vm_holder))
        return instance_vm_holder

    @visit.register
    def _(self, node: coolAst.BlockNode, scope: Scope) -> CilNode:
        last: CilNode = CilNode()
        # A block is simply a list of statements, so visit each one
        for stmt in node.expressions:
            last = self.visit(stmt, scope)
        # Return value of a block is its last statement
        return last

    @visit.register
    def _(self, node: coolAst.AssignNode, scope: Scope):
        # La asignacion tiene la siguiente forma:
        # id <- expr
        # Aqui asumimos que una variable interna llamada id
        # ya ha sido definida

        # Generar el codigo para el rvalue (expr)
        rvalue_vm_holder = self.visit(self, node.expr)
        assert isinstance(rvalue_vm_holder, LocalNode)

        # Es necesario diferenciar entre variable y atributo.
        # Las variables se diferencian en si son locales al
        # metodo que estamos creando o si son atributos.
        if scope.is_local(node.idx):
            # registrar la instruccion de asignacion
            self.register_instruction(
                cil.AssignNode(node.idx, rvalue_vm_holder))
        else:
            assert self.current_type is not None
            self.register_instruction(
                cil.SetAttributeNode(self.current_type, node.idx,
                                     rvalue_vm_holder))

    @visit.register
    def _(self, node: coolAst.WhileBlockNode, scope: Scope):
        # Evaluar la condicion y definir un LABEL al cual
        # retornar
        while_label = self.do_label('WHILE')
        end_label = self.do_label('WHILE_END')
        self.register_instruction(cil.LabelNode(while_label))
        cond_vm_holder = self.visit(node.cond, scope)

        # Probar la condicion, si es true continuar la ejecucion, sino saltar al LABEL end
        assert isinstance(cond_vm_holder, LocalNode)
        self.register_instruction(cil.IfZeroJump(cond_vm_holder, end_label))

        # Registrar las instrucciones del cuerpo del while
        self.visit(node.statements, scope)

        # Realizar un salto incondicional al chequeo de la condicion
        self.register_instruction(cil.UnconditionalJump(while_label))
        # Registrar el LABEL final
        self.register_instruction(cil.LabelNode(end_label))

    @visit.register
    def _(self, node: coolAst.CaseNode, scope: Scope):
        # Evalauar la expr0
        expr_vm_holder = self.visit(node.expression, scope)

        # Almacenar el tipo del valor retornado
        type_internal_local_holder = self.define_internal_local()
        sub_vm_local_holder = self.define_internal_local()

        assert isinstance(expr_vm_holder, LocalNode)
        self.register_instruction(
            cil.TypeOfNode(expr_vm_holder, type_internal_local_holder))

        # Variables internas para almacenar resultados intermedios
        min_ = self.define_internal_local()
        tdt_result = self.define_internal_local()
        min_check_local = self.define_internal_local()

        self.register_instruction(cil.AssignNode(min_,
                                                 len(self.context.types)))

        for i, action_node in enumerate(node.actions):
            # Calcular la distancia hacia el tipo, y actualizar el minimo de ser necesario
            self.register_instruction(
                cil.TdtLookupNode(action_node.typex,
                                  type_internal_local_holder, tdt_result))

            # Comparar el resultado obtenido con el minimo actual.
            self.register_instruction(
                cil.MinusNode(min_, tdt_result, min_check_local))
            not_min_label = self.do_label('Not_min{i}')
            self.register_instruction(
                cil.JumpIfGreaterThanZeroNode(min_check_local, not_min_label))

            # Si mejora el minimo, entonces actualizarlo.
            self.register_instruction(cil.AssignNode(min_, tdt_result))
            self.register_instruction(cil.LabelNode(not_min_label))

        # Ya tenemos la menor distancia entre el tipo calculado en la expr0, y todos los tipos definidos
        # en los branches del case.
        # Comprobar que tengamos una coincidencia
        self.register_instruction(
            cil.AssignNode(tdt_result, len(self.context.types)))
        self.register_instruction(
            cil.MinusNode(tdt_result, min_, sub_vm_local_holder))
        error_label = self.do_label("ERROR")
        self.register_instruction(
            cil.IfZeroJump(sub_vm_local_holder, error_label))

        end_label = self.do_label('END')

        # Procesar cada accion y ejecutar el tipo cuya distancia sea igual a min_
        for i, action_node in enumerate(node.actions):
            next_label = self.do_label(f'NEXT{i}')
            self.register_instruction(
                cil.TdtLookupNode(action_node.typex,
                                  type_internal_local_holder, tdt_result))
            self.register_instruction(
                cil.MinusNode(min_, tdt_result, min_check_local))
            self.register_instruction(
                cil.NotZeroJump(min_check_local, next_label))
            # Implemententacion del branch.
            # Registrar la variable <idk>
            var_info = scope.find_variable(action_node.idx)
            assert var_info is not None
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

    @visit.register
    def _(self, node: coolAst.PlusNode, scope: Scope) -> LocalNode:
        # Definir una variable interna local para almacenar el resultado
        sum_internal_local = self.define_internal_local()

        # Obtener el resultado del primero operando
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el resultado del segundo operando
        right_vm_holder = self.visit(node.right, scope)

        # registrar la instruccion de suma
        self.register_instruction(
            cil.PlusNode(sum_internal_local, left_vm_holder, right_vm_holder))

        # Devolver la variable interna que contiene la suma
        return sum_internal_local

    @visit.register
    def _(self, node: coolAst.DifNode, scope: Scope) -> LocalNode:
        # Definir una variable interna local para almacenar el resultado intermedio
        minus_internal_vm_holder = self.define_internal_local()

        # Obtener el resultado del minuendo
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el resultado del sustraendo
        right_vm_holder = self.visit(node.right, scope)

        # Registrar la instruccion de resta
        assert isinstance(left_vm_holder, LocalNode) and isinstance(
            right_vm_holder, LocalNode)
        self.register_instruction(
            cil.MinusNode(left_vm_holder, right_vm_holder,
                          minus_internal_vm_holder))

        # Devolver la variable que contiene el resultado
        return minus_internal_vm_holder

    @visit.register
    def _(self, node: coolAst.MulNode, scope: Scope) -> LocalNode:
        # Definir una variable interna local para almacenar el resultado intermedio
        mul_internal_vm_holder = self.define_internal_local()

        # Obtener el resultado del primer factor
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el resultado del segundo factor
        right_vm_holder = self.visit(node.right, scope)

        assert isinstance(left_vm_holder, LocalNode) and isinstance(
            right_vm_holder, LocalNode)

        # Registrar la instruccion de multimplicacion
        self.register_instruction(
            cil.StarNode(left_vm_holder, right_vm_holder,
                         mul_internal_vm_holder))

        # Retornar el resultado
        return mul_internal_vm_holder

    @visit.register
    def _(self, node: coolAst.DivNode, scope: Scope) -> LocalNode:
        # Definir una variable interna local para almacenar el resultado intermedio
        div_internal_vm_holder = self.define_internal_local()

        # Obtener el resultad del dividendo
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el resultado del divisor
        right_vm_holder = self.visit(node.right, scope)

        # Registrar la instruccion de division
        self.register_instruction(
            cil.DivNode(div_internal_vm_holder, left_vm_holder,
                        right_vm_holder))

        # Devolver el resultado
        return div_internal_vm_holder

    # *********************  IMPLEMENTACION DE LAS CONSTANTES
    #
    # *********************

    @visit.register
    def _(self, node: coolAst.IntegerConstant, scope: Scope) -> int:
        # devolver el valor
        return int(node.lex)

    @visit.register
    def _(self, node: coolAst.StringConstant, scope: Scope) -> LocalNode:
        # Variable interna que apunta al string
        str_const_vm_holder = self.define_internal_local()

        # Registrar el string en la seccion de datos
        s1 = self.register_data(node.lex)

        # Cargar el string en la variable interna
        self.register_instruction(cil.LoadNode(str_const_vm_holder, s1))

        # Devolver la variable que contiene el string
        return str_const_vm_holder

    @visit.register
    def _(self, node: coolAst.TrueConstant, scope: Scope) -> int:
        # variable interna que devuelve el valor de la constante
        return 1

    @visit.register
    def _(self, node: coolAst.FalseConstant, scope: Scope) -> int:
        return 0

    # *******************  Implementacion de las comparaciones ********************
    # Todas las operaciones de comparacion devuelven 1 si el resultado es verdadero,
    # o 0 si es falso.
    # *******************

    @visit.register
    def _(self, node: coolAst.EqualToNode, scope: Scope) -> int:
        expr_result_vm_holder = self.define_internal_local()
        true_label = self.do_label("TRUE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        # Realizar una resta y devolver el resultado
        assert isinstance(left_vm_holder, LocalNode) and isinstance(
            right_vm_holder, LocalNode)

        self.register_instruction(
            cil.MinusNode(left_vm_holder, right_vm_holder,
                          expr_result_vm_holder))

        # Si la resta da 0, entonces son iguales y se devuelve 1, si no, se devuelve 0
        self.register_instruction(
            cil.IfZeroJump(expr_result_vm_holder, true_label))

        # si la resta no da 0, almacenar 0 y retornar
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 0))
        self.register_instruction(cil.UnconditionalJump(end_label))

        # Si la resta da 0, devolver 1
        self.register_instruction(cil.LabelNode(true_label))
        expr_result_vm_holder = 1

        self.register_instruction(cil.LabelNode(end_label))

        # Devolver la variable con el resultado
        return expr_result_vm_holder

    @visit.register
    def _(self, node: coolAst.LowerThanNode, scope: Scope) -> LocalNode:
        expr_result_vm_holder = self.define_internal_local()
        false_label = self.do_label("FALSE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        # Comparar los resultados restando
        assert isinstance(left_vm_holder, LocalNode) and isinstance(
            right_vm_holder, LocalNode)
        self.register_instruction(
            cil.MinusNode(left_vm_holder, right_vm_holder,
                          expr_result_vm_holder))

        self.register_instruction(
            cil.JumpIfGreaterThanZeroNode(expr_result_vm_holder, false_label))
        self.register_instruction(
            cil.IfZeroJump(expr_result_vm_holder, false_label))

        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 1))
        self.register_instruction(cil.UnconditionalJump(end_label))

        self.register_instruction(cil.LabelNode(false_label))
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 0))
        self.register_instruction(cil.LabelNode(end_label))

        return expr_result_vm_holder

    @visit.register
    def _(self, node: coolAst.LowerEqual, scope: Scope) -> LocalNode:
        expr_result_vm_holder = self.define_internal_local()
        false_label = self.do_label("FALSE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        assert isinstance(left_vm_holder, LocalNode) and isinstance(
            right_vm_holder, LocalNode)

        self.register_instruction(
            cil.MinusNode(left_vm_holder, right_vm_holder,
                          expr_result_vm_holder))

        self.register_instruction(
            cil.JumpIfGreaterThanZeroNode(expr_result_vm_holder, false_label))

        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 1))
        self.register_instruction(cil.UnconditionalJump(end_label))

        self.register_instruction(cil.LabelNode(false_label))
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 0))
        self.register_instruction(cil.LabelNode(end_label))

        return expr_result_vm_holder

    @visit.register
    def _(self, node: coolAst.GreaterThanNode, scope: Scope) -> LocalNode:
        expr_result_vm_holder = self.define_internal_local()
        true_label = self.do_label("TRUE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        assert isinstance(left_vm_holder, LocalNode) and isinstance(
            right_vm_holder, LocalNode)

        self.register_instruction(
            cil.MinusNode(left_vm_holder, right_vm_holder,
                          expr_result_vm_holder))

        self.register_instruction(
            cil.JumpIfGreaterThanZeroNode(expr_result_vm_holder, true_label))

        # False Branch
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 0))
        self.register_instruction(cil.UnconditionalJump(end_label))

        # True Branch
        self.register_instruction(cil.LabelNode(true_label))
        self.register_instruction(cil.AssignNode(expr_result_vm_holder, 1))
        self.register_instruction(cil.LabelNode(end_label))

        return expr_result_vm_holder

    @visit.register
    def _(self, node: coolAst.GreaterEqualNode, scope: Scope) -> LocalNode:
        expr_result_vm_holder = self.define_internal_local()
        true_label = self.do_label("TRUE")
        end_label = self.do_label("END")

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # Obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        assert isinstance(left_vm_holder, LocalNode) and isinstance(
            right_vm_holder, LocalNode)

        self.register_instruction(
            cil.MinusNode(left_vm_holder, right_vm_holder,
                          expr_result_vm_holder))

        self.register_instruction(
            cil.JumpIfGreaterThanZeroNode(expr_result_vm_holder, true_label))
        self.register_instruction(
            cil.IfZeroJump(expr_result_vm_holder, true_label))

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

    @visit.register
    def _(self, node: coolAst.FunCall, scope: Scope) -> LocalNode:
        type_vm_holder = self.define_internal_local()
        return_vm_holder = self.define_internal_local()
        # Evaluar la expresion a la izquierda del punto
        expr = self.visit(node.obj, scope)

        assert isinstance(expr, LocalNode) or isinstance(expr, ParamNode)
        self.register_instruction(cil.TypeOfNode(expr, type_vm_holder))

        # Evaluar los argumentos
        for arg in node.args:
            arg_expr = self.visit(arg, scope)
            self.register_instruction(cil.ArgNode(arg_expr))

        self.register_instruction(
            cil.DynamicCallNode(type_vm_holder, node.id, return_vm_holder))

        return return_vm_holder

    @visit.register
    def _(self, node: coolAst.ParentFuncCall, scope: Scope) -> LocalNode:
        local_type_identifier = self.define_internal_local()
        return_expr_vm_holder = self.define_internal_local()

        # Evaluar los argumentos
        for arg in node.arg_list:
            arg_expr = self.visit(arg, scope)
            self.register_instruction(cil.ArgNode(arg_expr))

        # Asignar el tipo a una variable
        type_ = self.context.get_type(node.parent_type)
        self.register_instruction(cil.AssignNode(local_type_identifier, type_))

        self.register_instruction(
            cil.DynamicCallNode(local_type_identifier, node.idx,
                                return_expr_vm_holder))

        return return_expr_vm_holder


class CilDisplayFormatter:
    @singledispatchmethod
    def visit(self, node) -> str:
        return ""

    @visit.register
    def _(self, node: cil.CilProgramNode):
        # Primero imprimir la seccion .TYPES
        dottypes = '\n'.join(self.visit(type_) for type_ in node.dottypes)

        # Imprimir la seccion .DATA
        dotdata = '\n'.join(self.visit(data) for data in node.dotdata)

        # Imprimir la seccion .CODE
        dotcode = '\n'.join(self.visit(code) for code in node.dotcode)

        return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

    @visit.register
    def _(self, node: cil.TypeNode):
        attributes = '\n\t'.join(f'{x}' for x in node.attributes)
        methods = '\n\t'.join(f'method {x}: {y}' for x, y in node.methods)

        return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

    @visit.register
    def _(self, node: cil.FunctionNode):
        params = '\n\t'.join(self.visit(x) for x in node.params)
        localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
        instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

        return f'{node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

    @visit.register
    def _(self, node: cil.ParamNode) -> str:
        return f'PARAM {node.name}'

    @visit.register
    def _(self, node: cil.LocalNode) -> str:
        return f'{node.name}'

    @visit.register
    def _(self, node: cil.AssignNode) -> str:
        return f'{self.visit(node.dest)} = {self.visit(node.source)}'

    @visit.register
    def _(self, node: cil.PlusNode) -> str:
        return f'{self.visit(node.dest)} = {self.visit(node.left)} + {self.visit(node.right)}'

    @visit.register
    def _(self, node: cil.MinusNode) -> str:
        return f'{self.visit(node.dest)} = {self.visit(node.x)} - {self.visit(node.y)}'

    @visit.register
    def _(self, node: cil.StarNode) -> str:
        return f'{self.visit(node.dest)} = {self.visit(node.x)} * {self.visit(node.y)}'

    @visit.register
    def _(self, node: cil.DivNode) -> str:
        return f'{self.visit(node.dest)} = {self.visit(node.left)} / {self.visit(node.right)}'

    @visit.register
    def _(self, node: cil.AllocateNode) -> str:
        return f'{self.visit(node.dest)} = ALLOCATE {node.itype.name}'

    @visit.register
    def _(self, node: cil.TypeOfNode) -> str:
        return f'{self.visit(node.dest)} = TYPEOF {node.variable.name}'

    @visit.register
    def _(self, node: cil.DynamicCallNode) -> str:
        return f'{self.visit(node.dest)} = VCALL {node.xtype.name} {node.method}'

    @visit.register
    def _(self, node: cil.StaticCallNode) -> str:
        return f'{self.visit(node.dest)} = CALL {node.function}'

    @visit.register
    def _(self, node: cil.ArgNode) -> str:
        if isinstance(node.name, int):
            return f'ARG {self.visit(node.name)}'
        else:
            return f'ARG {node.name.name}'

    @visit.register
    def _(self, node: cil.ReturnNode) -> str:
        if isinstance(node.value, int):
            return f'RETURN {node.value}'
        elif isinstance(node.value, LocalNode):
            return f'RETURN {node.value.name}'
        return "RETURN"

    @visit.register
    def _(self, node: cil.DataNode) -> str:
        if isinstance(node.value, str):
            return f'{node.name} = "{node.value}" ;'
        elif isinstance(node.value, list):
            data = "\n\t".join(str(x) for x in node.value)
            return f'{node.name} = {data}'
        return f'{node.name} = {node.value}'

    @visit.register
    def _(self, node: cil.GetTypeIndex) -> str:
        return f'{node.dest} = GETTYPEINDEX {node.itype}'

    @visit.register
    def _(self, node: cil.TdtLookupNode) -> str:
        return f'{node.dest.name} = TYPE_DISTANCE {node.i} {node.j}'

    @visit.register
    def _(self, node: cil.IfZeroJump) -> str:
        return f'IF_ZERO {node.variable.name} GOTO {node.label}'

    @visit.register
    def _(self, node: cil.UnconditionalJump) -> str:
        return f'GOTO {node.label}'

    @visit.register
    def _(self, node: cil.JumpIfGreaterThanZeroNode) -> str:
        return f'IF_GREATER_ZERO {node.variable.name} GOTO {node.label}'

    @visit.register
    def _(self, node: cil.LabelNode) -> str:
        return f'{node.label}:'

    @visit.register
    def _(self, node: int) -> str:
        return str(node)

    @visit.register
    def _(self, node: cil.GetAttributeNode):
        return f'{node.dest.name} = GETATTRIBUTE {node.attrname} {node.itype.name}'

    def __call__(self, node) -> str:
        return self.visit(node)
