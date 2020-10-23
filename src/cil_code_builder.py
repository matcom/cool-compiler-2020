import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILCodeBuilder:
    def __init__(self, cil_ast, context):
        self.cil_ast = cil_ast
        self.context = context
        
    def build_entry_function(self, cool_ast):
        locals, body = [], []
        for attr_locals,_,_ in self.class_attributes["Main"].values():
            locals += attr_locals
        
        result = CIL_AST.LocalDec('result')
        instance = CIL_AST.LocalDec('instance')
        locals += [result, instance]

        allocate = CIL_AST.Allocate('Main')
        assign_instance = CIL_AST.Assign(instance.name, allocate)
        body.append(assign_instance)

        for attr, data in self.class_attributes["Main"].items():
            _, attr_body, attr_value = data
            if attr_value:
                setAttr = CIL_AST.SetAttr(instance.name, attr, attr_value)
                body += attr_body
                body.append(setAttr)

        arg = CIL_AST.Arg(instance.name)
        vcall = CIL_AST.VCall('Main', 'Main', 'main', 1)
        assign_result = CIL_AST.Assign(result.name, vcall)
        ret = CIL_AST.Return(0)
        
        body += [arg, assign_result, ret]

        entry_funtion = CIL_AST.Function("entry", [], locals, body)
        self.cil_ast.code.insert(0, entry_funtion)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(COOL_AST.Program)
    def visit(self, node):
        self.class_attributes = { type: {} for type in self.context.types.keys()}
        for klass in node.classes:
            self.visit(klass)
        
        self.build_entry_function(node)

    @visitor.when(COOL_AST.Class)
    def visit(self, node):
        self.expr_value_number = 0
        for feature in node.features:
            self.scope_depth = 0
            self.visit(feature, node.name)
    
    @visitor.when(COOL_AST.ClassMethod)
    def visit(self, node, self_type):
        self.params_names = [f'{param.name}_{self.scope_depth}' for param in node.params]
        params = [CIL_AST.ParamDec('self')] + [CIL_AST.ParamDec(param) for param in self.params_names]
        
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
        self.class_attributes[self_type][local.name] = expr_locals + [local], expr_code, expr_value 
    
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
        load = CIL_AST.Load(self.cil_ast.data[node.value])
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
        var_name = f'{node.name}{self.scope_depth}'
        expr_locals, expr_code, expr_value = self.visit(node.expr, self_type)
        assign = var_name in self.params_names and \
                    CIL_AST.Assign(var_name, expr_value) or \
                    CIL_AST.SetAttr('self', var_name, expr_value)

        return expr_locals, expr_code + [assign], None

    @visitor.when(COOL_AST.DynamicCall)
    def visit(self, node, self_type):
        inst_locals, inst_code, inst_value = self.visit(node.instance, self_type)
        instance_type = inst_value == 'self' and self_type

        if isinstance(node.instance, COOL_AST.Identifier) and instance_type != self_type:
            instance_type = next(attr.type.name for attr in self.context.types[self_type].attributes if attr.name == node.instance.name)

        instance_type = instance_type or node.instance.type        

        local = CIL_AST.LocalDec(f'expr_value_{self.expr_value_number}')
        self.expr_value_number += 1
        args = [CIL_AST.Arg(inst_value)] + [CIL_AST.Arg(arg.name) for arg in node.args]
        virtual_type = next(m.virtual_type for m in self.cil_ast.types[instance_type].methods if m.name == node.method)
        vcall = CIL_AST.VCall(instance_type, virtual_type, node.method, len(node.args))
        assign = CIL_AST.Assign(local.name, vcall)

        return inst_locals + [local], inst_code + args + [assign], local.name      


    @visitor.when(COOL_AST.NewType)
    def visit(self, node, self_type):
        local = CIL_AST.LocalDec(f'expr_value_{self.expr_value_number}')
        self.expr_value_number += 1
        allocate = CIL_AST.Allocate(node.type)
        assign = CIL_AST.Assign(local.name, allocate)

        locals, body = [local], [assign]
        for attr, data in self.class_attributes[allocate.type].items():
            attr_locals, attr_body, attr_value = data
            locals += attr_locals
            if attr_value:
                setAttr = CIL_AST.SetAttr(local.name, attr, attr_value)
                body += attr_body
                body.append(setAttr)
        
        return locals, body, local.name
    
    @visitor.when(COOL_AST.Identifier)
    def visit(self, node, self_type):
        return [], [], f'{node.name}_{self.scope_depth}'
    
    @visitor.when(COOL_AST.SELF)
    def visit(self, node, self_type):
        return [], [], 'self'