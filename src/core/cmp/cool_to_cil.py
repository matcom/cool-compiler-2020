import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.CoolUtils as cool
from core.cmp.semantic import Attribute, Method, Type, VariableInfo

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


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cool.ProgramNode)
    def visit(self, node, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################
        
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(cil.ReturnNode(0))
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
                
        self.current_type = None

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        #//TODO: Implement AttrDeclarationNode, assess whether this needs to be done
        pass
                
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
        #//TODO: Return type SELF_TYPE 
        if self.current_method.return_type.name is self.current_type.name:
            self.register_param(VariableInfo('self', None))
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
        
        vname = self.register_local(VariableInfo(node.id, None))
        self.visit(node.expr, scope)
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
        
        for arg in args:
            self.register_instruction(arg)

        if node.type:
            #Call of type <expr>@<type>.id(<expr>,...,<expr>)
            at_type = [typex for typex in self.dottypes if typex.name == node.type][0]
            #method = [method for method in at_type.methods if method.name == node.id][0]
            self.register_instruction(cil.DynamicCallNode(at_type.name, self.to_function_name(node.id, at_type.name), result))
            scope.ret_expr = result
        else:
            #Call of type <expr>.<id>(<expr>,...,<expr>)
            #//TODO: Check if node,obj's type is void, and in that case throw runtime error
            _, vtype = [vinfo for vinfo in scope.locals if vinfo.name == node.obj.lex][0]
            self.register_instruction(cil.StaticCallNode(self.to_function_name(node.id, vtype), result))
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
        self.register_instruction(cil.AllocateNode(node.type, instance))
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
