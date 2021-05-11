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
        self.label_count = 0
        self.context.set_type_tags()
        self.context.set_type_max_tags()
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def get_label(self):
        self.label_count += 1
        return f'label_{self.label_count}'

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
            cil_type.attributes = [f'{attr.name}' for attr in builtin_type.attributes]
            cil_type.methods = {f'{m}':f'{c}.{m}' for c, m  in builtin_type.get_all_methods()}
            if t in ['Int', 'String', 'Bool']:
                cil_type.attributes.append('value')
    
        #----------------Object---------------------
        #init
        self.current_function = self.register_function('Object_init')
        self.register_param(VariableInfo('self', None))
        self.register_instruction(CIL_AST.Return(None))

        #abort
        self.current_function = self.register_function(self.to_function_name('abort', 'Object'))
        self.register_param(VariableInfo('self',None))
        msg = self.define_internal_local(scope=scope, name="msg")
        key_msg = ''
        for s in self.dotdata.keys():
            if self.dotdata[s] == 'Abort called from class ':
                key_msg = s
        self.register_instruction(CIL_AST.LoadStr(key_msg, msg))
        self.register_instruction(CIL_AST.PrintString(msg))
        type_name = self.define_internal_local(scope=scope, name = "type_name" )
        self.register_instruction(CIL_AST.TypeOf('self', type_name))
        self.register_instruction(CIL_AST.PrintString(type_name))
        eol_local = self.define_internal_local(scope=scope, name="eol")
        for s in self.dotdata.keys():
            if self.dotdata[s] == '\n':
                eol = s
        self.register_instruction(CIL_AST.LoadStr(eol, eol_local))
        self.register_instruction(CIL_AST.PrintString(eol_local))
        self.register_instruction(CIL_AST.Halt())

        #type_name
        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'))
        self.register_param(VariableInfo('self', None))
        type_name = self.define_internal_local(scope=scope, name = "type_name" )
        self.register_instruction(CIL_AST.TypeOf('self', type_name))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String',self.context.get_type('String').tag ,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(type_name),CIL_AST.Arg(instance)],"String"))
        self.register_instruction(CIL_AST.Return(instance))

        #copy
        self.current_function = self.register_function(self.to_function_name('copy', 'Object'))
        self.register_param(VariableInfo('self',None))
        copy = self.define_internal_local(scope=scope, name= "copy")
        self.register_instruction(CIL_AST.Copy('self', copy))
        self.register_instruction(CIL_AST.Return(copy))

        #----------------IO---------------------
        #init
        self.current_function = self.register_function('IO_init')
        self.register_param(VariableInfo('self', None))
        self.register_instruction(CIL_AST.Return(None))        

        #out_string
        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        v = self.define_internal_local(scope=scope, name="v")
        self.register_instruction(CIL_AST.GetAttr(v, 'x','value','String'))
        self.register_instruction(CIL_AST.PrintString(v))
        self.register_instruction(CIL_AST.Return('self'))

        #out_int
        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        v = self.define_internal_local(scope=scope, name="v")
        self.register_instruction(CIL_AST.GetAttr(v, 'x','value','Int'))
        self.register_instruction(CIL_AST.PrintInteger(v))
        self.register_instruction(CIL_AST.Return('self'))

        #in_string
        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        msg = self.define_internal_local(scope=scope, name="read_str")
        self.register_instruction(CIL_AST.ReadString(msg))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String',self.context.get_type('String').tag ,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(msg),CIL_AST.Arg(instance)],"String"))
        self.register_instruction(CIL_AST.Return(instance))
      
        #in_int
        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        number = self.define_internal_local(scope=scope, name ="read_int")
        self.register_instruction(CIL_AST.ReadInteger(number))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Int_init', [ CIL_AST.Arg(number), CIL_AST.Arg(instance)], "Int"))
        self.register_instruction(CIL_AST.Return(instance))

        # ----------------String---------------------
        #init
        self.current_function=self.register_function('String_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(CIL_AST.SetAttr('self', 'value', 'v', 'String'))
        self.register_instruction(CIL_AST.Return(None))   

        #length
        self.current_function = self.register_function(self.to_function_name('length', 'String'))
        self.register_param(VariableInfo('self', None))
        length_result = self.define_internal_local(scope=scope, name="length")
        self.register_instruction(CIL_AST.Length('self', length_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init,'Int_init', [CIL_AST.Arg(length_result),CIL_AST.Arg(instance)], "Int"))
        self.register_instruction(CIL_AST.Return(instance))

        #concat
        self.current_function = self.register_function(self.to_function_name('concat', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('s', None))

        str1 = self.define_internal_local(scope=scope, name="str1")
        self.register_instruction(CIL_AST.GetAttr(str1, 'self','value','String'))
        len1 = self.define_internal_local(scope=scope, name="len1")
        self.register_instruction(CIL_AST.Call(len1, 'String.length', [CIL_AST.Arg('self')], 'String'))

        str2 = self.define_internal_local(scope=scope, name="str2")
        self.register_instruction(CIL_AST.GetAttr(str2, 's', 'value', 'String'))
        len2 = self.define_internal_local(scope=scope, name="len2")
        self.register_instruction(CIL_AST.Call(len2, 'String.length', [CIL_AST.Arg('s')], 'String'))

        local_len1 = self.define_internal_local(scope=scope, name="local_len1")
        self.register_instruction(CIL_AST.GetAttr(local_len1, len1, 'value', 'Int'))
        local_len2 = self.define_internal_local(scope=scope, name="local_len2")
        self.register_instruction(CIL_AST.GetAttr(local_len2, len2, 'value', 'Int'))

        concat_result = self.define_internal_local(scope=scope, name="concat")
        self.register_instruction(CIL_AST.Concat(str1, local_len1, str2, local_len2, concat_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String',self.context.get_type('String').tag ,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(concat_result), CIL_AST.Arg(instance)],"String"))
        self.register_instruction(CIL_AST.Return(instance))
        
    
        #substr
        self.current_function = self.register_function(self.to_function_name('substr', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        i_value=self.define_internal_local(scope=scope, name="i_value")
        self.register_instruction(CIL_AST.GetAttr(i_value, 'i','value','Int'))
        l_value = self.define_internal_local(scope=scope, name="l_value")
        self.register_instruction(CIL_AST.GetAttr(l_value, 'l','value','Int'))
        subs_result=self.define_internal_local(scope=scope, name="subs_result")
        self.register_instruction(CIL_AST.SubStr(i_value, l_value, 'self', subs_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String', self.context.get_type('String').tag,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(subs_result),CIL_AST.Arg(instance)],"String"))
        self.register_instruction(CIL_AST.Return(instance))
              
        #----------------Bool---------------------
        #init
        self.current_function=self.register_function('Bool_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(CIL_AST.SetAttr('self', 'value', 'v', 'Bool'))
        self.register_instruction(CIL_AST.Return(None))
        
        #----------------Int---------------------
        #init
        self.current_function=self.register_function('Int_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(CIL_AST.SetAttr('self', 'value', 'v', 'Int'))
        self.register_instruction(CIL_AST.Return(None)) 

    def build_string_equals_function(self, scope):
        self.current_function = self.register_function('String_equals')
        self.register_param(VariableInfo('str1', None))
        self.register_param(VariableInfo('str2', None))
        
        str1 = self.define_internal_local(scope=scope, name="str1")
        self.register_instruction(CIL_AST.GetAttr(str1, 'str1', 'value','String'))
        
        str2 = self.define_internal_local(scope=scope, name="str2")
        self.register_instruction(CIL_AST.GetAttr(str2, 'str2', 'value', 'String'))
        
        result = self.define_internal_local(scope=scope, name="comparison_result")
        self.register_instruction(CIL_AST.StringEquals(str1, str2, result))
        self.register_instruction(CIL_AST.Return(result))

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(COOL_AST.Program)
    def visit(self, node, scope = None):

        scope = Scope()
        self.current_function = self.register_function('main')
        instance = self.define_internal_local(scope = scope, name = "instance")
        result = self.define_internal_local(scope = scope, name = "result")
        self.register_instruction(CIL_AST.Allocate('Main',self.context.get_type('Main').tag, instance))
        self.register_instruction(CIL_AST.Call(result, 'Main_init', [CIL_AST.Arg(instance)],"Main"))
        self.register_instruction(CIL_AST.Call(result, self.to_function_name('main', 'Main'), [CIL_AST.Arg(instance)],"Main"))
        self.register_instruction(CIL_AST.Return(None))
        self.current_function = None

        self.register_data('Abort called from class ')
        self.register_data('\n')
        self.dotdata['empty_str'] = ''
        
        #Add built-in types in .TYPES section
        self.register_builtin_types(scope)

        #Add string equals function
        self.build_string_equals_function(scope)
        
        for klass in node.classes:
            self.visit(klass, scope.create_child())

        return CIL_AST.Program(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(COOL_AST.Class)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.name)
        
        #Handle all the .TYPE section
        cil_type = self.register_type(self.current_type.name)
        cil_type.attributes = [f'{attr.name}' for c, attr in self.current_type.get_all_attributes()]
        cil_type.methods = {f'{m}':f'{c}.{m}' for c, m  in self.current_type.get_all_methods()}

        scope.define_cil_local("self", self.current_type.name, self.current_type)

        func_declarations = [f for f in node.features if isinstance(f, COOL_AST.ClassMethod)]
        attr_declarations = [a for a in node.features if not isinstance(a, COOL_AST.ClassMethod)]
        for attr in attr_declarations:
            scope.define_cil_local(attr.name, attr.name, node.name)


        #-------------------------Init---------------------------------
        self.current_function = self.register_function(f'{node.name}_init')
        self.register_param(VariableInfo('self', None))

        #Init parents recursively
        result = self.define_internal_local(scope=scope, name = "result")
        self.register_instruction(CIL_AST.Call(result, f'{node.parent}_init',[CIL_AST.Arg('self')], node.parent))
        self.register_instruction(CIL_AST.Return(None))

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
        instance = None

        if node.type in ['Int', 'Bool']:
            instance = self.define_internal_local(scope=scope, name="instance")
            self.register_instruction(CIL_AST.Allocate(node.type,self.context.get_type(node.type).tag, instance))
            value = self.define_internal_local(scope=scope, name="value")
            self.register_instruction(CIL_AST.LoadInt(0,value))
            result_init = self.define_internal_local(scope=scope, name="result_init")
            self.register_instruction(CIL_AST.Call(result_init, f'{node.type}_init', [ CIL_AST.Arg(value), CIL_AST.Arg(instance)], node.type))
        elif node.type == 'String':
            instance = self.define_internal_local(scope=scope, name="instance")
            self.register_instruction(CIL_AST.Allocate(node.type,self.context.get_type(node.type).tag ,instance))
            value = self.define_internal_local(scope=scope, name="value")
            self.register_instruction(CIL_AST.LoadStr('empty_str',value))
            result_init = self.define_internal_local(scope=scope, name="result_init")
            self.register_instruction(CIL_AST.Call(result_init, f'{node.type}_init', [CIL_AST.Arg(value),CIL_AST.Arg(instance)], node.type))

        self.register_instruction(CIL_AST.SetAttr('self', node.name,instance, self.current_type.name))
    
    @visitor.when(COOL_AST.AttributeInit)
    def visit(self, node, scope):
        expr = self.visit(node.expr, scope)
        self.register_instruction(CIL_AST.SetAttr('self', node.name, expr, self.current_type.name))

    @visitor.when(COOL_AST.AssignExpr)
    def visit(self, node, scope):
        expr_local = self.visit(node.expr, scope)
        result_local = self.define_internal_local(scope=scope, name = "result" )
        cil_node_name = scope.find_cil_local(node.name)

        if self.is_defined_param(node.name):
            self.register_instruction(CIL_AST.Assign(node.name, expr_local))
        elif self.current_type.has_attr(node.name):
            cil_type_name = 'self'
            self.register_instruction(CIL_AST.SetAttr(cil_type_name, node.name, expr_local, self.current_type.name ))
        else:
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

        cond_value = self.visit(node.predicate, scope)

        if_then_label = self.get_label()
        self.register_instruction(CIL_AST.IfGoto(cond_value, if_then_label))

        else_value = self.visit(node.else_body, scope)
        self.register_instruction(CIL_AST.Assign(result_local, else_value))
      
        end_if_label = self.get_label()
        self.register_instruction(CIL_AST.Goto(end_if_label))

        self.register_instruction(CIL_AST.Label(if_then_label))
        then_value = self.visit(node.then_body, scope)
        self.register_instruction(CIL_AST.Assign(result_local, then_value))
        self.register_instruction(CIL_AST.Label(end_if_label))

        return result_local

    @visitor.when(COOL_AST.While)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope = scope, name = "result")
        
        loop_init_label = self.get_label()
        loop_body_label = self.get_label()
        loop_end_label = self.get_label()
        self.register_instruction(CIL_AST.Label(loop_init_label))
        pred_value = self.visit(node.predicate, scope)
        self.register_instruction(CIL_AST.IfGoto(pred_value, loop_body_label))
        self.register_instruction(CIL_AST.Goto(loop_end_label))
        
        self.register_instruction(CIL_AST.Label(loop_body_label))
        body_value = self.visit(node.body, scope)
        self.register_instruction(CIL_AST.Goto(loop_init_label))
        self.register_instruction(CIL_AST.Label(loop_end_label))

        self.register_instruction(CIL_AST.LoadVoid(result_local))
        return result_local
    
    @visitor.when(COOL_AST.DynamicCall)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope = scope, name = "result")
        expr_value = self.visit(node.instance, scope)

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope)
            call_args.append(CIL_AST.Arg(param_local))
        call_args.append(CIL_AST.Arg(expr_value))

        dynamic_type = node.instance.computed_type.name
        self.register_instruction(CIL_AST.VCall(result_local, node.method, call_args, dynamic_type, expr_value))
        
        return result_local

    @visitor.when(COOL_AST.StaticCall)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope = scope, name = "result")
        expr_value = self.visit(node.instance, scope)

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope)
            call_args.append(CIL_AST.Arg(param_local))
        call_args.append(CIL_AST.Arg(expr_value))

        static_instance = self.define_internal_local(scope=scope, name='static_instance')
        self.register_instruction(CIL_AST.Allocate(node.static_type,self.context.get_type(node.static_type).tag ,static_instance))
        
        self.register_instruction(CIL_AST.VCall(result_local, node.method, call_args, node.static_type, static_instance))
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
        instance = None

        if node.type in ['Int', 'Bool']:
            instance = self.define_internal_local(scope=scope, name="instance")
            self.register_instruction(CIL_AST.Allocate(node.type,self.context.get_type(node.type).tag, instance))
            value = self.define_internal_local(scope=scope, name="value")
            self.register_instruction(CIL_AST.LoadInt(0,value))
            result_init = self.define_internal_local(scope=scope, name="result_init")
            self.register_instruction(CIL_AST.Call(result_init, f'{node.type}_init', [ CIL_AST.Arg(value), CIL_AST.Arg(instance)], node.type))
        elif node.type == 'String':
            instance = self.define_internal_local(scope=scope, name="instance")
            self.register_instruction(CIL_AST.Allocate(node.type,self.context.get_type(node.type).tag ,instance))
            value = self.define_internal_local(scope=scope, name="value")
            self.register_instruction(CIL_AST.LoadStr('empty_str',value))
            result_init = self.define_internal_local(scope=scope, name="result_init")
            self.register_instruction(CIL_AST.Call(result_init, f'{node.type}_init', [CIL_AST.Arg(value), CIL_AST.Arg(instance)], node.type))
            
        var_def = self.define_internal_local(scope = scope, name = node.name, cool_var_name=node.name)
        self.register_instruction(CIL_AST.Assign(var_def, instance))
        return var_def
    
    
    @visitor.when(COOL_AST.Case)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope = scope, name = "result")
        case_expr = self.visit(node.expr, scope)

        exit_label = self.get_label()
        label = self.get_label()

        self.register_instruction(CIL_AST.Case(case_expr, label))
        
        tag_lst = []
        action_dict = {}
        for action in node.actions:
            tag = self.context.get_type(action.action_type).tag
            tag_lst.append(tag)
            action_dict[tag] = action
        tag_lst.sort()

        for t in reversed(tag_lst):
            action = action_dict[t]
            self.register_instruction(CIL_AST.Label(label))
            label = self.get_label()

            action_type = self.context.get_type(action.action_type) 
            self.register_instruction(CIL_AST.Action(case_expr, action_type.tag, action_type.max_tag, label))

            action_scope = scope.create_child()
            action_id = self.define_internal_local(scope=action_scope, name=action.name, cool_var_name=action.name)
            self.register_instruction(CIL_AST.Assign(action_id, case_expr))
            expr_result = self.visit(action.body, action_scope)

            self.register_instruction(CIL_AST.Assign(result_local, expr_result))
            self.register_instruction(CIL_AST.Goto(exit_label))
            
        self.register_instruction(CIL_AST.Label(label))
        self.register_instruction(CIL_AST.Goto('case_no_match_error'))
        self.register_instruction(CIL_AST.Label(exit_label))
        return result_local

    @visitor.when(COOL_AST.Action)
    def visit(self, node, scope):
        pass

    @visitor.when(COOL_AST.NewType)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        result_init = self.define_internal_local(scope=scope, name="init")
        
        if node.type == "SELF_TYPE":
            self.register_instruction(CIL_AST.Allocate(self.current_type.name,self.current_type.tag ,result_local))
            self.register_instruction(CIL_AST.Call(result_init, f'{self.current_type.name}_init', [result_local], self.current_type.name))
        else:
            self.register_instruction(CIL_AST.Allocate(node.type,self.context.get_type(node.type).tag ,result_local))
            self.register_instruction(CIL_AST.Call(result_init,f'{node.type}_init' ,[CIL_AST.Arg(result_local)], self.current_type.name ))

        return result_local
        
    @visitor.when(COOL_AST.IsVoid)
    def visit(self, node, scope):
        expre_value = self.visit(node.expr, scope)
        result_local = self.define_internal_local(scope=scope, name ="isvoid_result")
        self.register_instruction(CIL_AST.IsVoid(result_local, expre_value))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Bool',self.context.get_type('Bool').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(result_local),CIL_AST.Arg(instance)], "Bool"))
        return instance
       
    @visitor.when(COOL_AST.Sum)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.GetAttr(left_local, left_value, "value", node.left.computed_type.name))
        self.register_instruction(CIL_AST.GetAttr(right_local, right_value, "value", node.right.computed_type.name))

        self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "+"))

        # Allocate Int result
        self.register_instruction(CIL_AST.Allocate('Int',self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Int"))

        return result_local

    @visitor.when(COOL_AST.Sub)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.GetAttr(left_local, left_value, "value", node.left.computed_type.name))
        self.register_instruction(CIL_AST.GetAttr(right_local, right_value, "value", node.right.computed_type.name))

        self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "-"))

        # Allocate Int result
        self.register_instruction(CIL_AST.Allocate('Int',self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Int"))

        return result_local

    @visitor.when(COOL_AST.Mult)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.GetAttr(left_local, left_value, "value", node.left.computed_type.name))
        self.register_instruction(CIL_AST.GetAttr(right_local, right_value, "value", node.right.computed_type.name))

        self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "*"))

        # Allocate Int result
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Int"))

        return result_local

    @visitor.when(COOL_AST.Div)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.GetAttr(left_local, left_value, "value", node.left.computed_type.name))
        self.register_instruction(CIL_AST.GetAttr(right_local, right_value, "value", node.right.computed_type.name))

        self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "/"))

        # Allocate Int result
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Int"))

        return result_local

    @visitor.when(COOL_AST.LogicalNot)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        expr_local = self.define_internal_local(scope=scope) 
        
        expr_value = self.visit(node.expr, scope)
        
        self.register_instruction(CIL_AST.GetAttr(expr_local, expr_value, "value", node.expr.computed_type.name))
        self.register_instruction(CIL_AST.UnaryOperator(op_local, expr_local, "~"))

        # Allocate Int result
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Int"))

        return result_local
        
    @visitor.when(COOL_AST.Not)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        expr_local = self.define_internal_local(scope=scope) 
        
        expr_value = self.visit(node.expr, scope)
        
        self.register_instruction(CIL_AST.GetAttr(expr_local, expr_value, "value", node.expr.computed_type.name))
        self.register_instruction(CIL_AST.UnaryOperator(op_local, expr_local, "not"))

        # Allocate Bool result
        self.register_instruction(CIL_AST.Allocate('Bool',self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Bool"))

        return result_local

    @visitor.when(COOL_AST.LessThan)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.GetAttr(left_local, left_value, "value", node.left.computed_type.name))
        self.register_instruction(CIL_AST.GetAttr(right_local, right_value, "value", node.right.computed_type.name))

        self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "<"))

        # Allocate Bool result
        self.register_instruction(CIL_AST.Allocate('Bool',self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Bool"))

        return result_local

    @visitor.when(COOL_AST.LessOrEqualThan)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.GetAttr(left_local, left_value, "value", node.left.computed_type.name))
        self.register_instruction(CIL_AST.GetAttr(right_local, right_value, "value", node.right.computed_type.name))

        self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "<="))

        # Allocate Bool result
        self.register_instruction(CIL_AST.Allocate('Bool',self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Bool"))

        return result_local

    @visitor.when(COOL_AST.Equals)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        if node.left.computed_type.name == 'String':
            self.register_instruction(CIL_AST.Call(op_local, 'String_equals', [CIL_AST.Arg(right_value), CIL_AST.Arg(left_value)], 'String'))

            # Allocate Bool result
            self.register_instruction(CIL_AST.Allocate('Bool',self.context.get_type('Bool').tag, result_local))
            result_init = self.define_internal_local(scope=scope, name="result_init")
            self.register_instruction(CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Bool"))

            return result_local

        elif node.left.computed_type.name in ['Int', 'Bool']:
            self.register_instruction(CIL_AST.GetAttr(left_local, left_value, "value", node.left.computed_type.name))
            self.register_instruction(CIL_AST.GetAttr(right_local, right_value, "value", node.right.computed_type.name))
        else:
            self.register_instruction(CIL_AST.Assign(left_local, left_value))
            self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "="))

        # Allocate Bool result
        self.register_instruction(CIL_AST.Allocate('Bool',self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Bool"))

        return result_local

    @visitor.when(COOL_AST.Identifier)
    def visit(self, node, scope):
        if self.is_defined_param(node.name):
            return node.name
        elif self.current_type.has_attr(node.name): 
            result_local = self.define_internal_local(scope=scope, name = node.name, class_type=self.current_type.name)
            self.register_instruction(CIL_AST.GetAttr(result_local, 'self' , node.name, self.current_type.name))
            return result_local
        else:
            return scope.find_cil_local(node.name)
    
    @visitor.when(COOL_AST.INTEGER)
    def visit(self, node, scope):
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Int',self.context.get_type('Int').tag, instance))
        value = self.define_internal_local(scope=scope, name="value")
        self.register_instruction(CIL_AST.LoadInt(node.value,value))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(value),CIL_AST.Arg(instance)], "Int"))
        return instance

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
        self.register_instruction(CIL_AST.LoadStr(str_name, result_local))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String',self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(result_local),CIL_AST.Arg(instance)], "String"))
        return instance
        
    @visitor.when(COOL_AST.Boolean)
    def visit(self, node, scope):
        boolean = 0
        if str(node.value) == "true":
            boolean = 1
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Bool',self.context.get_type('Bool').tag, instance))
        value = self.define_internal_local(scope=scope, name="value")
        self.register_instruction(CIL_AST.LoadInt(boolean, value))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(value),CIL_AST.Arg(instance)], "Bool"))
        return instance

if __name__ == '__main__':
    import sys
    from cparser import Parser
    from semantic_analyzer import SemanticAnalyzer

    parser = Parser()

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

    
