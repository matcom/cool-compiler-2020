import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.CoolUtils as cool
from core.cmp.semantic import Attribute, Method, Type, VariableInfo, SemanticError

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        self.vself = VariableInfo('self', None)
        self.default_values = {'Int': 0, 'String': '', 'Bool': False}
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_param(self, vinfo):
        #'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        vinfo.name = vinfo.name
        param_node = cil.ParamNode(vinfo.name)
        self.params.append(param_node)
        return vinfo.name
    
    def register_local(self, vinfo):
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
        ###############################
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def register_label(self, label):
        lname = f'{label}_{self.current_function.labels_count}'
        self.current_function.labels_count += 1
        return cil.LabelNode(lname)

    def register_built_in(self):
        #Object
        type_node = self.register_type('Object')

        self.current_function = self.register_function(self.to_function_name('abort', 'Object'))
        vname = self.define_internal_local()
        self.register_instruction(cil.LoadNode(vname, 'data_0'))
        self.register_instruction(cil.PrintNode(vname))
        self.register_instruction(cil.ExitNode())
        # No need for RETURN here right??

        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.TypeNameNode(result, self.vself.name))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function(self.to_function_name('copy', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.CopyNode(result, self.vself.name))
        self.register_instruction(cil.ReturnNode(result))

        type_node.methods = [(name, self.to_function_name(name, 'Object')) for name in ['abort', 'type_name', 'copy']]

        #IO
        type_node = self.register_type('IO')

        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(cil.LoadNode(vname, 'x'))
        self.register_instruction(cil.PrintNode(vname))
        self.register_instruction(cil.ReturnNode(self.vself.name))

        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('x', None))
        self.register_instruction(cil.PrintNode('x'))
        self.register_instruction(cil.ReturnNode(self.vself.name)) 

        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadNode(result))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadNode(result))
        self.register_instruction(cil.ReturnNode(result))  

        #String
        type_node = self.register_type('String')

        self.current_function = self.register_function(self.to_function_name('length', 'String'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.LengthNode(result, self.vself.name))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function(self.to_function_name('concat', 'String'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('s', None))
        result = self.define_internal_local()
        self.register_instruction(cil.ConcatNode(result, self.vself.name, 's'))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function(self.to_function_name('substr', 'String'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        result = self.define_internal_local()
        self.register_instruction(cil.SubstringNode(result, self.vself.name, 'i', 'l'))
        self.register_instruction(cil.ReturnNode(result))

        #Int
        type_node = self.register_type('Int')
        #Bool
        type_node = self.register_type('Bool')


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    def __init__(self, context):
       super().__init__(context)

    def buildHierarchy(self, t:str):
        h = []
        if t == 'Object': return None
        h.extend([x for x in self.context.types if x.conforms_to(t)])
        return h
            
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cool.ProgramNode)
    def visit(self, node, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################
        
        self.current_function = self.register_function('entry')
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Main', self.vself.name))
        self.register_instruction(cil.ArgNode(self.vself.name))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(cil.ReturnNode(0))
        self.register_built_in()
        # Error message raised by Object:abort()
        self.register_data('Program aborted')
        self.current_function = None
        
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        
        self.current_type = self.context.get_type(node.id)
        
        # (Handle all the .TYPE section)
        type_node = self.register_type(node.id)
        type_node.attributes = [attr.name for attr, _ in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]

        func_declarations = (f for f in node.features if isinstance(f, cool.FuncDeclarationNode))
        for feature, child_scope in zip(func_declarations, scope.children):
            self.visit(feature, child_scope)

        #init
        self.current_function = self.register_function(self.to_function_name('init', node.id))
        #allocate
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.id, instance))
        scope.ret_expr = instance

        attr_declarations = (f for f in node.features if isinstance(f, cool.AttrDeclarationNode))
        for feature in attr_declarations:
            self.visit(feature, scope)
        self.register_instruction(cil.ReturnNode(instance))
        self.current_function = None
                
        self.current_type = None

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        instance = scope.ret_expr
        if node.expr:
            self.visit(node.expr, scope)
        else:
            try:
                scope.ret_expr = self.default_values[node.type]
            except KeyError:
                scope.ret_expr = None
        self.register_instruction(cil.SetAttribNode(instance, node.id, scope.ret_expr))
                
    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node, scope):
        #####################################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        #####################################
        
        self.current_method = self.current_type.get_method(node.id)
        type_name = self.current_type.name
        
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        
        # (Handle PARAMS)
        self.register_param(self.vself)
        for param_name, _ in node.params:
            self.register_param(VariableInfo(param_name, None))
        
        scope.ret_expr = None
        for instruction in node.body:
            self.visit(instruction, scope)
        # (Handle RETURN)
        if scope.ret_expr is None:
            self.register_instruction(cil.ReturnNode(''))
        elif self.current_function.name is 'entry':
            self.register_instruction(cil.ReturnNode(0))
        else:
            self.register_instruction(cil.ReturnNode(scope.ret_expr))
        
        self.current_method = None

    @visitor.when(cool.IfThenElseNode)
    def visit(self, node, scope):
        ###################################
        # node.condition -> ExpressionNode
        # node.if_body -> ExpressionNode
        # node.else_body -> ExpressionNode
        ##################################
        vret = self.register_local(VariableInfo('if_then_else_value', None))

        then_label_node = self.register_label('then_label')
        else_label_node = self.register_label('else_label')

        #If condition GOTO then_label
        self.visit(node.condition, scope)
        self.register_instruction(cil.GotoIfNode(scope.ret_expr, then_label_node.label))
        #GOTO else_label
        self.register_instruction(cil.GotoNode(else_label_node.label))
        #Label then_label
        self.register_instruction(then_label_node)
        self.visit(node.if_body, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr))
        #Label else_label
        self.register_instruction(else_label_node)
        self.visit(node.else_body, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr))

        scope.ret_expr = vret

    @visitor.when(cool.WhileLoopNode)
    def visit(self, node, scope):
        ###################################
        # node.condition -> ExpressionNode
        # node.body -> ExpressionNode
        ###################################

        while_label_node = self.register_label('while_label')
        loop_label_node = self.register_label('loop_label')
        pool_label_node = self.register_label('pool_label')
        #Label while
        self.register_instruction(while_label_node)
        #If condition GOTO loop
        self.visit(node.condition, scope)
        self.register_instruction(cil.GotoIfNode(scope.ret_expr, loop_label_node.label))
        #GOTO pool
        self.register_instruction(cil.GotoNode(pool_label_node.label))
        #Label loop
        self.register_instruction(loop_label_node)
        self.visit(node.body, scope)
        #GOTO while
        self.register_instruction(cil.GotoNode(while_label_node.label))
        #Label pool
        self.register_instruction(pool_label_node)

        #The result of a while loop is void
        scope.ret_expr = None

    @visitor.when(cool.BlockNode)
    def visit(self, node, scope):
        #######################################
        # node.exprs -> [ ExpressionNode ... ]
        #######################################
        for expr in node.exprs:
            self.visit(expr, scope)

    @visitor.when(cool.LetInNode)
    def visit(self, node, scope):
        ############################################
        # node.let_body -> [ LetAttributeNode ... ]
        # node.in_body -> ExpressionNode
        ############################################
        vret = self.register_local(VariableInfo('let_in_value', None))

        for let_att_node in node.let_body:
            self.visit(let_att_node, scope)
        self.visit(node.in_body, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr))
        scope.ret_expr = vret
        
    @visitor.when(cool.CaseOfNode)
    def visit(self, node, scope):
        ##############################################
        # node.expr -> ExpressionNode
        # node.branches -> [ CaseExpressionNode ... }
        ##############################################
         #//TODO: Implement CaseOfNode
        pass

    @visitor.when(cool.CaseExpressionNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        #//TODO: Implement CaseExpressionNode
        pass

    @visitor.when(cool.LetAttributeNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        #//TODO: See if node.type is string prior to add it to .DATA ???
        vname = self.register_local(VariableInfo(node.id, node.type))
        self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(vname, scope.ret_expr))
        scope.ret_expr = None

    @visitor.when(cool.AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        
        self.visit(node.expr, scope)

        try:
            self.current_type.attributes.get_attribute(node.id)
            self.register_instruction(cil.SetAttribNode(self.vself, node.id, scope.ret_expr))
            scope.ret_expr = node.id
        except SemanticError:
            vname = self.register_local(VariableInfo(node.id, None))
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))
            scope.ret_expr = vname

    @visitor.when(cool.NotNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        self.visit(node.expr, scope)
        self.register_instruction(cil.MinusNode(vname, 1, scope.ret_expr))
        scope.ret_expr = vname

    @visitor.when(cool.LessEqualNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr
        self.register_instruction(cil.LessEqualNode(vname, left, right))
        scope.ret_expr = vname

    @visitor.when(cool.LessNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr
        self.register_instruction(cil.LessNode(vname, left, right))
        scope.ret_expr = vname

    @visitor.when(cool.EqualNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr
        self.register_instruction(cil.EqualNode(vname, left, right))
        scope.ret_expr = vname

    @visitor.when(cool.PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr
        self.register_instruction(cil.PlusNode(vname, left, right))
        scope.ret_expr = vname

    @visitor.when(cool.MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr
        self.register_instruction(cil.MinusNode(vname, left, right))
        scope.ret_expr = vname

    @visitor.when(cool.StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr
        self.register_instruction(cil.StarNode(vname, left, right))
        scope.ret_expr = vname

    @visitor.when(cool.DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr
        self.register_instruction(cil.DivNode(vname, left, right))
        scope.ret_expr = vname

    @visitor.when(cool.IsVoidNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        #//TODO: Implement IsVoidNode
        pass

    @visitor.when(cool.ComplementNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        self.visit(node.expr, scope)
        self.register_instruction(cil.ComplementNode(vname, scope.ret_expr))
        scope.ret_expr = vname

    @visitor.when(cool.FunctionCallNode)
    def visit(self, node, scope):
        ######################################
        # node.obj -> AtomicNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        # node.type -> str
        #####################################

        args = []
        for arg in node.args:
            vname = self.register_local(VariableInfo(f'{node.id}_arg'))
            self.visit(arg, scope)
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))
            args.append(cil.ArgNode(vname))
        result = self.register_local(VariableInfo(f'return_value_of_{node.id}'))
        
        if node.type:
            #Call of type <expr>@<type>.id(<expr>,...,<expr>)
            #Is ok to search node.type in dottypes???
            at_type = [typex for typex in self.dottypes if typex.name == node.type][0]
            instance = self.define_internal_local()
            self.register_instruction(cil.StaticCallNode(self.to_function_name('init', at_type.name), instance))
            #self for Static Dispatch
            self.register_instruction(cil.ArgNode(instance))
            for arg in args:
                self.register_instruction(arg)
                
            #method = [method for method in at_type.methods if method.name == node.id][0]
            #Shall we look method node.id in at_type parents???
            self.register_instruction(cil.StaticCallNode(self.to_function_name(node.id, at_type.name), result))
            scope.ret_expr = result
        else:
            #Call of type <expr>.<id>(<expr>,...,<expr>)
            type_of_node = self.register_local(VariableInfo(f'{node.id}_type'))
            self.register_instruction(cil.TypeOfNode(node.obj.lex, type_of_node))
            instance = self.define_internal_local()
            self.register_instruction(cil.DynamicCallNode(type_of_node, 'init', instance))
            #self for Dynamic Dispatch
            self.register_instruction(cil.ArgNode(instance))
            for arg in args:
                self.register_instruction(arg)

            self.register_instruction(cil.DynamicCallNode(type_of_node, node.id, result))
            scope.ret_expr = result

    @visitor.when(cool.MemberCallNode)
    def visit(self, node, scope):
        ######################################
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        ######################################
        method = [self.to_function_name(method.name, xtype.name) for method, xtype in self.current_type.all_methods() if method.name == node.id][0]
        
        args = []
        for arg in node.args:
            vname = self.register_local(VariableInfo(f'{node.id}_arg'))
            self.visit(arg, scope)
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))
            args.append(cil.ArgNode(vname))
        result = self.register_local(VariableInfo(f'return_value_of_{node.id}'))

        self.register_instruction(cil.ArgNode(self.vself.name))
        for arg in args:
            self.register_instruction(arg)
        
        self.register_instruction(cil.StaticCallNode(method, result))
        scope.ret_expr = result

    @visitor.when(cool.NewNode)
    def visit(self, node, scope):
        ###############################
        # node.type -> str
        ###############################
        instance = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', node.type), instance))
        scope.ret_expr = instance

    @visitor.when(cool.IntegerNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        scope.ret_expr = node.lex

    @visitor.when(cool.IdNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        try:
            self.current_type.attributes.get_attribute(node.lex)
            attr = self.register_local(VariableInfo('attr_value', None))
            self.register_instruction(cil.GetAttribNode(attr, self.vself, node.lex))
            scope.ret_expr = attr
        except SemanticError:
            param_names = [pn.name for pn in self.current_function.params]
            if node.lex in param_names:
                for n in param_names:
                    if node.lex in n.split("_"):
                        scope.ret_expr = n
                        break
            else:
                for n in [lv.name for lv in self.current_function.localvars]:
                    if node.lex in n.split("_"):
                        scope.ret_expr = n
                        break

    @visitor.when(cool.StringNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        data_node = self.register_data(node.lex)
        vname = self.register_local(VariableInfo('msg', None))
        self.register_instruction(cil.LoadNode(vname, data_node.name))
        scope.ret_expr = vname

    @visitor.when(cool.BoolNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        if node.lex is 'true':
            scope.ret_expr = 1
        else:
            scope.ret_expr = 0
