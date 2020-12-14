import sys
sys.path.append('/..')
from code_generation import *
from semantic.context import *
from semantic.features import *
from semantic.types import *
import visitors.visitor as visitor
from cl_ast import *

class ScopeCIL:
    def __init__(self, parent=None):
        self.locals = []
        self.cil_locals = {}
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = ScopeCIL(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def define_cil_local(self, vname, cilname, vtype = None):
        self.define_variable(vname, vtype)
        self.cil_locals[vname] = cilname
        
    
    def get_cil_local(self, vname):
        if self.cil_locals.__contains__(vname):
            return self.cil_locals[vname]
        else: 
            return None
    
    def find_cil_local(self, vname, index=None):
        locals = self.cil_locals.items() if index is None else itt.islice(self.cil_locals.items(), index)
        try:
            return next(cil_name for name, cil_name in locals if name == vname)
        except StopIteration:
            return self.parent.find_cil_local(vname, self.index) if (self.parent is not None) else None

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(
            self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if (self.parent is not None) else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_defined_cil_local(self, vname):
        return self.find_cil_local(vname ) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def remove_local(self, vname):
        self.locals = [local for local in self.locals if local.name != vname]

class codeVisitor:

    def __init__(self, context):
        self.dottypes = {}
        self.dotdata = {}
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        self.label_count = 0
        self.count = ''
        # self.scope = scope
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
        param_node = ParamNodeIL(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def is_defined_param(self, name):
        for p in self.params:
            if p.name == name:
                return True
        return False
    
    def register_local(self, var_name):
        local_node = LocalNodeIL(var_name)
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
        function_node = FunctionNodeIL(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = TypeNodeIL(name)
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
        self.register_instruction(ReturnNodeIL(None))

        #abort
        self.current_function = self.register_function(self.to_function_name('abort', 'Object'))
        self.register_param(VariableInfo('self',None))
        msg = self.define_internal_local(scope=scope, name="msg")
        key_msg = ''
        for s in self.dotdata.keys():
            if self.dotdata[s] == 'Abort called from class ':
                key_msg = s
        self.register_instruction(LoadNodeIL(key_msg, msg))
        self.register_instruction(OutStringNodeIL(msg))
        type_name = self.define_internal_local(scope=scope, name = "type_name" )
        self.register_instruction(TypeOfNodeIL('self', type_name))
        self.register_instruction(OutStringNodeIL(type_name))
        eol_local = self.define_internal_local(scope=scope, name="eol")
        for s in self.dotdata.keys():
            if self.dotdata[s] == '\n':
                eol = s
        self.register_instruction(LoadNodeIL(eol, eol_local))
        self.register_instruction(OutStringNodeIL(eol_local))
        self.register_instruction(HaltNodeIL())

        #type_name
        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'))
        self.register_param(VariableInfo('self', None))
        type_name = self.define_internal_local(scope=scope, name = "type_name" )
        self.register_instruction(TypeOfNodeIL('self', type_name))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('String',self.context.get_type('String').tag ,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'String_init', [ArgNodeIL(type_name),ArgNodeIL(instance)],"String"))
        self.register_instruction(ReturnNodeIL(instance))

        #copy
        self.current_function = self.register_function(self.to_function_name('copy', 'Object'))
        self.register_param(VariableInfo('self',None))
        copy = self.define_internal_local(scope=scope, name= "copy")
        self.register_instruction(CopyNodeIL('self', copy))
        self.register_instruction(ReturnNodeIL(copy))

        #----------------IO---------------------
        #init
        self.current_function = self.register_function('IO_init')
        self.register_param(VariableInfo('self', None))
        self.register_instruction(ReturnNodeIL(None))        

        #out_string
        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        v = self.define_internal_local(scope=scope, name="v")
        self.register_instruction(GetAttribNodeIL(v, 'x','value','String'))
        self.register_instruction(OutStringNodeIL(v))
        self.register_instruction(ReturnNodeIL('self'))

        #out_int
        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        v = self.define_internal_local(scope=scope, name="v")
        self.register_instruction(GetAttribNodeIL(v, 'x','value','Int'))
        self.register_instruction(OutIntNodeIL(v))
        self.register_instruction(ReturnNodeIL('self'))

        #in_string
        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        msg = self.define_internal_local(scope=scope, name="read_str")
        self.register_instruction(ReadStringNodeIL(msg))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('String',self.context.get_type('String').tag ,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'String_init', [ArgNodeIL(msg),ArgNodeIL(instance)],"String"))
        self.register_instruction(ReturnNodeIL(instance))
    
        #in_int
        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        number = self.define_internal_local(scope=scope, name ="read_int")
        self.register_instruction(ReadIntNodeIL(number))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('Int', self.context.get_type('Int').tag,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Int_init', [ ArgNodeIL(number), ArgNodeIL(instance)], "Int"))
        self.register_instruction(ReturnNodeIL(instance))

        # ----------------String---------------------
        #init
        self.current_function=self.register_function('String_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(SetAttribNodeIL('self', 'value', 'v', 'String'))
        self.register_instruction(ReturnNodeIL(None))   

        #length
        self.current_function = self.register_function(self.to_function_name('length', 'String'))
        self.register_param(VariableInfo('self', None))
        length_result = self.define_internal_local(scope=scope, name="length")
        self.register_instruction(LengthNodeIL('self', length_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('Int', self.context.get_type('Int').tag,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init,'Int_init', [ArgNodeIL(length_result),ArgNodeIL(instance)], "Int"))
        self.register_instruction(ReturnNodeIL(instance))

        #concat
        self.current_function = self.register_function(self.to_function_name('concat', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('s', None))

        str1 = self.define_internal_local(scope=scope, name="str1")
        self.register_instruction(GetAttribNodeIL(str1, 'self','value','String'))
        len1 = self.define_internal_local(scope=scope, name="len1")
        self.register_instruction(StaticCallNodeIL(len1, 'String.length', [ArgNodeIL('self')], 'String'))

        str2 = self.define_internal_local(scope=scope, name="str2")
        self.register_instruction(GetAttribNodeIL(str2, 's', 'value', 'String'))
        len2 = self.define_internal_local(scope=scope, name="len2")
        self.register_instruction(StaticCallNodeIL(len2, 'String.length', [ArgNodeIL('s')], 'String'))

        local_len1 = self.define_internal_local(scope=scope, name="local_len1")
        self.register_instruction(GetAttribNodeIL(local_len1, len1, 'value', 'Int'))
        local_len2 = self.define_internal_local(scope=scope, name="local_len2")
        self.register_instruction(GetAttribNodeIL(local_len2, len2, 'value', 'Int'))

        concat_result = self.define_internal_local(scope=scope, name="concat")
        self.register_instruction(ConcatNodeIL(str1, local_len1, str2, local_len2, concat_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('String',self.context.get_type('String').tag ,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'String_init', [ArgNodeIL(concat_result), ArgNodeIL(instance)],"String"))
        self.register_instruction(ReturnNodeIL(instance))
        
    
        #substr
        self.current_function = self.register_function(self.to_function_name('substr', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        i_value=self.define_internal_local(scope=scope, name="i_value")
        self.register_instruction(GetAttribNodeIL(i_value, 'i','value','Int'))
        l_value = self.define_internal_local(scope=scope, name="l_value")
        self.register_instruction(GetAttribNodeIL(l_value, 'l','value','Int'))
        subs_result=self.define_internal_local(scope=scope, name="subs_result")
        self.register_instruction(SubstringNodeIL(i_value, l_value, 'self', subs_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('String', self.context.get_type('String').tag,instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'String_init', [ArgNodeIL(subs_result),ArgNodeIL(instance)],"String"))
        self.register_instruction(ReturnNodeIL(instance))
        
        #----------------Bool---------------------
        #init
        self.current_function=self.register_function('Bool_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(SetAttribNodeIL('self', 'value', 'v', 'Bool'))
        self.register_instruction(ReturnNodeIL(None))
        
        #----------------Int---------------------
        #init
        self.current_function=self.register_function('Int_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(SetAttribNodeIL('self', 'value', 'v', 'Int'))
        self.register_instruction(ReturnNodeIL(None)) 

    def build_string_equals_function(self, scope):
        self.current_function = self.register_function('String_equals')
        self.register_param(VariableInfo('str1', None))
        self.register_param(VariableInfo('str2', None))
        
        str1 = self.define_internal_local(scope=scope, name="str1")
        self.register_instruction(GetAttribNodeIL(str1, 'str1', 'value','String'))
        
        str2 = self.define_internal_local(scope=scope, name="str2")
        self.register_instruction(GetAttribNodeIL(str2, 'str2', 'value', 'String'))
        
        result = self.define_internal_local(scope=scope, name="comparison_result")
        self.register_instruction(StringEqualsNodeIL(str1, str2, result))
        self.register_instruction(ReturnNodeIL(result))

    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope, sscope):
        
        if not scope: 
            scope = ScopeCIL()
            
        self.current_function = self.register_function('main')
        instance = self.define_internal_local(scope = scope, name = "instance")
        result = self.define_internal_local(scope = scope, name = "result")
        self.register_instruction(AllocateNodeIL('Main',self.context.get_type('Main').tag, instance))
        # self.register_instruction(ArgNodeIL(instance))
        self.register_instruction(StaticCallNodeIL(result, 'Main_init', [ArgNodeIL(instance)],"Main"))
        # self.register_instruction(ArgNodeIL(instance))
        self.register_instruction(StaticCallNodeIL(result, self.to_function_name('main', 'Main'), [ArgNodeIL(instance)],"Main"))
        self.register_instruction(ReturnNodeIL(None))
        self.current_function = None

        self.register_data('Abort called from class ')
        self.register_data('\n')
        self.dotdata['empty_str'] = ''
        
        #Add built-in types in .TYPES section
        self.register_builtin_types(scope)

        #Add string equals function
        self.build_string_equals_function(scope)
        
        for klass in node.declarations:
            self.visit(klass, scope.create_child(), sscope.cls_scopes[klass.id])

        return ProgramNodeIL(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(SelfCallNode)
    def visit(self, node, scope, sscope):
        # print(node)
        # print(node.id)
        # print('args:',node.args)
        self.count += 'SelfCall \n-------------------\n'+ node.id + '(' + str(node.args)+')' + '--------\n '
        result_local = self.define_internal_local(scope = scope, name = "result")
        expr_value = 'self'

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope, sscope)
            call_args.append(ArgNodeIL(param_local))
        call_args.append(ArgNodeIL(expr_value))

        # dynamic_type = 'Void'
        self.count += expr_value + '\n'
        self.register_instruction(DynamicCallNodeIL(result_local, node.id, call_args, self.current_type.name, expr_value))
        
        return result_local
    
    @visitor.when(FormalParamNode)
    def visit(self, node, scope, sscope):
        pass
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope, sscope):
        self.current_type = self.context.get_type(node.id)
        
        #Handle all the .TYPE section
        cil_type = self.register_type(self.current_type.name)
        cil_type.attributes = [f'{attr.name}' for c, attr in self.current_type.get_all_attributes()]
        cil_type.methods = {f'{m}':f'{c}.{m}' for c, m  in self.current_type.get_all_methods()}

        scope.define_cil_local("self", self.current_type.name, self.current_type)

        func_declarations = [f for f in node.features if isinstance(f, FuncDeclarationNode)]
        attr_declarations = [a for a in node.features if not isinstance(a, FuncDeclarationNode)]
        for attr in attr_declarations:
            scope.define_cil_local(attr.id, attr.id, node.id)


        #-------------------------Init---------------------------------
        self.current_function = self.register_function(f'{node.id}_init')
        self.register_param(VariableInfo('self', None))
        # instance = self.define_internal_local(scope=scope, name="instance", class_type=self.current_type.name)
        # self.register_instruction(AllocateNodeIL(node.name, self.context.get_type(node.name).name,instance))
        # self.current_type.instance = instance

        #Init parents recursively
        result = self.define_internal_local(scope=scope, name = "result")
        # self.register_instruction(ArgNodeIL('instance'))
        # print('ID: ', node.id)
        # print('Parent: ', node.parent)
        self.register_instruction(StaticCallNodeIL(result, f'{node.parent}_init',[ArgNodeIL('self')], node.parent))
        self.register_instruction(ReturnNodeIL(None))
        print('Class: ', self.current_type.name)
        for attr in attr_declarations:
            print('Attr')
            print('id: ', attr.id)
            print('type:', attr.type)
            self.visit(attr, scope, sscope)
        #---------------------------------------------------------------
        self.current_function = None
        
        for feature in func_declarations:
            self.visit(feature, scope.create_child(), sscope)
                
        self.current_type = None
                
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope, sscope):
        fscope = sscope.func_scopes[node.id]
        # print('func:::: ', node.id)
        self.current_method = self.current_type.get_method(node.id)
        self.dottypes[self.current_type.name].methods[node.id] = f'{self.current_type.name}.{node.id}'
        cil_method_name = self.to_function_name(node.id, self.current_type.name)
        self.current_function = self.register_function(cil_method_name)

        self.register_param(VariableInfo('self', self.current_type))
        for p in node.params:
            self.register_param(VariableInfo(p.id, p.type))
        
        value = self.visit(node.body, scope, fscope)

        self.register_instruction(ReturnNodeIL(value)) 
        self.current_method = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope, sscope):
        ascope = sscope.attr_scopes[node.id]

        if not node.expr:
            instance = None
            # print('attr_type:::::::::: ', node.type)
            if node.type in ['Int', 'Bool']:
                instance = self.define_internal_local(scope=scope, name="instance")
                self.register_instruction(AllocateNodeIL(node.type,self.context.get_type(node.type).tag, instance))
                value = self.define_internal_local(scope=scope, name="value")
                self.register_instruction(LoadNodeIL(0,value))
                result_init = self.define_internal_local(scope=scope, name="result_init")
                self.register_instruction(StaticCallNodeIL(result_init, f'{node.type}_init', [ ArgNodeIL(value), ArgNodeIL(instance)], node.type))
            elif node.type == 'String':
                instance = self.define_internal_local(scope=scope, name="instance")
                self.register_instruction(AllocateNodeIL(node.type,self.context.get_type(node.type).tag ,instance))
                value = self.define_internal_local(scope=scope, name="value")
                self.register_instruction(LoadNodeIL('empty_str',value))
                result_init = self.define_internal_local(scope=scope, name="result_init")
                self.register_instruction(StaticCallNodeIL(result_init, f'{node.type}_init', [ArgNodeIL(value),ArgNodeIL(instance)], node.type))

            self.register_instruction(SetAttribNodeIL('self', node.id,instance, self.current_type.name))
        else:
            print('attr_type::::IN_______EXPRRRRRR:::::: ', node.type)
            expr = self.visit(node.expr, scope, ascope)
            self.register_instruction(SetAttribNodeIL('self', node.id, expr, self.current_type.name))
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope, sscope):
        print('var_decl: ',node.id)
        expr = self.visit(node.expr, scope, sscope)
        self.register_instruction(SetAttribNodeIL('self', node.name, expr, self.current_type.name))

    @visitor.when(AssignNode)
    def visit(self, node, scope, sscope):
        expr_local = self.visit(node.expr, scope, sscope)
        result_local = self.define_internal_local(scope=scope, name = "result" )
        cil_node_name = scope.find_cil_local(node.id)

        if self.is_defined_param(node.id):
            print('-----------Assign----------------')
            print('-----------expr_local ',expr_local )
            self.register_instruction(AssignNodeIL(node.id, expr_local))
        elif self.current_type.has_attr(node.id):
            cil_type_name = 'self'
            self.register_instruction(SetAttribNodeIL(cil_type_name, node.id, expr_local, self.current_type.name ))
        else:
            print('-----------Assign----------------')
            print('-----------expr_local ', expr_local)
            self.register_instruction(AssignNodeIL(cil_node_name, expr_local))
        return expr_local

    @visitor.when(BlockNode)
    def visit(self, node, scope, sscope):
        for e in node.expr_list:
            result_local = self.visit(e, scope, sscope)
        return result_local

    @visitor.when(VariableNode)
    def visit(self, node, scope, sscope):
        if self.is_defined_param(node.id):
            # print('------------------------------')
            # print('defined PARAM ', node.id)
            return node.id
        elif self.current_type.has_attr(node.id): 
            result_local = self.define_internal_local(scope=scope, name = node.id, class_type=self.current_type.name)
            # self.count += 1
            self.register_instruction(GetAttribNodeIL(result_local, 'self' , node.id, self.current_type.name))
            return result_local
        else:
            return scope.find_cil_local(node.id)
    
    @visitor.when(ConditionalNode)
    def visit(self, node, scope, sscope):
        result_local = self.define_internal_local(scope=scope, name = "result")

        cond_value = self.visit(node.cond, scope, sscope)

        if_then_label = self.get_label()
        self.register_instruction(GotoIfNodeIL(cond_value, if_then_label))

        else_value = self.visit(node.else_stm, scope, sscope)
        print('-----------Cond----------------')
        print('-----------else_value ', else_value)
        self.register_instruction(AssignNodeIL(result_local, else_value))
    
        end_if_label = self.get_label()
        self.register_instruction(GotoNodeIL(end_if_label))

        self.register_instruction(LabelNodeIL(if_then_label))
        then_value = self.visit(node.stm, scope, sscope)
        print('-----------Cond----------------')
        print('-----------then_value ', then_value)
        self.register_instruction(AssignNodeIL(result_local, then_value))
        self.register_instruction(LabelNodeIL(end_if_label))

        return result_local

    @visitor.when(WhileNode)
    def visit(self, node, scope, sscope):
        result_local = self.define_internal_local(scope = scope, name = "result")
        
        loop_init_label = self.get_label()
        loop_body_label = self.get_label()
        loop_end_label = self.get_label()
        self.register_instruction(LabelNodeIL(loop_init_label))
        pred_value = self.visit(node.cond, scope, sscope)
        self.register_instruction(GotoIfNodeIL(pred_value, loop_body_label))
        self.register_instruction(GotoNodeIL(loop_end_label))
        
        self.register_instruction(LabelNodeIL(loop_body_label))
        body_value = self.visit(node.expr, scope, sscope)
        self.register_instruction(GotoNodeIL(loop_init_label))
        self.register_instruction(LabelNodeIL(loop_end_label))

        self.register_instruction(LoadNodeIL(None, result_local))
        return result_local
    
    @visitor.when(ExprCallNode)
    def visit(self, node, scope, sscope):
        self.count += 'ExprCall: \n-------------------\n'+ node.id + '(' + str(node.row) +','+ str(node.col)+')' + '--------\n '
        result_local = self.define_internal_local(scope = scope, name = "result")
        expr_value = self.visit(node.obj, scope, sscope)

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope, sscope)
            call_args.append(ArgNodeIL(param_local))
        call_args.append(ArgNodeIL(expr_value))
        
        # dynamic_type = self.define_internal_local(scope= scope, name="dyn_type")
        # self.register_instruction(TypeOfNodeIL(expr_value, dynamic_type))

        # for arg in call_args:
        #     self.register_instruction(ArgNodeIL(arg))

        dynamic_type = self.context.exprs_dict[node.obj]
        self.count += expr_value + '\n'
        self.register_instruction(DynamicCallNodeIL(result_local, node.id, call_args, dynamic_type.name, expr_value))
        
        return result_local

    @visitor.when(ParentCallNode)
    def visit(self, node, scope, sscope):
        self.count += 'ParentCall \n-------------------\n'+ node.id + '(' + str(node.row) +','+ str(node.col)+')' + '--------\n '
        result_local = self.define_internal_local(scope = scope, name = "result")
        expr_value = self.visit(node.obj, scope, sscope)

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope, sscope)
            call_args.append(ArgNodeIL(param_local))
        call_args.append(ArgNodeIL(expr_value))

        # for p in call_args:
        #     self.register_instruction(ArgNodeIL(p))

        static_instance = self.define_internal_local(scope=scope, name='static_instance')
        self.register_instruction(AllocateNodeIL(node.type,self.context.get_type(node.type).tag ,static_instance))
        self.count += static_instance + '\n'
        self.register_instruction(DynamicCallNodeIL(result_local, node.id, call_args, node.type, static_instance))
        return result_local
        
    @visitor.when(LetNode)
    def visit(self, node, scope, sscope):
        chld_scope = sscope.expr_dict[node]
        iscope = chld_scope

        let_scope = scope.create_child()
        for var in node.init_list:
            self.visit(var, let_scope, iscope)
            iscope = iscope.children[0]
        
        body_value = self.visit(node.expr, let_scope, iscope)
        result_local = self.define_internal_local(scope = scope, name = "let_result")
        print('-----------LET----------------')
        print('-----------body_value ', body_value)

        self.register_instruction(AssignNodeIL(result_local, body_value))
        return result_local
    
    @visitor.when(LetDeclarationNode)
    def visit(self, node, scope, sscope):
        # print(type(node.expr))
        if node.expr != None:
            expr_value = self.visit(node.expr, scope, sscope)
            var_init = self.define_internal_local(scope = scope, name = node.id, cool_var_name= node.id)
            print('-----------LET_Decl----------------')
            print('-----------expr_value ', expr_value)
            self.register_instruction(AssignNodeIL(var_init, expr_value))
            return var_init
        else:
            instance = None

            if node.type in ['Int', 'Bool']:
                instance = self.define_internal_local(scope=scope, name="instance")
                self.register_instruction(AllocateNodeIL(node.type,self.context.get_type(node.type).tag, instance))
                value = self.define_internal_local(scope=scope, name="value")
                self.register_instruction(LoadNodeIL(0,value))
                result_init = self.define_internal_local(scope=scope, name="result_init")
                self.register_instruction(StaticCallNodeIL(result_init, f'{node.type}_init', [ ArgNodeIL(value), ArgNodeIL(instance)], node.type))
            elif node.type == 'String':
                instance = self.define_internal_local(scope=scope, name="instance")
                self.register_instruction(AllocateNodeIL(node.type,self.context.get_type(node.type).tag ,instance))
                value = self.define_internal_local(scope=scope, name="value")
                self.register_instruction(LoadNodeIL('empty_str',value))
                result_init = self.define_internal_local(scope=scope, name="result_init")
                self.register_instruction(StaticCallNodeIL(result_init, f'{node.type}_init', [ArgNodeIL(value), ArgNodeIL(instance)], node.type))
                
            var_def = self.define_internal_local(scope = scope, name = node.id, cool_var_name=node.id)
            self.register_instruction(AssignNodeIL(var_def, instance))
            return var_def
        
    # @visitor.when(COOL_AST.LetVarDef)
    # def visit(self, node, scope):
    #     instance = None

    #     if node.type in ['Int', 'Bool']:
    #         instance = self.define_internal_local(scope=scope, name="instance")
    #         self.register_instruction(AllocateNodeIL(node.type,self.context.get_type(node.type).name, instance))
    #         value = self.define_internal_local(scope=scope, name="value")
    #         self.register_instruction(LoadNodeIL(0,value))
    #         result_init = self.define_internal_local(scope=scope, name="result_init")
    #         self.register_instruction(StaticCallNodeIL(result_init, f'{node.type}_init', [ ArgNodeIL(value), ArgNodeIL(instance)], node.type))
    #     elif node.type == 'String':
    #         instance = self.define_internal_local(scope=scope, name="instance")
    #         self.register_instruction(AllocateNodeIL(node.type,self.context.get_type(node.type).name ,instance))
    #         value = self.define_internal_local(scope=scope, name="value")
    #         self.register_instruction(LoadNodeIL('empty_str',value))
    #         result_init = self.define_internal_local(scope=scope, name="result_init")
    #         self.register_instruction(StaticCallNodeIL(result_init, f'{node.type}_init', [ArgNodeIL(value), ArgNodeIL(instance)], node.type))
            
    #     var_def = self.define_internal_local(scope = scope, name = node.name, cool_var_name=node.name)
    #     self.register_instruction(AssignNodeIL(var_def, instance))
    #     return var_def
    
    
    @visitor.when(CaseNode)
    def visit(self, node, scope, sscope):
        result_local = self.define_internal_local(scope = scope, name = "result")
        case_expr = self.visit(node.expr, scope, sscope)
        print('EXPRRRRRRRR:', type(node.expr))
        nscope = sscope.expr_dict[node]

        exit_label = self.get_label()
        label = self.get_label()

        self.register_instruction(CaseNodeIL(case_expr, label))
        
        tag_lst = []
        option_dict = {}
        for option, c_scp in zip(node.case_list, nscope.children):
            tag = self.context.get_type(option.typex).name
            tag_lst.append( (tag, c_scp) )
            option_dict[tag] = option
        tag_lst.sort()

        for t, c_scp in reversed(tag_lst):
            option = option_dict[t]
            option_type = self.context.get_type(option.typex) 
            self.register_instruction(LabelNodeIL(label))
            label = self.get_label()

            #changes
            # print(option_type.name)
            # if option_type.name != 'Object'
            self.register_instruction(OptionNodeIL(case_expr, option_type.tag, option_type.max_tag, label))

            option_scope = scope.create_child()
            option_id = self.define_internal_local(scope=option_scope, name=option.id, cool_var_name=option.id)
            print('-----------Case----------------')
            print('-----------case_expr ', case_expr)
            self.register_instruction(AssignNodeIL(option_id, case_expr))
            expr_result = self.visit(option.expr, option_scope, c_scp)
            print('-----------Case----------------')
            print('-----------expr_result ', expr_result)
            self.register_instruction(AssignNodeIL(result_local, expr_result))
            self.register_instruction(GotoNodeIL(exit_label))
            
        self.register_instruction(LabelNodeIL(label))
        self.register_instruction(GotoNodeIL('case_no_match_error'))
        self.register_instruction(LabelNodeIL(exit_label))
        return result_local

    @visitor.when(OptionNode)
    def visit(self, node, scope, sscope):
        pass

    @visitor.when(NewNode)
    def visit(self, node, scope, sscope):
        result_local = self.define_internal_local(scope=scope, name="result")
        result_init = self.define_internal_local(scope=scope, name="init")
        
        # print('ID:', node.id)
        print('type:', node.type)

        if node.type == "SELF_TYPE":
            # get_type_local = self.define_internal_local(scope = scope, name = "type_name")
            # self.register_instruction(TypeOfNodeIL("self", get_type_local))
            self.register_instruction(AllocateNodeIL(self.current_type.name,self.current_type.tag ,result_local))
            # self.register_instruction(ArgNodeIL(result_local))
            self.register_instruction(StaticCallNodeIL(result_init, f'{self.current_type.name}_init', [result_local], self.current_type.name))
        else:
            self.register_instruction(AllocateNodeIL(node.type,self.context.get_type(node.type).tag ,result_local))
            # self.register_instruction(ArgNodeIL(result_local))
            self.register_instruction(StaticCallNodeIL(result_init,f'{node.type}_init' ,[ArgNodeIL(result_local)], self.current_type.name ))

        return result_local
        
    @visitor.when(IsVoidNode)
    def visit(self, node, scope, sscope):
        expre_value = self.visit(node.expr, scope, sscope)
        result_local = self.define_internal_local(scope=scope, name ="isvoid_result")
        self.register_instruction(IsVoidNodeIL(result_local, expre_value))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('Bool',self.context.get_type('Bool').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Bool_init', [ArgNodeIL(result_local),ArgNodeIL(instance)], "Bool"))
        return instance
    
    @visitor.when(SumNode)
    def visit(self, node, scope, sscope):
        #self.count += ' +'
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope, sscope)
        right_value = self.visit(node.right, scope, sscope)

        if hasattr(node.left, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.left]))
        else:
            left_type = 'Int'
            if isinstance(node.left, IntegerNode):
                left_type = 'Int'
            elif isinstance(node.left, BoolNode):
                left_type = 'Bool'
            elif isinstance(node.left, StringNode):
                left_type = 'String'
            else:
                try:
                    left_type = (sscope.find_variable(node.left.id)).type.name
                except:
                    left_type = 'Int'
            # #self.count += 1
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", left_type))

        if hasattr(node.right, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.right]))
        else:
            right_type = 'Int'
            if isinstance(node.right, IntegerNode):
                right_type = 'Int'
            elif isinstance(node.right, BoolNode):
                right_type = 'Bool'
            elif isinstance(node.right, StringNode):
                right_type = 'String'
            else:
                try:
                    right_type = (sscope.find_variable(node.right.id)).type.name
                except:
                    right_type = 'Int'
            # #self.count += 1
            self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", right_type))

        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", node.left.computed_type.name))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", node.right.computed_type.name))

        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", None))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", None))

        self.register_instruction(BinaryNodeIL(op_local, left_local, right_local, "+"))

        # Allocate Int result
        self.register_instruction(AllocateNodeIL('Int',self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Int_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Int"))

        return result_local

    @visitor.when(DiffNode)
    def visit(self, node, scope, sscope):
        #self.count += ' -'
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope, sscope)
        right_value = self.visit(node.right, scope, sscope)

        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", node.left.computed_type.name))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", node.right.computed_type.name))

        if hasattr(node.left, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.left]))
        else:
            left_type = 'Int'
            if isinstance(node.left, IntegerNode):
                left_type = 'Int'
            elif isinstance(node.left, BoolNode):
                left_type = 'Bool'
            elif isinstance(node.left, StringNode):
                left_type = 'String'
            else:
                try:
                    left_type = (sscope.find_variable(node.left.id)).type.name
                except:
                    left_type = 'Int'
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", left_type))

        if hasattr(node.right, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.right]))
        else:
            right_type = 'Int'
            if isinstance(node.right, IntegerNode):
                right_type = 'Int'
            elif isinstance(node.right, BoolNode):
                right_type = 'Bool'
            elif isinstance(node.right, StringNode):
                right_type = 'String'
            else:
                try:
                    right_type = (sscope.find_variable(node.right.id)).type.name
                except:
                    right_type = 'Int'
            self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", right_type))

        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", None))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", None))

        self.register_instruction(BinaryNodeIL(op_local, left_local, right_local, "-"))

        # Allocate Int result
        self.register_instruction(AllocateNodeIL('Int',self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Int_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Int"))

        return result_local

    @visitor.when(StarNode)
    def visit(self, node, scope, sscope):
        #self.count += ' *'
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope, sscope)
        right_value = self.visit(node.right, scope, sscope)

        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", node.left.computed_type.name))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", node.right.computed_type.name))

        # if hasattr(node.left, 'expr'):
        #     self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.left]))
        # else:
        #     left_type = 'Int'
        #     if isinstance(node.left, IntegerNode):
        #         left_type = 'Int'
        #     elif isinstance(node.left, BoolNode):
        #         left_type = 'Bool'
        #     elif isinstance(node.left, StringNode):
        #         left_type = 'String'
        #     else:
        #         try:
        #             left_type = (sscope.find_variable(node.left.id)).type.name
        #         except:
        #             left_type = 'Int'
        left_type = self.context.exprs_dict[node.left].name
        right_type = self.context.exprs_dict[node.right].name
        #self.count += f'({left_local},{right_local})'
        self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", left_type))

        # right_type = 'Int'
        # if hasattr(node.right, 'expr'):
        #     if isinstance(node.right.expr, IntegerNode):
        #         right_type = 'Int'
        #     elif isinstance(node.right.expr, BoolNode):
        #         right_type = 'Bool'
        #     elif isinstance(node.right.expr, StringNode):
        #         right_type = 'String'
        #     else:
        #         self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", self.context.exprs_dict[node.right]))
        # else:
        #     if isinstance(node.right, IntegerNode):
        #         right_type = 'Int'
        #     elif isinstance(node.right, BoolNode):
        #         right_type = 'Bool'
        #     elif isinstance(node.right, StringNode):
        #         right_type = 'String'
        #     else:
        #         try:
        #             right_type = (sscope.find_variable(node.right.id)).type.name
        #         except:
        #             right_type = 'Int'
        self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", right_type))
        self.register_instruction(BinaryNodeIL(op_local, left_local, right_local, "*"))

        # Allocate Int result
        self.register_instruction(AllocateNodeIL('Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Int_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Int"))

        return result_local

    @visitor.when(DivNode)
    def visit(self, node, scope, sscope):
        #self.count += ' /'
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope, sscope)
        right_value = self.visit(node.right, scope, sscope)

        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", node.left.computed_type.name))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", node.right.computed_type.name))

        if hasattr(node.left, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.left]))
        else:
            left_type = 'Int'
            if isinstance(node.left, IntegerNode):
                left_type = 'Int'
            elif isinstance(node.left, BoolNode):
                left_type = 'Bool'
            elif isinstance(node.left, StringNode):
                left_type = 'String'
            else:
                try:
                    left_type = (sscope.find_variable(node.left.id)).type.name
                except:
                    left_type = 'Int'
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", left_type))

        if hasattr(node.right, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.right]))
        else:
            right_type = 'Int'
            if isinstance(node.right, IntegerNode):
                right_type = 'Int'
            elif isinstance(node.right, BoolNode):
                right_type = 'Bool'
            elif isinstance(node.right, StringNode):
                right_type = 'String'
            else:
                try:
                    right_type = (sscope.find_variable(node.right.id)).type.name
                except:
                    right_type = 'Int'
            self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", right_type))

        self.register_instruction(BinaryNodeIL(op_local, left_local, right_local, "/"))

        # Allocate Int result
        self.register_instruction(AllocateNodeIL('Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Int_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Int"))

        return result_local

    @visitor.when(BitNotNode)
    def visit(self, node, scope, sscope):
        #self.count += ' ~'
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        expr_local = self.define_internal_local(scope=scope) 
        
        expr_value = self.visit(node.expr, scope, sscope)
        
        # self.register_instruction(GetAttribNodeIL(expr_local, expr_value, "value", node.expr.computed_type.name))
        if hasattr(node, 'expr') and (not isinstance(node.expr, VariableNode)):
            typeX = 'Int'
            if isinstance(node, SelfCallNode):
                typeX = self.current_type.name
            else:
                try:
                    typeX = self.context.exprs_dict[node.expr].name
                except:
                    typeX = 'Int'
            # #self.count += 1
            self.register_instruction(GetAttribNodeIL(expr_local, expr_value, "value", typeX))
        else:
            right_type = 'Int'
            if isinstance(node.expr, IntegerNode):
                right_type = 'Int'
            elif isinstance(node.expr, BoolNode):
                right_type = 'Bool'
            elif isinstance(node.expr, StringNode):
                right_type = 'String'
            else:
                try:
                    right_type = (sscope.find_variable(node.expr.id)).type.name
                except:
                    right_type = 'Int'
            # #self.count += 1
            self.register_instruction(GetAttribNodeIL(expr_local, expr_value, "value", right_type))
        self.register_instruction(UnaryNodeIL(op_local, expr_local, "~"))

        # Allocate Int result
        self.register_instruction(AllocateNodeIL('Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Int_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Int"))

        return result_local
        
    @visitor.when(NotNode)
    def visit(self, node, scope, sscope):
        #self.count += ' !'
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        expr_local = self.define_internal_local(scope=scope) 
        
        expr_value = self.visit(node.expr, scope, sscope)
        
        # self.register_instruction(GetAttribNodeIL(expr_local, expr_value, "value", node.expr.computed_type.name))
        if hasattr(node, 'expr') and (not isinstance(node.expr, VariableNode)):
            typeX = 'Int'
            if isinstance(node, SelfCallNode):
                typeX = self.current_type.name
            else:
                try:
                    typeX = self.context.exprs_dict[node.expr].name
                except:
                    typeX = 'Int'
            self.register_instruction(GetAttribNodeIL(expr_local, expr_value, "value", typeX))
        else:
            self.register_instruction(GetAttribNodeIL(expr_local, expr_value, "value", (sscope.find_variable(node.expr.id)).type.name))
        self.register_instruction(UnaryNodeIL(op_local, expr_local, "not"))

        # Allocate Bool result
        self.register_instruction(AllocateNodeIL('Bool',self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Bool_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Bool"))

        return result_local

    @visitor.when(LessNode)
    def visit(self, node, scope, sscope):
        #self.count += ' <'
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope, sscope)
        right_value = self.visit(node.right, scope, sscope)

        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", node.left.computed_type.name))
        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", None))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", node.right.computed_type.name))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", None))

        if hasattr(node.left, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.left].name))
        else:
            left_type = 'Int'
            if isinstance(node.left, IntegerNode):
                left_type = 'Int'
            elif isinstance(node.left, BoolNode):
                left_type = 'Bool'
            elif isinstance(node.left, StringNode):
                left_type = 'String'
            else:
                try:
                    left_type = (sscope.find_variable(node.left.id)).type.name
                except:
                    left_type = 'Int'
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", left_type))

        if hasattr(node.right, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.right].name))
        else:
            right_type = 'Int'
            if isinstance(node.right, IntegerNode):
                right_type = 'Int'
            elif isinstance(node.right, BoolNode):
                right_type = 'Bool'
            elif isinstance(node.right, StringNode):
                right_type = 'String'
            else:
                try:
                    right_type = (sscope.find_variable(node.right.id)).type.name
                except:
                    right_type = 'Int'
            self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", right_type))

        self.register_instruction(BinaryNodeIL(op_local, left_local, right_local, "<"))

        # Allocate Bool result
        self.register_instruction(AllocateNodeIL('Bool',self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Bool_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Bool"))

        return result_local

    @visitor.when(LessEqualNode)
    def visit(self, node, scope, sscope):
        #self.count += ' <='
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")

        left_value = self.visit(node.left, scope, sscope)
        right_value = self.visit(node.right, scope, sscope)

        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", node.left.computed_type.name))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", node.right.computed_type.name))

        # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", None))
        # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", None))

        if hasattr(node.left, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.left].name))
        else:
            left_type = 'Int'
            if isinstance(node.left, IntegerNode):
                left_type = 'Int'
            elif isinstance(node.left, BoolNode):
                left_type = 'Bool'
            elif isinstance(node.left, StringNode):
                left_type = 'String'
            else:
                try:
                    left_type = (sscope.find_variable(node.left.id)).type.name
                except:
                    left_type = 'Int'
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", left_type))

        if hasattr(node.right, 'expr'):
            self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.right].name))
        else:
            right_type = 'Int'
            if isinstance(node.right, IntegerNode):
                right_type = 'Int'
            elif isinstance(node.right, BoolNode):
                right_type = 'Bool'
            elif isinstance(node.right, StringNode):
                right_type = 'String'
            else:
                try:
                    right_type = (sscope.find_variable(node.right.id)).type.name
                except:
                    right_type = 'Int'
            self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", right_type))

        self.register_instruction(BinaryNodeIL(op_local, left_local, right_local, "<="))

        # Allocate Bool result
        self.register_instruction(AllocateNodeIL('Bool',self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Bool_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Bool"))

        return result_local

    @visitor.when(EqualNode)
    def visit(self, node, scope, sscope):
        #self.count += ' =='
        # print('----got in equalss----')
        # print(node)
        result_local = self.define_internal_local(scope=scope, name = "result")
        op_local = self.define_internal_local(scope=scope, name = "op")
        left_local = self.define_internal_local(scope=scope, name = "left")
        right_local = self.define_internal_local(scope=scope, name = "right")
        # print('left: ', left_local)

        left_value = self.visit(node.left, scope, sscope)
        right_value = self.visit(node.right, scope, sscope)
        # print('res_local: ', result_local)
        # print('op_local: ', op_local)
        # print('left_local: ', left_local)
        # print('right_local: ', right_local)
        # print('left: ', node.left)
        # print('left_value: ',left_value)
        # print('right: ', node.right)
        # print('right_value: ',right_value)
        # print('Got here')
        left_type = self.context.exprs_dict[node.left].name
        right_type = self.context.exprs_dict[node.right].name
        # if hasattr(node.left, 'expr'):
        #     left_type = self.context.exprs_dict[node.left.expr].name
        # else:
        #     left_type = 'Int'
        #     if isinstance(node.left, IntegerNode):
        #         left_type = 'Int'
        #     elif isinstance(node.left, BoolNode):
        #         left_type = 'Bool'
        #     elif isinstance(node.left, StringNode):
        #         left_type = 'String'
        #     else:
        #         try:
        #             left_type = (sscope.find_variable(node.left.id)).type.name
        #         except:
        #             left_type = 'Int'
            # left_type = (sscope.find_variable(node.left.id)).type.name.name
        # if hasattr(node.right, 'expr'):
        #     right_type = self.context.exprs_dict[node.right.expr].name
        # else:
        #     right_type = (sscope.find_variable(node.right.id)).type.name.name

        # if isinstance(node.left, StringNode) and isinstance(node.right, StringNode):
        print('----left_type ', left_type)
        print('----right_type,', right_type)
        print(node.left)
        print(node.right)
        if left_type == 'String':
            self.register_instruction(StaticCallNodeIL(op_local, 'String_equals', [ArgNodeIL(right_value), ArgNodeIL(left_value)], 'String'))
            print('Got string equals')

            # Allocate Bool result
            self.register_instruction(AllocateNodeIL('Bool',self.context.get_type('Bool').tag, result_local))
            result_init = self.define_internal_local(scope=scope, name="result_init")
            self.register_instruction(StaticCallNodeIL(result_init, 'Bool_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Bool"))

            return result_local

        # elif (isinstance(node.left, IntegerNode) and isinstance(node.right, IntegerNode)) or (isinstance(node.left, BoolNode) and isinstance(node.right, BoolNode)):
        elif left_type in ['Int', 'Bool']:
            # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", node.left.computed_type.name))
            # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", node.right.computed_type.name))
            # self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", None))
            # self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", None))
            if hasattr(node.left, 'expr'):
                self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.left].name))
            else:
                left_type = 'Int'
                if isinstance(node.left, IntegerNode):
                    left_type = 'Int'
                elif isinstance(node.left, BoolNode):
                    left_type = 'Bool'
                elif isinstance(node.left, StringNode):
                    left_type = 'String'
                else:
                    try:
                        left_type = (sscope.find_variable(node.left.id)).type.name
                    except:
                        left_type = 'Int'
                self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", left_type))

            if hasattr(node.right, 'expr'):
                self.register_instruction(GetAttribNodeIL(left_local, left_value, "value", self.context.exprs_dict[node.right].name))
            else:
                right_type = 'Int'
                if isinstance(node.right, IntegerNode):
                    right_type = 'Int'
                elif isinstance(node.right, BoolNode):
                    right_type = 'Bool'
                elif isinstance(node.right, StringNode):
                    right_type = 'String'
                else:
                    try:
                        right_type = (sscope.find_variable(node.right.id)).type.name
                    except:
                        right_type = 'Int'
                self.register_instruction(GetAttribNodeIL(right_local, right_value, "value", right_type))
        else:
            print('---------Equal------')
            print('-----------left_value ', left_value)
            print('-----------right_value ', right_value)
            self.register_instruction(AssignNodeIL(left_local, left_value))
            self.register_instruction(AssignNodeIL(right_local, right_value))

        self.register_instruction(BinaryNodeIL(op_local, left_local, right_local, "="))

        # Allocate Bool result
        self.register_instruction(AllocateNodeIL('Bool',self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Bool_init', [ArgNodeIL(op_local), ArgNodeIL(result_local)], "Bool"))

        return result_local

    @visitor.when(ConstantNode)
    def visit(self, node, scope, sscope):
        if self.is_defined_param(node.lex):
            return node.lex
        elif self.current_type.has_attr(node.lex): 
            result_local = self.define_internal_local(scope=scope, name = node.lex, class_type=self.current_type.name)
            self.register_instruction(GetAttribNodeIL(result_local, 'self' , node.lex, self.current_type.name))
            return result_local
        else:
            return scope.find_cil_local(node.lex)
    
    @visitor.when(IntegerNode)
    def visit(self, node, scope, sscope):
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('Int',self.context.get_type('Int').tag, instance))
        value = self.define_internal_local(scope=scope, name="value")
        self.register_instruction(LoadNodeIL(node.lex,value))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Int_init', [ArgNodeIL(value),ArgNodeIL(instance)], "Int"))
        return instance

    @visitor.when(StringNode)
    def visit(self, node, scope, sscope):
        str_name = ""
        for s in self.dotdata.keys():
            if self.dotdata[s] == node.lex:
                str_name = s
                break
        if str_name == "":
            str_name = self.register_data(node.lex)

        result_local = self.define_internal_local(scope=scope)
        self.register_instruction(LoadNodeIL(str_name, result_local))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('String',self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'String_init', [ArgNodeIL(result_local),ArgNodeIL(instance)], "String"))
        return instance
        
    @visitor.when(BoolNode)
    def visit(self, node, scope, sscope):
        boolean = 0
        if str(node.lex) == "True":
            boolean = 1
        # print('booolean--------------- ', node.lex)
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(AllocateNodeIL('Bool',self.context.get_type('Bool').tag, instance))
        value = self.define_internal_local(scope=scope, name="value")
        self.register_instruction(LoadNodeIL(boolean, value))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(StaticCallNodeIL(result_init, 'Bool_init', [ArgNodeIL(value),ArgNodeIL(instance)], "Bool"))
        return instance


def get_formatter():
    
    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNodeIL)
        def visit(self, node):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes.values())
            dotdata = '\n'.join(f'{t}: {node.dotdata[t]}' for t in node.dotdata.keys())
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(TypeNodeIL)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x} : {node.methods[x]}' for x in node.methods.keys())

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(FunctionNodeIL)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

        @visitor.when(ParamNodeIL)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalNodeIL)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(AssignNodeIL)
        def visit(self, node):
            return f'{node.dest} = {node.source}'

        @visitor.when(GotoIfNodeIL)
        def visit(self, node):
            return f'IF {node.cond} GOTO {node.label}'
        
        @visitor.when(LabelNodeIL)
        def visit(self, node):
            return f'LABEL {node.label}'
        
        @visitor.when(GotoNodeIL)
        def visit(self, node):
            return f'GOTO {node.label}'

        @visitor.when(UnaryNodeIL)
        def visit(self, node):
            return f'{node.dest} = {node.op} {node.expr}'

        @visitor.when(BinaryNodeIL)
        def visit(self, node):
            return f'{node.dest} = {node.left} {node.op} {node.right}'

        @visitor.when(AllocateNodeIL)
        def visit(self, node):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(LoadNodeIL)
        def visit(self, node):
            return f'{node.dest} = LOAD {node.msg}'

        # @visitor.when(LoadInt)
        # def visit(self, node):
        #     return f'{node.local_dest} = LOAD {node.num}'

        # @visitor.when(LoadVoid)
        # def visit(self, node):
        #     return f'{node.local_dest} = LOAD VOID'

        @visitor.when(GetAttribNodeIL)
        def visit(self, node):
            return f'{node.dest} = GetAttr {node.obj} {node.attr} '

        @visitor.when(SetAttribNodeIL)
        def visit(self, node):
            return f'SetAttr {node.obj} {node.attr} {node.value}'


        @visitor.when(TypeOfNodeIL)
        def visit(self, node):
            return f'{node.dest} = TYPEOF {node.obj}'

        @visitor.when(StaticCallNodeIL)
        def visit(self, node):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(DynamicCallNodeIL)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.type} {node.method} '

        @visitor.when(ArgNodeIL)
        def visit(self, node):
            return f'ARG {node.arg}'

        @visitor.when(ReturnNodeIL)
        def visit(self, node):
            return f'\n RETURN {node.value if node.value is not None else ""}'

        @visitor.when(IsVoidNodeIL)
        def visit(self, node):
            return f'{node.result_local} ISVOID {node.expre_value}'

        @visitor.when(HaltNodeIL)
        def visit(self, node):
            return 'HALT'
        
        @visitor.when(CopyNodeIL)
        def visit(self, node):
            return f'{node.dest} = COPY {node.source}'

        @visitor.when(LengthNodeIL)
        def visit(self, node):
            return f'{node.dest} = LENGTH {node.arg}'

        @visitor.when(ConcatNodeIL)
        def visit(self, node):
            return f'{node.dest} = CONCAT {node.arg1}  {node.arg2}'

        @visitor.when(SubstringNodeIL)
        def visit(self, node):
            return f'{node.dest} = SUBSTR {node.begin}  {node.end}  {node.word}'
        
        @visitor.when(StringEqualsNodeIL)
        def visit(self, node):
            return f'{node.result} = {node.s1} = {node.s2}'

        @visitor.when(ReadStringNodeIL)
        def visit(self, node):
            return f'{node.dest} = READ STR'

        @visitor.when(ReadIntNodeIL)
        def visit(self, node):
            return f'{node.dest} = READ INT'

        @visitor.when(OutStringNodeIL)
        def visit(self, node):
            return f'PRINT_STR {node.value}'

        @visitor.when(OutIntNodeIL)
        def visit(self, node):
            return f'PRINT_INT {node.value}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))