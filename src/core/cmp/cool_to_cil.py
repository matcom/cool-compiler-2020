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
        
        # (Handle PARAMS)
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        for param_name, _ in node.params:
            self.register_param(VariableInfo(param_name, None))
        
        scope.ret_expr = None
        for instruction in node.body:
            self.visit(instruction, scope)
        # (Handle RETURN)
        #//TODO: Handle RETURN 0 and RETURN 
        if type(scope.ret_expr) is str:
            self.register_instruction(cil.ReturnNode(scope.ret_expr))
        else:
            self.register_instruction(cil.ReturnNode(scope.ret_expr.dest))
        
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
        self.register_instruction(cil.GotoIfNode(scope.ret_expr.dest, then_label_node.label))
        #GOTO else_label
        self.register_instruction(cil.GotoNode(else_label_node.label))
        #Label then_label
        self.register_instruction(then_label_node)
        self.visit(node.if_body, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr.dest))
        #Label else_label
        self.register_instruction(else_label_node)
        self.visit(node.else_body, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr.dest))

        scope.ret_expr = vret

    @visitor.when(cool.WhileLoopNode)
    def visit(self, node, scope):
        ###################################
        # node.condition -> ExpressionNode
        # node.body -> ExpressionNode
        ###################################
        vret = self.register_local(VariableInfo('while_value', None))

        while_label_node = self.register_label('while_label')
        loop_label_node = self.register_label('loop_label')
        pool_label_node = self.register_label('pool_label')
        #Label while
        self.register_instruction(while_label_node)
        #If condition GOTO loop
        self.visit(node.condition, scope)
        self.register_instruction(cil.GotoIfNode(scope.ret_expr.dest, loop_label_node.label))
        #GOTO pool
        self.register_instruction(cil.GotoNode(pool_label_node.label))
        #Label loop
        self.register_instruction(loop_label_node)
        self.visit(node.body, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr.dest))
        #GOTO while
        self.register_instruction(cil.GotoNode(while_label_node.label))
        #Label pool
        self.register_instruction(pool_label_node)

        scope.ret_expr = vret


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
         #//TODO: Implement LetInNode
        pass

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
        
        vname = self.register_local(VariableInfo(node.id, node.type))
        expr = self.visit(node.expr, scope)
        return self.register_instruction(cil.AssignNode(vname, expr))

    @visitor.when(cool.AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        
        vname = self.register_local(VariableInfo(node.id, None))
        expr = self.visit(node.expr, scope)
        if issubclass(type(expr), cil.InstructionNode):
            return self.register_instruction(cil.AssignNode(vname, expr.dest))
        return self.register_instruction(cil.AssignNode(vname, node.expr))

    @visitor.when(cool.NotNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        #//TODO: Implement NotNode
        pass

    @visitor.when(cool.LessEqualNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        #//TODO: Implement LessEqualNode
        pass

    @visitor.when(cool.LessNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        #//TODO: Implement LessNode
        pass

    @visitor.when(cool.EqualNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        #//TODO: Implement EqualNode
        pass

    @visitor.when(cool.PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        plus = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        return self.register_instruction(cil.PlusNode(plus, left, right))

    @visitor.when(cool.MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        minus = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        return self.register_instruction(cil.MinusNode(minus, left, right))

    @visitor.when(cool.StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        star = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        return self.register_instruction(cil.StarNode(star, left, right))

    @visitor.when(cool.DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        div = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        return self.register_instruction(cil.DivNode(div, left, right))

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
        #//TODO: Implement ComplementNode
        pass

    @visitor.when(cool.FunctionCallNode)
    def visit(self, node, scope):
        ######################################
        # node.obj -> AtomicNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        # node.type -> str
        #####################################
        
        for arg in node.args:
            vname = self.define_internal_local()
            value = self.visit(arg, scope)
            self.register_instruction(cil.AssignNode(vname, value))
            self.register_instruction(cil.ArgNode(vname))
        result = self.define_internal_local()
        
        obj = self.visit(node.obj, scope)
        if type(obj) is cil.AllocateNode:
            return self.register_instruction(cil.StaticCallNode(self.to_function_name(node.id, obj.type), result))
        elif type(obj) is str:
            for n in [lv.name for lv in self.current_function.localvars]:
                if obj in n.split("_"):
                    return n
        return None

    @visitor.when(cool.MemberCallNode)
    def visit(self, node, scope):
        ######################################
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        ######################################
        #//TODO: Implement MemberCallNode
        pass

    @visitor.when(cool.NewNode)
    def visit(self, node, scope):
        ###############################
        # node.type -> str
        ###############################
        
        instance = self.define_internal_local()
        return self.register_instruction(cil.AllocateNode(node.type, instance))

    @visitor.when(cool.IntegerNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        return node.lex

    @visitor.when(cool.IdNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        param_names = [pn.name for pn in self.current_function.params]
        if node.lex in param_names:
            for n in param_names:
                if node.lex in n.split("_"):
                    return n
        for n in [lv.name for lv in self.current_function.localvars]:
            if node.lex in n.split("_"):
                return n

    @visitor.when(cool.StringNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        return node.lex

    @visitor.when(cool.StringNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        return node.lex
