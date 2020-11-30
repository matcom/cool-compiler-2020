from AST import *
from Scope import *
from Cool_Type import *
import visitor as visitor

class Semantics_Checker:
    
    def safe_methods(self, node1:MethodNode, node2: MethodNode, scope:Scope):
        if not node1.name == node2.name:
            return True
        if len(node1.parameters)==len(node2.parameters):
            for i in range(len(node1.parameters)):
                if node1.parameters[i].type != node2.parameters[i].type:
                    print('('+str(node1.line)+', '+str(node1.index)+') - SemanticError: In redifined method '+node1.name+', parameter type '+node1.parameters[i].type+' is different from original type '+node2.parameters[i].type +'.')
                    scope.invalidate()
            if node1.return_type != node2.return_type:
                 print('('+str(node1.line)+', '+str(node1.index)+') - SemanticError: In redifined method '+node1.name+', return type '+node1.return_type+' is different from original return type '+node2.return_type +'.')
                 scope.invalidate()
            return True
        print('('+str(node1.line)+', '+str(node1.index)+') - SemanticError: Incompatible number of formal parameters in redifined method '+node1.name+'.')
        scope.invalidate()
        return False
    
    def params_for_method(self, node1:list, node2: MethodNode, scope:Scope):
        if len(node1)==len(node2.parameters):
            for i in range(len(node2.parameters)):
                if not scope.lower_than(node1[i], scope.get_type(node2.parameters[i].type)):
                    return node2.parameters[i].name
            return "all clear"
        return "wrong number"

    def check_inheritance(self, classes: list, scope:Scope):
        mask = [0] * (len(classes) + 2)
        mapper = {}
        mask[-1] = 2
        mask[-2] = 2
        mapper["Object"] = len(classes) + 1
        mapper["IO"] = len(classes)
        for i in range(len(classes)):
            cclass = classes[i]
            mapper[cclass.name] = i
        for cclass in classes:
            if cclass.parent in ["Int","String","Bool"]:
                mask[mapper[cclass.name]]=2
            elif not cclass.parent in mapper:
                print('('+str(cclass.line)+', '+str(cclass.index)+') - TypeError: Class '+ cclass.name +' inherits from an undefined class '+ cclass.parent +'.')
                scope.invalidate()
                cclass.parent = 'Object'            
        for i in range(len(classes)):
            cclass = classes[i]
            if cclass.parent in ["Int","String","Bool","Object","IO","SELF_TYPE"]:
                pass
            elif not self.check_cyclic_inheritance(i,mask,mapper,classes,scope)==2:
                return False
        return True
    
    def check_cyclic_inheritance(self, cclass: int, mask: list, mapper: dict, classes: list, scope:Scope):
        if mask[cclass] == 2:
            return 2
        elif mask[cclass] == 1:
            mask[cclass] = 2
            return 1
        mask[cclass] = 1
        parent = mapper[classes[cclass].parent]
        ret = self.check_cyclic_inheritance(parent, mask, mapper, classes,scope)
        if ret == 1:
             print('('+str(classes[cclass].line)+', '+str(classes[cclass].index)+') - SemanticError: Class '+ classes[cclass].name +', or an ancestor of '+ classes[cclass].name +', is involved in an inheritance cycle.')
             scope.invalidate()
             return 0
        mask[cclass] = 2
        return ret

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
        rscope = Scope(None)
        if self.check_inheritance(node.classes,rscope):
            for c_class in node.classes:
                cool_type = Cool_Type(c_class.name, c_class.parent, c_class.attributes, c_class.methods)
                if cool_type.name in ["Int","String","Bool","Object","IO","SELF_TYPE"]:
                    print('('+str(c_class.line)+', '+str(c_class.index)+') - SemanticError:  Redefinition of basic class '+c_class.name+'.')
                    rscope.invalidate()
                elif not rscope.create_type(cool_type):
                    print('('+str(c_class.line)+', '+str(c_class.index)+') - SemanticError: Classes may not be redifined.')
                    rscope.invalidate()
            for c_class in node.classes:
                if not c_class.name in ["Int","String","Bool","Object","IO","SELF_TYPE"]:
                    scope = Scope(c_class.name,rscope)
                    self.visit(c_class,scope)
                else:
                    pass
        return rscope.valid

    @visitor.when(ClassNode)
    def visit(self, node: ClassNode, scope: Scope):
        parent = node.parent
        if node.parent in ["Int","String","Bool"]:
            print('('+str(node.line)+', '+str(node.index)+') - SemanticError: Class '+ node.name +' cannot inherit class '+node.parent+'.')
            scope.invalidate()
        cparent = scope.get_type(parent)
        for attr in node.attributes:
            if cparent:
                p_attr = scope.get_parent_attribute(attr.name)
                if p_attr and attr.name == p_attr.name:
                    print('('+str(attr.line)+', '+str(attr.index)+') - SemanticError: Attribute '+attr.name+' is an attribute of an inherited class.')
                    scope.invalidate()
            if not scope.define_attribute(attr.name, attr.type, attr.value):
                print('('+str(attr.line)+', '+str(attr.index)+') - SemanticError: Attribute '+attr.name+' is multiply defined in class.')
                scope.invalidate()
        for method in node.methods:
            if cparent:
                p_method = scope.get_parent_method(method.name)
                if not p_method is None:
                    self.safe_methods(method, p_method,scope)
            if not scope.define_method(method.name, method.parameters, method.return_type, method.body):
                 print('('+str(method.line)+', '+str(method.index)+') - SemanticError: Method '+method.name+' is multiply defined.')
                 scope.invalidate()
        for attr in node.attributes:
            self.visit(attr,scope)
        for method in node.methods:
            nscope = Scope(scope.class_name,scope)
            self.visit(method,nscope)

    @visitor.when(AttributeNode)
    def visit(self, node: AttributeNode, scope: Scope):
        if not scope.exists_type(node.type) and scope.local:
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: Class '+node.type+' of let-bound identifier '+node.name+' is undefined.')
            scope.invalidate()
        elif not scope.exists_type(node.type):
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: Class '+node.type+' of attribute '+node.name+' is undefined.')
            scope.invalidate()
        else:
            node.static_type = scope.get_type(node.type)
            t_value = node.static_type
            if node.value:
                t_value = self.visit(node.value,scope)
            if scope.local:
                if not scope.define_variable(node.name, node.static_type, True, node.value):
                    print('('+str(node.line)+', '+str(node.index)+") - SemanticError: 'self' cannot be bound in a 'let' expression.")
                    scope.invalidate()
                elif not scope.lower_than(t_value, node.static_type):
                    print('('+str(node.line)+', '+str(node.index)+') - TypeError: Inferred type '+ t_value.name + ' of initialization of '+ node.name + ' does not conform to identifiers declared type ' + node.type)
                    scope.invalidate()
            else:
                if node.name == 'self':
                    print('('+str(node.line)+', '+str(node.index)+") - SemanticError: 'self' cannot be the name of an attribute")
                    scope.invalidate()
                elif t_value and not scope.lower_than(t_value, node.static_type):
                    print('('+str(node.line)+', '+str(node.index)+') - TypeError: Inferred type '+ t_value.name + ' of initialization of attribute '+ node.name + ' does not conform to declared type ' + node.type)
                    scope.invalidate()
            return scope.get_type(node.type)
            
    
    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope: Scope):
        nscope = Scope(scope.class_name, scope, True)
        for param in node.parameters:
            self.visit(param, nscope)
        if not nscope.exists_type(node.return_type):
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: Undefined return type '+node.return_type+' in method '+node.name+'.')
            scope.invalidate()
        else:
            t_value = self.visit(node.body,nscope)
            node.static_type = nscope.get_type(node.return_type)
            if not node.static_type.name == 'SELF_TYPE' and t_value.name == 'SELF_TYPE':
                t_value = nscope.get_type(scope.class_name)
            if not nscope.lower_than(t_value, node.static_type):
                print('('+str(node.line)+', '+str(node.index)+') - TypeError: Inferred return type '+ t_value.name + ' of method '+ node.name + ' does not conform to declared return type ' + node.return_type)
                scope.invalidate()
    
    @visitor.when(ParameterNode)
    def visit(self, node: ParameterNode, scope: Scope):
        if not scope.exists_type(node.type):
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: Class '+node.type+' of formal parameter '+node.name+' is undefined.')
            scope.invalidate()
        else:
            if node.name == 'self':
                print('('+str(node.line)+', '+str(node.index)+") - SemanticError: 'self' cannot be the name of a formal parameter")
                scope.invalidate()
            elif not scope.define_variable(node.name,scope.get_type(node.type)):
                print('('+str(node.line)+', '+str(node.index)+') - SemanticError: Formal parameter '+ node.name +' is multiply defined.')
                scope.invalidate()

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
        if node.static_type is None:
            print('('+str(node.line)+', '+str(node.index)+") - TypeError: 'new' used with undefined class "+node.type+".")
            scope.invalidate()
        return scope.get_type(node.type)
    
    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        if not scope.exists_variable(node.id):
            print('('+str(node.line)+', '+str(node.index)+') - NameError: Undeclared identifier '+node.id)
            scope.invalidate()
        return_type = scope.get_variable_type(node.id)
        node.static_type = return_type
        return return_type

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope: Scope):
        node.static_type = scope.get_type('Bool')
        t_value = self.visit(node.expression, scope)
        node.tipo=t_value.name
        # if not scope.lower_than(t_value, node.static_type):
        #     pass
        #     #Agregar error de tipo invalido en la expresion
        return scope.get_type("Bool")
    
    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        t_value = self.visit(node.expression,scope)
        if not scope.exists_variable(node.variable):
            pass
            #Agregar error de variable indefinida
        else:
            static_type = scope.get_variable_type(node.variable)
            if node.variable == 'self':
                print('('+str(node.line)+', '+str(node.index)+") - SemanticError: Cannot assign to 'self'.")
                scope.invalidate()
            elif not scope.lower_than(t_value, static_type):
                print('('+str(node.line)+', '+str(node.index)+') - TypeError: Inferred type '+ t_value.name + ' of initialization of attribute '+ node.variable + ' does not conform to declared type ' + static_type.name)
                scope.invalidate()
        node.static_type = t_value
        return t_value
    
    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        expr_type = None
        for expr in node.expressions:
            expr_type = self.visit(expr, scope)
        node.static_type = expr_type
        return expr_type

    @visitor.when(DispatchNode)
    def visit(self, node: DispatchNode, scope: Scope):
        if node.line==95:
            print()
        if node.left_expression:
            param_types = []
            for param in node.parameters:
                param_type = self.visit(param,scope)
                if param_type.name == "SELF_TYPE":
                    param_type = scope.get_type(scope.class_name)
                param_types.append(param_type)
            dtype = self.visit(node.left_expression,scope)
            if dtype.name == "SELF_TYPE":
                dtype = scope.get_type(scope.class_name)
            node.left_type=dtype.name
            if node.left_type==None:
                print()
            if not scope.exists_type_method(dtype,node.func_id):
                print('('+str(node.line)+', '+str(node.index)+') - AttributeError: Dispatch to undefined method '+node.func_id+'.')
                scope.invalidate()
            else:
                method = scope.get_type_method(dtype,node.func_id)
                params = self.params_for_method(param_types,method,scope)
                if params == "wrong number":
                    print('('+str(node.line)+', '+str(node.index)+') - SemanticError: Method '+node.func_id+' called with wrong number of arguments.')
                    scope.invalidate()
                elif not params == "all clear":
                    print('('+str(node.line)+', '+str(node.index)+') - TypeError: In call of method '+ node.func_id +', type of parameter '+params+' does not conform to declared type.')
                    scope.invalidate()
                return_type = scope.get_type(method.return_type)
                if return_type.name == "SELF_TYPE":
                    return_type = dtype
                node.static_type = return_type
                return return_type
        else:
            param_types = []
            for param in node.parameters:
                param_types.append(self.visit(param,scope)) 
            dtype = scope.get_type(scope.class_name)
            node.left_type=dtype.name
            if node.left_type==None:
                print()
            if not scope.exists_type_method(dtype,node.func_id):
                print('('+str(node.line)+', '+str(node.index)+') - AttributeError: Dispatch to undefined method '+node.func_id)
                scope.invalidate()
            else:
                method = scope.get_type_method(dtype,node.func_id)
                params = self.params_for_method(param_types,method,scope)
                if params == "wrong number":
                    print('('+str(node.line)+', '+str(node.index)+') - SemanticError: Method '+node.func_id+' called with wrong number of arguments.')
                    scope.invalidate()
                elif not params == "all clear":
                    print('('+str(node.line)+', '+str(node.index)+') - TypeError: In call of method '+ node.func_id +', type of parameter '+params+' does not conform to declared type.')
                    scope.invalidate()
                return_type = scope.get_type(method.return_type)
                if return_type.name == "SELF_TYPE":
                    return_type = dtype
                node.static_type = return_type
                return return_type
    
    @visitor.when(StaticDispatchNode)
    def visit(self, node: StaticDispatchNode, scope: Scope):
            param_types = []
            for param in node.parameters:
                param_type = self.visit(param, scope)
                if param_type.name == "SELF_TYPE":
                    param_type = scope.get_type(scope.class_name)
                param_types.append(param_type)
            dtype = self.visit(node.left_expression,scope)
            if dtype.name == "SELF_TYPE":
                dtype = scope.get_type(scope.class_name)
            node.left_type=dtype.name         
            parent_type = scope.get_type(node.parent_id)
            if not scope.lower_than(dtype, parent_type):
                print('('+str(node.line)+', '+str(node.index)+') - TypeError: Expression type '+ dtype.name +' does not conform to declared static dispatch type '+ parent_type.name +'.')
                scope.invalidate()
            elif not scope.exists_type_method(dtype,node.func_id):
                print('('+str(node.line)+', '+str(node.index)+') - AttributeError: Dispatch to undefined method '+node.func_id)
                scope.invalidate()
            else:
                method = scope.get_type_method(parent_type,node.func_id)
                params = self.params_for_method(param_types,method,scope)
                if params == "wrong number":
                    print('('+str(node.line)+', '+str(node.index)+') - SemanticError: Method '+node.func_id+' called with wrong number of arguments.')
                    scope.invalidate()
                elif not params == "all clear":
                    print('('+str(node.line)+', '+str(node.index)+') - TypeError: In call of method '+ node.func_id +', type of parameter '+params+' does not conform to declared type.')
                    scope.invalidate()
                return_type = scope.get_type(method.return_type)
                if return_type.name == "SELF_TYPE":
                    return_type = dtype
                node.static_type = return_type
                return return_type
    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        nscope = Scope(scope.class_name, scope,True)
        for declaration in node.declarations:
            self.visit(declaration, nscope)
        b_value = self.visit(node.body,nscope)
        node.static_type = b_value
        return b_value 
    
    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope):
        ptype = self.visit(node.predicate,scope)
        if ptype and not ptype.name == "Bool":
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: Predicate of '+"'if'"+ 'does not have type Bool.')
            scope.invalidate()
        ttype = self.visit(node.then_body,scope)
        etype = self.visit(node.else_body,scope)
        if not ttype and not etype:
            node.static_type = scope.get_type('Object')
            return scope.get_type('Object')
        elif not etype:
            node.static_type = ttype
            return ttype
        elif not ttype:
            node.static_type = etype
            return etype
        elif ttype.name == 'SELF_TYPE' and etype.name == 'SELF_TYPE':
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
        ptype = self.visit(node.predicate, scope)
        if not ptype.name == "Bool":
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: Loop condition does not have type Bool.')
            scope.invalidate()
        self.visit(node.body,scope)
        node.static_type = scope.get_type("Object")
        return scope.get_type("Object")
    
    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):
        sub_types = []
        dtype = self.visit(node.expression,scope)
        for subcase in node.subcases:
            if not subcase.type in sub_types:
                sub_types.append(subcase.type)
            else:
                print('('+str(subcase.line)+', '+str(subcase.index)+') - SemanticError: Duplicate branch'+subcase.type+'in case statement.')
                scope.invalidate()
        sub_rtypes = []
        for subcase in node.subcases:
            nscope = Scope(scope.class_name,scope,True)
            sub_rtypes.append(self.visit(subcase,nscope))
        return_type = sub_rtypes[0]
        for subtype in sub_rtypes:
            if return_type.name == "SELF_TYPE" and subtype.name == "SELF_TYPE":
                continue
            elif return_type.name == "SELF_TYPE":
                return_type = scope.join(scope.get_type(scope.class_name),subtype)
            elif subtype.name == "SELF_TYPE":
                return_type = scope.join(scope.get_type(scope.class_name),return_type)
            else:
                return_type = scope.join(return_type,subtype)
        node.static_type = return_type
        return return_type
    
    @visitor.when(SubCaseNode)
    def visit(self, node: SubCaseNode, scope: Scope):
        stype = scope.get_type(node.type)
        if stype is None:
             print('('+str(node.line)+', '+str(node.index)+') - TypeError: Class '+node.type+' of case branch is undefined.')
             scope.invalidate()
        scope.define_variable(node.name,stype,True)
        return_type = self.visit(node.expression,scope)
        node.static_type = return_type
        return return_type
    
    @visitor.when(IntComplementNode)
    def visit(self, node: IntComplementNode, scope: Scope):
        etype = self.visit(node.right, scope)
        if not etype.name == "Int":
            print('('+str(node.line)+', '+str(node.index)+") - TypeError: Argument of '~' has type "+etype.name+" instead of Int.")
            scope.invalidate()
        int_type = scope.get_type('Int')
        node.static_type = int_type
        return int_type
    
    @visitor.when(BoolComplementNode)
    def visit(self, node: BoolComplementNode, scope: Scope):
        etype = self.visit(node.right, scope)
        if not etype.name == "Bool":
            print('('+str(node.line)+', '+str(node.index)+") - TypeError: Argument of 'not' has type "+etype.name+" instead of Bool.")
            scope.invalidate()
        bool_type = scope.get_type('Bool')
        node.static_type = bool_type
        return bool_type
    
    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if ltype and rtype and (not ltype.name == 'Int' or not rtype.name == 'Int'):
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: non-Int arguments: '+ ltype.name +' '+node.operator+' '+rtype.name)
            scope.invalidate()
        int_type = scope.get_type('Int')
        node.static_type = int_type
        return int_type
    
    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if not ltype.name == 'Int' or not rtype.name == 'Int':
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: non-Int arguments: '+ ltype.name +' '+node.operator+' '+rtype.name)
            scope.invalidate()
        int_type = scope.get_type('Int')
        node.static_type = int_type
        return int_type
    
    @visitor.when(MultNode)
    def visit(self, node: MultNode, scope: Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if not ltype.name == 'Int' or not rtype.name == 'Int':
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: non-Int arguments: '+ ltype.name +' '+node.operator+' '+rtype.name)
            scope.invalidate()
        int_type = scope.get_type('Int')
        node.static_type = int_type
        return int_type
    
    @visitor.when(DivNode)
    def visit(self, node: DivNode, scope: Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if not ltype.name == 'Int' or not rtype.name == 'Int':
            print('('+str(node.line)+', '+str(node.index)+') - TypeError: non-Int arguments: '+ ltype.name +' '+node.operator+' '+rtype.name)
            scope.invalidate()
        int_type = scope.get_type('Int')
        node.static_type = int_type
        return int_type
    
    @visitor.when(LesserNode)
    def visit(self, node: LesserNode, scope: Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if node.operator == '=':
            if ltype.name in ['Int','Bool','String'] or rtype.name in ['Int','Bool','String']:
                if not ltype.name == rtype.name:
                     print('('+str(node.line)+', '+str(node.index)+') - TypeError: Illegal comparison with a basic type.')
                     scope.invalidate()
        else:
            if not ltype.name == 'Int' or not rtype.name == 'Int':
                print('('+str(node.line)+', '+str(node.index)+') - TypeError: non-Int arguments: '+ ltype.name +' '+node.operator+' '+rtype.name)
                scope.invalidate()
        bool_type = scope.get_type('Bool')
        node.static_type = bool_type
        return bool_type
    
    @visitor.when(LesserEqualNode)
    def visit(self, node: LesserEqualNode, scope: Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if node.operator == '=':
            if ltype.name in ['Int','Bool','String'] or rtype.name in ['Int','Bool','String']:
                if not ltype.name == rtype.name:
                     print('('+str(node.line)+', '+str(node.index)+') - TypeError: Illegal comparison with a basic type.')
                     scope.invalidate()
        else:
            if not ltype.name == 'Int' or not rtype.name == 'Int':
                print('('+str(node.line)+', '+str(node.index)+') - TypeError: non-Int arguments: '+ ltype.name +' '+node.operator+' '+rtype.name)
                scope.invalidate()
        bool_type = scope.get_type('Bool')
        node.static_type = bool_type
        return bool_type
    
    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if node.operator == '=':
            if ltype.name == 'String':
                node.isString=True
            if ltype.name in ['Int','Bool','String'] or rtype.name in ['Int','Bool','String']:
                if not ltype.name == rtype.name:
                     print('('+str(node.line)+', '+str(node.index)+') - TypeError: Illegal comparison with a basic type.')
                     scope.invalidate()
        else:
            if not ltype.name == 'Int' or not rtype.name == 'Int':
                print('('+str(node.line)+', '+str(node.index)+') - TypeError: non-Int arguments: '+ ltype.name +' '+node.operator+' '+rtype.name)
                scope.invalidate()
        bool_type = scope.get_type('Bool')
        node.static_type = bool_type
        return bool_type





                
        
        
        
        

