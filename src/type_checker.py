
import visitor
import ast_hierarchy
import context

#   To Do list:
#       *Hacer los visit de Method y Attr
#       *Poner la linea a todos

class TypeCheckerVisitor:
    def __init__(self):
        self.current_type = None # type(current_type) = Type

    @visitor.on('node')
    def visit(self, node, context, errors):
        pass

    # [Program]
    @visitor.when(ast_hierarchy.ProgramNode)
    def visit(self, node, context, errors):
        '''
        In this method is where we start the visitor over
        the ast_hierarchy, checking all classes and last the main class
        and it's main method.
        '''
        # build the types_graph
        context.BuildTypesHierarchy()
        # check if Program has a clas Main with a local method main
        context.CheckMain()
        # check if are not cycles in the inheritance graph
        context.IsTree(errors)
        if len(errors) > 0: 
            return
        # check inheritance features and build LCA preprocessing

        # check if classes are ok

        for _class in node.classes:
            child_context = context.CreateChildContext()
            self.visit(_class, child_context, errors)

    # [Class]
    @visitor.when(ast_hierarchy.ClassNode)
    def visit(self, node, context, errors):
        self.current_type = context.GetType(node.typeName)

        # adding to the current enviroment all the class attributes
        parent = self.current_type.Parent
        for attr in self.current_type.AttrList: 
            #verificar que el attr no exista en ningun ancestro antes de crearlo
            if  attr.Name == 'self' or not parent.IsDefineAttr2(attr, parent):
                _attr = context.DefineVar(attr.Name, attr.Type, None)
            else:
                errors.append("error")
                return 
        for meth_name in self.current_type.MethList:
            meth = self.current_type.MethList[meth_name]
            parent_meth = context.IsDefineMeth2(self.current_type.Parent, meth_name)
            if meth is not None:
                if parent_meth is not None:
                    if parent_meth.ReturnType != meth.ReturnType:
                        errors.append("SemanticError: In redefined method " + meth.Name + ", return type " + meth.ReturnType + "is different from original return type " + parent_meth.ReturnType + ". ")
                        return
                    if len(parent_meth.ParamsName) != len(meth.ParamsName):
                        errors.append("SemanticError: Incompatible number of formal parameters in redefined method " + meth.Name + ".")
                        return
                    for i in range(len(meth.ParamsName)):
                        if meth.ParamsType[i] != parent_meth.ParamsType[i]:
                            errors.append("SemanticError: In redefined method " + meth.Name + ", parameter type " + meth.ParamsType[i] + " is different from original type " + parent_meth.ParamsType[i] + ".")
                            return
                for i in range(len(meth.ParamsName)):
                    param_name = meth.ParamsName[i]
                    param_type = meth.ParamsType[i]
                    var = meth.Context.DefineVar(param_name, param_type)

        for _f in node.features:
            child_context = context.CreateChildContext()
            self.visit(_f, child_context, errors)


    @visitor.when(ast_hierarchy.FunctionFeatureNode)
    def visit(self, node, context, errors):
        node.ComputedType = [] 
        meth = context.IsDefineMeth2(self.current_type, node.id)
        self.visit(node.statements, meth.Context, errors)
        node.ComputedType = node.statements.ComputedType
        for _type in node.ComputedType:
            if not (node.typeName == _type.Name or context.IsDerived( _type.Name, node.typeName)):
                errors.append("TypeError: Inferred return type " + _type.Name +" of method " + node.id + " does not conform to declared type " + node.typeName + ".")
        meth.ComputedType = node.ComputedType

    @visitor.when(ast_hierarchy.FunctionCallStatement)
    def visit(self, node, context, errors):
        node.ComputedType = []
        d = node.dispatchType
        self.visit(node.instance, context, errors)
        instance_type = context.GetType(node.instance.typeName) if node.instance.typeName != 'self' else self.current_type
        if d is not None:
            #revisar si d es padre de instance, en caso positivo, hacer instance igual a d
                if not (d == instance_type.Name  or context.IsDerived( d, instance_type.Name)):
                    errors.append("TypeError: Expression type " + instance_type.Name + "does not conform to declared static dispatch type " + d +". ")
            #en caso negativo lanzar error que debe imprimir dispatch6

        meth = context.IsDefineMeth2(instance_type, node.function) 
        if meth is not None:
            if len(meth.ParamsName) != len(node.args):
                errors.append("SemanticError: Method " + meth.Name + " called with wrong number of arguments. ")
            for i in range(len(meth.ParamsName)):
                var_name = meth.ParamsName[i]
                var = meth.Context.Variables[var_name]
                param_type = var.Type
                arg = node.args[i]
                self.visit(arg, context, errors)
                for _type in arg.ComputedType:
                    if not (param_type == _type.Name  or context.IsDerived( _type.Name, param_type)):
                        errors.append("TypeError: In call of method " + meth.Name +", type " + _type.Name +  " of parameter " + var_name + " does not conform to declared type " + param_type + ".")
                        break    
            self.visit(node.instance, meth.Context, errors)
            node.typeName = meth.ReturnType
            node.ComputedType = [context.GetType(meth.ReturnType)]
        else:
            errors.append("AttributeError: Dispatch to undefined method " + node.function + ". ")
          
    @visitor.when(ast_hierarchy.AttributeFeatureNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        
        if (not context.Hierarchy.__contains__(node.typeName)):
                errors.append("TypeError: Class " + node.typeName + " of identifier " + node.id + " is undefined.")
        if node.expression is not None:
            node.ComputedType = []
            self.visit(node.expression, context, errors)
            #revisar si debo preguntar por el typeName o por el ComputedType
            for _type in node.expression.ComputedType:
                if not (node.typeName == _type.Name or context.IsDerived( _type.Name, node.typeName)):
                    errors.append("TypeError: Inferred type " + _type.Name +" of initialization of " + node.id + " does not conform to identifier's declared type " + node.typeName + ".")
                else: 
                    node.ComputedType.append(_type) 
            attr = context.Variables[node.id]
            attr.ComputedType = node.ComputedType            

    @visitor.when(ast_hierarchy.NewStatementNode)
    def visit(self, node, context, errors):
        _type = context.GetType(node.typeName)
        if not _type is None:
            node.ComputedType = [_type]
        else: 
            errors.append("TypeError: 'new' used with undefined class " + node.typeName + ".")

    @visitor.when(ast_hierarchy.ConditionalStatementNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        
        self.visit(node.ifExpr, context, errors)
        self.visit(node.evalExpr, context, errors)
        self.visit(node.elseExpr, context, errors)
        node.typeName = node.evalExpr.typeName if context.IsDerived(node.elseExpr.typeName, node.ifExpr.typeName) else node.elseExpr.typeName
        for _type in node.evalExpr.ComputedType:
            if (_type.Name != "Bool"):
                errors.append("TypeError: Predicate of 'if' does not have type Bool.")
        node.ComputedType = node.ifExpr.ComputedType + node.elseExpr.ComputedType

    @visitor.when(ast_hierarchy.LoopStatementNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = 'null'
        self.visit(node.loopExpr, context, errors)
        self.visit(node.evalExpr, context, errors)
        for _type in node.evalExpr.ComputedType:
            if _type.Name != "Bool":
                errors.append("TypeError: Loop condition does not have type Bool.")
                return
            
        node.ComputedType = node.loopExpr.ComputedType

    @visitor.when(ast_hierarchy.BlockStatementNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        
        for _expr in node.expressions:
            self.visit(_expr,context, errors)

        node.ComputedType = node.expressions[-1].ComputedType
        node.typeName = node.expressions[-1].typeName
    

    @visitor.when(ast_hierarchy.VariableNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = 'error'

        if (node.lex == 'self'):
            node.typeName = self.current_type.Name
            node.ComputedType = [context.GetType(node.typeName)]
        else:
            node.ComputedType = []
            _var = context.GetAttr(self.current_type, node.lex)
            if _var is None:
                errors.append("NameError: Undefined identifier " + node.lex)
            else:
                node.typeName = _var.Type
                node.ComputedType = [context.GetType(node.typeName)]

    @visitor.when(ast_hierarchy.LetStatementNode)
    def visit(self, node, context, errors):
        node.ComputedType = []

        child_context = context.CreateChildContext()
        child_context.Variables = {}
        for _var in node.variables:
            if _var.id == 'self':
                errors.append("SemanticError: 'self' cannot be bound in a 'let' expression.")
                return
            ans = child_context.DefineVar(_var.id, _var.typeName)
            self.visit(_var,child_context, errors)
        self.visit(node.expression,child_context, errors)
        node.ComputedType = node.expression.ComputedType
        node.typeName = node.expression.typeName

    @visitor.when(ast_hierarchy.CaseStatementNode)
    def visit(self, node, context, errors):
        node.ComputedType = []

        self.visit(node.expression, context, errors)
        #Implementar lo que pasara con el body
        _types = []
        for x in node.body:
            if _types.__contains__(x.typeName):
                errors.append("SemanticError: Duplicate branch " + x.typeName + " in case statement.")
                return
            self.visit(x, context, errors)
            _types.append(x.typeName)
            node.ComputedType = node.ComputedType + x.ComputedType
        node.typeName = 'Object'
        #chaquear que el retorno no sea void

    @visitor.when(ast_hierarchy.CaseBranchNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        if not context.Hierarchy.keys().__contains__(node.typeName):
            errors.append("TypeError: Class " + node.typeName + " of case branch is undefined.")
            return
        self.visit(node.expression, context, errors)
        node.ComputedType = node.expression.ComputedType
        #Responder:
        #En que momento hacer chequeo de tipos
        #Quienes son id, type

    @visitor.when(ast_hierarchy.AssignStatementNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error"
        if node.id.lex == 'self': 
            errors.append("SemanticError: Cannot assign to 'self'.")
        self.visit(node.id, context, errors)
        self.visit(node.expression, context, errors)
                #pedir el atributo que se llama node.id y verificar sus tipos para ver si es posible hacer la asignación
        for _type in node.expression.ComputedType:
            #if coinciden los tipos del id y de la expresion:
            
            attr = None
            for var in context.Variables.keys():
                toks = var.split()
                t = toks[-1]
                if len(toks) == 1 or toks[1] == node.id.lex:
                    attr = context.Variables[var]
                    break
            if attr is None:
                errors.append("Undefined identifier "+ node.id.lex + ".")
                return
            if not attr.Name == 'self' and not (attr.Type == _type.Name or context.IsDerived( _type.Name, attr.Type)):
                node.typeName = "error in assign"
                errors.append("Not matching type for assignment in " + attr.Type + "=" + _type.Name )
            else:
                node.ComputedType.append(_type)
                node.typeName = attr.Type 
                




    #Unary Operations
    @visitor.when(ast_hierarchy.ComplementNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error in complement"
        self.visit(node.expression,context, errors)
        for _type in node.expression.ComputedType:
            if (_type.Name != "Int"):
                node.typeName = "error in complement"
                errors.append("TypeError: Argument of '~' has type " + _type.Name + " instead of Int.")
            else:
                node.ComputedType = [context.Hierarchy.get("Int")]

    @visitor.when(ast_hierarchy.IsVoidNode)
    def visit(self,node, context, errors):
        node.typeName = "Bool"

        self.visit(node.expression, context, errors)
        node.ComputedType = [context.Hierarchy.get("Bool")]

    @visitor.when(ast_hierarchy.NotNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error in not"
        self.visit(node.expression, context, errors)
        for _type in node.expression.ComputedType:
            if (_type.Name != "Bool"):
                node.typeName = "error in not"
                errors.append("TypeError: Argument of 'not' has type " + _type.Name +  " instead of Bool.")
            else:
                node.ComputedType = [context.Hierarchy.get("Bool") ]



    #Binary int expressions   
    @visitor.when(ast_hierarchy.PlusNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error in plus"

        self.visit(node.left, context, errors)
        self.visit(node.right, context, errors)
        left_type = node.left.ComputedType
        right_type = node.right.ComputedType
        for left_type in node.left.ComputedType:
            for right_type in node.right.ComputedType:
                if (left_type.Name == "Int" and right_type.Name == "Int"):
                    node.ComputedType = [context.Hierarchy.get("Int")]
                    node.typeName = "Int"
                else:
                    errors.append("TypeError: non-Int arguments: " + left_type.Name + " + " + right_type.Name)

    @visitor.when(ast_hierarchy.MinusNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error in minus"

        self.visit(node.left, context, errors)
        self.visit(node.right, context, errors)
        left_type = node.left.ComputedType
        right_type = node.right.ComputedType
        for left_type in node.left.ComputedType:
            for right_type in node.right.ComputedType:
                if (left_type.Name == "Int" and right_type.Name == "Int"):
                    node.ComputedType = [context.Hierarchy.get("Int")]
                    node.typeName = "Int"
                else:
                    errors.append("TypeError: non-Int arguments: " + left_type.Name + " - " + right_type.Name)

    @visitor.when(ast_hierarchy.TimesNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error in times"

        self.visit(node.left, context, errors)
        self.visit(node.right, context, errors)
        for left_type in node.left.ComputedType:
            for right_type in node.right.ComputedType:
                if (left_type.Name == "Int" and right_type.Name == "Int"):
                    node.ComputedType = [context.Hierarchy.get("Int")]
                    node.typeName = "Int"
                else:
                    errors.append("TypeError: non-Int arguments: " + left_type.Name + " * " + right_type.Name)

    @visitor.when(ast_hierarchy.DivideNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error in div"

        self.visit(node.left, context, errors)
        self.visit(node.right, context, errors)
        for left_type in node.left.ComputedType:
            for right_type in node.right.ComputedType:
                if (left_type.Name == "Int" and right_type.Name == "Int"):
                    node.ComputedType = [context.Hierarchy.get("Int")]
                    node.typeName = "Int"
                else:
                    errors.append("TypeError: non-Int arguments: " + left_type.Name + " / " + right_type.Name)

 
 
    #Binary bool expressions
    @visitor.when(ast_hierarchy.EqualNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error ="

        self.visit(node.left, context, errors)
        self.visit(node.right, context, errors)
        for left_type in node.left.ComputedType:
            for right_type in node.right.ComputedType:
                if (left_type.Name == "Int" and right_type.Name == "Int"):
                    node.ComputedType = [context.Hierarchy.get("Bool")]
                    node.typeName = "Bool"
                else:
                    errors.append("TypeError: non-Int arguments: " + left_type.Name + " = " + right_type.Name)

    @visitor.when(ast_hierarchy.LessNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error <"

        self.visit(node.left, context, errors)
        self.visit(node.right, context, errors)
        for left_type in node.left.ComputedType:
            for right_type in node.right.ComputedType:
                if (left_type.Name == "Int" and right_type.Name == "Int"):
                    node.ComputedType = [context.Hierarchy.get("Bool")]
                    node.typeName = "Bool"
                else:
                    errors.append("TypeError: non-Int arguments: " + left_type.Name + " < " + right_type.Name)

    @visitor.when(ast_hierarchy.LessEqualNode)
    def visit(self, node, context, errors):
        node.ComputedType = []
        node.typeName = "error <="
        self.visit(node.left, context, errors)
        self.visit(node.right, context, errors)
        for left_type in node.left.ComputedType:
            for right_type in node.right.ComputedType:
                if (left_type.Name == "Int" and right_type.Name == "Int"):
                    node.ComputedType = [context.Hierarchy.get("Bool")]
                    node.typeName = "Bool"
                else:
                    errors.append("TypeError: non-Int arguments: " + left_type.Name + " <= " + right_type.Name)

  
    #Ctes
    @visitor.when(ast_hierarchy.ConstantNumericNode)
    def visit(self, node, context, errors):
        node.ComputedType = [context.Hierarchy.get("Int")]
        node.typeName = "Int"
        node.ComputedType = [context.GetType(node.typeName)]

    @visitor.when(ast_hierarchy.ConstantBoolNode)
    def visit(self, node, context, errors):
        node.ComputedType = [context.Hierarchy.get("Bool")]
        node.typeName = "Bool"
        node.ComputedType = [context.GetType(node.typeName)]

    @visitor.when(ast_hierarchy.ConstantStringNode)
    def visit(self, node, context, errors):
        node.ComputedType = [context.Hierarchy.get("String")]
        node.typeName = "String"    
        node.ComputedType = [context.GetType(node.typeName)]