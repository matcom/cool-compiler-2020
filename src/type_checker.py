
import visitor
import ast_hierarchy
import context



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
        context.IsTree()
        # check inheritance features and build LCA preprocessing

        # check if classes are ok
        for _class in node.class_list:
            child_context = context.CreateChildContext()
            self.visit(_class, child_context)

    # [Class]
    @visitor.when(ast_hierarchy.ClassNode)
    def visit(self, node, context, errors):
        self.current_type = context.GetType(node.typeName)

        # adding to the current enviroment all the class attributes
        for attr in self.current_type.AttrList:    
            context.DefineVar(attr.name, attr._type, None)

        for _f in node.features:
            self.visit(_f, context)

    @visitor.when(ast_hierarchy.ConditionalStatementNode)
    def visit(self, node, context, errors):
        self.visit(node.ifExpr)
        self.visit(node.evalExpr)
        self.visit(node.elseExpr)
        if (node.ifExpr.ComputedType.Name != "Bool"):
            errors.append("TypeError: Predicate of 'if' does not have type Bool.")
            pass

    @visitor.when(ast_hierarchy.LoopStatementNode)
    def visit(self, node, context, errors):
        self.visit(node.loopExpr, context)
        self.visit(node.evalExpr, context)

    @visitor.when(ast_hierarchy.BlockStatementNode)
    def visit(self, node, context, errors):
        for _expr in node.expressions:
            self.visit(_expr,context)
    
    @visitor.when(ast_hierarchy.LetStatementNode)
    def visit(self, node, context, errors):
        for _var in self.variables:
            self.visit(_var,context)
        self.visit(node.expr,context)

    @visitor.when(ast_hierarchy.CaseStatementNode)
    def visit(self, node, context, errors):
        self.visit(node.expression)
        #Implementar lo que pasara con el body
        for x in node.body:
            self.visit(x, context)
        #chaquear que el retorno no sea void

    @visitor.when(ast_hierarchy.CaseBranchNode)
    def visit(self, node, context, errors):
        self.visit(node.expr, context)
        #Responder:
        #En que momento hacer chequeo de tipos
        #Quienes son id, type

    @visitor.when(ast_hierarchy.AssignStatementNode)
    def visit(self, node, context, errors):
        self.visit(node.expr, context)
        self.visit(node.id, context)
        if (node.id.ComputedType == node.expr.ComputedType):
            #todoOK
            node.ComputedType = context.Hierarchy.get(node.id.ComputedType.Name)
            pass
        else:
            errors.append("TypeError: Inferred type " + id.ComputedType.Name + " of initialization of attribute " + node.id.id + " does not conform to declared type " + node.expression.Computedtype.Name + ".")
            pass




    #Unary Operations
    @visitor.when(ast_hierarchy.ComplementNode)
    def visit(self, node, context, errors):
        self.visit(node.expression)
        if (node.expression.ComputedType.Name != "Int"):
            errors.append("ypeError: Argument of '~' has type " + node.expression.ComputedType.Name + " instead of Int.")
        else:
            node.ComputedType = context.Hierarchy.get("Int")

    @visitor.when(ast_hierarchy.IsVoidNode)
    def visit(self,node, context, errors):
        self.visit(node.expression)
        if (node.expression.ComputedType.Name != "Void"):
            #error
            pass
        else:
            node.ComputedType = context.Hierarchy.get("Bool")

    @visitor.when(ast_hierarchy.NotNode)
    def visit(self, node, context, errors):
        self.visit(node.expression, context)
        if (node.expression.ComputedType.Name != "Bool"):
            errors.append("TypeError: Argument of 'not' has type " + node.expression.ComputedType.Name +  " instead of Bool.")
            pass
        else:
            node.ComputedType = context.Hierarchy.get("Bool") 



    #Binary int expressions   
    @visitor.when(ast_hierarchy.PlusNode)
    def visit(self, node, context, errors):
        self.visit(node.left, context)
        self.visit(node.rigth, context)
        left_type = _left.ComputedType
        right_type = _right.ComputedType
        if (left_type.Name == "Int" and right_type.Name == "Int"):
            node.ComputedType = context.Hierarchy.get("Int")
        else:
            errors.append("TypeError: non-Int arguments: " + left_type.Name + " + " + right_type.Name)

    @visitor.when(ast_hierarchy.MinusNode)
    def visit(self, node, context, errors):
        self.visit(node.left, context)
        self.visit(node.rigth, context)
        left_type = _left.ComputedType
        right_type = _right.ComputedType
        if (left_type.Name == "Int" and right_type.Name == "Int"):
            node.ComputedType = context.Hierarchy.get("Int")
        else:
            errors.append("TypeError: non-Int arguments: " + left_type.Name + " - " + right_type.Name)

    @visitor.when(ast_hierarchy.TimesNode)
    def visit(self, node, context, errors):
        self.visit(node.left, context)
        self.visit(node.rigth, context)
        left_type = _left.ComputedType
        right_type = _right.ComputedType
        if (left_type.Name == "Int" and right_type.Name == "Int"):
            node.ComputedType = context.Hierarchy.get("Int")
        else:
            errors.append("TypeError: non-Int arguments: " + left_type.Name + " * " + right_type.Name)

    @visitor.when(ast_hierarchy.DivideNode)
    def visit(self, node, context, errors):
        self.visit(node.left, context)
        self.visit(node.rigth, context)
        left_type = _left.ComputedType
        right_type = _right.ComputedType
        if (left_type.Name == "Int" and right_type.Name == "Int"):
            node.ComputedType = context.Hierarchy.get("Int")
        else:
            errors.append("TypeError: non-Int arguments: " + left_type.Name + " / " + right_type.Name)

 
 
    #Binary bool expressions
    @visitor.when(ast_hierarchy.EqualNode)
    def visit(self, node, context, errors):
        self.visit(node.left, context)
        self.visit(node.rigth, context)
        left_type = _left.ComputedType
        right_type = _right.ComputedType
        if (left_type.Name == "Int" and right_type.Name == "Int"):
            node.ComputedType = context.Hierarchy.get("Bool")
        else:
            errors.append("TypeError: non-Int arguments: " + left_type + " == " + right_type)
        
    @visitor.when(ast_hierarchy.LessNode)
    def visit(self, node, context, errors):
        self.visit(node.left, context)
        self.visit(node.rigth, context)
        left_type = _left.ComputedType
        right_type = _right.ComputedType
        if (left_type.Name == "Int" and right_type.Name == "Int"):
            node.ComputedType = context.Hierarchy.get("Bool")
        else:
            errors.append("TypeError: non-Int arguments: " + left_type + " < " + right_type)
        
    @visitor.when(ast_hierarchy.LessEqualNode)
    def visit(self, node, context, errors):
        self.visit(node.left, context)
        self.visit(node.rigth, context)
        left_type = _left.ComputedType
        right_type = _right.ComputedType
        if (left_type.Name == "Int" and right_type.Name == "Int"):
            node.ComputedType = context.Hierarchy.get("Bool")
        else:
            errors.append("TypeError: non-Int arguments: " + left_type + " <= " + right_type)

  
    #Ctes
    @visitor.when(ast_hierarchy.ConstantNumericNode)
    def visit(self, node, context, errors):
        node.ComputedType = context.Hierarchy.get("Int")

    @visitor.when(ast_hierarchy.ConstantBoolNode)
    def visit(self, node, context, errors):
        node.ComputedType = context.Hierarchy.get("Bool")

    @visitor.when(ast_hierarchy.ConstantStringNode)
    def visit(self, node, context, errors):
        node.ComputedType = context.Hierarchy.get("String")    