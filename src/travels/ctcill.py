from re import L
from abstract.semantics import Context, Type
from abstract.tree import (
    AttributeDef,
    ClassDef,
    EqualToNode,
    IsVoidNode,
    MethodDef,
    NotNode,
    SelfNode,
)
import cil.baseCilVisitor as baseCilVisitor
import abstract.tree as coolAst
import abstract.semantics as semantics
from typing import List, Optional, Tuple
from functools import singledispatchmethod
import re

import cil.nodes

from cil.nodes import (
    AbortNode,
    AllocateBoolNode,
    AllocateIntNode,
    AllocateNode,
    AllocateStringNode,
    ArgNode,
    AssignNode,
    BitwiseNotNode,
    CharToCharStringCompare,
    CilNode,
    CilProgramNode,
    CompareSTRType,
    CompareStringLengthNode,
    CompareType,
    ConcatString,
    DataNode,
    DivNode,
    DynamicCallNode,
    EqualToCilNode,
    FunctionNode,
    GetAttributeNode,
    GetTypeIndex,
    GetValue,
    IfZeroJump,
    InitSelfNode,
    InstructionNode,
    JumpIfGreater,
    JumpIfGreaterThanZeroNode,
    LabelNode,
    LoadNode,
    LocalNode,
    MinusNode,
    MinusNodeComp,
    NotZeroJump,
    ParamNode,
    PlusNode,
    PrintIntNode,
    PrintNode,
    PureMinus,
    ReadIntNode,
    ReadNode,
    ReferenceEqualNode,
    RestoreSelf,
    ReturnNode,
    SaveSelf,
    SetAttributeNode,
    StarNode,
    StaticCallNode,
    SubstringNode,
    TdtLookupNode,
    TypeName,
    TypeNode,
    TypeOffsetNode,
    UnconditionalJump,
)


def find_min_i(vtables: List[List[Tuple[str, str]]], method: str):
    return min(
        [i for vtable in vtables for i, (m, _) in enumerate(vtable) if m == method]
    )


def sort_methods_tables(vtables: List[List[Tuple[str, str]]]):
    methods = set([m for v in vtables for m, _ in v])
    new_tables = [[] for _ in vtables]
    for m in methods:
        for i, vtable in enumerate(vtables):
            if m in [x for x, _ in vtable]:
                name = next(n for x, n in vtable if x == m)
                new_tables[i].append((m, name))
            else:
                new_tables[i].append(("__not_a_func", "dummy"))
    return new_tables


def find_method_in_parent(type_: Type, method: str, typeNodes: List[TypeNode]):
    methods = []
    if type_.parent is not None:
        parent = next(n for n in typeNodes if n.name == type_.name)
        methods = [m for _, m in parent.methods]
    if type_.parent is None or f"function_{method}_at_{type_.name}" in methods:
        return type_
    return find_method_in_parent(type_.parent, method, typeNodes)


ExpressionReturn = Tuple[List[InstructionNode], List[LocalNode]]
Scope = semantics.Scope


