from AST import *
from Scope import *
from Cool_Type import *
import visitor as visitor

class Semantics_Checker:
    
    def safe_methods(self, node1:MethodNode, node2: MethodNode):
        if not node1.name == node2.name:
            return True
        if len(node1.parameters)==len(node2.parameters):
            for i in range(len(node1.parameters)):
                if node1.parameters[i].type != node2.parameters[i].type:
                    return False
            return True
        return False
    
    def params_for_method(self, node1:list, node2: MethodNode, scope:Scope):
        if len(node1)==len(node2.parameters):
            for i in range(len(node2.parameters)):
                if not node1[i] < scope.get_type(node2.parameters[i].type):
                    return False
            return True
        return False

    def check_inheritance(self, classes: list):
        mask = [0] * (len(classes) + 2)
        mapper = {}
        mask[-1] = 2
        mask[-2] = 2
        mapper["Object"] = len(classes)
        mapper["IO"] = len(classes) - 1
        for i in range(len(classes)):
            cclass = classes[i]
            mapper[cclass.name] = i
        for cclass in classes:
            if not cclass.parent in mapper:
                pass
                #Agregar error de padre indefinido
                
        for i in range(len(classes)):
            cclass = classes[i]
            if not check_cyclic(cclass,mask,mapper):
                pass
                #Agregar el error de herencia ciclica
                
        return True
    
    def check_cyclic_inheritance(self, cclass: ClassNode, mask: list, mapper: dict):
        if mask[mapper[cclass.name]] == 2:
            return True
        elif mask[mapper[cclass.name]] == 1:
            return False
        mask[mapper[cclass.name]] = 1
        parent = cclass.parent
        return check_cyclic_inheritance(parent, mask, mapper)

    # def types_sort(self, types: dict):
    #     list_types = list(types.values())
    #     mask = [False] * len(list_types)
    #     mapper = {}
    #     sorted = [] 
    #     for i in range(len(classes)):
    #         cclass = classes[i]
    #         mapper[classes.name] = i
    #     mask[mapper["Object"]] = True

    #     for i in range(len(classes)):
            


    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, _):
        check_inheritance(node.classes)
        rscope = Scope(None, None)
        for c_class in node.classes:
            cool_type = Cool_Type(c_class.name, c_class.parent, c_class.attributes, c_class.methods)
            scope.create_type(cool_type)
        for c_class in node.classes:
            scope = Scope(c_class.name,rscope)
            visit(cclass,scope)
        return rscope

    @visitor.when(ClassNode)
    def visit(self, node: ClassNode, scope: Scope):
        parent = node.parent
        if parent in ["Int","String","Bool"]:
            pass
            #Agregar error de tipos invalidos para heredar
        cparent = scope.get_type(parent)
        for attr in node.attributes:
            for p_attr in cparent.attributes:
                if attr.name == p_attr.name:
                    pass
                    #Agregar error de atributo definido en el padre
            if not scope.define_attribute(attr.name, attr.type, attr.value):
                 pass
                 #Agregar error de atributo ya definido
        for method in node.methods:
            for p_method in cparent.methods:
                if not safe_methods(method, p_method):
                    pass
                    #Agregar error de redifinicion invalida de metodos heredados
            if not scope.define_method(method.name, method.parameters, method.return_type, method.body):
                 pass
                 #Agregar error de metodo ya definido en la clase
        for attr in node.attributes:
            visit(attr,scope)
        for method in node.methods:
            visit(method,scope)

    @visitor.when(AttributeNode)
    def visit(self, node: AttributeNode, scope: Scope):
        if not scope.exists_type(node.type):
            pass
            #Agregar error de tipo indefinido
        else:
            if node.value:
                t_value = visit(node.value,scope)
                node.static_type = scope.get_type(node.type)
                if scope.local:
                    scope.define_variable(node.name, node.static_type, True, node.value)
                if not t_value < node.static_type:
                    pass
                    #Agregar error de expresion con tipo invalido
                return scope.get_type(node.type)
    
    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope: Scope):
        nscope = Scope(scope.class_name, scope, True)
        for param in node.parameters:
            visit(param, nscope)
        if not nscope.exists_type(node.return_type):
            pass
            #Agregar error de tipo de retorno indefinido
        else:
            t_value = visit(node.body,nscope)
            if node.return_type == "SELF_TYPE":
                node.static_type = nscope.get_type(nscope.class_name)
                if not t_value < node.static_type:
                        pass
                        #Agregar error de expresion con tipo invalido
            else:
                node.static_type = nscope.get_type(node.return_type)
                if not t_value < node.static_type:
                    pass
                    #Agregar error de expresion con tipo invalido
    
    @visitor.when("ParameterNode")
    def visit(self, node: ParameterNode, scope: Scope):
        if not scope.exists_type(node.type):
            pass
            #Agregar error de tipo indefinido
        else:
            if not scope.define_variable(node.name,scope.get_type(node.type)):
                pass
                #Agregar error de nombre repetido

    @visitor.when(IntegerNode)
    def visit(self, node: IntegerNode, scope: Scope):
        node.static_type = scope.get_type('Int')
        return scope.get_type("Int")

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope):
        node.static_type = scope.get_type('String')
        return scope.get_type("String")

    @visitor.when(BoolNode)
    def visit(self, node: BoolNode, scope: Scope):
        node.static_type = scope.get_type('Bool')
        return scope.get_type("Bool")

    @visitor.when(NewNode)
    def visit(self, node: NewNode, scope: Scope):
        node.static_type = scope.get_type(node.type)
        return scope.get_type(node.type)
    
    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        if not scope.exists_variable(node.id):
            pass
            #Agregar error de variable no definida
        return_type = scope.get_variable_type(node.id)
        node .static_type = return_type
        return return_type

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope: Scope):
        node.static_type = scope.get_type('Bool')
        t_value = visit(node.expression, scope)
        if not t_value < node.static_type:
            pass
            #Agregar error de tipo invalido en la expresion
        return scope.get_type("Bool")
    
    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        t_value = visit(node.body,nscope)
        if not scope.exists_variable(node.variable):
            pass
            #Agregar error de variable indefinida
        else:
            static_type = scope.get_variable_type(node.variable)
            if not t_value < static_type:
                    pass
                    #Agregar error de expresion con tipo invalido
        node.static_type = t_value
        return t_value
    
    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        expr_type = None
        for expr in node.expressions:
            expr_type = visit(expr, scope)
        node.static_type = expr_type
        return expr_type

    @visitor.when(DispatchNode)
    def visit(self, node: DispatchNode, scope: Scope):
        if node.left_expression:
            param_types = []
            for param in node.parameters:
                param_types.append(visit(param,scope)) 
            dtype = visit(node.left_expression,scope)
            if not dtype.exists_method(node.func_id):
                pass
                #Agregar error de metodo indefinido
            else:
                method = dtype.get_method(node.func_id)
                if not params_for_method(param_types,method,scope):
                    pass
                    #Agregar error de parametros incorrectos
                return_type = method.return_type
                if return_type == "SELF_TYPE":
                    return_type = dtype
                node.static_type = return_type
                return return_type
        else:
            param_types = []
            for param in node.parameters:
                param_types.append(visit(param,scope)) 
            dtype = scope.get_type(scope.class_name)
            if not dtype.exists_method(node.func_id):
                pass
                #Agregar error de metodo indefinido
            else:
                method = dtype.get_method(node.func_id)
                if not params_for_method(param_types,method,scope):
                    pass
                    #Agregar error de parametros incorrectos
                return_type = method.return_type
                if return_type == "SELF_TYPE":
                    return_type = dtype
                node.static_type = return_type
                return return_type
    
    @visitor.when(StaticDispatchNode)
    def visit(self, node: StaticDispatchNode, scope: Scope):
            param_types = []
            for param in node.parameters:
                param_types.append(visit(param,scope)) 
            dtype = visit(node.left_expression,scope)         
            if not dtype.exists_method(node.func_id):
                pass
                #Agregar error de metodo indefinido
            else:
                parent_type = scope.get_type(node.parent_id)
                if not dtype < parent_type:
                    pass
                    #Agregar error de tipo de padre invalido
                method = parent.get_method(node.func_id)
                if not params_for_method(param_types,method,scope):
                    pass
                    #Agregar error de parametros incorrectos
                return_type = method.return_type
                if return_type == "SELF_TYPE":
                    return_type = dtype
                node.static_type = return_type
                return return_type
    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        nscope = Scope(scope.classname, scope)
        for declaration in node.declarations:
            visit(declaration, nscope)
        b_value = visit(node.body,nscope)
        node.static_type = b_value
        return b_value 
    
    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope):
        ptype = visit(node.predicate)
        if not ptype.name == "Bool":
            pass
            #Agregar error de predicado invalido
        ttype = visit(node.then_body,scope)
        etype = visit(node.else_body,scope)
        if ttype.name == 'SELF_TYPE' and etype.name == 'SELF_TYPE':
            node.static_type = ttype
            return ttype
        elif ttype.name == 'SELF_TYPE':
            return_type = scope.join(etype,scope.get_type(scope.classname))
            node.static_type = return_type
            return return_type
        elif etype.name == 'SELF_TYPE':
            return_type = scope.join(ttype,scope.get_type(scope.classname))
            node.static_type = return_type
            return return_type
        else:
            return_type = scope.join(ttype,etype)
            node.static_type = return_type
            return return_type
    
    @visitor.when(LoopNode)
    def visit(self, node: LoopNode, scope: Scope):
        ptype = visit(node.predicate)
        if not ptype.name == "Bool":
            pass
            #Agregar error de predicado invalido
        visit(node.body,scope)
        node.static_type = scope.get_type("Object")
        return scope.get_type("Object")
    
    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):
        sub_types = []
        for subcase in node.subcases:
            if not subcase.type in sub_types:
                sub_types.append(subcase.type)
            else:
                pass
                #Agregar error de tipo de subcaso repetido
        sub_rtypes = []
        for subcase in node.subcases:
            nscope = Scope(scope.class_name,scope,True)
            sub_rtypes.append(visit(subcase,nscope))
        return_type = sub_rtypes[0]
        for subtype in sub_rtypes:
            if return_type.name == "SELF_TYPE" and subtype.name == "SELF_TYPE":
                continue
            elif return_type.name == "SELF_TYPE":
                return_type = scope.join(scope.get_type(scope.class_name),subtype)
            elif subtype == "SELF_TYPE":
                return_type = scope.join(scope.get_type(scope.class_name),return_type)
            else:
                return_type = scope.join(return_type,subtype)
        node.static_type = return_type
        return return_type
    
    @visitor.when(SubCaseNode)
    def visit(self, node: SubCaseNode, scope: Scope):
        stype = scope.get_type(node.type)
        scope.define_variable(name,stype,True)
        return_type = visit(node.expression,scope)
        node.static_type = return_type
        return return_type
    
    @visitor.when(IntComplementNode)
    def visit(self, node: IntComplementNode, scope: Scope):
        etype = self.visit(IntComplementNode, scope)
        if not etype.name == "Int":
            pass
            #Agregar error de tipo de expresion distinto de int
        int_type = scope.get_type('Int')
        node.static_type = int_type
        return int_type
    
    @visitor.when(BoolNotNode)
    def visit(self, node: BoolNotNode, scope: Scope):
        etype = self.visit(BoolNotNode, scope)
        if not etype.name == "Bool":
            pass
            #Agregar error de tipo de expresion distinto de bool
        bool_type = scope.get_type('Bool')
        node.static_type = bool_type
        return bool_type
    
    @visitor.when(BinaryOperatorNode)
    def visit(self, node: BinaryOperatorNode, scope: Scope):
        ltype = self.visit(node.first, scope)
        rtype = self.visit(node.second, scope)
        if not ltype.name == 'Int' or not rtype.name == 'Int':
            pass
            #Agregar error de tipo de expresion distinto de int
        int_type = scope.getType('Int')
        node.static_type = int_type
        return int_type
    
    @visitor.when(ComparisonNode)
    def visit(self, node: ComparisonNode, scope: Scope):
        ltype = self.visit(node.first, scope)
        rtype = self.visit(node.second, scope)
        if not ltype.name == 'Bool' or not rtype.name == 'Bool':
            pass
            #Agregar error de tipo de expresion distinto de bool
        bool_type = scope.get_type('Bool')
        node.static_type = bool_type
        return bool_type





                
        
        
        
        

