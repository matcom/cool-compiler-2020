import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILCodeBuilder:
    def __init__(self, cil_ast, context):
        self.cil_ast = cil_ast
        self.context = context
        
    def build_entry_function(self, cool_ast):
        main = next(cil_type for cil_type in self.cil_ast.types if cil_type.name == 'Main')
        locals = [CIL_AST.LocalDec(f'l_{attr.name}') for attr in main.attributes]
        locals.append(CIL_AST.LocalDec('inst_Main'))
        locals.append(CIL_AST.LocalDec('result'))

        # self.types_initializer.visit(cool_ast)
            
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(COOL_AST.Program)
    def visit(self, node):
        self.build_entry_function(node)
        cil_object_type = next(cil_type for cil_type in self.cil_ast.types if cil_type.name == 'Object')
        cil_IO_type = next(cil_type for cil_type in self.cil_ast.types if cil_type.name == 'IO')
        
        self.class_attributes = { type: {} for type in self.context.types.keys()}
        for klass in node.classes:
            self.visit(klass)
    
    @visitor.when(COOL_AST.Class)
    def visit(self, node):
        for feature in node.features:
            self.scope_depth = 0
            self.expr_value_number = 0
            self.visit(feature, node.name)
    
    @visitor.when(COOL_AST.ClassMethod)
    def visit(self, node, self_type):
        params_names = [f'{param.name}{self.scope_depth}' for param in node.params]
        params = [CIL_AST.ParamDec('self')] + [CIL_AST.ParamDec(param) for param in params_names]
        
        # locals = [local for local in self.class_locals if local.name not in params_names]
        
        locals, body, return_value = self.visit(node.expr, self_type)

        func_name = f'func_{self_type}_{node.name}'
        # function = CIL_AST.Function(func_name, params, locals + expr_locals, body)
        function = CIL_AST.Function(func_name, params, locals, body)
        self.cil_ast.code.append(function)
    
    @visitor.when(COOL_AST.AttributeDef)
    def visit(self, node, self_type):
        local = CIL_AST.LocalDec(f'{node.name}_{self.scope_depth}')
        # value = node.type in ['Int', 'Bool']  and 0
        self.class_attributes[self_type][local.name] = [local], [], None

    @visitor.when(COOL_AST.AttributeInit)
    def visit(self, node, self_type):
        local = CIL_AST.LocalDec(f'{node.name}_{self.scope_depth}')
        expr_locals, expr_code, expr_value = self.visit(node.expr, self_type)
        self.class_attributes[local.name] = expr_locals + [local], expr_code, expr_value 
    
    @visitor.when(COOL_AST.INTEGER)
    def visit(self, node, self_type):
        local = CIL_AST.LocalDec(f'expr_value_{self.expr_value_number}')
        self.expr_value_number += 1
        value = CIL_AST.INTEGER(node.value)
        assign = CIL_AST.Assign(local.name, value)
        return [local], [assign], local.name
    
    @visitor.when(COOL_AST.Boolean)
    def visit(self, node, self_type):
        local = CIL_AST.LocalDec(f'expr_value_{self.expr_value_number}')
        self.expr_value_number += 1
        assign = CIL_AST.Assign(local.name, node.value == 'true' and 1 or 0)
        return [local], [assign], local.name

    @visitor.when(COOL_AST.STRING)
    def visit(self, node, self_type):
        local = CIL_AST.LocalDec(f'expr_value_{self.expr_value_number}')
        self.expr_value_number += 1
        load = CIL_AST.Load(self.code[node.value])
        assign = CIL_AST.Assign(local.name, load)
        return [local], [assign], local.name
    
    @visitor.when(COOL_AST.Block)
    def visit(self, node, self_type):
        expr_locals, expr_code, expr_value = [], [], None
        for expr in node.exprs:
            locals, code, expr_value = self.visit(expr, self_type)
            expr_locals += locals
            expr_code += code

        return expr_locals, expr_code, expr_value
    
    @visitor.when(COOL_AST.AssignExpr)
    def visit(self, node, self_type):
        var_name = f'{node.name.name}{self.scope_depth}'
        expr_locals, expr_code, expr_value = self.visit(node.expr, self_type)
        assign = CIL_AST.Assign(var_name, expr_value)
        if isinstance(node.expr, COOL_AST.DynamicCall) or \
           isinstance(node.expr, COOL_AST.StaticCall):
           assign = CIL_AST.Assign(var_name, expr_code[-1])
           return expr_locals, expr_code[:-1] + [assign], None
        
        # code = expr_code + [assign] 

        return expr_locals, expr_code + [assign], None

    @visitor.when(COOL_AST.DynamicCall)
    def visit(self, node, self_type):
        instance_type = self.visit(node.instance, self_type)
        if isinstance(node.instance, COOL_AST.Identifier) and instance_type != self_type:
            instance_type = next(attr.type.name for attr in self.context.types[self_type].attributes if attr.name == node.instance.name)
        
        args = [CIL_AST.Arg(arg) for arg in node.args]

        vcall_assign = CIL_AST.VCall(instance_type, node.method, len(node.args))

        return [], args + vcall_assign, vcall_assign        


    @visitor.when(COOL_AST.NewType)
    def visit(self, node, self_type):
        return node.type
    
    @visitor.when(COOL_AST.Identifier)
    def visit(self, node, self_type):
        return node.name
    
    @visitor.when(COOL_AST.SELF)
    def visit(self, node, self_type):
        return self_type