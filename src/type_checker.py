
import visitor
import ast_hierarchy
import context

class TypeCheckerVisitor:
    def __init__(self):
        self.current_type = None # type(current_type) = Type

    @visitor.on('node')
    def visit(self, node, context):
        pass

    # [Program]
    @visitor.when(ast_hierarchy.ProgramNode)
    def visit(self, node, context):
        '''
        In this method is where we start the visitor over
        the ast_hierarchy, checking all classes and last the main class
        and it's main method.
        '''
        # build the types_graph
        context.BuilTypesGraph()
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
    def visit(self, node, context):
        self.current_type = context.GetType(node.typeName)

        # adding to the current enviroment all the class attributes
        for attr in self.current_type.AttrList:    
            context.DefineVar(attr.name, attr._type, None)

        for _f in node.features:
            self.visit(_f, context)

    

    @visitor.when(ast_hierarchy.ComplementNode)
    def visit(self, node, context):
        self.visit(node.expression)
        if (node.expression.ComputedType.Name != "Int"):
            #error
            pass
        else:
            node.ComputedType = context.Hierarchy.get("Int")

    @visitor.when(ast_hierarchy.IsVoidNode)
    def visit(self,node,context):
        self.visit(node.expression)
        if (node.expression.ComputedType.Name != "Void"):
            #error
            pass
        else:
            node.ComputedType = context.Hierarchy.get("Bool")

    @visitor.when(ast_hierarchy.NotNode)
    def visit(self, node, context):
        self.visit(node.expression, context)
        if (node.expression.ComputedType.Name != "Bool")
            #error
            pass
        else:
            node.ComputedType = context.Hierarchy.get("Bool") 
        
    @visitor.when(ast_hierarchy.IntBinaryNode)
    def visit(self, node, context):
        self.visit(node.left, context)
        self.visit(node.rigth, context)
        left_type = _left.ComputedType
        right_type = _right.ComputedType
        if (left_type.Name == "Int" and right_type.Name == "Int"):
            node.ComputedType = context.Hierarchy.get("Int")
        #error

    @visitor.when(ast_hierarchy.BoolBinaryNode)
    def visit(self, node, context):
        self.visit(node.left, context)
        self.visit(node.rigth, context)
        left_type = _left.ComputedType
        right_type = _right.ComputedType
         if (left_type.Name == "Bool" and right_type.Name == "Bool"):
            node.ComputedType = context.Hierarchy.get("Bool")
        
    @visitor.when(ast_hierarchy.ConstantNumericNode)
    def visit(self, node, context):
        node.ComputedType = context.Hierarchy.get("Int")

    @visitor.when(ast_hierarchy.ConstantBoolNode)
    def visit(self, node, context):
        node.ComputedType = context.Hierarchy.get("Bool")

    @visitor.when(ast_hierarchy.ConstantStringBool)
    def visit(self, node, context):
        node.ComputedType = context.Hierarchy.get("String")    