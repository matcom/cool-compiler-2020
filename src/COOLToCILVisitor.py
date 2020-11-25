import cil
from BaseToCILVisitor import BaseCOOLToCILVisitor
from AstNodes import *
from semantic import *
import visitor

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        self.current_function = self.register_function('main')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        result2 = self.define_internal_local()

        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgsNode([instance]))
        self.register_instruction(cil.DynamicCallNode('Main', self.to_function_name('Ctr', 'Main'), result))
        self.register_instruction(cil.ArgsNode([result]))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('main', 'Main'), result2))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        
        self.current_type = self.context.get_type(node.id)
        
        cil_type = self.register_type(node.id)

        for attr, type_attr in self.current_type.all_attributes():
            cil_type.attributes.append(self.to_attribute_name(attr.name, type_attr.name))
        
        for func, type_func in self.current_type.all_methods():
            cil_type.methods.append((func.name, self.to_function_name(func.name, type_func.name)))
        
        nodeFunctions = [x for x in node.features if isinstance(x, FuncDeclarationNode)]
        for feature, child_scope in zip(nodeFunctions, scope.children[0].children):
            self.visit(feature, child_scope)

        #ctr
        name = self.to_function_name("Ctr", self.current_type.name)
        self.current_function = self.register_function(name)
        self.register_param(VariableInfo('self', self.current_type))

        parentResult = self.define_internal_local()
        self.register_instruction(cil.ArgsNode(['self']))
        self.register_instruction(cil.DynamicCallNode(self.current_type.name, self.to_function_name('Ctr', self.current_type.parent.name), parentResult))


        nodeatt = [x for x in node.features if isinstance(x, AttrDeclarationNode)]
        for feature, child_scope in zip(nodeatt, scope.children[1].children):
            self.visit(feature, child_scope)
        
        self.register_instruction(cil.ReturnNode('self'))

        self.current_type = None
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################
        
        self.current_method = self.current_type.get_method(node.id)
        
        name = self.to_function_name(node.id, self.current_type.name)
        self.current_function = self.register_function(name)

        self.register_param(VariableInfo('self', self.current_type))
        for param in scope.locals:
            self.register_param(param)

        value = self.visit(node.body, scope.children[0])

        self.register_instruction(cil.ReturnNode(value))
        self.current_method = None


    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        if not node.expression is None:
            value = self.visit(node.expression, scope.children[0])
        else:
            if node.type == 'String':
                value = '_empty'
            elif node.type == 'Bool' or node.type == 'Int':
                value = 0
            else:
                value = '_void'

        self.register_instruction(cil.SetAttribNode('self', self.to_attribute_name(node.id, self.current_type.name), value))

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
       
        scopeOpen = scope.children[0]
        
        value = None
        for init in node.let_body:
            if not init[2] is None:
                value = self.visit(init[2], scopeOpen)
            else:
                if init[1] == 'String':
                    value = '_empty'
                elif init[1] == 'Bool' or init[1] == 'Int':
                    value = 0
                else:
                    value = '_void'

            scopeOpen = scopeOpen.children[0]
            vinfo = scopeOpen.find_variable(init[0])
            vname = self.register_local(vinfo)
            self.register_instruction(cil.AssignNode(vname, value))

        return self.visit(node.in_body, scopeOpen.children[0])

    @visitor.when(CaseOfNode)
    def visit(self, node, scope):
        pass

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expression, child in zip(node.expressions, scope.children):
            value = self.visit(expression, child)

        return value

    @visitor.when(IfThenElseNode)
    def visit(self, node, scope):
        cond = self.visit(node.condition, scope.children[0])
        
        labelTrue = self.register_label()
        labelFalse = self.register_label()
        result = self.define_internal_local()

        self.register_instruction(cil.GotoIfNode(labelTrue, cond))
        vfalse = self.visit(node.else_body, scope.children[2])
        self.register_instruction(cil.AssignNode(result, vfalse))
        self.register_instruction(cil.GotoNode(labelFalse))
        self.register_instruction(cil.LabelNode(labelTrue))
        vtrue = self.visit(node.if_body, scope.children[1])
        self.register_instruction(cil.AssignNode(result, vtrue))
        self.register_instruction(cil.LabelNode(labelFalse))

        return result
        
    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        labelWhileStart = self.register_label()
        labelWhileContinue = self.register_label()
        labelWhileBreak = self.register_label()

        self.register_instruction(cil.LabelNode(labelWhileStart))
        
        cond = self.visit(node.condition, scope.children[0])
        
        self.register_instruction(cil.GotoIfNode(labelWhileContinue, cond))
        self.register_instruction(cil.GotoNode(labelWhileBreak))
        self.register_instruction(cil.LabelNode(labelWhileContinue))
        self.visit(node.body, scope.children[1])
        self.register_instruction(cil.GotoNode(labelWhileStart))
        self.register_instruction(cil.LabelNode(labelWhileBreak))

        result = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result, '_void'))
        return result

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        
        vinfo = scope.find_variable(node.id)
        value = self.visit(node.expression, scope.children[0])

        if vinfo is None:
            self.register_instruction(cil.SetAttribNode('self', self.to_attribute_name(node.id, self.current_type.name), value))
        else:
            self.register_instruction(cil.AssignNode(vinfo.cilName, value))
        
        return value

    @visitor.when(FunctionCallNode)
    def visit(self, node, scope):
        ###############################
        # node.obj -> AtomicNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        ###############################
        result = self.define_internal_local()

        obj = self.visit(node.obj, scope.children[0])
        
        valuesArgs = []
        for arg, child in zip(node.args, scope.children[1:]):
            valuesArgs.append(self.visit(arg, child))

        if node.typex is None:
            node.typex = node.obj.type.name

        self.register_instruction(cil.ArgsNode( list[reversed(valuesArgs)] + ['self']))

        self.register_instruction(cil.DynamicCallNode(node.typex, self.to_function_name(node.id, node.typex), result))
        return result

    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        
        valuesArgs = []
        for arg, child in zip(node.args, scope.children):
            valuesArgs.append(self.visit(arg, child))

        self.register_instruction(cil.ArgsNode( list[reversed(valuesArgs)] + ['self']))
        self.register_instruction(cil.StaticCallNode(self.to_function_name(node.id, self.current_type.name), result))
        return result

    @visitor.when(IntegerNode)
    def visit(self, node, scope):
        return int(node.token)


    @visitor.when(BoolNode)
    def visit(self, node, scope):
        if node.token:
            return 1
        return 0


    @visitor.when(StringNode)
    def visit(self, node, scope):
        return self.register_data(node.token).name


    @visitor.when(IdNode)
    def visit(self, node:IdNode, scope):
        vinfo = scope.find_variable(node.token)

        if vinfo is None:
            result = self.define_internal_local()
            self.register_instruction(cil.GetAttribNode('self', self.to_attribute_name(node.token, self.current_type.name), result))
            return result

        return vinfo.cilName


    @visitor.when(NewNode)
    def visit(self, node, scope):
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.type.name, instance))
        
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.DynamicCallNode(node.type, self.to_function_name('Ctr', node.type), result))
        return instance


    @visitor.when(PlusNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        self.register_instruction(cil.PlusNode(result, left, right))
        return result


    @visitor.when(MinusNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        self.register_instruction(cil.MinusNode(result, left, right))
        return result


    @visitor.when(StarNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        self.register_instruction(cil.StarNode(result, left, right))
        return result

    @visitor.when(DivNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        self.register_instruction(cil.DivNode(result, left, right))
        return result

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        self.register_instruction(cil.MinusNode(result, left, right))
        
        return result
        
    @visitor.when(LessNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        self.register_instruction(cil.LessNode(result, left, right))

        return result

    @visitor.when(LessEqualNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        self.register_instruction(cil.LessEqualNode(result, left, right))

        return result  

    @visitor.when(NotNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        value = self.visit(node.expression, scope.children[0])

        labelTrue = self.register_label()
        labelEnd = self.register_label()

        self.register_instruction(cil.GotoIfNode(labelTrue, value))
        self.register_instruction(cil.AssignNode(result, 1))
        self.register_instruction(cil.GotoNode(labelEnd))
        self.register_instruction(cil.LabelNode(labelTrue))
        self.register_instruction(cil.AssignNode(result, 0))
        self.register_instruction(cil.LabelNode(labelEnd))

        return result

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        expression = self.visit(node.expression, scope.children[0])

        self.register_instruction(cil.ComplementNode(expression, result))
        return result

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        expression = self.visit(node.expression, scope.children[0])

        self.register_instruction(cil.IsVoidNode(expression, result))
        return result