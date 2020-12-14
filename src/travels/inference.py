from functools import singledispatchmethod
from typing import List, Optional

import abstract.semantics as semantic
import abstract.tree as coolAst
from abstract.semantics import Scope, SemanticError, Type
from abstract.tree import ActionNode, AttributeDef, CaseNode, IsVoidNode, MethodDef, ParentFuncCall, SelfNode
from travels.context_actions import (
    update_attr_type,
    update_method_param,
    update_scope_variable,
)

void = semantic.VoidType()

def get_type_attribute_chain(type_: Type):
    if type_.name == "Object":
        return []
    else:
        assert type_.parent is not None
        return type_.attributes + get_type_attribute_chain(type_.parent)


def find_common_parent(e1, e2):
    if e1.conforms_to(e2):
        return e2
    elif e2.conforms_to(e1):
        return e1
    else:
        e1_types: List[Type] = []
        while e1:
            e1_types.append(e1.parent)
            e1 = e1.parent

        while e2 not in e1_types:
            e2 = e2.parent
        return e2
        # e1_parent = e1.parent
        # e2_parent = e2.parent
        # while e2_parent != e1_parent:
        #     if e1_parent.name != "Object":
        #         e1_parent = e1_parent.parent
        #     if e2_parent.name != "Object":
        #         e2_parent = e2_parent.parent
        # return e1_parent


def TypeError(s, l, c):
    return f"({l}, {c}) - TypeError: {s}"