class CoolToCILVisitor(baseCilVisitor.BaseCoolToCilVisitor):
    @singledispatchmethod
    def visit(self, node, scope: Scope) -> CilNode:
        # Devolver un nodo vacio, al final este metodo no
        # se debe llamar nunca.
        return CilNode()

    @visit.register
    def _(self, node: coolAst.ProgramNode, scope: Scope) -> CilProgramNode:

        # Definir el punto de entrada del programa.
        self.current_function = self.register_function("entry")
        instance = self.define_internal_local()
        result = self.define_internal_local()

        # El primer metodo que se invoca es el metodo main de la clase Main

        # Reservar memoria para el objeto Main
        main_type = self.context.get_type("Main")
        self.register_instruction(AllocateNode(main_type, instance))
        self.register_instruction(InitSelfNode(instance))

        # Llamar al metodo main
        self.register_instruction(StaticCallNode(instance, main_type, "main", result))
        self.register_instruction(ReturnNode(0))
        self.current_function = None

        class_list = self.topological_sort_classDefs(node.class_list)
        # Ordenar los scopes
        children = []
        for x in class_list:
            i = next(i for i, c in enumerate(node.class_list) if c.idx == x.idx)
            children.append(scope.children[i])

        for c in class_list:
            self.register_type(c.idx)

        for klass, child_scope in zip(class_list, children):
            self.visit(klass, child_scope)

        # print("\n".join(str(x) for x in sort_methods_tables([t.methods for t in self.dot_types])))
        new_vtable = sort_methods_tables([t.methods for t in self.dot_types])
        for i in range(len(self.dot_types)):
            self.dot_types[i].methods = new_vtable[i]

        return CilProgramNode(self.dot_types, self.dot_data, self.dot_code)

    #  *************** IMPLEMENTACION DE LAS DEFINICIONES DE CLASES *****************

    @visit.register
    def _(self, node: coolAst.ClassDef, scope: Scope) -> None:
        # Registrar el tipo que creamos en .Types section
        self.current_type = self.context.get_type(node.idx)
        new_type_node = next(x for x in self.dot_types if x.name == node.idx)

        methods = self.current_type.methods
        attributes = self.current_type.attributes

        # Manejar los features heredados como atributos y metodos
        if self.current_type.parent is not None:
            for attribute in self.current_type.parent.attributes:
                new_type_node.attributes.append(attribute)

            parent = next(
                t for t in self.dot_types if t.name == self.current_type.parent.name
            )

            for method, _ in parent.methods:
                # Manejar la redefinicion de metodos
                if method not in methods:
                    new_type_node.methods.append(
                        (
                            method,
                            self.to_function_name(
                                method,
                                find_method_in_parent(
                                    self.current_type.parent, method, self.dot_types
                                ).name,
                            ),
                        )
                    )
                else:
                    new_type_node.methods.append(
                        (method, self.to_function_name(method, node.idx))
                    )

        defined_methods = [x for x, _ in new_type_node.methods]

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
            if attribute not in self.current_type.parent.attributes:
                new_type_node.attributes.append(attribute)

        for method in methods:
            if method not in defined_methods:
                new_type_node.methods.append(
                    (method, self.to_function_name(method, node.idx))
                )

        attrib = [x for x in node.features if isinstance(x, AttributeDef)]
        meth = [x for x in node.features if isinstance(x, MethodDef)]
        features = attrib + meth

        self.current_type.attributes = new_type_node.attributes

        for f, s in zip(features, scope.children):
            self.visit(f, s)

        self.current_type = None

    # ******************  IMPLEMENTACION DE LAS DEFINICIONES DE METODOS ******************

    @visit.register
    def _(self, node: coolAst.AttributeDef, scope: Scope) -> None:
        self.current_function = self.register_function(
            f"__{self.current_type.name}__attrib__{node.idx}__init"
        )
        local = self.define_internal_local()
        if node.default_value is not None:
            # Generar el codigo de la expresion de inicializacion
            # y devolver el valor de esta
            value = self.visit(node.default_value, scope)
            self.register_instruction(ReturnNode(value))

        else:
            # Si no tiene expresion de inicializacion entonces devolvemos
            # 0 en caso de que sea Int, Bool u otro tipo excepto String
            # (0 = false y 0 = void)
            # attribute_type = self.context.get_type(node.typex)
            attribute_type = scope.find_variable(node.idx).type
            if attribute_type.name == "String":
                self.register_instruction(AllocateStringNode(local, self.null, 0))
                self.register_instruction(ReturnNode(local))
            elif attribute_type.name == "Bool":
                self.register_instruction(AllocateBoolNode(local, 0))
                self.register_instruction(ReturnNode(local))
            elif attribute_type.name == "Int":
                self.register_instruction(AllocateIntNode(local, 0))
                self.register_instruction(ReturnNode(local))
            else:
                self.register_instruction(ReturnNode(0))

    @visit.register
    def _(self, node: coolAst.MethodDef, scope: Scope) -> None:
        self.current_method = self.current_type.get_method(node.idx)

        # Registrar la nueva funcion en .CODE
        function_node = self.register_function(
            self.to_function_name(node.idx, self.current_type.name)
        )

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
            self.register_instruction(ReturnNode(last))
        else:
            self.register_instruction(ReturnNode())

        self.current_method = None
        self.current_function = None

    # **************   IMPLEMENTACION DE LAS EXPRESIONES CONDICIONAES (IF, WHILE, CASE) Y LAS DECLARACIONES
    #                  DE VARIABLES (let)
    # **************

    @visit.register
    def _(self, node: coolAst.IfThenElseNode, scope: Scope):  # noqa: F811
        # Crear un LABEL al cual realizar un salto.
        false_label = self.do_label("FALSEIF")
        end_label = self.do_label("ENDIF")
        cond_value = self.define_internal_local()
        return_expr = self.define_internal_local()

        # Salvar las instrucciones relacionadas con la condicion,
        # cada expresion retorna el nombre de la variable interna que contiene el valor ??
        internal_cond_vm_holder = self.visit(node.cond, scope)

        # Condicion es un Bool
        self.register_instruction(GetValue(cond_value, internal_cond_vm_holder))

        # Chequear y saltar si es necesario.
        self.register_instruction(IfZeroJump(cond_value, false_label))

        # Salvar las instrucciones relacionadas con la rama TRUE.
        expr = self.visit(node.expr1, scope)
        self.register_instruction(AssignNode(return_expr, expr))

        self.register_instruction(UnconditionalJump(end_label))

        # Registrar las instrucciones relacionadas con la rama ELSE
        self.register_instruction(LabelNode(false_label))
        expr2 = self.visit(node.expr2, scope)
        self.register_instruction(AssignNode(return_expr, expr2))

        self.register_instruction(LabelNode(end_label))

        return return_expr

    @visit.register
    def _(self, node: coolAst.VariableDeclaration, scope: Scope) -> CilNode:
        for var_idx, var_type, var_init_expr, _, _ in node.var_list:

            # Registrar las variables en orden.
            var_info = scope.find_variable(var_idx)
            assert var_info is not None, f"Var not found {var_idx}"
            local_var = self.register_local(var_info)

            # Reservar memoria para la variable y realizar su inicializacion si tiene
            assert var_info.type is not None

            # Si la variable es int, string o boolean, su valor por defecto es 0
            if var_info.type.name not in ("String", "Int", "Bool"):
                self.register_instruction(AssignNode(local_var, 0))
            elif var_info.type.name == "String":
                self.register_instruction(AllocateStringNode(local_var, self.null, 0))
            elif var_info.type.name == "Int":
                self.register_instruction(AllocateIntNode(local_var, 0))
            elif var_info.type.name == "Bool":
                self.register_instruction(AllocateBoolNode(local_var, 0))

            if var_init_expr is not None:
                expr_init_vm_holder = self.visit(var_init_expr, scope)
                # Assignar el valor correspondiente a la variable reservada
                self.register_instruction(AssignNode(local_var, expr_init_vm_holder))

        # Compute the associated expr, if any, to the let declaration
        # A block defines a new scope, so it is important to manage it
        return self.visit(node.block_statements, scope)

    @visit.register
    def _(self, node: coolAst.VariableCall, scope: Scope):
        return self.visit(node.idx, scope)

    @visit.register
    def _(self, node: coolAst.InstantiateClassNode, scope: Scope) -> LocalNode:
        # Reservar una variable que guarde la nueva instancia
        type_ = self.context.get_type(node.type_)
        instance_vm_holder = self.define_internal_local()

        if type_.name not in ("String", "Int", "Bool"):
            self.register_instruction(AllocateNode(type_, instance_vm_holder))
        elif type_.name == "String":
            self.register_instruction(
                AllocateStringNode(instance_vm_holder, self.null, 0)
            )
        elif type_.name == "Int":
            self.register_instruction(AllocateIntNode(instance_vm_holder, 0))
        elif type_.name == "Bool":
            self.register_instruction(AllocateBoolNode(instance_vm_holder, 0))

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
        rvalue_vm_holder = self.visit(node.expr, scope)
        var_inf = scope.find_variable(node.idx)

        # Es necesario diferenciar entre variable y atributo.
        # Las variables se diferencian en si son locales al
        # metodo que estamos creando o si son atributos.
        if var_inf.location == "PARAM":
            # Buscar la variable en los parametros
            var = next(
                v
                for v in self.params
                if f"param_{self.current_function.name[9:]}_{var_inf.name}_" in v.name
            )
            # registrar la instruccion de asignacion
            self.register_instruction(AssignNode(var, rvalue_vm_holder))
        elif var_inf.location == "LOCAL":
            var = next(
                v
                for v in list(reversed(self.localvars))
                if f"local_{self.current_function.name[9:]}_{var_inf.name}_" in v.name
            )
            self.register_instruction(AssignNode(var, rvalue_vm_holder))
        else:
            assert self.current_type is not None
            self.register_instruction(
                SetAttributeNode(self.current_type, node.idx, rvalue_vm_holder)
            )

    @visit.register
    def _(self, node: str, scope: Scope):
        var_inf = scope.find_variable(node)

        # Es necesario diferenciar entre variable y atributo.
        # Las variables se diferencian en si son locales al
        # metodo que estamos creando o si son atributos.
        if var_inf.location == "PARAM":
            # Buscar la variable en los parametros
            var = next(
                v
                for v in self.params
                if f"param_{self.current_function.name[9:]}_{var_inf.name}_" in v.name
            )
            # registrar la instruccion de asignacion
            return var
        elif var_inf.location == "LOCAL":
            var = next(
                v
                for v in list(reversed(self.localvars))
                if f"local_{self.current_function.name[9:]}_{var_inf.name}_" in v.name
            )
            return var
        else:
            local = self.define_internal_local()
            assert self.current_type is not None
            self.register_instruction(
                GetAttributeNode(self.current_type, var_inf.name, local)
            )
            return local

    @visit.register
    def _(self, node: coolAst.WhileBlockNode, scope: Scope):
        # Evaluar la condicion y definir un LABEL al cual
        # retornar
        cond_value = self.define_internal_local()
        while_label = self.do_label("WHILE")
        end_label = self.do_label("WHILE_END")
        self.register_instruction(LabelNode(while_label))
        cond_vm_holder = self.visit(node.cond, scope)

        # Lo que viene en cond es un Bool
        self.register_instruction(GetValue(cond_value, cond_vm_holder))

        # Probar la condicion, si es true continuar la ejecucion, sino saltar al LABEL end
        self.register_instruction(IfZeroJump(cond_value, end_label))

        # Registrar las instrucciones del cuerpo del while
        self.visit(node.statements, scope)

        # Realizar un salto incondicional al chequeo de la condicion
        self.register_instruction(UnconditionalJump(while_label))
        # Registrar el LABEL final
        self.register_instruction(LabelNode(end_label))

    @visit.register
    def _(self, node: coolAst.CaseNode, scope: Scope):
        # Evalauar la expr0
        expr_vm_holder = self.visit(node.expression, scope)

        # Almacenar el tipo del valor retornado
        type_internal_local_holder = self.define_internal_local()
        sub_vm_local_holder = self.define_internal_local()
        result_vm_holder = self.define_internal_local()

        self.register_instruction(
            TypeOffsetNode(expr_vm_holder, type_internal_local_holder)
        )

        # Variables internas para almacenar resultados intermedios
        min_ = self.define_internal_local()
        tdt_result = self.define_internal_local()

        self.register_instruction(AssignNode(min_, len(self.context.types)))

        for i, action_node in enumerate(node.actions):
            # Calcular la distancia hacia el tipo, y actualizar el minimo de ser necesario
            self.register_instruction(
                TdtLookupNode(action_node.typex, type_internal_local_holder, tdt_result)
            )

            not_min_label = self.do_label(f"Not_min{i}")

            # Comparar el resultado obtenido con el minimo actual.
            self.register_instruction(JumpIfGreater(tdt_result, min_, not_min_label))

            # Si mejora el minimo, entonces actualizarlo.
            self.register_instruction(AssignNode(min_, tdt_result))
            self.register_instruction(LabelNode(not_min_label))

        # Ya tenemos la menor distancia entre el tipo calculado en la expr0, y todos los tipos definidos
        # en los branches del case.
        # Comprobar que tengamos una coincidencia
        self.register_instruction(AssignNode(tdt_result, len(self.context.types)))
        self.register_instruction(
            ReferenceEqualNode(tdt_result, min_, sub_vm_local_holder)
        )
        error_label = self.do_label("ERROR")
        self.register_instruction(IfZeroJump(sub_vm_local_holder, error_label))

        end_label = self.do_label("END")

        # Procesar cada accion y ejecutar el tipo cuya distancia sea igual a min_
        for i, (action_node, s) in enumerate(zip(node.actions, scope.children)):
            next_label = self.do_label(f"NEXT{i}")
            self.register_instruction(
                TdtLookupNode(action_node.typex, type_internal_local_holder, tdt_result)
            )
            self.register_instruction(JumpIfGreater(tdt_result, min_, next_label))
            # Implemententacion del branch.
            # Registrar la variable <idk>
            var_info = s.find_variable(action_node.idx)
            assert var_info is not None
            idk = self.register_local(var_info)
            # Asignar al identificador idk el valor de expr0
            self.register_instruction(AssignNode(idk, expr_vm_holder))
            # Generar el codigo de la expresion asociada a esta rama
            expr_val_vm_holder = self.visit(action_node.actions, s)
            # Salvar el resultado
            self.register_instruction(AssignNode(result_vm_holder, expr_val_vm_holder))
            # Generar un salto de modo que no se chequee otra rama
            self.register_instruction(UnconditionalJump(end_label))
            self.register_instruction(LabelNode(next_label))

        self.register_instruction(LabelNode(error_label))
        self.register_instruction(TypeName(expr_vm_holder))
        self.register_instruction(
            AbortNode(expr_vm_holder, self.abortion, self.newLine)
        )

        self.register_instruction(LabelNode(end_label))
        return result_vm_holder

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
            PlusNode(sum_internal_local, left_vm_holder, right_vm_holder)
        )

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

        self.register_instruction(
            MinusNode(left_vm_holder, right_vm_holder, minus_internal_vm_holder)
        )

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

        # Registrar la instruccion de multimplicacion
        self.register_instruction(
            StarNode(left_vm_holder, right_vm_holder, mul_internal_vm_holder)
        )

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
            DivNode(div_internal_vm_holder, left_vm_holder, right_vm_holder)
        )

        # Devolver el resultado
        return div_internal_vm_holder

    # *********************  IMPLEMENTACION DE LAS CONSTANTES
    #
    # *********************

    @visit.register
    def _(self, node: coolAst.IntegerConstant, scope: Scope):
        # devolver el valor
        return_vm_holder = self.define_internal_local()
        self.register_instruction(AllocateIntNode(return_vm_holder, int(node.lex)))
        return return_vm_holder

    @visit.register
    def _(self, node: coolAst.StringConstant, scope: Scope) -> LocalNode:
        # Variable interna que apunta al string
        str_const_vm_holder = self.define_internal_local()

        # Registrar el string en la seccion de datos
        s1 = self.register_data(node.lex)

        pluses = len(re.findall(r"\\n", node.lex)) + 2

        # Cargar el string en la variable interna
        self.register_instruction(
            AllocateStringNode(str_const_vm_holder, s1, len(node.lex) - pluses)
        )

        # Devolver la variable que contiene el string
        return str_const_vm_holder

    @visit.register
    def _(self, node: coolAst.TrueConstant, scope: Scope):
        # variable interna que devuelve el valor de la constante
        expr = self.define_internal_local()
        self.register_instruction(AllocateBoolNode(expr, 1))
        return expr

    @visit.register
    def _(self, node: coolAst.FalseConstant, scope: Scope):
        # variable interna que devuelve el valor de la constante
        expr = self.define_internal_local()
        self.register_instruction(AllocateBoolNode(expr, 0))
        return expr

    # *******************  Implementacion de las comparaciones ********************
    # Todas las operaciones de comparacion devuelven 1 si el resultado es verdadero,
    # o 0 si es falso.
    # *******************

    @visit.register
    def _(self, node: coolAst.NegNode, scope: Scope):
        # Obtener el valor de la expresion
        expr_result = self.visit(node.lex, scope)
        result_vm_holder = self.define_internal_local()

        if isinstance(expr_result, int):
            self.register_instruction(
                AssignNode(result_vm_holder, abs(expr_result - 1))
            )
            return result_vm_holder
        else:
            false_label = self.do_label("FALSE")
            not_end_label = self.do_label("NOT_END")
            assert isinstance(expr_result, LocalNode)
            self.register_instruction(GetValue(expr_result, expr_result))
            # Si expr = 0 entonces devolver 1
            self.register_instruction(IfZeroJump(expr_result, false_label))
            # Si expr = 1 devolver 0
            self.register_instruction(AllocateBoolNode(result_vm_holder, 0))
            self.register_instruction(UnconditionalJump(not_end_label))
            self.register_instruction(LabelNode(false_label))
            # Si expr = 0 entonces devolver 1
            self.register_instruction(AllocateBoolNode(result_vm_holder, 1))
            self.register_instruction(LabelNode(not_end_label))
            return result_vm_holder

    @visit.register
    def _(self, node: coolAst.EqualToNode, scope: Scope) -> LocalNode:
        expr_result_vm_holder = self.define_internal_local()
        temp_expr_vm_holder = self.define_internal_local()

        # Obtener el valor de la expresion izquierda
        left_vm_holder = self.visit(node.left, scope)

        # obtener el valor de la expresion derecha
        right_vm_holder = self.visit(node.right, scope)

        false_ = self.do_label("FALSE")
        true_ = self.do_label("TRUE")
        end = self.do_label("END")
        compare_string = self.do_label("COMPARE_STRING")
        compare_by_value = self.do_label("COMPARE_BY_VALUE")
        continue_ = self.do_label("CONTINUE")
        while_label = self.do_label("WHILE_STR_COMP")
        end_while_label = self.do_label("WHILE_STR_COMP_END")

        # Si left es un string realizar la comparacion entre strings
        # si no realizar una resta y devolver el resultado

        # Si right = void o left = void (0) devolver false
        self.register_instruction(IfZeroJump(left_vm_holder, false_))
        self.register_instruction(IfZeroJump(right_vm_holder, false_))

        # Si es un string comparar char a char
        self.register_instruction(CompareSTRType(temp_expr_vm_holder, left_vm_holder))
        # CompareType devuelve 0 para True y 1 para False
        self.register_instruction(IfZeroJump(temp_expr_vm_holder, compare_string))
        # No es un string, comparar por valor si es bool o int
        self.register_instruction(
            CompareType(temp_expr_vm_holder, left_vm_holder, "Bool")
        )
        self.register_instruction(IfZeroJump(temp_expr_vm_holder, compare_by_value))

        self.register_instruction(
            CompareType(temp_expr_vm_holder, left_vm_holder, "Int")
        )
        self.register_instruction(IfZeroJump(temp_expr_vm_holder, compare_by_value))

        # Comparar por referencia
        self.register_instruction(
            ReferenceEqualNode(left_vm_holder, right_vm_holder, temp_expr_vm_holder)
        )
        self.register_instruction(IfZeroJump(temp_expr_vm_holder, true_))
        self.register_instruction(UnconditionalJump(false_))

        self.register_instruction(LabelNode(compare_by_value))
        self.register_instruction(
            MinusNodeComp(left_vm_holder, right_vm_holder, temp_expr_vm_holder)
        )
        self.register_instruction(IfZeroJump(temp_expr_vm_holder, true_))
        self.register_instruction(UnconditionalJump(false_))

        self.register_instruction(LabelNode(compare_string))
        self.register_instruction(
            CompareStringLengthNode(
                temp_expr_vm_holder, left_vm_holder, right_vm_holder
            )
        )
        # Compare devuelve 0 para true y 1 para true
        self.register_instruction(IfZeroJump(temp_expr_vm_holder, continue_))
        self.register_instruction(UnconditionalJump(false_))

        # Los lengths son iguales, seguir comparando
        self.register_instruction(LabelNode(continue_))
        self.register_instruction(
            CharToCharStringCompare(
                temp_expr_vm_holder,
                left_vm_holder,
                right_vm_holder,
                while_label,
                end_while_label,
            )
        )
        self.register_instruction(IfZeroJump(temp_expr_vm_holder, true_))

        self.register_instruction(LabelNode(false_))
        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 0))
        self.register_instruction(UnconditionalJump(end))

        self.register_instruction(LabelNode(true_))
        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 1))
        self.register_instruction(LabelNode(end))

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

        self.register_instruction(
            MinusNodeComp(left_vm_holder, right_vm_holder, expr_result_vm_holder)
        )

        self.register_instruction(
            JumpIfGreaterThanZeroNode(expr_result_vm_holder, false_label)
        )
        self.register_instruction(IfZeroJump(expr_result_vm_holder, false_label))

        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 1))
        self.register_instruction(UnconditionalJump(end_label))

        self.register_instruction(LabelNode(false_label))
        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 0))
        self.register_instruction(LabelNode(end_label))

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

        self.register_instruction(
            MinusNodeComp(left_vm_holder, right_vm_holder, expr_result_vm_holder)
        )

        self.register_instruction(
            JumpIfGreaterThanZeroNode(expr_result_vm_holder, false_label)
        )

        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 1))
        self.register_instruction(UnconditionalJump(end_label))

        self.register_instruction(LabelNode(false_label))
        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 0))
        self.register_instruction(LabelNode(end_label))

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
            right_vm_holder, LocalNode
        )

        self.register_instruction(
            MinusNodeComp(left_vm_holder, right_vm_holder, expr_result_vm_holder)
        )

        self.register_instruction(
            JumpIfGreaterThanZeroNode(expr_result_vm_holder, true_label)
        )

        # False Branch
        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 0))
        self.register_instruction(UnconditionalJump(end_label))

        # True Branch
        self.register_instruction(LabelNode(true_label))
        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 1))
        self.register_instruction(LabelNode(end_label))

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
            right_vm_holder, LocalNode
        )

        self.register_instruction(
            MinusNodeComp(left_vm_holder, right_vm_holder, expr_result_vm_holder)
        )

        self.register_instruction(
            JumpIfGreaterThanZeroNode(expr_result_vm_holder, true_label)
        )
        self.register_instruction(IfZeroJump(expr_result_vm_holder, true_label))

        # False Branch
        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 0))
        self.register_instruction(UnconditionalJump(end_label))

        # True Branch
        self.register_instruction(LabelNode(true_label))
        self.register_instruction(AllocateBoolNode(expr_result_vm_holder, 1))
        self.register_instruction(LabelNode(end_label))

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

        self.register_instruction(AssignNode(type_vm_holder, expr))

        self.register_instruction(SaveSelf())

        # Evaluar los argumentos
        for arg in node.args:
            arg_expr = self.visit(arg, scope)
            self.register_instruction(ArgNode(arg_expr))

        self.register_instruction(
            DynamicCallNode(type_vm_holder, node.id, return_vm_holder)
        )

        self.register_instruction(RestoreSelf())

        return return_vm_holder

    @visit.register
    def _(self, node: coolAst.ParentFuncCall, scope: Scope) -> LocalNode:
        return_expr_vm_holder = self.define_internal_local()

        # Evaluar el objeto sobre el que se llama la funcion
        obj_dispatched = self.visit(node.obj, scope)

        self.register_instruction(SaveSelf())

        # Evaluar los argumentos
        for arg in node.arg_list:
            arg_expr = self.visit(arg, scope)
            self.register_instruction(ArgNode(arg_expr))

        # Asignar el tipo a una variable
        type_ = self.context.get_type(node.parent_type)
        self.register_instruction(
            StaticCallNode(obj_dispatched, type_, node.idx, return_expr_vm_holder)
        )

        self.register_instruction(RestoreSelf())

        return return_expr_vm_holder

    @visit.register
    def _(self, node: SelfNode, scope: Scope) -> LocalNode:
        return_expr_vm_holder = self.define_internal_local()
        self.register_instruction(cil.nodes.SelfNode(return_expr_vm_holder))
        return return_expr_vm_holder

    @visit.register
    def _(self, node: IsVoidNode, scope: Scope):
        return_bool_vm_holder = self.define_internal_local()
        val = self.visit(node.expr, scope)
        true_label = self.do_label("TRUE")
        end_label = self.do_label("END")
        self.register_instruction(IfZeroJump(val, true_label))
        # Bool con valor false
        self.register_instruction(AllocateBoolNode(return_bool_vm_holder, 0))
        self.register_instruction(UnconditionalJump(end_label))
        self.register_instruction(LabelNode(true_label))
        self.register_instruction(AllocateBoolNode(return_bool_vm_holder, 1))
        self.register_instruction(LabelNode(end_label))
        return return_bool_vm_holder

    @visit.register
    def _(self, node: NotNode, scope: Scope):
        expr = self.define_internal_local()
        result = self.visit(node.lex, scope)
        self.register_instruction(BitwiseNotNode(result, expr))
        self.register_instruction(AllocateIntNode(expr, expr))
        return expr


