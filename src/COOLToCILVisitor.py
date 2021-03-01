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

        self.register_instruction(cil.JumpNode(self.to_function_name('Ctr', 'Main'), result))
        self.register_instruction(cil.ArgsNode([result]))

        realMethod = self.get_method(self.context.get_type('Main').name, 'main')
        self.register_instruction(cil.DynamicCallNode('Main', realMethod , result2, result))
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

        self.register_instruction(cil.LoadNode('self', f'{self.current_type.name}_name'))
        self.register_instruction(cil.LoadIntNode('self', f'{self.current_type.name}_size', 4))
        self.register_instruction(cil.LoadNode('self', f'__virtual_table__{self.current_type.name}', 8))

        initResult = self.define_internal_local()
        self.register_instruction(cil.ArgsNode(['self']))
        self.register_instruction(cil.JumpNode(self.to_function_name('Init', self.current_type.name), initResult))

        # nodeatt = [x for x in node.features if isinstance(x, AttrDeclarationNode)]
        # for feature, child_scope in zip(nodeatt, scope.children[1].children):
        #     self.visit(feature, child_scope)
        
        self.register_instruction(cil.ReturnNode('self'))


        #init
        name = self.to_function_name('Init', self.current_type.name)
        self.current_function = self.register_function(name)
        self.register_param(VariableInfo('self', self.current_type))

        parentResult = self.define_internal_local()
        self.register_instruction(cil.ArgsNode(['self']))
        self.register_instruction(cil.JumpNode(self.to_function_name('Init', self.current_type.parent.name), parentResult))

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

            if  node.type == 'Object' and node.expression.type.name in ['Int', 'Bool', 'String']:
               value = self.box(node.expression.type.name, value)
            
        else:
            if node.type == 'String':
                internal = self.define_internal_local()
                self.register_instruction(cil.LoadAddressNode(internal, "_empty"))
                value = internal
            elif node.type == 'Bool' or node.type == 'Int':
                value = 0
            else:
                internal = self.define_internal_local()
                self.register_instruction(cil.LoadAddressNode(internal, "_void"))
                value = internal

        attrib = self.get_attr(self.current_type.name, node.id)
        self.register_instruction(cil.SetAttribNode('self', attrib, value))

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        scopeOpen = scope.children[0]
        
        value = None
        for init in node.let_body:
            if not init[2] is None:
                value = self.visit(init[2], scopeOpen)

                if init[2].type.name in ['Int', 'Bool', 'String'] and init[1]== 'Object':
                    value = self.box(init[2].type.name, value)

            else:
                if init[1] == 'String':
                    internal = self.define_internal_local()
                    self.register_instruction(cil.LoadAddressNode(internal, "_empty"))
                    value = internal
                elif init[1] == 'Bool' or init[1] == 'Int':
                    value = 0
                else:
                    internal = self.define_internal_local()
                    self.register_instruction(cil.LoadAddressNode(internal, "_void"))
                    value = internal

            scopeOpen = scopeOpen.children[-1]
            vinfo = scopeOpen.find_variable(init[0])
            vname = self.register_local(vinfo)
            self.register_instruction(cil.AssignNode(vname, value))

        return self.visit(node.in_body, scopeOpen.children[0])

    @visitor.when(CaseOfNode)
    def visit(self, node, scope):
        result = self.define_internal_local()

        internal_expression = self.define_internal_local()
        value_expression =  self.visit(node.expression, scope.children[0])
        self.register_instruction(cil.AssignNode(internal_expression, value_expression))

        types_ordered = self.sort_types([self.context.get_type(x[1]) for x in node.branches])
        list_label = []
        labels = dict()

        for typex in types_ordered:
            labelTypex = self.register_label()
            labels[typex.name] = labelTypex
            pre = self.get_preordenTypes(typex)
            for typex2 in pre:
                if not typex2 in [x[0] for x in list_label]:
                    list_label.append((typex2, labelTypex))

        for typex in list_label:    
            self.register_instruction(cil.CaseOption(value_expression, typex[1], typex[0]))
        #error

        labelEnd = self.register_label()
        for branch, scopeBranch in zip(node.branches, scope.children[1].children):
            vinfo = scopeBranch.find_variable(branch[0])
            xxx = self.register_local(vinfo)
            self.register_instruction(cil.LabelNode(labels[branch[1]]))
            self.register_instruction(cil.AssignNode(xxx, value_expression))
           
            valueBranch = self.visit(branch[2], scopeBranch)
            self.register_instruction(cil.AssignNode(result, valueBranch))
            self.register_instruction(cil.GotoNode(labelEnd))

        self.register_instruction(cil.LabelNode(labelEnd))
        return result


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
        self.register_instruction(cil.LoadAddressNode(result, "_void"))
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
            attrib = self.get_attr(self.current_type.name, node.id)
            self.register_instruction(cil.SetAttribNode('self', attrib, value))
        else:
            self.register_instruction(cil.AssignNode(vinfo.cilName, value))
        
        return value

    @visitor.when(FunctionCallNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        obj = self.visit(node.obj, scope.children[0])
        
        if node.obj.type.name in ['Int', 'Bool', 'String']:
            if node.id in ['abort', 'type_name', 'copy']:
                obj = self.box(node.obj.type.name, obj)

        valuesArgs = []
        for arg, child in zip(node.args, scope.children[1:]):
            value = self.visit(arg, child)

            if arg.type.name in ['Int', 'Bool', 'String']:
                method = self.context.get_type(node.typex).get_method(node.id)
                param_type =  method.param_types[node.args.index(arg)]

                if param_type.name == 'Object':
                    valuesArgs.append(self.box(arg.type.name, value))
                    continue

            valuesArgs.append(value)
                                        
        if node.typexa is None:
            node.typex = node.obj.type.name

        self.register_instruction(cil.ArgsNode( list(reversed(valuesArgs)) + [obj]))
        
        if node.obj.type.name == 'String' and node.id in ['length', 'concat', 'substr']:
            self.register_instruction(cil.JumpNode(self.to_function_name(node.id, 'String'), result))
        else:
            realMethod = self.get_method(node.typex, node.id)
            self.register_instruction(cil.DynamicCallNode(node.typexa, realMethod, result, obj))
        return result

    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        
        valuesArgs = []
        for arg, child in zip(node.args, scope.children):
            value = self.visit(arg, child)

            if arg.type.name in ['Int', 'Bool', 'String']:
                method = self.current_type.get_method(node.id)
                param_type =  method.param_types[node.args.index(arg)]

                if param_type.name == 'Object':
                    valuesArgs.append(self.box(arg.type.name, value))
                    continue

            valuesArgs.append(value)

        self.register_instruction(cil.ArgsNode( list(reversed(valuesArgs)) + ['self']))

        realMethod = self.get_method(self.current_type.name, node.id)
        self.register_instruction(cil.StaticCallNode(realMethod, result))
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
        msg = self.register_data(node.token).name
        internal = self.define_internal_local()
        self.register_instruction(cil.LoadAddressNode(internal, msg))
        return internal


    @visitor.when(IdNode)
    def visit(self, node:IdNode, scope):
        if node.token == 'self':
            return 'self'

        vinfo = scope.find_variable(node.token)

        if vinfo is None:
            result = self.define_internal_local()
            attrib = self.get_attr(self.current_type.name, node.token)

            self.register_instruction(cil.GetAttribNode('self', attrib, result))
            return result

        return vinfo.cilName


    @visitor.when(NewNode)
    def visit(self, node:NewNode, scope):
        if not node.type.name == "Int":
            instance = self.define_internal_local()
            result = self.define_internal_local()
            self.register_instruction(cil.AllocateNode(node.type.name, instance))
            self.register_instruction(cil.ArgsNode([instance]))
            self.register_instruction(cil.JumpNode(self.to_function_name('Ctr', node.type.name), result))
            return instance
        else:
            return 0
        


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

        if node.left.type.name == 'String':
            self.register_instruction(cil.StringComparer(result, left, right))
        else:
            labelEquals = self.register_label()
            labelsEnd = self.register_label()

            resultComparer = self.define_internal_local()
            self.register_instruction(cil.MinusNode(resultComparer, left, right))

            self.register_instruction(cil.GotoIfNode(labelEquals, resultComparer))
            self.register_instruction(cil.AssignNode(result, 1))
            self.register_instruction(cil.GotoNode(labelsEnd))
            self.register_instruction(cil.LabelNode(labelEquals))
            self.register_instruction(cil.AssignNode(result, 0))
            self.register_instruction(cil.LabelNode(labelsEnd))

        return result
        
    @visitor.when(LessNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])

        labelTrue = self.register_label()
        labelEnd = self.register_label()

        self.register_instruction(cil.LessNode(result, left, right, labelTrue, labelEnd))
        return result

    @visitor.when(LessEqualNode)
    def visit(self, node, scope):
        result = self.define_internal_local()
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])

        labelTrue = self.register_label()
        labelEnd = self.register_label()

        self.register_instruction(cil.LessEqualNode(result, left, right, labelTrue,labelEnd))
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

        labelEnd = self.register_label()

        self.register_instruction(cil.IsVoidNode(expression, result, labelEnd))
        return result


    # utils
    def request_pos(self, name):
        if name in [x.name for x in self.current_function.localvars]:
            numb = int( name.split('_')[-1])
            return f'-{(numb+1) * 4}($fp)'
        elif name in [x.name for x in self.current_function.params]:
            numb = [param.name for param in self.function.params].index(name)
            return f'{(numb + 1) * 4}($fp)'
        else:
            return None