class TypeInferer:
    """
    Para inferir los tipos en un programa se aprovecha el AST devuelto al evaluar el parse de dicho programa.
    Para este propósito, se toma el programa como una gran expresión, y entonces se realiza un recorrido en bottom-up
    para inferir los tipos de las subexpresiones que sean necesarias. Empezando por las hojas que corresponden a las constantes
    y tipos previamente definidos, que por supuesto ya tienen su tipo bien calculado, se procede a ir subiendo por el árbol
    calculando el tipo de cada subexpresión en dependencia de su regla funcional y de los tipos previamente calculados
    en el contexto del programa. Como ejemplo tomemos el de la expresion  "if bool then e1 else e2":

    La regla de dicha expresion se puede representar como :
    C|-bool: BOLEAN, C|-e1:T1, C|-e2:T2
    --------------------------------------
        C|- if bool then e1 else e2: T3
    donde T1 <= T2 <= T3.

    O sea que si en el contexto conocemos el tipo de e1 y el de e2 y además aseguramos que bool es una expresión de tipo
    BOLEAN entonces el tipo de la expresión completa sera el Ancestro Común Mas Cercano  a los tipos T1 y T2, o en otras palabras,
    el menor tipo T3 tal que T1 se conforme en T3 y T2 se conforme en T3.
    """

    def __init__(self, context: semantic.Context, errors=[]):
        self.context: semantic.Context = context
        self.current_type: Optional[semantic.Type] = None
        self.INTEGER = self.context.get_type("Int")
        self.OBJECT = self.context.get_type("Object")
        self.STRING = self.context.get_type("String")
        self.BOOL = self.context.get_type("Bool")
        self.AUTO_TYPE = self.context.get_type("AUTO_TYPE")
        self.SELF_TYPE = self.context.get_type("SELF_TYPE")
        self.errors = errors
        self.current_method: Optional[semantic.Method] = None

    @singledispatchmethod
    def visit(self, node, scope, infered_type=None) -> Type:
        # Devolver un tipo por defecto, en verdad
        # no importa ya que este metodo nunca sera llamado.
        return Type("")

    # --------------------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------------EXPRESIONES----------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------#

    # ---------------------------------------------------------------
    # Calcular todos los tipos en el contexto del programa.        |
    # ---------------------------------------------------------------
    @visit.register
    def _(self, node: coolAst.ProgramNode, scope=None, infered_type=None, deep=1):
        program_scope = semantic.Scope() if scope is None else scope
        if deep == 1:
            for class_ in node.class_list:
                self.visit(class_, program_scope.create_child())
        else:
            for class_, child_scope in zip(node.class_list, program_scope.children):
                self.visit(class_, child_scope, deep=deep)
        return program_scope

    # -----------------------------------------------------------------
    # Calcular los tipos en esta clase, visitar primero los atributos |
    # y luego los métodos para garantizar que al revisar los métodos  |
    # ya todos los atributos estén definidos en el scope.             |
    # -----------------------------------------------------------------
    @visit.register
    def _(
        self, node: coolAst.ClassDef, scope: semantic.Scope, infered_type=None, deep=1
    ):
        self.current_type = self.context.get_type(node.idx)
        # Definir los atributos heredados
        if deep == 1:
            for attribute in (
                get_type_attribute_chain(self.current_type)
            ):
                scope.define_variable(attribute.name, attribute.type, "ATTRIBUTE")

        attrib = [x for x in node.features if isinstance(x, AttributeDef)]
        meth = [x for x in node.features if isinstance(x, MethodDef)]
        features = attrib + meth
        
        if deep == 1:
            for f in features:
                self.visit(f, scope.create_child(), deep)
        else:
            for f, s in zip(features, scope.children):
                self.visit(f, s, deep)

        # for feature in node.features:
        #     if isinstance(feature, coolAst.AttributeDef):
        #         self.visit(feature, scope, deep=deep)
        # if deep == 1:
        #     for feature in node.features:
        #         if isinstance(feature, coolAst.MethodDef):
        #             self.visit(feature, scope.create_child(), deep=deep)
        # else:
        #     methods = (f for f in node.features if isinstance(f, coolAst.MethodDef))
        #     for feature, child_scope in zip(methods, scope.children):
        #         self.visit(feature, child_scope, deep=deep)

    # ---------------------------------------------------------
    # Definir un atributo en el scope.                        |
    # ---------------------------------------------------------
    @visit.register
    def _(
        self,
        node: coolAst.AttributeDef,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ):
        atrib = self.current_type.get_attribute(node.idx)

        # Checkear que el valor de retorno de la expresion
        # de inicializacion del atributo (si existe) se
        # conforme con el tipo del atributo
        if node.default_value is not None:
            return_type = self.visit(node.default_value, scope, infered_type, deep)

            if atrib.type == self.AUTO_TYPE:
                # Inferir el tipo del atributo segun su expresion de inicializacion
                atrib.type = return_type
            elif not return_type.conforms_to(atrib.type):
                raise SemanticError(
                    TypeError(
                        f"Attribute {node.idx} of type {atrib.type.name} can not be initialized with an expression of type {return_type.name}",
                        node.default_value.line,
                        node.default_value.column,
                    )
                )

    # ---------------------------------------------------------------------
    # Si el método no tiene un tipo definido, entonces tratar de inferir  |
    # su tipo en dependencia del tipo de su expresién de retorno.         |
    # Notar que al revisar el body del método se pueden inferir también   |
    # los argumentos que no hayan sido definidos con tipos específicos.   |
    # ---------------------------------------------------------------------
    @visit.register
    def _(self, node: coolAst.MethodDef, scope, infered_type=None, deep=1):
        assert self.current_type is not None
        method = self.current_type.get_method(node.idx)
        self.current_method = method
        params = []
        for param in node.param_list:
            if param in params:
                raise SemanticError(
                    f"({param.line}, {param.column}) - SemanticError: Param {param.id} multiply defined."
                )
            self.visit(param, scope, deep=deep)
            params.append(param)

        last = self.visit(node.statements, scope, deep=deep)
        if last.name == "SELF_TYPE":
            last = self.current_type
        if not method.return_type != self.AUTO_TYPE:
            method.return_type = last
        else:
            if not last.conforms_to(method.return_type):
                raise SemanticError(
                    TypeError(
                        f"Inferred return type {last.name} of method {node.idx} does not conform to declared return type {method.return_type.name}",
                        node.statements.line,
                        node.statements.column,
                    )
                )

    @visit.register
    def _(
        self, node: coolAst.BlockNode, scope: semantic.Scope, infered_type=None, deep=1
    ):
        # Visitar cada expr del bloque, el tipo del bloque es el tipo de la ultima expresion
        last = None
        for expr in node.expressions:
            last = self.visit(expr, scope, infered_type, deep)
        return last

    @visit.register
    def _(self, node: coolAst.Param, scope: semantic.Scope, infered_type=None, deep=1):
        type_ = self.context.get_type(node.type)
        if deep == 1:
            scope.define_variable(node.id, type_, "PARAM")

    # -------------------------------------------------------------------------
    # Checkear si la variable a la que se le va a asignar el resultado de la  |
    # expresión tiene un tipo bien definido: en caso de tenerlo, verificar que|
    # el tipo de la expresión coincide con el tipo de la variable, de lo con- |
    # trario asignarle a la variable el tipo de retorno de la expresión.      |
    # -------------------------------------------------------------------------
    @visit.register
    def _(
        self, node: coolAst.AssignNode, scope: semantic.Scope, infered_type=None, deep=1
    ):
        var_info = scope.find_variable(node.idx)
        assert self.current_type is not None
        if var_info:
            e = self.visit(node.expr, scope, infered_type)
            if var_info.type == self.AUTO_TYPE:
                var_info.type = e
                if not scope.is_local(var_info.name):
                    update_attr_type(self.current_type, var_info.name, var_info.type)
                else:
                    update_method_param(
                        self.current_type,
                        self.current_method.name,
                        var_info.name,
                        var_info.type,
                    )
                update_scope_variable(var_info.name, e, scope)
                return e
            else:
                if not e.conforms_to(var_info.type):
                    raise SemanticError(
                        f"Expresion of type {e.name} cannot be assigned to variable {var_info.name} of type {var_info.type.name}"
                    )
                return e
        else:
            raise SemanticError(f"Undefined variable name: {node.idx}")

    @visit.register
    def _(
        self,
        node: coolAst.VariableCall,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ):
        var_info = scope.find_variable(node.idx)
        assert self.current_type is not None
        if var_info:
            if infered_type and var_info.type == self.AUTO_TYPE:
                var_info.type = infered_type
                if scope.is_local(var_info.name):
                    update_method_param(
                        self.current_type,
                        self.current_method.name,
                        var_info.name,
                        var_info.type,
                    )
                update_scope_variable(var_info.name, infered_type, scope)
            return var_info.type
        else:
            raise SemanticError(
                f"{node.line, node.column} - NameError: Undeclared identifier {node.idx}."
            )

    @visit.register
    def _(self, node: SelfNode, scope: Scope, infered_type=None, deep=1):
        return self.current_type

    @visit.register
    def _(
        self,
        node: coolAst.IfThenElseNode,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ):
        cond = self.visit(node.cond, scope, infered_type, deep)
        e1 = self.visit(node.expr1, scope, infered_type, deep)
        e2 = self.visit(node.expr2, scope, infered_type, deep)
        if cond != self.BOOL:
            raise SemanticError(
                f"{node.cond.line, node.cond.column} - TypeError: Predicate of 'if' does not have type Bool."
            )
        return find_common_parent(e1, e2)

    @visit.register
    def _(self, node: CaseNode, scope: Scope, infered_type=None, deep=1):
        if deep == 1:
            types: List[Type] = [
                self.visit(action, scope.create_child(), infered_type, deep)
                for action in node.actions
            ]
        else:
            types = [
                self.visit(action, s, infered_type, deep)
                for action, s in zip(node.actions, scope.children)
            ]

        actions_types = [action.typex for action in node.actions]

        for i, action in enumerate(node.actions):
            try:
                self.context.get_type(action.typex)
            except SemanticError:
                raise SemanticError(
                    f"{action.line, action.column} - TypeError: Class {action.typex} of case branch is undefined."
                )
            if action.typex in actions_types[:i]:
                raise SemanticError(
                    f"{action.line, action.column} - SemanticError: Duplicate branch {action.typex} in case statement."
                )

        if len(types) == 1:
            return types[0]
        elif len(types) == 2:
            return find_common_parent(types[0], types[1])
        else:
            common = find_common_parent(*types[:2])
            for type_ in types[2:]:
                common = find_common_parent(type_, common)
            return common

    @visit.register
    def _(self, node: ActionNode, scope: Scope, infered_type=None, deep=1):
        if deep == 1:
            try:
                scope.define_variable(
                    node.idx, self.context.get_type(node.typex), "LOCAL"
                )
            except SemanticError:
                raise SemanticError(
                    f"{node.line, node.column} - TypeError: Undefined type {node.typex}"
                )
        return self.visit(node.actions, scope, infered_type, deep)

    @visit.register
    def _(
        self,
        node: coolAst.VariableDeclaration,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ):
        # if deep == 1:
        #     scope = scope.create_child()
        # else:
        #     scope = scope.children[0] if scope.children else scope
        for var_id, var_type, var_init_expr, l, c in node.var_list:
            try:
                type_ = self.context.get_type(var_type)
            except SemanticError:
                raise SemanticError(
                    TypeError(
                        f"Class {var_type} of let-bound identifier b is undefined.",
                        l,
                        c,
                    )
                )
            # Revisar que la expresion de inicializacion (de existir) se conforme con el tipo
            # de la variable.
            # Se pueden dar varios casos:
            # - La variable se inicializa en AUTO_TYPE y existe la expresion de inicializacion,
            #   en este caso la variable adquiere el tipo de la expresion
            # - La variable se inicializa en un tipo T_1 y existe la expresion de inicializacion con tipo estatico T_2,
            #   en este caso T_2 < T_1.
            # - La variable se inicializa en un tipo T y no existe expr de inicializacion (solo se define la variable).
            # - La variable se inicializa en AUTO_TYPE y no existe la expr, en este caso se define la variable
            #   y su tipo se deja a inferir por el contexto.
            if var_init_expr:
                init_expr_type: Optional[Type] = self.visit(
                    var_init_expr, scope, infered_type, deep
                )
                if type_ != self.AUTO_TYPE:
                    if not init_expr_type.conforms_to(type_):
                        raise SemanticError(
                            TypeError(
                                f"Declared type {init_expr_type.name} does not conform to type {type_.name} in var {var_id}.",
                                node.line,
                                node.column,
                            )
                        )
                    else:
                        if deep == 1:
                            scope.define_variable(var_id, type_, "LOCAL")
                else:
                    if deep == 1:
                        scope.define_variable(var_id, init_expr_type, "LOCAL")
            else:
                # No hay expresion de inicializacion, entonces solo queda definir la variable, y si es necesario,
                # se actualizara su tipo al chequear el contexto.
                if not (scope.is_defined(var_id) and scope.is_local(var_id)):
                    scope.define_variable(var_id, type_, "LOCAL")

        # Visitar la expresion asociada.
        return_type = self.visit(node.block_statements, scope, infered_type, deep)
        return return_type

    @visit.register
    def _(self, node: ParentFuncCall, scope: Scope, infered_type=None, deep=1):
        assert self.current_type is not None

        # Encontrar el tipo que hace el dispatch
        try:
            dispatch_type = self.context.get_type(node.parent_type)
        except SemanticError:
            raise SemanticError(
                f"{node.line, node.column} - TypeError: Type {node.parent_type} is undefined."
            )

        # Evaluar la expresion sobre la que se hace el dispatch
        static_expr0_type = self.visit(node.obj, scope, infered_type, deep)

        if static_expr0_type.name == "SELF_TYPE":
            static_expr0_type = self.current_type

        if not static_expr0_type.conforms_to(dispatch_type):
            raise SemanticError(
                f"{node.line, node.column} - TypeError: Expression type {static_expr0_type.name} does not conform to declared static dispatch type {dispatch_type.name}."
            )

        # Encontrar el metodo en el tipo.
        try:
            method: semantic.Method = dispatch_type.get_method(node.idx)
        except SemanticError:
            raise SemanticError(
                f"{node.line, node.column} - AttributeError: Dispatch to undefined method {node.idx}."
            )

        if len(method.param_names) != len(node.arg_list):
            raise SemanticError(
                f"{node.line, node.column} - SemanticError: Method {node.idx} called with wrong number of arguments."
            )

        # Iterar por cada parametro del metodo y chequear que cada expresion corresponda en tipo.
        for expr_i, type_i, param_name in zip(
            node.arg_list, method.param_types, method.param_names
        ):
            type_expr_i = self.visit(expr_i, scope, infered_type, deep)
            if not type_expr_i.conforms_to(type_i):
                raise semantic.SemanticError(
                    f"{expr_i.line, expr_i.column} - TypeError: Expression corresponding to param {param_name} in call to {node.idx} must conform to {type_i.name}"
                )

        # Procesar el tipo de retorno de la funcion
        if method.return_type == self.SELF_TYPE:
            return static_expr0_type
        if method.return_type != self.AUTO_TYPE:
            return method.return_type
        elif infered_type:
            method.return_type = infered_type
            return infered_type
        else:
            return self.AUTO_TYPE

    @visit.register
    def _(
        self, node: coolAst.FunCall, scope: semantic.Scope, infered_type=None, deep=1
    ):
        assert self.current_type is not None
        # Detectar el tipo estatico de la expr0.
        static_expr0_type: semantic.Type = self.visit(
            node.obj, scope, infered_type, deep
        )

        if static_expr0_type.name == "SELF_TYPE":
            static_expr0_type = self.current_type

        # Encontrar el metodo en el tipo.
        try:
            method: semantic.Method = static_expr0_type.get_method(node.id)
        except SemanticError:
            raise SemanticError(
                f"{node.line, node.column} - AttributeError: Dispatch to undefined method {node.id}."
            )

        if len(method.param_names) != len(node.args):
            raise SemanticError(
                f"{node.line, node.column} - SemanticError: Method {node.id} called with wrong number of arguments."
            )

        # Iterar por cada parametro del metodo y chequear que cada expresion corresponda en tipo.
        for expr_i, type_i, param_name in zip(
            node.args, method.param_types, method.param_names
        ):
            type_expr_i = self.visit(expr_i, scope, infered_type, deep)
            if type_i == self.AUTO_TYPE:
                update_scope_variable(param_name, type_expr_i, scope)
            elif not type_expr_i.conforms_to(type_i):
                raise semantic.SemanticError(
                    f"{expr_i.line, expr_i.column} - TypeError: Expression corresponding to param {param_name} in call to {node.id} must conform to {type_i.name}"
                )

        # Procesar el tipo de retorno de la funcion
        if method.return_type == self.SELF_TYPE:
            return static_expr0_type
        if method.return_type != self.AUTO_TYPE:
            return method.return_type
        elif infered_type:
            method.return_type = infered_type
            return infered_type
        else:
            return self.AUTO_TYPE

    @visit.register
    def _(
        self,
        node: coolAst.InstantiateClassNode,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ):
        try:
            ret_type = self.context.get_type(node.type_)
        except SemanticError:
            raise SemanticError(
                f"{node.line, node.column + 4} - TypeError: 'new' used with undefined class {node.type_}."
            )
        if ret_type in (
            self.AUTO_TYPE,
            void,
        ):
            self.errors.append(f"Cannot instantiate {ret_type.name}")
        return ret_type

    @visit.register
    def _(
        self,
        node: coolAst.WhileBlockNode,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ):
        cond_type = self.visit(node.cond, scope, infered_type, deep)
        if cond_type != self.BOOL:
            raise SemanticError(
                f"{node.cond.line, node.cond.column} - TypeError: Loop condition does not have type Bool."
            )
        ret_type = self.visit(node.statements, scope, infered_type, deep)
        return self.OBJECT

    # ---------------------------------------------------------------------------------------------------------------------------#
    # ---------------------------------------OPERACIONES ARITMÉTICAS-------------------------------------------------------------#
    # ---------------------------------------------------------------------------------------------------------------------------#

    # -------------------------------------------------------------------------------------------------
    # Todas las operaciones aritméticas estan definidas solamente para los enteros, luego, de checkeo|
    # de cada operación se realiza evaluando sus operandos y viendo si sus tipos son consistentes con|
    # INTEGER.                                                                                       |
    # -------------------------------------------------------------------------------------------------

    @visit.register
    def _(
        self, node: coolAst.PlusNode, scope: semantic.Scope, infered_type=None, deep=1
    ):
        left = self.visit(node.left, scope, self.INTEGER, deep)
        right = self.visit(node.right, scope, self.INTEGER, deep)
        if left.conforms_to(self.INTEGER) and right.conforms_to(self.INTEGER):
            return self.INTEGER
        else:
            raise SemanticError(
                TypeError(
                    f"Invalid operation: {left.name} + {right.name}",
                    node.line,
                    node.column,
                )
            )

    @visit.register
    def _(
        self, node: coolAst.DifNode, scope: semantic.Scope, infered_type=None, deep=1
    ):
        left = self.visit(node.left, scope, self.INTEGER, deep)
        right = self.visit(node.right, scope, self.INTEGER, deep)
        if left.conforms_to(self.INTEGER) and right.conforms_to(self.INTEGER):
            return self.INTEGER
        else:
            raise SemanticError(
                TypeError(
                    f"Invalid operation: {left.name} - {right.name}",
                    node.line,
                    node.column,
                )
            )

    @visit.register
    def _(
        self, node: coolAst.DivNode, scope: semantic.Scope, infered_type=None, deep=1
    ):
        left = self.visit(node.left, scope, self.INTEGER, deep)
        right = self.visit(node.right, scope, self.INTEGER, deep)
        if left.conforms_to(self.INTEGER) and right.conforms_to(self.INTEGER):
            return self.INTEGER
        else:
            raise SemanticError(
                TypeError(
                    f"Invalid operation: {left.name} / {right.name}",
                    node.line,
                    node.column,
                )
            )

    @visit.register
    def _(
        self, node: coolAst.MulNode, scope: semantic.Scope, infered_type=None, deep=1
    ):
        left = self.visit(node.left, scope, self.INTEGER, deep)
        right = self.visit(node.right, scope, self.INTEGER, deep)
        if left.conforms_to(self.INTEGER) and right.conforms_to(self.INTEGER):
            return self.INTEGER
        else:
            raise SemanticError(
                TypeError(
                    f"Invalid operation: {left.name} * {right.name}",
                    node.line,
                    node.column,
                )
            )

    # -------------------------------------------------------------------------------------------#
    # -----------------------------------OPERACIONES COMPARATIVAS -------------------------------#
    # -------------------------------------------------------------------------------------------#

    # ---------------------------------------------------------------------------------------------
    # Para poder comparar dos expresiones, estas deben ser del mismo tipo. El tipo de retorno de |
    # toda operación comparativa es BOOLEAN.                                                     |
    # ---------------------------------------------------------------------------------------------
    @visit.register
    def _(
        self,
        node: coolAst.GreaterThanNode,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ):
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
            return self.BOOL
        else:
            raise SemanticError(
                TypeError(
                    f"Invalid operation: {left.name} > {right.name}",
                    node.line,
                    node.column,
                )
            )

    @visit.register
    def _(
        self,
        node: coolAst.GreaterEqualNode,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ):
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
            return self.BOOL
        else:
            raise SemanticError(
                TypeError(
                    f"Invalid operation: {left.name} >= {right.name}",
                    node.line,
                    node.column,
                )
            )

    @visit.register
    def _(
        self,
        node: coolAst.LowerThanNode,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ):
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
            return self.BOOL
        else:
            raise SemanticError(
                TypeError(
                    f"Invalid operation: {left.name} < {right.name}",
                    node.line,
                    node.column,
                )
            )

    @visit.register
    def _(
        self, node: coolAst.LowerEqual, scope: semantic.Scope, infered_type=None, deep=1
    ):
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
            return self.BOOL
        else:
            raise SemanticError(
                TypeError(
                    f"Invalid operation: {left.name} <= {right.name}",
                    node.line,
                    node.column,
                )
            )

    @visit.register
    def _(
        self,
        node: coolAst.EqualToNode,
        scope: semantic.Scope,
        infered_type=None,
        deep=1,
    ) -> Type:
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left in (self.BOOL, self.INTEGER, self.STRING) or left in (
            self.BOOL,
            self.INTEGER,
            self.STRING,
        ):
            if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
                return self.BOOL
            else:
                raise SemanticError(
                    TypeError(
                        f"Invalid operation: {left.name} = {right.name}",
                        node.line,
                        node.column,
                    )
                )
        else:
            return self.BOOL

    @visit.register
    def _(
        self, node: coolAst.NotNode, scope: semantic.Scope, infered_type=None, deep=1
    ):
        val_type = self.visit(node.lex, scope, infered_type, deep)
        if val_type == self.AUTO_TYPE or val_type == self.INTEGER:
            return self.INTEGER
        else:
            raise SemanticError(
                TypeError(
                    f"Argument of ~ has type {val_type.name} instead of Int.",
                    node.line,
                    node.column,
                )
            )

    @visit.register
    def _(
        self, node: coolAst.NegNode, scope: semantic.Scope, infered_type=None, deep=1
    ) -> Type:
        val_type = self.visit(node.lex, scope, infered_type, deep)
        if val_type == self.AUTO_TYPE or val_type == self.BOOL:
            return self.BOOL
        else:
            raise SemanticError(
                f"{node.line, node.column} - TypeError: Argument of 'not' has type {val_type.name} instead of Bool."
            )

    # -----------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------CONSTANTES-----------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------------#

    @visit.register
    def _(self, node: coolAst.IntegerConstant, scope, infered_t=None, deep=1):
        return self.INTEGER

    @visit.register
    def _(self, node: coolAst.StringConstant, scope, infered_t=None, deep=1):
        return self.STRING

    @visit.register
    def _(self, node: coolAst.TrueConstant, scope, infered_type=None, deep=1):
        return self.BOOL

    @visit.register
    def _(self, node: coolAst.FalseConstant, scope, infered_type=None, deep=1):
        return self.BOOL

    @visit.register
    def _(self, node: coolAst.IsVoidNode, scope, infered_type=None, deep=1):
        return self.BOOL

    @visit.register
    def _(self, node: SelfNode, scope, infered_type=None, deep=1):
        return self.current_type
