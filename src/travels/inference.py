import abstract.semantics as semantic
import abstract.tree as coolAst
from travels.context_actions import update_attr_type, update_method_param, update_scope_variable
from typing import Optional
from functools import singledispatchmethod

void = semantic.VoidType()


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
        self.INTEGER = self.context.get_type('Int')
        self.OBJECT = self.context.get_type('Object')
        self.STRING = self.context.get_type('String')
        self.BOOL = self.context.get_type('Bool')
        self.AUTO_TYPE = self.context.get_type('AUTO_TYPE')
        self.errors = errors
        self.current_method: Optional[semantic.Method] = None

    @singledispatchmethod
    def visit(self, node, scope, infered_type=None):
        pass

    # --------------------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------------EXPRESIONES----------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------#

    # ---------------------------------------------------------------
    # Calcular todos los tipos en el contexto del programa.        |
    # ---------------------------------------------------------------
    @visit.register
    def _(self,
          node: coolAst.ProgramNode,
          scope=None,
          infered_type=None,
          deep=1):  # noqa: F811
        program_scope = semantic.Scope() if scope is None else scope
        print(f"Este es el scope en la vuelta {deep} :\n {program_scope}")
        if deep == 1:
            for class_ in node.class_list:
                self.visit(class_, program_scope.create_child())
        else:
            for class_, child_scope in zip(node.class_list,
                                           program_scope.children):
                self.visit(class_, child_scope, deep=deep)
        return program_scope

    # -----------------------------------------------------------------
    # Calcular los tipos en esta clase, visitar primero los atributos |
    # y luego los métodos para garantizar que al revisar los métodos  |
    # ya todos los atributos estén definidos en el scope.             |
    # -----------------------------------------------------------------
    @visit.register
    def _(self,
          node: coolAst.ClassDef,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        self.current_type = self.context.get_type(node.idx)
        for feature in node.features:
            if isinstance(feature, coolAst.AttributeDef):
                self.visit(feature, scope, deep=deep)
        if deep == 1:
            for feature in node.features:
                if isinstance(feature, coolAst.MethodDef):
                    self.visit(feature, scope.create_child(), deep=deep)
        else:
            methods = (f for f in node.features
                       if isinstance(f, coolAst.MethodDef))
            for feature, child_scope in zip(methods, scope.children):
                self.visit(feature, child_scope, deep=deep)

    # ---------------------------------------------------------
    # Definir un atributo en el scope.                        |
    # ---------------------------------------------------------
    @visit.register
    def _(self,
          node: coolAst.AttributeDef,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        atrib = self.current_type.get_attribute(node.idx)
        if deep == 1:
            scope.define_variable(atrib.name, atrib.type, "ATTRIBUTE")

    # ---------------------------------------------------------------------
    # Si el método no tiene un tipo definido, entonces tratar de inferir  |
    # su tipo en dependencia del tipo de su expresién de retorno.         |
    # Notar que al revisar el body del método se pueden inferir también   |
    # los argumentos que no hayan sido definidos con tipos específicos.   |
    # ---------------------------------------------------------------------
    @visit.register
    def _(self,
          node: coolAst.MethodDef,
          scope,
          infered_type=None,
          deep=1):  # noqa: F811
        print(node.idx)
        method = self.current_type.get_method(node.idx)
        self.current_method = method
        for param in node.param_list:
            self.visit(param, scope, deep=deep)

        last = self.visit(node.statements, scope, deep=deep)
        if not method.return_type != self.AUTO_TYPE:
            print(f'Infered type {last.name} for {node.idx}')
            method.return_type = last
        else:
            if not last.conforms_to(method.return_type):
                self.errors.append(
                    f'Method {method.name} cannot return {last}')
        print(scope)

    @visit.register
    def _(self,
          node: coolAst.BlockNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        # Visitar cada expr del bloque, el tipo del bloque es el tipo de la ultima expresion
        last = None
        for expr in node.expressions:
            last = self.visit(expr, scope, infered_type, deep)
        return last

    @visit.register
    def _(self,
          node: coolAst.Param,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
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
    def _(self,
          node: coolAst.AssignNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        var_info = scope.find_variable(node.idx)
        if var_info:
            e = self.visit(node.expr, scope, infered_type)
            if var_info.type == self.AUTO_TYPE:
                print(f'Infered type {e.name} for {node.idx}')
                var_info.type = e
                if not scope.is_local(var_info.name):
                    update_attr_type(self.current_type, var_info.name,
                                     var_info.type)
                else:
                    update_method_param(self.current_type,
                                        self.current_method.name,
                                        var_info.name, var_info.type)
                update_scope_variable(var_info.name, e, scope)
                return void
            else:
                if not e.conforms_to(var_info.type):
                    self.errors.append(
                        f'Expresion of type {e.name} cannot be assigned to variable {var_info.name} of type {var_info.type.name}'
                    )
                return void
        else:
            self.errors.append(f'Undefined variable name: {node.idx}')

    @visit.register
    def _(self,
          node: coolAst.VariableCall,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        var_info = scope.find_variable(node.idx)
        if var_info:
            if infered_type and var_info.type == self.AUTO_TYPE:
                print(f'Infered type {infered_type.name} for {var_info.name}')
                var_info.type = infered_type
                if not scope.is_local(var_info.name):
                    update_attr_type(self.current_type, var_info.name,
                                     var_info.type)
                else:
                    update_method_param(self.current_type,
                                        self.current_method.name,
                                        var_info.name, var_info.type)
                update_scope_variable(var_info.name, infered_type, scope)
            return var_info.type
        else:
            self.errors.append(f'Name {node.idx} is not define.')

    @visit.register
    def _(self,
          node: coolAst.IfThenElseNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        cond = self.visit(node.cond, scope, infered_type, deep)
        e1 = self.visit(node.expr1, scope, infered_type, deep)
        e2 = self.visit(node.expr2, scope, infered_type, deep)
        if cond != self.BOOL:
            self.errors.append(
                f'Se esperaba una expresion de tipo bool y se obtuvo una de tipo {cond}.'
            )
        if e1.conforms_to(e2):
            return e2
        elif e2.conforms_to(e1):
            return e1
        else:
            e1_parent = e1.parent
            e2_parent = e2.parent
            while e2_parent != e1_parent:
                e1_parent = e1_parent.parent
                e2_parent = e2_parent.parent
            return e1_parent

    # @visitor.when(coolAst.VariableDeclaration)  #type: ignore  # noqa
    # # TODO FIX THIS, IT is not working after change in grammar, REIMPLEMENT IT!!!!
    # def visit(self, node: coolAst.VariableDeclaration, scope: semantic.Scope, infered_type=None, deep=1):  # noqa: F811
    #     for var_idx, var_type, var_init_exp in node.var_list:
    #         type_ = self.context.get_type(var_type)
    #         if type_ != self.AUTO_TYPE:
    #             if deep == 1:
    #                 scope.define_variable(var_idx, type_, "LOCAL")
    #         else:
    #             if deep == 1:
    #                 type_ = self.visit(node.block_statements, scope, infered_type, deep)
    #                 print(f'Infered type {type_.name} for {var_idx}')
    #                 scope.define_variable(node.idx, type_, "LOCAL")
    #     return void
    @visit.register
    def _(self,
          node: coolAst.VariableDeclaration,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        for var_id, var_type, var_init_expr in node.var_list:
            type_ = self.context.get_type(var_type)
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
                init_expr_type: semantic.Type = self.visit(
                    var_init_expr, scope, infered_type, deep)
                if type_ != self.AUTO_TYPE:
                    if not init_expr_type.conforms_to(type_):
                        self.errors.append(
                            f"Init expression of {var_id} must conform to type {type_}"
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
        return_type = self.visit(node.block_statements, scope, infered_type,
                                 deep)
        return return_type

    # @visitor.when(coolAst.FunCall)  #type: ignore  # noqa
    # def visit(self, node: coolAst.FunCall, scope: semantic.Scope, infered_type=None, deep=1):  # noqa: F811
    #     if isinstance(node.obj, semantic.Type):
    #         method = node.obj.get_method(node.id)
    #     elif node.obj == 'self':
    #         method = self.current_type.get_method(node.id)
    #     else:
    #         method = self.context.get_type(node.obj).get_method(node.id)

    #     for arg in node.args:
    #         self.visit(arg, scope, infered_type, deep)

    #     if method.return_type != self.AUTO_TYPE:
    #         return method.return_type
    #     elif infered_type:
    #         print(f'Infered type {infered_type.name} for {node.id}')
    #         method.return_type = infered_type
    #         return infered_type
    #     else:
    #         return self.AUTO_TYPE

    @visit.register
    def _(self,
          node: coolAst.FunCall,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        # Detectar el tipo estatico de la expr0.
        static_expr0_type: semantic.Type = self.visit(node.obj, scope,
                                                      infered_type, deep)

        # Encontrar el metodo en el tipo.
        method: semantic.Method = static_expr0_type.get_method(node.id)

        # Iterar por cada parametro del metodo y chequear que cada expresion corresponda en tipo.
        for expr_i, type_i, param_name in zip(node.args, method.param_types,
                                              method.param_names):
            type_expr_i = self.visit(expr_i, scope, infered_type, deep)
            if not type_expr_i.conforms_to(type_i):
                raise semantic.SemanticError(
                    f"Expression corresponding to param {param_name} in call to {node.id} must conform to {type_i}"
                )

        # Procesar el tipo de retorno de la funcion
        if method.return_type != self.AUTO_TYPE:
            return method.return_type
        elif infered_type:
            method.return_type = infered_type
            return infered_type
        else:
            return self.AUTO_TYPE

    @visit.register
    def _(self,
          node: coolAst.InstantiateClassNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        ret_type = self.context.get_type(node.type_)
        if ret_type in (self.AUTO_TYPE, void, self.STRING, self.INTEGER,
                        self.OBJECT, self.BOOL):
            self.errors.append(f'Cannot instantiate {ret_type}')
        return ret_type

    @visit.register
    def _(self,
          node: coolAst.WhileBlockNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        ret_type = None
        for st in node.statements:
            ret_type = self.visit(st, scope, infered_type, deep)
        return ret_type

    # ---------------------------------------------------------------------------------------------------------------------------#
    # ---------------------------------------OPERACIONES ARITMÉTICAS-------------------------------------------------------------#
    # ---------------------------------------------------------------------------------------------------------------------------#


# -------------------------------------------------------------------------------------------------
# Todas las operaciones aritméticas estan definidas solamente para los enteros, luego, de checkeo|
# de cada operación se realiza evaluando sus operandos y viendo si sus tipos son consistentes con|
# INTEGER.                                                                                       |
# -------------------------------------------------------------------------------------------------

    @visit.register
    def _(self,
          node: coolAst.PlusNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        left = self.visit(node.left, scope, self.INTEGER, deep)
        right = self.visit(node.right, scope, self.INTEGER, deep)
        if left.conforms_to(self.INTEGER) and right.conforms_to(self.INTEGER):
            return self.INTEGER
        else:
            self.errors.append(
                f'Invalid operation :{left.name} + {right.name}')
            return self.INTEGER

    @visit.register
    def _(self,
          node: coolAst.DifNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        left = self.visit(node.left, scope, self.INTEGER, deep)
        right = self.visit(node.right, scope, self.INTEGER, deep)
        if left.conforms_to(self.INTEGER) and right.conforms_to(self.INTEGER):
            return self.INTEGER
        else:
            self.errors.append(
                f'Invalid operation :{left.name} - {right.name}')
            return self.INTEGER

    @visit.register
    def _(self,
          node: coolAst.DivNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        left = self.visit(node.left, scope, self.INTEGER, deep)
        right = self.visit(node.right, scope, self.INTEGER, deep)
        if left.conforms_to(self.INTEGER) and right.conforms_to(self.INTEGER):
            return self.INTEGER
        else:
            self.errors.append(
                f'Invalid operation :{left.name} / {right.name}')
            return self.INTEGER

    @visit.register
    def _(self,
          node: coolAst.MulNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        left = self.visit(node.left, scope, self.INTEGER, deep)
        right = self.visit(node.right, scope, self.INTEGER, deep)
        if left.conforms_to(self.INTEGER) and right.conforms_to(self.INTEGER):
            return self.INTEGER
        else:
            self.errors.append(
                f'Invalid operation :{left.name} * {right.name}')
            return self.INTEGER

    # -------------------------------------------------------------------------------------------#
    # -----------------------------------OPERACIONES COMPARATIVAS -------------------------------#
    # -------------------------------------------------------------------------------------------#

    # ---------------------------------------------------------------------------------------------
    # Para poder comparar dos expresiones, estas deben ser del mismo tipo. El tipo de retorno de |
    # toda operación comparativa es BOOLEAN.                                                     |
    # ---------------------------------------------------------------------------------------------
    @visit.register
    def _(self,
          node: coolAst.GreaterThanNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
            return self.BOOL
        else:
            self.errors.append(
                f'Invalid operation: {left.name} > {right.name}')
            return self.BOOL

    @visit.register
    def _(self,
          node: coolAst.GreaterEqualNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
            return self.BOOL
        else:
            self.errors.append(
                f'Invalid operation: {left.name} >= {right.name}')
            return self.BOOL

    @visit.register
    def _(self,
          node: coolAst.LowerThanNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
            return self.BOOL
        else:
            self.errors.append(
                f'Invalid operation: {left.name} < {right.name}')
            return self.BOOL

    @visit.register
    def _(self,
          node: coolAst.LowerEqual,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
            return self.BOOL
        else:
            self.errors.append(
                f'Invalid operation: {left.name} <= {right.name}')
            return self.BOOL

    @visit.register
    def _(self,
          node: coolAst.EqualToNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        left = self.visit(node.left, scope, infered_type, deep)
        right = self.visit(node.right, scope, infered_type, deep)
        if left == right or left == self.AUTO_TYPE or right == self.AUTO_TYPE:
            return self.BOOL
        else:
            self.errors.append(
                f'Invalid operation: {left.name} == {right.name}')
            return self.BOOL

    @visit.register
    def _(self,
          node: coolAst.NotNode,
          scope: semantic.Scope,
          infered_type=None,
          deep=1):  # noqa: F811
        val_type = self.visit(node.lex, scope, infered_type, deep)
        if val_type == self.AUTO_TYPE or val_type == self.BOOL:
            return self.BOOL
        else:
            self.errors.append(f'Invalid operation: ! {val_type.name}')
            return self.BOOL

    # -----------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------CONSTANTES-----------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------------#

    @visit.register
    def _(self,
          node: coolAst.IntegerConstant,
          scope,
          infered_type=None,
          deep=1):  # noqa: F811
        return self.INTEGER

    @visit.register
    def _(self,
          node: coolAst.StringConstant,
          scope,
          infered_type=None,
          deep=1):  # noqa: F811
        return self.STRING

    @visit.register
    def _(self,
          node: coolAst.TrueConstant,
          scope,
          infered_type=None,
          deep=1):  # noqa: F811
        return self.BOOL

    @visit.register
    def _(self,
          node: coolAst.FalseConstant,
          scope,
          infered_type=None,
          deep=1):  # noqa: F811
        return self.BOOL
