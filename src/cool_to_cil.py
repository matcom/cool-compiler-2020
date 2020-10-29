from cil_types_collector import CILTypesCollector
from cil_data_collector import CILDataCollector
from cil_code_builder import CILCodeBuilder
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
    
    @property
    def labels(self):
        return self.current_function.labels

    def register_param(self, vinfo):
        param_node = CIL_AST.ParamDec(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def is_defined_param(self, name):
        for p in self.params:
            if p.name == name:
                return True
        return False
    
    def register_local(self, name):
        var_name = f'{name}_{len(self.localvars)}'
        local_node = CIL_AST.LocalDec(var_name)
        self.localvars.append(local_node)
        return var_name

    def define_internal_local(self):
        return self.register_local("internal")

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'

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
    
    def register_builtin_types(self):
        for t in ['Object', 'Int', 'String', 'Bool', 'IO']:
            builtin_type = self.context.get_type(t)
            cil_type = self.register_type(t)
            cil_type.attributes = {f'{t}.{attr.name}':attr for attr in builtin_type.attributes}
            cil_type.methods = {f'{t}.{m}': m for _, m  in builtin_type.get_all_methods()}
                        
        #----------------Object---------------------
        object_type = self.context.get_type('Object')
        object_cil = self.register_type('Object')
        object_cil.attributes = []
        object_cil.methods = [(method, self.to_function_name(method, kclass)) for kclass, method in object_type.get_all_methods()]

        #init
        self.current_function = self.register_function(self.to_function_name('init', 'Object'))
        self.register_param(VariableInfo('instance', None))
        self.register_instruction(CIL_AST.Return(0))

        #abort
        self.current_function = self.register_function(self.to_function_name('abort', 'Object'))
        self.register_param(VariableInfo('self',None))
        msg = self.define_internal_local()
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
        type_name = self.define_internal_local()
        self.register_instruction(CIL_AST.TypeOf('self', type_name))
        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('String', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Arg(type_name))
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', 'String'), result))
        self.register_instruction(CIL_AST.Return(instance))

        #copy
        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'))
        self.register_param(VariableInfo('self', None))
        self.register_instruction(CIL_AST.Return(0))

        #----------------IO---------------------
        IO_type = self.context.get_type('IO')
        IO_cil = self.register_type('IO')
        IO_cil.attributes = []
        IO_cil.methods = [(method, self.to_function_name(method, kclass)) for kclass, method in IO_type.get_all_methods()]

        #init
        self.current_function = self.register_function(self.to_function_name('init', 'IO'))
        self.register_param(VariableInfo('instance', None))
        self.register_instruction(CIL_AST.Return(0))        

        #out_string
        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        msg = self.define_internal_local()
        self.register_instruction(CIL_AST.GetAttr(msg, 'x', 'value', 'String'))
        self.register_instruction(CIL_AST.PrintString(msg))
        self.register_instruction(CIL_AST.Return('self'))

        #out_int
        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        number = self.define_internal_local()
        self.register_instruction(CIL_AST.GetAttr(number, 'x', 'value', 'Int'))
        self.register_instruction(CIL_AST.PrintInteger(number))
        self.register_instruction(CIL_AST.Return('self'))

        #in_string
        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        msg = self.define_internal_local()
        self.register_instruction(CIL_AST.ReadString(msg))
        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('String', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Arg(msg))
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', 'String'), result))
        self.register_instruction(CIL_AST.Return(instance))
      
        #in_int
        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        number = self.define_internal_local()
        self.register_instruction(CIL_AST.ReadInteger(number))
        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('Int', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Arg(number))
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', 'Int'), result))
        self.register_instruction(CIL_AST.Return(instance))

        #----------------Int---------------------
        int_type = self.context.get_type('Int')
        int_cil = self.register_type('Int')
        int_cil.attributes = ['value']
        int_cil.methods = [(method, self.to_function_name(method, kclass)) for kclass, method in int_type.get_all_methods()]

        #init
        self.current_function = self.register_function(self.to_function_name('init', 'Int'))
        self.register_param(VariableInfo('instance', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(CIL_AST.SetAttr('instance','value','v','Int'))
        self.register_instruction(CIL_AST.Return(0))        


        # ----------------String---------------------
        object_type = self.context.get_type('String')
        object_cil = self.register_type('String')
        object_cil.attributes = ['value', 'length']
        object_cil.methods = [(method, self.to_function_name(method, kclass)) for kclass, method in object_type.get_all_methods()]

        #init
        self.current_function = self.register_function(self.to_function_name('init', 'String'))
        self.register_param(VariableInfo('instance', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(CIL_AST.SetAttr('instance', 'value', 'v', 'String'))
        number = self.define_internal_local()
        self.register_instruction(CIL_AST.Length('v', number))
        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('Int', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Arg(number))
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', 'Int'), result))
        self.register_instruction(CIL_AST.SetAttr('instance', 'length', instance, 'Int'))
        self.register_instruction(CIL_AST.Return(0))

        #length
        self.current_function = self.register_function(self.to_function_name('length', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_instruction(CIL_AST.GetAttr(result, 'self', 'length', 'String'))
        self.register_instruction(CIL_AST.Return(result))

        #concat
        self.current_function = self.register_function(self.to_function_name('concat', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('s', None))
        string1 = self.define_internal_local()
        string2 = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.GetAttr(string1, 'self', 'value', 'String'))
        self.register_instruction(CIL_AST.GetAttr(string2, 's', 'value', 'String'))
        self.register_instruction(CIL_AST.Concat(string1, string2, result))
        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('String', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Arg(result))
        result_init = self.define_internal_local()
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', 'String'), result_init))
        self.register_instruction(CIL_AST.Return(instance))

        #substr
        self.current_function = self.register_function(self.to_function_name('substr', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        pos = self.define_internal_local()
        len_sub = self.define_internal_local()
        self.register_instruction(CIL_AST.GetAttr(pos, 'i', 'value', 'Int'))
        self.register_instruction(CIL_AST.GetAttr(len_sub, 'l', 'value', 'Int'))
        string = self.define_internal_local()
        substring = self.define_internal_local()  
        self.register_instruction(CIL_AST.GetAttr(string, 'self', 'value', 'String'))
        self.register_instruction(CIL_AST.SubStr(pos, len_sub, string, substring))
        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('String', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Arg(substring))
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', 'String'), result))
        self.register_instruction(CIL_AST.Return(instance))        

        #----------------Bool---------------------
        bool_type = self.context.get_type('Bool')
        bool_cil = self.register_type('Bool')
        bool_cil.attributes = ['value']
        bool_cil.methods = [(method, self.to_function_name(method, kclass)) for kclass, method in int_type.get_all_methods()]

        #init
        self.current_function = self.register_function(self.to_function_name('init', 'Bool'))
        self.register_param(VariableInfo('instance', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(CIL_AST.SetAttr('instance','value','v','Bool'))
        self.register_instruction(CIL_AST.Return(0))  


class MiniCOOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(COOL_AST.Program)
    def visit(self, node, scope):

        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('Main', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Call(result, self.to_function_name('init', 'Main'), [instance],"Main")
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Call(result, self.to_function_name('main', 'Main'), [instance],"Main"))
        self.register_instruction(CIL_AST.Return(0))
        self.current_function = None

        self.register_data('Execution aborted')

        #Add built-in types in .TYPES section
        self.register_builtin_types()
        
        for klass, child_scope in zip(node.classes, scope.children):
            self.visit(klass, child_scope)

        return CIL_AST.Program(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(COOL_AST.Class)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.name)
        
        #Handle all the .TYPE section
        cil_type = self.register_type(self.current_type.name)
        cil_type.attributes = {f'{self.current_type.name}.{attr.name}':attr for attr in self.current_type.get_all_attributes()}
        cil_type.methods = {f'{self.current_type.name}.{m}': m for _, m  in self.current_type.get_all_methods()}


        func_declarations = (f for f in node.features if isinstance(f, COOL_AST.ClassMethod))
        for feature, child_scope in zip(func_declarations, scope.children):
            self.visit(feature, child_scope)
        
        attr_declarations = (f for f in node.features if not isinstance(f, COOL_AST.ClassMethod))

        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate(node.name, instance))
        self.current_type.instance = instance

        #-------------------------Init---------------------------------
        self.current_function = self.to_function_name('init', node.name)
        self.register_param(VariableInfo('instance', None))

        #Init parents recursively
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', node.parent), result))

        for attr in attr_declarations:
            self.visit(attr, scope)

        self.register_instruction(CIL_AST.Return(0))
        #---------------------------------------------------------------

        self.current_function = None
        self.current_type = None
                
    @visitor.when(COOL_AST.ClassMethod)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.name)
        
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
        self.register_instruction(CIL_AST.SetAttr('instance', node.name,0, node.type))
    
    @visitor.when(COOL_AST.AttributeInit)
    def visit(self, node, scope):
        expr = self.visit(node.expr, scope)
        self.register_instruction(CIL_AST.SetAttr('instance', node.name, expr, node.type))

    @visitor.when(COOL_AST.AssignExpr)
    def visit(self, node, scope):
        expr_local = self.visit(node.expr, scope)
        result_local = self.define_internal_local()

        if self.is_defined_param(node.name):
            self.register_instruction(CIL_AST.Assign(node.name, expr_local))
            return expr_local
        elif self.current_type.has_attr(node.name):
            self.register_instruction(CIL_AST.SetAttr("self", node.name, expr_local, self.current_type.name ))
            return expr_local
        else:
            print("visit COOL ASSIGN error ")
        #TODO: cuando no es ninguno de los casos

    @visitor.when(COOL_AST.Block)
    def visit(self, node, scope):
        for e in node.exprs:
            result_local = self.visit(e, scope)
        return result_local
                 
    @visitor.when(COOL_AST.If)
    def visit(self, node, scope):
        
        result_local = self.define_internal_local()
        cond_local = self.define_internal_local()
        then_local = self.define_internal_local()
        else_local = self.define_internal_local()

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
        result_local = self.define_internal_local()

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
        result_local = self.define_internal_local()
        expr_value = self.visit(node.instance, scope)

        call_args = [expr_value]
        for arg in node.args:
            param_local = self.visit(arg, scope)
            call_args.append(param_local)
        
        dynamic_type = self.define_internal_local()
        self.register_instruction(CIL_AST.TypeOf(expr_value, dynamic_type))

        for arg in call_args:
            self.register_instruction(CIL_AST.Arg(arg))
        self.register_instruction(CIL_AST.VCall(result_local, node.method, call_args, dynamic_type ))
        
        return result_local

    @visitor.when(COOL_AST.StaticCall)
    def visit(self, node, scope):
        result_local = self.define_internal_local()

        call_args = ["self"]
        for arg in node.args:
            param_local = self.visit(arg, scope)
            call_args.append(param_local)

        for p in call_args:
            self.register_instruction(CIL_AST.Arg(p))
        
        self.register_instruction(CIL_AST.Call(result_local, node.method, call_args,  node.static_type, ))
        return result_local

    @visitor.when(COOL_AST.Case)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Action)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Let)
    def visit(self, node, scope):
        pass
    
    @visitor.when(COOL_AST.LetVarInit)
    def visit(self, node, scope):
        pass

    @visitor.when(COOL_AST.LetVarDef)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.NewType)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        result_init = self.define_internal_local()

        if node.type == "SELF_TYPE":
            get_type_local = self.define_internal_local()
            self.register_instruction(CIL_AST.TypeOf("self", get_type_local))
            self.register_instruction(CIL_AST.Allocate(get_type_local, result_local))
            self.register_instruction(CIL_AST.Arg(result_local))
            self.register_instruction(CIL_AST.Call(self.to_function_name('init', get_type_local), result_init))
        else:
            self.register_instruction(CIL_AST.Allocate(node.type, result_local))
            self.register_instruction(CIL_AST.Arg(result_local))
            self.register_instruction(CIL_AST.Call(self.to_function_name('init', node.type), result_init))

        return result_local
        
    @visitor.when(COOL_AST.IsVoid)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Sum)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.define_internal_local()
        right_local = self.define_internal_local()

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "+"))

        return result_local

    @visitor.when(COOL_AST.Sub)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.define_internal_local()
        right_local = self.define_internal_local()

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "-"))

        return result_local

    @visitor.when(COOL_AST.Mult)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.define_internal_local()
        right_local = self.define_internal_local()

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "*"))

        return result_local

    @visitor.when(COOL_AST.Div)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.define_internal_local()
        right_local = self.define_internal_local()

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "/"))

        return result_local

    @visitor.when(COOL_AST.LogicalNot)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        expr_local = self.define_internal_local() 
        
        expr_value = self.visit(node.expr, scope)
        
        self.register_instruction(CIL_AST.Assign(expr_local, expr_value))
        self.register_instruction(CIL_AST.UnaryOperator(result_local, expr_local, "~"))

        return result_local
        
    @visitor.when(COOL_AST.Not)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        expr_local = self.define_internal_local() 
        
        expr_value = self.visit(node.expr, scope)
        
        self.register_instruction(CIL_AST.Assign(expr_local, expr_value))
        self.register_instruction(CIL_AST.UnaryOperator(result_local, expr_local, "not"))

        return result_local

    @visitor.when(COOL_AST.LessThan)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.define_internal_local()
        right_local = self.define_internal_local()

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator(result_local, left_local, right_local, "<"))

        return result_local

    @visitor.when(COOL_AST.LessOrEqualThan)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.define_internal_local()
        right_local = self.define_internal_local()

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "<="))

        return result_local

    @visitor.when(COOL_AST.Equals)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.define_internal_local()
        right_local = self.define_internal_local()

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CIL_AST.Assign(left_local, left_value))
        self.register_instruction(CIL_AST.Assign(right_local, right_value))

        self.register_instruction(CIL_AST.BinaryOperator( result_local, left_local, right_local, "="))

        return result_local

    @visitor.when(COOL_AST.Identifier)
    def visit(self, node, scope):
        if self.is_defined_param(node.name):
            return node.name
        else: 
            self.current_type.has_attr(node.name) #load class attr
            result_local = self.define_internal_local()
            self.register_instruction(CIL_AST.GetAttr(result_local, "self", node.name, self.current_type.name))
            return result_local
    
    @visitor.when(COOL_AST.INTEGER)
    def visit(self, node, scope):
        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('Int', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Arg(node.value))
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', 'Int'), result))
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

        result_local = self.define_internal_local()
        self.register_instruction(CIL_AST.Load(str_name, result_local))
        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('String', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Arg(result_local))
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', 'String'), result))
        return instance   
        
    @visitor.when(COOL_AST.Boolean)
    def visit(self, node, scope):
        val = 0
        if str(node.value) == "true":
            val = 1
        instance = self.define_internal_local()
        self.register_instruction(CIL_AST.Allocate('Bool', instance))
        self.register_instruction(CIL_AST.Arg(instance))
        self.register_instruction(CIL_AST.Arg(val))
        result = self.define_internal_local()
        self.register_instruction(CIL_AST.Call(self.to_function_name('init', 'Bool'), result))
        return instance

if __name__ == '__main__':
    import sys
    from cparser import Parser
    from semantic_analyzer import SemanticAnalyzer

    parser = Parser()

    sys.argv.append('hello_world.cl')

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
        
        cool_to_cil = MiniCOOLToCILVisitor(context)
        cil_ast = cool_to_cil.visit(cool_ast, scope)

        formatter = CIL_AST.get_formatter()
        print(formatter(cil_ast))
       
        # with open(f'{sys.argv[1][:-3]}.cil', 'w') as f:
        #     f.write(f'{cil_ast}')

    
