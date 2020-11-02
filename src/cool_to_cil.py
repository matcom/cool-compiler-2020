from semantic import Scope, VariableInfo
import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = {}
        self.dotdata = {}
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
        param_node = CIL_AST.ParamDec(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def is_defined_param(self, name):
        for p in self.params:
            if p.name == name:
                return True
        return False
    
    def register_local(self, var_name):
        local_node = CIL_AST.LocalDec(var_name)
        self.localvars.append(local_node)
        return var_name

    def define_internal_local(self, scope, name = "internal", cool_var_name = None, class_type = None):
        if class_type != None:
            cilname = f'{class_type}.{name}'
            scope.define_cil_local(cool_var_name, cilname, None)
            self.register_local(cilname)
        else :
            cilname = f'{name}_{len(self.localvars)}'
            scope.define_cil_local(cool_var_name, cilname, None)
            self.register_local(cilname)
        return cilname

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'{type_name}.{method_name}'

    def register_function(self, function_name):
        function_node = CIL_AST.Function(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = CIL_AST.Type(name)
        self.dottypes[name] = type_node
        return type_node

    def is_in_data(self, name):
        return name in self.dotdata.keys

    def register_data(self, value):
        vname = f's_{len(self.dotdata)}'
        self.dotdata[vname] = value
        return vname
    
    def register_builtin_types(self, scope):
        for t in ['Object', 'Int', 'String', 'Bool', 'IO']:
            builtin_type = self.context.get_type(t)
            cil_type = self.register_type(t)
            cil_type.attributes = {f'{attr.name}':attr for attr in builtin_type.attributes}
            cil_type.methods = {f'{m}':f'{c}.{m}' for c, m  in builtin_type.get_all_methods()}
            if t in ['Object','IO']:
                cil_type.methods['init'] = f'{t}.init'

        #----------------Object---------------------
        #init
        self.current_function = self.register_function(self.to_function_name('init', 'Object'))
        self.register_param(VariableInfo('instance', None))
        self.register_instruction(CIL_AST.Return(0))

        #abort
        self.current_function = self.register_function(self.to_function_name('abort', 'Object'))
        self.register_param(VariableInfo('self',None))
        msg = self.define_internal_local(scope=scope, name="msg")
        key_msg = ''
        for s in self.dotdata.keys():
            if self.dotdata[s] == 'Execution aborted':
                key_msg = s
        self.register_instruction(CIL_AST.Load(key_msg, msg))
        self.register_instruction(CIL_AST.PrintString(msg))
        self.register_instruction(CIL_AST.Halt())

        #type_name
        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'))
        self.register_param(VariableInfo('self', None))
        type_name = self.define_internal_local(scope=scope, name = "type_name" )
        self.register_instruction(CIL_AST.TypeOf('self', type_name))
        self.register_instruction(CIL_AST.Return(type_name))

        #copy
        self.current_function = self.register_function(self.to_function_name('copy', 'Object'))
        self.register_param(VariableInfo('self',None))
        copy = self.define_internal_local(scope=scope, name= "copy")
        self.register_instruction(CIL_AST.Copy('self', copy))
        self.register_instruction(CIL_AST.Return(copy))

        #----------------IO---------------------
        #init
        self.current_function = self.register_function(self.to_function_name('init', 'IO'))
        self.register_param(VariableInfo('instance', None))
        self.register_instruction(CIL_AST.Return(0))        

        #out_string
        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        self.register_instruction(CIL_AST.PrintString("x"))
        self.register_instruction(CIL_AST.Return('self'))

        #out_int
        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        self.register_instruction(CIL_AST.PrintInteger("x"))
        self.register_instruction(CIL_AST.Return('self'))

        #in_string
        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        msg = self.define_internal_local(scope=scope, name="read_str")
        self.register_instruction(CIL_AST.ReadString(msg))
        self.register_instruction(CIL_AST.Return(msg))
      
        #in_int
        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        number = self.define_internal_local(scope=scope, name ="read_int")
        self.register_instruction(CIL_AST.ReadInteger(number))
        self.register_instruction(CIL_AST.Return(number))

        # ----------------String---------------------

        #length
        self.current_function = self.register_function(self.to_function_name('length', 'String'))
        self.register_param(VariableInfo('self', None))
        length_result = self.define_internal_local(scope=scope, name="length")
        self.register_instruction(CIL_AST.Length('self', length_result))
        self.register_instruction(CIL_AST.Return(length_result))

        #concat
        self.current_function = self.register_function(self.to_function_name('concat', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('s', None))
        concat_result = self.define_internal_local(scope=scope, name="concat")
        self.register_instruction(CIL_AST.Concat('self', 's', concat_result ))
        self.register_instruction(CIL_AST.Return(concat_result))
        
    
        #substr
        self.current_function = self.register_function(self.to_function_name('substr', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        subs_result = self.define_internal_local(scope=scope, name="subs_result")

        self.register_instruction(CIL_AST.SubStr('i', 'l', 'self', subs_result))
        self.register_instruction(CIL_AST.Return(subs_result))        

        #----------------Bool---------------------


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(COOL_AST.Program)
    def visit(self, node, scope = None):

        scope = Scope()
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local(scope = scope, name = "instance")
        result = self.define_internal_local(scope = scope, name = "result")
        self.register_instruction(CIL_AST.Allocate('Main', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Call(result, self.to_function_name('init', 'Main'), [instance],"Main"))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Call(result, self.to_function_name('main', 'Main'), [instance],"Main"))
        self.register_instruction(CIL_AST.Return(0))
        self.current_function = None

        self.register_data('Execution aborted')
        
        #Add built-in types in .TYPES section
        self.register_builtin_types(scope)
        
        for klass in node.classes:
            self.visit(klass, scope.create_child())

        return CIL_AST.Program(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(COOL_AST.Class)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.name)
        
        #Handle all the .TYPE section
        cil_type = self.register_type(self.current_type.name)
        cil_type.attributes = {f'{attr.name}':attr for c, attr in self.current_type.get_all_attributes()}
        cil_type.methods = {f'{m}':f'{c}.{m}' for c, m  in self.current_type.get_all_methods()}
        cil_type.methods['init'] = f'{node.name}.init'

        scope.define_cil_local("self", self.current_type, self.current_type.name)

        func_declarations = (f for f in node.features if isinstance(f, COOL_AST.ClassMethod))
        attr_declarations = (a for a in node.features if not isinstance(a, COOL_AST.ClassMethod))
        for attr in attr_declarations:
            scope.define_cil_local(attr.name, attr.name, node.name)

        #-------------------------Init---------------------------------
        self.current_function = self.register_function(self.to_function_name('init', node.name))
        instance = self.define_internal_local(scope=scope, name="instance", class_type=self.current_type.name)
        self.register_param(VariableInfo('instance', None))
        self.register_instruction(CIL_AST.Allocate(node.name, instance))
        self.current_type.instance = instance

        #Init parents recursively
        result = self.define_internal_local(scope=scope, name = "result")
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Call(result, self.to_function_name('init', node.parent),[instance], node.parent ))
        self.register_instruction(CIL_AST.Return(0))

        for attr in attr_declarations:
            self.visit(attr, scope)

        
        #---------------------------------------------------------------
        self.current_function = None
        
        for feature in func_declarations:
            self.visit(feature, scope.create_child())
                
        self.current_type = None
                
    @visitor.when(COOL_AST.ClassMethod)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.name)
        self.dottypes[self.current_type.name].methods[node.name] = f'{self.current_type.name}.{node.name}'
        cil_method_name = self.to_function_name(node.name, self.current_type.name)
        self.current_function = self.register_function(cil_method_name)

        self.register_param(VariableInfo('self', self.current_type))
        for p in node.params:
            self.register_param(VariableInfo(p.name, p.param_type))
        
        value = self.visit(node.expr, scope)
        
        self.register_instruction(CIL_AST.Return(value)) 
        self.current_method = None

    @visitor.when(COOL_AST.AttributeDef)
    def visit(self, node, scope):
        self.register_instruction(CIL_AST.SetAttr('instance', node.name, 0, node.type))
    
    @visitor.when(COOL_AST.AttributeInit)
    def visit(self, node, scope):
        expr = self.visit(node.expr, scope)
        self.register_instruction(CIL_AST.SetAttr('instance', node.name, expr, node.type))

    @visitor.when(COOL_AST.AssignExpr)
    def visit(self, node, scope):
        expr_local = self.visit(node.expr, scope)
        result_local = self.define_internal_local(scope=scope, name = "result" )
        cil_node_name = scope.find_cil_local(node.name)

        if self.is_defined_param(node.name):
            self.register_instruction(CIL_AST.Assign(node.name, expr_local))
        elif self.current_type.has_attr(node.name):
            cil_type_name = 'self'
            self.register_instruction(CIL_AST.SetAttr(cil_type_name, cil_node_name, expr_local, self.current_type.name ))
            print(cil_node_name)
        else:
            cil_node_name = scope.find_cil_local(node.name)
            self.register_instruction(CIL_AST.Assign(cil_node_name, expr_local))
        return expr_local

    @visitor.when(COOL_AST.Block)
    def visit(self, node, scope):
        for e in node.exprs:
            result_local = self.visit(e, scope)
        return result_local
                 
    @visitor.when(COOL_AST.If)
    def visit(self, node, scope):
        
        result_local = self.define_internal_local(scope=scope, name = "result")
        cond_local = self.define_internal_local(scope=scope, name = "predicate")
        then_local = self.define_internal_local(scope= scope, name = "then_value")
        else_local = self.define_internal_local(scope=scope, name="else_value")

        cond_value = self.visit(node.predicate, scope)
        self.register_instruction(CIL_AST.Assign(cond_local, cond_value))
        
        self.register_instruction(CIL_AST.IfGoto(cond_local, "if_then"))

        else_value = self.visit(node.else_body, scope)
        self.register_instruction(CIL_AST.Assign(else_local, else_value))
        self.register_instruction(CIL_AST.Assign(result_local, else_local))
      
        self.register_instruction(CIL_AST.Goto("endif"))

        self.register_instruction(CIL_AST.Label("if_then"))
        then_value = self.visit(node.then_body, scope)
        self.register_instruction(CIL_AST.Assign(then_local, then_value))
        self.register_instruction(CIL_AST.Assign(result_local, then_local))
        self.register_instruction(CIL_AST.Label("endif"))

        return result_local

    @visitor.when(COOL_AST.While)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope = scope, name = "result")

        self.register_instruction(CIL_AST.Label("loop_init"))
        pred_value = self.visit(node.predicate, scope)
        self.register_instruction(CIL_AST.IfGoto(pred_value, "loop_body"))
        self.register_instruction(CIL_AST.Goto("loop_end"))
        
        self.register_instruction(CIL_AST.Label("loop_body"))
        body_value = self.visit(node.body, scope)
        self.register_instruction(CIL_AST.Goto("loop_init"))
        self.register_instruction(CIL_AST.Label("loop_end"))

        self.register_instruction(CIL_AST.Assign(result_local, body_value))

        return result_local
    
    @visitor.when(COOL_AST.DynamicCall)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope = scope, name = "result")
        expr_value = self.visit(node.instance, scope)

        call_args = [expr_value]
        for arg in node.args:
            param_local = self.visit(arg, scope)
            call_args.append(param_local)
        
        # dynamic_type = self.define_internal_local(scope= scope, name="dyn_type")
        # self.register_instruction(CIL_AST.TypeOf(expr_value, dynamic_type))

        for arg in call_args:
            self.register_instruction(CIL_AST.Arg(arg))
        self.register_instruction(CIL_AST.VCall(result_local, node.method, call_args, expr_value ))
        
        return result_local

    @visitor.when(COOL_AST.StaticCall)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope = scope, name = "result")

        call_args = ["self"]
        for arg in node.args:
            param_local = self.visit(arg, scope)
            call_args.append(param_local)

        for p in call_args:
            self.register_instruction(CIL_AST.Arg(p))

        static_instance = define_internal_local(scope=scope, name='static_instance')
        self.register_instruction(CIL_AST.Allocate(node.static_type, static_instance))
        
        self.register_instruction(CIL_AST.Call(result_local, node.method, call_args,  static_instance ))
        return result_local
        
    @visitor.when(COOL_AST.Let)
    def visit(self, node, scope):
        let_scope = scope.create_child()
        for var in node.var_list:
            self.visit(var, let_scope)
        
        body_value = self.visit(node.body, let_scope)
        result_local = self.define_internal_local(scope = scope, name = "let_result")
        self.register_instruction(CIL_AST.Assign(result_local, body_value))
        return result_local
    
    @visitor.when(COOL_AST.LetVarInit)
    def visit(self, node, scope):
        expr_value = self.visit(node.expr, scope)
        var_init = self.define_internal_local(scope = scope, name = node.name, cool_var_name= node.name)
        self.register_instruction(CIL_AST.Assign(var_init, expr_value))
        return var_init

    @visitor.when(COOL_AST.LetVarDef)
    def visit(self, node, scope):
        var_def = self.define_internal_local(scope = scope, name = node.name, cool_var_name=node.name)
        self.register_instruction(CIL_AST.Assign(var_def, 0))
        return var_def
    
    
    @visitor.when(COOL_AST.Case)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Action)
    def visit(self, node, scope):
        pass

    @visitor.when(COOL_AST.NewType)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        result_init = self.define_internal_local(scope=scope, name="init")
        
        if node.type == "SELF_TYPE":
            get_type_local = self.define_internal_local(scope = scope, name = "type_name")
            self.register_instruction(CIL_AST.TypeOf("self", get_type_local))
            self.register_instruction(CIL_AST.Allocate(get_type_local, result_local))
            self.register_instruction(CIL_AST.Arg(result_local))
            self.register_instruction(CIL_AST.Call(result_init, self.to_function_name('init', get_type_local), [], self.current_type.name))
        else:
            self.register_instruction(CIL_AST.Allocate(node.type, result_local))
            self.register_instruction(CIL_AST.Arg(result_local))
            self.register_instruction(CIL_AST.Call(result_init,self.to_function_name('init', node.type),[], self.current_type.name ))

        return result_local
        
    @visitor.when(COOL_AST.IsVoid)
    def visit(self, node, scope):
        expre_value = self.visit(node.expr)
        result_local = self.define_internal_local(scope=scope, name ="isvoid_result")
        self.register_instruction(CIL_AST.IsVoid(result_local, expre_value))
        return result_local
       
    @visitor.when(COOL_AST.Sum)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "+"))

        return result_local

    @visitor.when(COOL_AST.Sub)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "-"))

        return result_local

    @visitor.when(COOL_AST.Mult)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "*"))

        return result_local

    @visitor.when(COOL_AST.Div)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "/"))

        return result_local

    @visitor.when(COOL_AST.LogicalNot)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        expr_local = self.define_internal_local(scope=scope) 
        
        expr_value = self.visit(node.expr, scope)
        
        self.register_instruction(CIL_AST.Assign(expr_local, expr_value))
        self.register_instruction(CIL_AST.UnaryOperator(result_local, expr_local, "~"))

        return result_local
        
    @visitor.when(COOL_AST.Not)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        expr_local = self.define_internal_local(scope=scope) 
        
        expr_value = self.visit(node.expr, scope)
        
        self.register_instruction(CIL_AST.Assign(expr_local, expr_value))
        self.register_instruction(CIL_AST.UnaryOperator(result_local, expr_local, "not"))

        return result_local

    @visitor.when(COOL_AST.LessThan)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator(result_local, left_local, right_local, "<"))

        return result_local

    @visitor.when(COOL_AST.LessOrEqualThan)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "<="))

        return result_local

    @visitor.when(COOL_AST.Equals)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "="))

        return result_local

    @visitor.when(COOL_AST.Identifier)
    def visit(self, node, scope):
        cil_name = scope.find_cil_local(node.name)
        if cil_name == None and self.is_defined_param(node.name):
            return node.name
        elif cil_name == None and self.current_type.has_attr(node.name): 
            result_local = self.define_internal_local(scope=scope, name = node.name, class_type=self.current_type.name)
            self.register_instruction(CIL_AST.GetAttr(result_local, "self", node.name, self.current_type.name))
            return result_local
        else:
            return cil_name
    
    @visitor.when(COOL_AST.INTEGER)
    def visit(self, node, scope):
        return node.value

    @visitor.when(COOL_AST.STRING)
    def visit(self, node, scope):
        str_name = ""
        for s in self.dotdata.keys():
            if self.dotdata[s] == node.value:
                str_name = s
                break
        if str_name == "":
            str_name = self.register_data(node.value)

        result_local = self.define_internal_local(scope=scope)
        self.register_instruction(CIL_AST.Load(str_name, result_local))
        return result_local
        
    @visitor.when(COOL_AST.Boolean)
    def visit(self, node, scope):
        if str(node.value) == "true":
            return 1
        else:
            return 0

if __name__ == '__main__':
    import sys
    from cparser import Parser
    from semantic_analyzer import SemanticAnalyzer

    parser = Parser()

    sys.argv.append('test.cl')

    if len(sys.argv) > 1:

        input_file = sys.argv[1]
        with open(input_file, encoding="utf-8") as file:
            cool_program_code = file.read()

        cool_ast = parser.parse(cool_program_code)

        if parser.errors:
            print(parser.errors)
        
        if parser.errors:
            exit(1)

        semantic_analyzer = SemanticAnalyzer(cool_ast)
        context, scope = semantic_analyzer.analyze()

        for e in semantic_analyzer.errors:
            print(e)

        if semantic_analyzer.errors:    
            exit(1)
        
        cool_to_cil = COOLToCILVisitor(context)
        cil_ast = cool_to_cil.visit(cool_ast)

        formatter = CIL_AST.get_formatter()
        print(formatter(cil_ast))
       
        # with open(f'{sys.argv[1][:-3]}.cil', 'w') as f:
        #     f.write(f'{cil_ast}')

    
