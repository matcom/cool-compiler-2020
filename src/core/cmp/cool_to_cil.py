import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.CoolUtils as cool
from core.cmp.semantic import Attribute, Method, Type, VariableInfo, SemanticError
from core.cmp.functions import get_token

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

    def register_built_in(self):
        #Object
        type_node = self.register_type('Object')

        self.current_function = self.register_function(self.to_function_name('init', 'Object'))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Object', instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('abort', 'Object'))
        vname = self.define_internal_local()
        data_node = [dn for dn in self.dotdata if dn.value == 'Program aborted'][0]
        self.register_instruction(cil.LoadNode(vname, data_node))
        self.register_instruction(cil.PrintStrNode(vname))
        self.register_instruction(cil.ExitNode())
        # No need for RETURN here right??

        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.TypeNameNode(result, self.vself.name))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('copy', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.CopyNode(result, self.vself.name))
        self.register_instruction(cil.ReturnNode(result))

        type_node.methods = [(name, self.to_function_name(name, 'Object')) for name in ['init', 'abort', 'type_name', 'copy']]
        obj_methods = ['abort', 'type_name', 'copy']

        #IO
        type_node = self.register_type('IO')

        self.current_function = self.register_function(self.to_function_name('init', 'IO'))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Object', instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(vname, 'x', 'value', 'String'))
        self.register_instruction(cil.PrintStrNode(vname))
        self.register_instruction(cil.ReturnNode(self.vself.name))

        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(vname, 'x', 'value', 'Int'))
        self.register_instruction(cil.PrintIntNode(vname))
        self.register_instruction(cil.ReturnNode(self.vself.name)) 

        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadStrNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadIntNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'Int'), instance))
        self.register_instruction(cil.ReturnNode(instance))  

        type_node.methods = [(name, self.to_function_name(name, 'IO')) for name in ['init', 'out_string', 'out_int', 'in_string', 'in_int']]
        type_node.methods += [(method, self.to_function_name(method, 'Object')) for method in obj_methods]

        #String
        type_node = self.register_type('String')
        type_node.attributes = ['value', 'length']

        self.current_function = self.register_function(self.to_function_name('init', 'String'))
        self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('String', instance))
        self.register_instruction(cil.SetAttribNode(instance, 'value', 'val', 'String'))
        result = self.define_internal_local()
        self.register_instruction(cil.LengthNode(result, 'val'))
        attr = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'Int'), attr))
        self.register_instruction(cil.SetAttribNode(instance, 'length', attr, 'String'))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('length', 'String'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(result, self.vself.name, 'length', 'String'))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function(self.to_function_name('concat', 'String'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('s', None))
        str_1 = self.define_internal_local()
        str_2 = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(str_1, self.vself.name, 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(str_2, 's', 'value', 'String'))
        result = self.define_internal_local()
        self.register_instruction(cil.ConcatNode(result, str_1, str_2))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('substr', 'String'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        result = self.define_internal_local()
        index_value = self.define_internal_local()
        length_value = self.define_internal_local()
        length_attr = self.define_internal_local()
        length_substr = self.define_internal_local()
        less_value = self.define_internal_local()
        str_value = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(str_value, self.vself.name, 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(index_value, 'i', 'value', 'Int'))
        self.register_instruction(cil.GetAttribNode(length_value, 'l', 'value', 'Int'))
        #Check Out of range error
        self.register_instruction(cil.GetAttribNode(length_attr, self.vself.name, 'length', 'String'))
        self.register_instruction(cil.PlusNode(length_substr, length_value, index_value))
        self.register_instruction(cil.LessNode(less_value, length_attr, length_substr))
        self.register_runtime_error(less_value, 'Substring out of range')
        self.register_instruction(cil.SubstringNode(result, str_value, index_value, length_value))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = [(name, self.to_function_name(name, 'String')) for name in ['init', 'length', 'concat', 'substr']]
        type_node.methods += [(method, self.to_function_name(method, 'Object')) for method in obj_methods]

        #Int
        type_node = self.register_type('Int')
        type_node.attributes = ['value']

        self.current_function = self.register_function(self.to_function_name('init', 'Int'))
        self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Int', instance))
        self.register_instruction(cil.SetAttribNode(instance, 'value', 'val', 'Int'))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = [('init', self.to_function_name('init', 'Int'))]
        type_node.methods += [(method, self.to_function_name(method, 'Object')) for method in obj_methods]

    def register_runtime_error(self, condition, msg):
        error_node = self.register_label('error_label')
        continue_node = self.register_label('continue_label')
        self.register_instruction(cil.GotoIfNode(condition, error_node.label))
        self.register_instruction(cil.GotoNode(continue_node.label))
        self.register_instruction(error_node)
        data_node = self.register_data(msg)
        self.register_instruction(cil.ErrorNode(data_node))
        
        self.register_instruction(continue_node)


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    def __init__(self, context):
       super().__init__(context)

    def buildHierarchy(self, t:str):
        if t == 'Object': return None
        return {x.name for x in self.context.types.values() if x.conforms_to(self.context.get_type(t))}
            
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
        instance = self.register_local(VariableInfo('instance', None))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'Main'), instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(cil.ReturnNode(0))
        # Error message raised by Object:abort()
        self.register_data('Program aborted')
        self.register_built_in()
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
            self.register_instruction(cil.SetAttribNode(instance, node.id, scope.ret_expr, self.current_type))
        scope.ret_expr = instance
                
    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node, scope):
        #####################################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> ExpressionNode
        #####################################
        
        self.current_method = self.current_type.get_method(node.id)
        type_name = self.current_type.name
        
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, type_name))
        
        # (Handle PARAMS)
        self.register_param(self.vself)
        for param_name, _ in node.params:
            self.register_param(VariableInfo(param_name, None))
        
        scope.ret_expr = None
        #//TODO: scope children used here ???
        self.visit(node.body, scope)
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
        scope.ret_expr = cil.VoidNode()

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

        for let_attr_node in node.let_body:
            self.visit(let_attr_node, scope)
        self.visit(node.in_body, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr))
        scope.ret_expr = vret
        
    @visitor.when(cool.CaseOfNode)
    def visit(self, node, scope):
        ##############################################
        # node.expr -> ExpressionNode
        # node.branches -> [ CaseExpressionNode ... }
        ##############################################
        vexpr = self.register_local(VariableInfo('case_expr_value', None))
        vtype = self.register_local(VariableInfo('typeName_value', None))
        vcond = self.register_local(VariableInfo('equal_value', None))
        vret = self.register_local(VariableInfo('case_value', None))
        self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(vexpr, scope.ret_expr))
        self.register_instruction(cil.TypeNameNode(vtype, scope.ret_expr))

        #Check if node.expr is void and raise proper error if vexpr value is void
        void = cil.VoidNode()
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, vexpr, void))

        token = get_token(node.expr)
        self.register_runtime_error(equal_result,  f'({token.row},{token.column}) - RuntimeError: Case on void\n')

        end_label = self.register_label('end_label')
        labels = []
        old = {}
        for idx, b in enumerate(node.branches):
            labels.append(self.register_label(f'{idx}_label'))
            h = self.buildHierarchy(b.type)
            if not h:
                self.register_instruction(cil.GotoNode(labels[-1].label))
                break
            h.add(b.type)
            for s in old:
                h -= s
            for t in h:
                vbranch_type_name = self.register_local(VariableInfo('branch_type_name', None))
                self.register_instruction(cil.NameNode(vbranch_type_name, t))
                self.register_instruction(cil.EqualNode(vcond, vtype, vbranch_type_name))
                self.register_instruction(cil.GotoIfNode(vcond, labels[-1].label))

        for idx, l in enumerate(labels):
            self.register_instruction(l)
            vid = self.register_local(VariableInfo(node.branches[idx].id, None))
            self.register_instruction(cil.AssignNode(vid, vexpr))
            self.visit(node.branches[idx], scope)
            self.register_instruction(cil.AssignNode(vret, scope.ret_expr))
            self.register_instruction(cil.GotoNode(end_label.label))

        #Raise runtime error if no Goto was executed
        data_node = self.register_data(f'({token.row + 5},{token.column + 1 + len(node.branches)}) - RuntimeError: Execution of a case statement without a matching branch\n')
        self.register_instruction(cil.ErrorNode(data_node))

        self.register_instruction(end_label)

    @visitor.when(cool.CaseExpressionNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        self.visit(node.expr, scope)

    @visitor.when(cool.LetAttributeNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        vname = self.register_local(VariableInfo(node.id, node.type))
        if node.expr:
            self.visit(node.expr, scope)
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))
        
    @visitor.when(cool.AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        
        self.visit(node.expr, scope)

        try:
            self.current_type.get_attribute(node.id)
            self.register_instruction(cil.SetAttribNode(self.vself, node.id, scope.ret_expr, self.current_type.name))
        except SemanticError:
            vname = None
            param_names = [pn.name for pn in self.current_function.params]
            if node.id in param_names:
                for n in param_names:
                    if node.id in n.split("_"):
                        vname = n
                        break
            else:
                for n in [lv.name for lv in self.current_function.localvars]:
                    if node.id in n.split("_"):
                        vname = n
                        break
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))

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
        type_left = self.define_internal_local()
        type_int = self.define_internal_local()
        type_string = self.define_internal_local()
        equal_result = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()

        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr

        self.register_instruction(cil.TypeNameNode(type_left, left))
        self.register_instruction(cil.NameNode(type_int, 'Int'))
        self.register_instruction(cil.NameNode(type_string, 'String'))

        int_node = self.register_label('int_label')
        string_node = self.register_label('string_label')
        reference_node = self.register_label('reference_label')
        continue_node = self.register_label('continue_label')
        self.register_instruction(cil.EqualNode(equal_result, type_left, type_int))
        self.register_instruction(cil.GotoIfNode(equal_result, int_node.label))
        self.register_instruction(cil.EqualNode(equal_result, type_left, type_string))
        self.register_instruction(cil.GotoIfNode(equal_result, string_node.label))
        self.register_instruction(cil.GotoNode(reference_node.label))

        self.register_instruction(int_node)
        self.register_instruction(cil.GetAttribNode(left_value, left, 'value', 'Int'))
        self.register_instruction(cil.GetAttribNode(right_value, right, 'value', 'Int'))
        self.register_instruction(cil.EqualNode(vname, left_value, right_value))
        self.register_instruction(cil.GotoNode(continue_node.label))

        self.register_instruction(string_node)
        self.register_instruction(cil.GetAttribNode(left_value, left, 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(right_value, right, 'value', 'String'))
        self.register_instruction(cil.EqualNode(vname, left_value, right_value))
        self.register_instruction(cil.GotoNode(continue_node.label))

        self.register_instruction(reference_node)
        self.register_instruction(cil.EqualNode(vname, left, right))

        self.register_instruction(continue_node)
        scope.ret_expr = vname

    @visitor.when(cool.PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(vleft, scope.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(vright, scope.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.PlusNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'Int'), instance))
        scope.ret_expr = instance

    @visitor.when(cool.MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(vleft, scope.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(vright, scope.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.MinusNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'Int'), instance))
        scope.ret_expr = instance

    @visitor.when(cool.StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(vleft, scope.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(vright, scope.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.StarNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'Int'), instance))
        scope.ret_expr = instance

    @visitor.when(cool.DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(vleft, scope.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(vright, scope.ret_expr, 'value', 'Int'))

        #Check division by 0
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, vright, 0))
        token = get_token(node.right)
        self.register_runtime_error(equal_result, f'({token.row},{token.column}) - RuntimeError: Division by zero\n')

        self.register_instruction(cil.DivNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'Int'), instance))
        scope.ret_expr = instance

    @visitor.when(cool.IsVoidNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        void = cil.VoidNode()
        value = self.define_internal_local()
        self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(value, scope.ret_expr))
        result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(result, value, void))
        scope.ret_expr = result

    @visitor.when(cool.ComplementNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        value = self.define_internal_local()
        self.visit(node.expr, scope)
        self.register_instruction(cil.GetAttribNode(value, scope.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.ComplementNode(vname, value))
        scope.ret_expr = vname

    @visitor.when(cool.FunctionCallNode)
    def visit(self, node, scope):
        ######################################
        # node.obj -> ExpressionNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        # node.type -> str
        #####################################

        args = []
        for arg in node.args:
            vname = self.register_local(VariableInfo(f'{node.id}_arg', None))
            self.visit(arg, scope)
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))
            args.append(cil.ArgNode(vname))
        result = self.register_local(VariableInfo(f'return_value_of_{node.id}', None))
        
        vobj = self.define_internal_local()
        self.visit(node.obj, scope)
        self.register_instruction(cil.AssignNode(vobj, scope.ret_expr))

        #Check if node.obj is void
        void = cil.VoidNode()
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, vobj, void))

        token = get_token(node.obj)
        self.register_runtime_error(equal_result, f'({token.row},{token.column}) - RuntimeError: Dispatch on void\n')
        
        #self
        self.register_instruction(cil.ArgNode(vobj))
        for arg in args:
            self.register_instruction(arg)

        if node.type:
            #Call of type <obj>@<type>.id(<expr>,...,<expr>)
            self.register_instruction(cil.StaticCallNode(self.to_function_name(node.id, node.type), result))
        else:
            #Call of type <obj>.<id>(<expr>,...,<expr>)
            type_of_node = self.register_local(VariableInfo(f'{node.id}_type', None))
            self.register_instruction(cil.TypeOfNode(vobj, type_of_node))
            computed_type = node.obj.computed_type
            if computed_type.name == 'SELF_TYPE':
                computed_type = computed_type.fixed
            self.register_instruction(cil.DynamicCallNode(type_of_node, node.id, result, computed_type.name))

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
            vname = self.register_local(VariableInfo(f'{node.id}_arg', None))
            self.visit(arg, scope)
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))
            args.append(cil.ArgNode(vname))
        result = self.register_local(VariableInfo(f'return_value_of_{node.id}', None))

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
        
        if node.type == 'SELF_TYPE':
            vtype = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(self.vself, vtype))
            self.register_instruction(cil.AllocateNode(vtype, instance))
        elif node.type == 'Int' or node.type == 'Bool':
            self.register_instruction(cil.ArgNode(0))
        elif node.type == 'String':
            data_node = [dn for dn in self.dotdata if dn.value == ''][0]
            vmsg = self.register_local(VariableInfo('msg', None))
            self.register_instruction(cil.LoadNode(vmsg, data_node))
            self.register_instruction(cil.ArgNode(vmsg))

        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', node.type), instance))
        scope.ret_expr = instance

    @visitor.when(cool.IntegerNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(int(node.lex)))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'Int'), instance))
        scope.ret_expr = instance

    @visitor.when(cool.IdNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        try:
            self.current_type.get_attribute(node.lex)
            attr = self.register_local(VariableInfo(node.lex, None))
            self.register_instruction(cil.GetAttribNode(attr, self.vself.name, node.lex, self.current_type.name))
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
        try:
            data_node = [dn for dn in self.dotdata if dn.value == node.lex][0]
        except IndexError:
            data_node = self.register_data(node.lex)
        vmsg = self.register_local(VariableInfo('msg', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.LoadNode(vmsg, data_node))
        self.register_instruction(cil.ArgNode(vmsg))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'String'), instance))
        scope.ret_expr = instance

    @visitor.when(cool.BoolNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        if node.lex is 'true':
            scope.ret_expr = 1
        else:
            scope.ret_expr = 0
        instance = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode(self.to_function_name('init', 'Int'), instance))
        self.register_instruction(cil.SetAttribNode(instance, 'value', scope.ret_expr, 'Int'))
        scope.ret_expr = instance
