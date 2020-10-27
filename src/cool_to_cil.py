from cil_types_collector import CILTypesCollector
from cil_data_collector import CILDataCollector
from cil_code_builder import CILCodeBuilder
from semantic import Scope, VariableInfo
import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

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
    
    @property
    def labels(self):
        return self.current_function.labels

    def register_param(self, vinfo):
        # vinfo.name = f'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        param_node = CIL_AST.ParamDec(vinfo.name)
        self.params.append(param_node)
        return vinfo.name
    
    def register_local(self, vinfo):
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = CIL_AST.LocalDec(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def register_label(self, expre_name):
        label_name = f'LABEL_{expre_name}_{len(self.labels)}'
        label_node = CIL_AST.Label(label_name)
        self.labels.append(label_node)
        return label_name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

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
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node
    
    def register_builtin_types(self):
        for t in ['Object', 'Int', 'String', 'Bool', 'IO']:
            builtin_type = self.context.get_type(t)
            cil_type = self.register_type(t)
            cil_type.attributes = [attr.name for attr in builtin_type.attributes]
            cil_type.methods = [(method, self.to_function_name(method, kclass)) for kclass, method  in builtin_type.get_all_methods()]
        
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
        self.register_instruction(CIL_AST.Call(self.to_function_name('main', 'Main'), result))
        self.register_instruction(CIL_AST.Return(0))
        self.current_function = None

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
        cil_type.attributes = [attr.name for attr in self.current_type.attributes]
        cil_type.methods = [(method, self.to_function_name(method, kclass)) for kclass, method  in self.current_type.get_all_methods()]
        
        func_declarations = (f for f in node.features if isinstance(f, COOL_AST.ClassMethod))
        for feature, child_scope in zip(func_declarations, scope.children):
            self.visit(feature, child_scope)
                
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
        vname = self.register_local(VariableInfo(node.name, node.type))
    
    @visitor.when(COOL_AST.AttributeInit)
    def visit(self, node, scope):
        vname = self.register_local(VariableInfo(node.name, node.type))
        expr = self.visit(node.expr, scope)
        return self.register_instruction(cil.Assign(vname, expr))

    @visitor.when(COOL_AST.AssignExpr)
    def visit(self, node, scope):
        var_info = scope.find_variable(node.name)
        local_var = self.register_local(var_info)
        
        value = self.visit(node.expr, scope)
        self.register_instruction(CIL_AST.Assign(local_var, value))
        return local_var

    @visitor.when(COOL_AST.Block)
    def visit(self, node, scope):
        for e in node.exprs:
            result_local = self.visit(e, scope)
        return result_local
                 
    @visitor.when(COOL_AST.If)
    def visit(self, node, scope):
        cond_local = self.visit(node.predicate)
        
    @visitor.when(COOL_AST.FormalParameter)
    def visit(self, node, scope):
        pass

    @visitor.when(COOL_AST.DynamicCall)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.StaticCall)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Case)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Action)
    def visit(self, node, scope):
        pass

    @visitor.when(COOL_AST.While)
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
        pass
        
    @visitor.when(COOL_AST.IsVoid)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Sum)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.visit(node.left, scope)
        right_local = self.visit(node.right, scope)
        self.register_instruction(CIL_AST.Plus(result_local, left_local, right_local))
        return result_local
        

    @visitor.when(COOL_AST.Sub)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.visit(node.left, scope)
        right_local = self.visit(node.right, scope)
        self.register_instruction(CIL_AST.Minus(result_local, left_local, right_local))
        return result_local

    @visitor.when(COOL_AST.Mult)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.visit(node.left, scope)
        right_local = self.visit(node.right, scope)
        self.register_instruction(CIL_AST.Star(result_local, left_local, right_local))
        return result_local

    @visitor.when(COOL_AST.Div)
    def visit(self, node, scope):
        result_local = self.define_internal_local()
        left_local = self.visit(node.left, scope)
        right_local = self.visit(node.right, scope)
        self.register_instruction(CIL_AST.Div(result_local, left_local, right_local))
        return result_local
        
    @visitor.when(COOL_AST.LogicBinOp)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Not)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.LogicalNot)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Equals)
    def visit(self, node, scope):
        pass
        
    @visitor.when(COOL_AST.Identifier)
    def visit(self, node, scope):
        return node.name
    
    @visitor.when(COOL_AST.INTEGER)
    def visit(self, node, scope):
        return node.value

    @visitor.when(COOL_AST.STRING)
    def visit(self, node, scope):
        return node.value
        
    @visitor.when(COOL_AST.Boolean)
    def visit(self, node, scope):
        if str(node.value) == "True":
            return 1
        else:
            return 0

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

    