class CilDisplayFormatter:
    @singledispatchmethod
    def visit(self, node) -> str:
        return ""

    @visit.register
    def _(self, node: CilProgramNode):
        # Primero imprimir la seccion .TYPES
        dottypes = "\n".join(self.visit(type_) for type_ in node.dottypes)

        # Imprimir la seccion .DATA
        dotdata = "\n".join(self.visit(data) for data in node.dotdata)

        # Imprimir la seccion .CODE
        dotcode = "\n".join(self.visit(code) for code in node.dotcode)

        return f".TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}"

    @visit.register
    def _(self, node: TypeNode):
        attributes = "\n\t".join(f"{x}" for x in node.attributes)
        methods = "\n\t".join(f"method {x}: {y}" for x, y in node.methods)

        return f"type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}"

    @visit.register
    def _(self, node: FunctionNode):
        params = "\n\t".join(self.visit(x) for x in node.params)
        localvars = "\n\t".join(self.visit(x) for x in node.localvars)
        instructions = "\n\t".join(self.visit(x) for x in node.instructions)

        return f"{node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}"

    @visit.register
    def _(self, node: ParamNode) -> str:
        return f"PARAM {node.name}"

    @visit.register
    def _(self, node: LocalNode) -> str:
        return f"{node.name}"

    @visit.register
    def _(self, node: AssignNode) -> str:
        return f"{self.visit(node.dest)} = {self.visit(node.source)}"

    @visit.register
    def _(self, node: PlusNode) -> str:
        return f"{self.visit(node.dest)} = {self.visit(node.left)} + {self.visit(node.right)}"

    @visit.register
    def _(self, node: MinusNode) -> str:
        return f"{self.visit(node.dest)} = {self.visit(node.x)} - {self.visit(node.y)}"

    @visit.register
    def _(self, node: StarNode) -> str:
        return f"{self.visit(node.dest)} = {self.visit(node.x)} * {self.visit(node.y)}"

    @visit.register
    def _(self, node: DivNode) -> str:
        return f"{self.visit(node.dest)} = {self.visit(node.left)} / {self.visit(node.right)}"

    @visit.register
    def _(self, node: AllocateNode) -> str:
        return f"{self.visit(node.dest)} = ALLOCATE {node.itype.name}"

    @visit.register
    def _(self, node: TypeOffsetNode) -> str:
        return f"{self.visit(node.dest)} = TYPEOF {node.variable.name}"

    @visit.register
    def _(self, node: DynamicCallNode) -> str:
        return f"{self.visit(node.dest)} = VCALL {node.xtype.name} {node.method}"

    @visit.register
    def _(self, node: StaticCallNode) -> str:
        return f"{self.visit(node.dest)} = CALL {node.function}"

    @visit.register
    def _(self, node: ArgNode) -> str:
        if isinstance(node.name, int):
            return f"ARG {self.visit(node.name)}"
        else:
            return f"ARG {node.name.name}"

    @visit.register
    def _(self, node: ReturnNode) -> str:
        if isinstance(node.value, int):
            return f"RETURN {node.value}"
        elif isinstance(node.value, LocalNode):
            return f"RETURN {node.value.name}"
        return "RETURN"

    @visit.register
    def _(self, node: DataNode) -> str:
        if isinstance(node.value, str):
            return f'{node.name} = "{node.value}" ;'
        elif isinstance(node.value, list):
            data = "\n\t".join(str(x) for x in node.value)
            return f"{node.name} = {data}"
        return f"{node.name} = {node.value}"

    @visit.register
    def _(self, node: GetTypeIndex) -> str:
        return f"{node.dest} = GETTYPEINDEX {node.itype}"

    @visit.register
    def _(self, node: TdtLookupNode) -> str:
        return f"{node.dest.name} = TYPE_DISTANCE {node.i} {node.j}"

    @visit.register
    def _(self, node: IfZeroJump) -> str:
        return f"IF_ZERO {node.variable.name} GOTO {node.label}"

    @visit.register
    def _(self, node: UnconditionalJump) -> str:
        return f"GOTO {node.label}"

    @visit.register
    def _(self, node: JumpIfGreaterThanZeroNode) -> str:
        return f"IF_GREATER_ZERO {node.variable.name} GOTO {node.label}"

    @visit.register
    def _(self, node: LabelNode) -> str:
        return f"{node.label}:"

    @visit.register
    def _(self, node: int) -> str:
        return str(node)

    @visit.register
    def _(self, node: GetAttributeNode):
        return f"{node.dest.name} = GETATTRIBUTE {node.attrname} {node.itype.name}"

    @visit.register
    def _(self, node: cil.nodes.SelfNode):
        return f"{node.dest.name} = SELF"

    @visit.register
    def _(self, node: NotNode):
        return f"NOT {node.src.name}"

    @visit.register
    def _(self, node: PrintIntNode):
        return f"PRINT_INT {node.src.name}"

    @visit.register
    def _(self, node: ReadIntNode):
        return f"{node.dest.name} = READ_INT"

    @visit.register
    def _(self, node: ReadNode):
        return f"{node.dest.name} = READ_STR"

    @visit.register
    def _(self, node: PrintNode):
        return f"PRINT_STR {node.src.name}"

    @visit.register
    def _(self, node: SubstringNode):
        return f"{self.visit(node.dest)} = SUBSTRING {self.visit(node.l)} {self.visit(node.r)} self"

    @visit.register
    def _(self, node: ConcatString):
        return f"{self.visit(node.dest)} = self.CONCAT {node.s}"

    def __call__(self, node) -> str:
        return self.visit(node)
