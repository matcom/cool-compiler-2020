import core.cmp.visitor as visitor
from core.cmp.CoolUtils import *
from core.cmp.utils import InferenceSets
from core.cmp.semantic import SemanticError
from core.cmp.semantic import Attribute, Method, Type
from core.cmp.semantic import ErrorType, IntType, StringType, BoolType, IOType, VoidType, AutoType
from core.cmp.semantic import Context, Scope

WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined.'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
CONDITION_NOT_BOOL = '"%s" conditions return type must be Bool not "%s"'

ST, AT = ['SELF_TYPE', 'AUTO_TYPE']
sealed = ['Int', 'String', 'Bool', 'SELF_TYPE', 'AUTO_TYPE']
built_in_types = [ 'Int', 'String', 'Bool', 'Object', 'IO', 'SELF_TYPE', 'AUTO_TYPE']
INT, STRING, BOOL, OBJ = None, None, None, None

def define_built_in_types(context):
    obj = context.create_type('Object')
    i = context.append_type(IntType())
    i.set_parent(obj)
    s = context.append_type(StringType())
    s.set_parent(obj)
    b = context.append_type(BoolType())
    b.set_parent(obj)
    io = context.append_type(IOType())
    io.set_parent(obj)
    st = context.create_type('SELF_TYPE')
    context.append_type(AutoType())

    obj.define_method('abort', [], [], obj)
    obj.define_method('type_name', [], [], s)
    obj.define_method('copy', [], [], st)

    io.define_method('out_string', ['x'], [s], st)
    io.define_method('out_int', ['x'], [i], st)
    io.define_method('in_string', [], [], s)
    io.define_method('in_int', [], [], i)

    s.define_method('length', [], [], i)
    s.define_method('concat', ['s'], [s], s)
    s.define_method('substr', ['i', 'l'], [i, i], s)

    global INT, STRING, BOOL, OBJ
    INT, STRING, BOOL, OBJ = i, s, b, obj

def fixed_type(type1, type2):
    return type1 if type1.name != ST else type2

def update_condition(target, value):
    c1 = isinstance(target, AutoType)
    c2 = (not isinstance(value, AutoType)) and value
    return c1 and c2

#AST Printer
class FormatVisitor:
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.declarations)
        return f'{ans}\n{statements}'
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tabs=0):
        parent = '' if node.parent is None else f"inherits {node.parent}"
        ans = '\t' * tabs + f'\\__ClassDeclarationNode: class {node.id} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(self.visit(child, tabs + 1) for child in node.features)
        return f'{ans}\n{features}'
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tabs=0):
        sons = [node.expr] if node.expr else []
        text = '<- <expr>' if node.expr else ''
        ans = '\t' * tabs + f'\\__{node.__class__.__name__}: {node.id} : {node.type} {text}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}' if body else f'{ans}'
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(' : '.join(param) for param in node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: {node.id}({params}) : {node.type} {{<body>}}'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'
    
    @visitor.when(IfThenElseNode)
    def visit(self, node, tabs=0):
        sons = [node.condition, node.if_body, node.else_body]
        ans = '\t' * tabs + f'\\__IfThenElseNode: if <cond> then <body> else <body> fi'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(WhileLoopNode)
    def visit(self, node, tabs=0):
        sons = [node.condition, node.body]
        ans = '\t' * tabs + f'\\__WhileLoopNode: while <cond> loop <body> pool'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(BlockNode)
    def visit(self, node, tabs=0):
        sons = node.exprs
        ans = '\t' * tabs + f'\\__BlockNode: {{<expr> ... <expr>}}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(LetInNode)
    def visit(self, node, tabs=0):
        sons = node.let_body + [node.in_body]
        ans = '\t' * tabs + f'\\__LetInNode: let {{<attr> ... <attr>}} in <expr>'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(CaseOfNode)
    def visit(self, node, tabs=0):
        sons = [node.expr] + node.branches
        ans = '\t' * tabs + f'\\__CaseOfNode: case <expr> of {{<case> ... <case>}} esac'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(CaseExpressionNode)
    def visit(self, node, tabs=0):
        sons = [node.expr]
        ans = '\t' * tabs + f'\\__CaseExpressionNode: {node.id} : {node.type} => <expr>'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(AssignNode)
    def visit(self, node, tabs=0):
        sons = [node.expr]
        ans = '\t' * tabs + f'\\__AssignNode: {node.id} = <expr>'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(UnaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__}: {node.symbol.lex} <expr>'
        right = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{right}'
   
    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__}: <expr> {node.symbol.lex} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
    
    @visitor.when(FunctionCallNode)
    def visit(self, node, tabs=0):
        obj = self.visit(node.obj, tabs + 1)
        ans = '\t' * tabs + f'\\__FunctionCallNode: <obj>.{node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        ans = f'{ans}\n{obj}'
        if args: ans += f'\n{args}'
        return ans

    @visitor.when(MemberCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MemberCallNode: {node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        if args: ans += f'\n{args}'
        return ans
    
    @visitor.when(NewNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__NewNode: new {node.type}()'

# Type Collector
class TypeCollector:
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
        self.type_level = {}
        self.parent = {}
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        define_built_in_types(self.context)
        
        for def_class in node.declarations:
            self.visit(def_class)
             
        # comparison for sort node.declarations
        def get_type_level(typex):
            try:
                parent = self.type_level[typex]
            except KeyError:
                return 0
            
            if parent == 0:
                node = self.parent[typex]
                node.parent = "Object"
                self.errors.append(('Cyclic heritage.', node.tparent))
            elif type(parent) is not int:
                self.type_level[typex] = 0 if parent else 1
                if type(parent) is str:
                    self.type_level[typex] = get_type_level(parent) + 1
                
            return self.type_level[typex]
        
        node.declarations.sort(key = lambda node: get_type_level(node.id))               
                
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        def new_type():
            self.context.create_type(node.id)
            self.type_level[node.id] = node.parent
            self.parent[node.id] = node

        def make_a_duplicate():
            while True:
                node.id = '1' + node.id
                try: new_type()
                except SemanticError: pass
                else: break

        if node.id not in built_in_types:
            try: new_type()
            except SemanticError as ex:
                self.errors.append((ex.text, node.tid))
                make_a_duplicate()
        else:
            self.errors.append((f'{node.id} is an invalid class name', node.tid))
            make_a_duplicate()

# Type Builder
class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
        self.methods = {}
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        main_token = None
        for def_class in node.declarations:
            self.visit(def_class)
            if def_class.id == 'Main':
                main_token = def_class.tid
            
        try:
            main = self.context.get_type('Main')
            method = main.methods['main']
            tmethod = self.methods['Main']['main']
            if method.param_names:
                self.errors.append(('Method "main" must takes no formal parameters', tmethod))
        except SemanticError:
            self.errors.append(('No definition for class "Main"', empty_token))
        except KeyError:
            self.errors.append(('Class "Main" must have a method "main"', main_token))         
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        
        if node.parent:
            if node.parent in sealed:
                self.errors.append((f'Is not possible to inherits from "{node.parent}"', node.tparent))
                node.parent = 'Object'
            try:
                parent_type = self.context.get_type(node.parent)
                self.current_type.set_parent(parent_type)
            except SemanticError as ex:
                self.errors.append((ex.text, node.tparent))
        
        for feature in node.features:
            self.visit(feature)
            
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append((ex.text, node.ttype))
            attr_type = ErrorType()
        node.attr_type = attr_type

        try:
            attr = self.current_type.define_attribute(node.id, attr_type)
            attr.node = node
            node.attr = attr
        except SemanticError as ex:
            self.errors.append((ex.text, node.tid))
        
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        arg_names, arg_types, arg_nodes = [], [], []
        for i, arg in enumerate(node.params):
            idx, typex = arg
            try:
                arg_type = self.context.get_type(typex)
            except SemanticError as ex:
                self.errors.append((ex.text, node.params[i].ttype))
                arg_type = ErrorType()
                
            arg_names.append(idx)
            arg_types.append(arg_type)
            arg_nodes.append(arg)
            arg.idx = i
            arg.method_types = arg_types
        
        try:
            ret_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append((ex.text, node.ttype))
            ret_type = ErrorType()
        node.ret_type = ret_type
        node.arg_types = arg_types
        node.arg_names = arg_names
        node.arg_nodes = arg_nodes

        try:
            method = self.current_type.define_method(node.id, arg_names, arg_types, ret_type)
            method.nodes = arg_nodes
            method.ret_node = node
            node.method = method
            for arg in node.params:
                arg.method = method
            if not self.current_type.name in self.methods:
                self.methods[self.current_type.name] = {}
            self.methods[self.current_type.name][node.id] = node.tid    
        except SemanticError as ex:
            self.errors.append((ex.text, node.tid))

# Compute the Lowest Common Ancestor in
# the type hierarchy tree
def LCA(type_list):
    counter = {}

    if any([isinstance(t, AutoType) for t in type_list]):
        return AutoType()
    if any([isinstance(t, ErrorType) for t in type_list]):
        return ErrorType()
    for typex in type_list:
        node = typex
        while True:
            try:
                counter[node.name] += 1
            except KeyError:
                counter[node.name] = 1
            if counter[node.name] == len(type_list):
                return node
            if not node.parent:
                break
            node = node.parent

def check_path(D, ans):
    for t in D:
        l = [ans, t]
        lca = LCA(l)
        try: l.remove(lca)
        except ValueError:
            return False, None
        ans = l[0]
    return True, ans

# Type Checker
class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        
        scope.define_variable('self', self.current_type)
        cur_type = self.current_type.parent
        while True:
            for attr in cur_type.attributes:
                var = scope.define_variable(attr.name, attr.type)
                var.node = attr.node
            if not cur_type.parent:
                break
            cur_type = cur_type.parent
            
        cur_type = self.current_type
        pending, count = [], 0
        for idx, feature in enumerate(node.features):
            if isinstance(feature, AttrDeclarationNode):
                self.visit(feature, scope)
                if not scope.is_defined(feature.id):
                    var = scope.define_variable(feature.id, cur_type.attributes[count].type)
                    var.node = cur_type.attributes[count].node
                count += 1
            else:
                pending.append(feature)

        for feature in pending:  
            self.visit(feature, scope.create_child())
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        if not node.expr:
            return

        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        real_type = fixed_type(node.attr_type, self.current_type)
        node.info = [expr_type, real_type]

        if not expr_type.conforms_to(real_type):
            self.errors.append((INCOMPATIBLE_TYPES % (expr_type.name, real_type.name),  node.arrow))
            
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = node.id
        
        for pname, ptype, pnode in zip(node.arg_names, node.arg_types, node.arg_nodes):
            var = scope.define_variable(pname, ptype)
            var.node = pnode
            
        self.visit(node.body, scope)
            
        body_type = node.body.computed_type
        method_rtn_type = fixed_type(node.ret_type, self.current_type)
        node.info = [body_type, method_rtn_type]

        if not body_type.conforms_to(method_rtn_type):
            self.errors.append((INCOMPATIBLE_TYPES % (body_type.name, method_rtn_type.name), node.ttype))
            
    @visitor.when(AssignNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node_type = node.expr.computed_type
        var_type = None

        try:
            if not scope.is_defined(node.id):
                raise SemanticError(VARIABLE_NOT_DEFINED % (node.id))
            var = scope.find_variable(node.id)
            if var.name == 'self':
                raise SemanticError(SELF_IS_READONLY)
            var_type = fixed_type(var.type, self.current_type)
            if not node_type.conforms_to(var_type): 
                raise SemanticError(INCOMPATIBLE_TYPES % (node_type.name, var.type.name))
        except SemanticError as ex:
            self.errors.append((ex.text, node.tid))
            node_type = ErrorType()
        
        node.info = [node_type, var_type]
        node.computed_type = node_type
        
    @visitor.when(CaseOfNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        
        types_list = []
        for case in node.branches:
            self.visit(case, scope.create_child())
            types_list.append(case.computed_type)

        node.computed_type = LCA(types_list)

    @visitor.when(CaseExpressionNode)
    def visit(self, node, scope):
        node.scope = scope
        try:
            branch_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append((ex.text, node.ttype))
            branch_type = ErrorType()
        node.branch_type = branch_type

        var = scope.define_variable(node.id, branch_type)
        var.node = node
        self.visit(node.expr, scope)
        node.computed_type = node.expr.computed_type
            
    @visitor.when(LetInNode)
    def visit(self, node, scope):
        child = scope.create_child()
        node.scope = child
        
        for expr in node.let_body:
            self.visit(expr, child)
        
        self.visit(node.in_body, child)
        node.computed_type = node.in_body.computed_type

    @visitor.when(LetAttributeNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append((ex.text, node.ttype))
            node_type = ErrorType()
        node.attr_type = node_type
        node.scope = None
        
        if not scope.is_local(node.id):
            var = scope.define_variable(node.id, node_type)
            var.node = node
        else:
            self.errors.append((LOCAL_ALREADY_DEFINED % (node.id, self.current_method), node.tid))
        
        if node.expr:
            self.visit(node.expr, scope)
            expr_type = node.expr.computed_type
            real_type = fixed_type(node_type, self.current_type)
            node.info = [expr_type, real_type]

            if not expr_type.conforms_to(real_type): 
                self.errors.append((INCOMPATIBLE_TYPES % (expr_type.name, real_type.name), node.arrow))
        
    @visitor.when(IfThenElseNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        node.cond_type = node.condition.computed_type

        if not node.cond_type.conforms_to(BOOL):
            self.errors.append((CONDITION_NOT_BOOL % ('If', cond_type.name), node.token))

        self.visit(node.if_body, scope)
        if_type = node.if_body.computed_type

        self.visit(node.else_body, scope)
        else_type = node.else_body.computed_type
        node.computed_type = LCA([if_type, else_type])
        
    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.exprs:
            self.visit(expr, scope)

        last_expr = node.exprs[-1]
        node.computed_type = last_expr.computed_type    
            
    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        node.cond_type = node.condition.computed_type

        if not node.cond_type.conforms_to(BOOL):
            self.errors.append((CONDITION_NOT_BOOL % ('While', cond_type.name), node.token))

        self.visit(node.body, scope)
        node.computed_type = OBJ
    
    @visitor.when(FunctionCallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope)
        obj_type = node.obj.computed_type
        
        error = False

        arg_types, real_types = [], []
        for arg in node.args:
            self.visit(arg, scope)
            arg_types.append(arg.computed_type)
        
        try:
            if node.type:
                token = node.ttype
                cast_type = self.context.get_type(node.type)
                if cast_type.name == ST:
                    raise SemanticError("Invalid use of SELF_TYPE")
                if cast_type.name == AT:
                    raise SemanticError('Is not possible to use AUTO_TYPE in a cast')
                if not obj_type.conforms_to(cast_type):
                    raise SemanticError(INCOMPATIBLE_TYPES % (obj_type.name, node.type))
                obj_type = cast_type
            
            token = node.tid
            obj_method = obj_type.get_method(node.id)
            node.obj_method = obj_method
            if len(node.args) == len(obj_method.param_types):
                for idx, (arg, param_type) in enumerate(zip(arg_types, obj_method.param_types)):
                    real_type = fixed_type(param_type, obj_type)
                    real_types.append(real_type)

                    if not arg.conforms_to(real_type):
                        self.errors.append((INCOMPATIBLE_TYPES % (arg.name, real_type.name + f" in the argument #{idx} of {node.id}"), token))
                        error = True
            else:
                raise SemanticError(f'Method "{obj_method.name}" of "{obj_type.name}" only accepts {len(obj_method.param_types)} argument(s)')
            assert not error
            node_type = fixed_type(obj_method.return_type, obj_type)
        except SemanticError as ex:
            self.errors.append((ex.text, token))
            node_type = ErrorType()
        except AssertionError:
            node_type = ErrorType()
        
        node.info = [arg_types, real_types]
        node.computed_type = node_type

    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        obj_type = self.current_type
        
        error = False

        arg_types, real_types = [], []
        for arg in node.args:
            self.visit(arg, scope)
            arg_types.append(arg.computed_type)

        try:
            token = node.tid
            obj_method = obj_type.get_method(node.id)
            node.obj_method = obj_method
            if len(node.args) == len(obj_method.param_types):
                for arg, param_type in zip(arg_types, obj_method.param_types):
                    real_type = fixed_type(param_type, self.current_type)
                    real_types.append(real_type)
                    
                    if not arg.conforms_to(real_type):
                        self.errors.append((INCOMPATIBLE_TYPES % (arg.name, real_type.name + f" in the argument #{idx} of {node.id}"), token))
                        error = True
            else:
                raise SemanticError(f'Method "{obj_method.name}" of "{obj_type.name}" only accepts {len(obj_method.param_types)} argument(s)')
            assert not error
            node_type = fixed_type(obj_method.return_type, self.current_type)
        except SemanticError as ex:
            self.errors.append((ex.text, token))
            node_type = ErrorType()
        except AssertionError:
            node_type = ErrorType()

        node.info = [arg_types, real_types] 
        node.computed_type = node_type
    
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.computed_type
        
        self.visit(node.right, scope)
        right_type = node.right.computed_type
        node.info = [left_type, right_type]
        
        if not (right_type.conforms_to(INT) and left_type.conforms_to(INT)):
            self.errors.append((INVALID_OPERATION % (left_type.name, right_type.name), node.symbol))
            
        node.computed_type = [BOOL, INT][isinstance(node, ArithmeticNode)]
    
    @visitor.when(IntegerNode)
    def visit(self, node, scope):
        node.computed_type = INT
        
    @visitor.when(StringNode)
    def visit(self, node, scope):
        node.computed_type = STRING
        
    @visitor.when(BoolNode)
    def visit(self, node, scope):
        node.computed_type = BOOL

    @visitor.when(IdNode)
    def visit(self, node, scope):
        if scope.is_defined(node.lex):
            var = scope.find_variable(node.lex)
            node_type = fixed_type(var.type, self.current_type)       
        else:
            self.errors.append((VARIABLE_NOT_DEFINED % (node.lex), node.token))
            node_type = ErrorType()
        
        node.computed_type = node_type

    @visitor.when(NewNode)
    def visit(self, node, scope):
        try:
            raw_type = self.context.get_type(node.type)
            node_type = fixed_type(raw_type, self.current_type)
        except SemanticError as ex:
            self.errors.append((ex.text, node.ttype))
            node_type = ErrorType()
            
        node.computed_type = node_type

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.computed_type = BOOL

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        node.expr_type = expr_type

        if not expr_type.conforms_to(INT):
            self.errors.append(("Complement works only for Int", node.symbol))
        node.computed_type = INT

    @visitor.when(NotNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        node.expr_type = expr_type

        if not expr_type.conforms_to(BOOL):
            self.errors.append(("Not operator works only for Bool", node.symbol))
        node.computed_type = BOOL

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.computed_type
        
        self.visit(node.right, scope)
        right_type = node.right.computed_type
        node.info = [left_type, right_type]
        
        valid_types = [IntType(), BoolType(), StringType()]
        try:
            cur_types = [right_type, left_type]
            for op_type in valid_types:
                try:
                    cur_types.remove(op_type)
                    assert cur_types[0].conforms_to(op_type)
                    break
                except ValueError: pass
        except AssertionError:
            self.errors.append((INVALID_OPERATION % (left_type.name, right_type.name), node.symbol))
            
        node.computed_type = BOOL


# Type Inference Visitor
class InferenceVisitor(TypeChecker):
    def __init__(self, context, errors=[]):
        super().__init__(context, errors)
        self.variable = {}

    def inference(self, node, ntype, conforms=True):
        try:
            self.variable[node].add(ntype, conforms)
        except KeyError:
            self.variable[node] = InferenceSets().add(ntype, conforms)

    @visitor.on('node')
    def context_update(self, node, ntype):
        pass

    @visitor.when(Node)
    def context_update(self, node, ntype):
        pass

    @visitor.when(Param)
    def context_update(self, node, ntype):
        node.method_types[node.idx] = ntype
        try: node.method.param_types[node.idx] = ntype
        except AttributeError: pass
    
    @visitor.when(AttrDeclarationNode)
    def context_update(self, node, ntype):
        try: node.attr_type = ntype
        except AttributeError: pass
        try: node.branch_type = ntype
        except AttributeError: pass
        try: node.attr.type = ntype
        except AttributeError: pass

    @visitor.when(FuncDeclarationNode)
    def context_update(self, node, ntype):
        node.ret_type = ntype
        try: node.method.return_type = ntype
        except AttributeError: pass

    @visitor.on('node')
    def update(self, node, scope, ntype):
    	pass

    @visitor.when(AssignNode)
    def update(self, node, scope, ntype):
        self.update(node.expr, scope, ntype)

    @visitor.when(CaseOfNode)
    def update(self, node, scope, ntype):
        for branch in node.branches:
            if isinstance(branch.computed_type, AutoType):
                self.update(branch, scope, ntype)

    @visitor.when(CaseExpressionNode)
    def update(self, node, scope, ntype):
        self.update(node.expr, node.scope, ntype)

    @visitor.when(LetInNode)
    def update(self, node, scope, ntype):
        self.update(node.in_body, node.scope, ntype)

    @visitor.when(IfThenElseNode)
    def update(self, node, scope, ntype):
        if isinstance(node.if_body.computed_type, AutoType):
            self.update(node.if_body, scope, ntype)
        if isinstance(node.else_body.computed_type, AutoType):
            self.update(node.else_body, scope, ntype)

    @visitor.when(BlockNode)
    def update(self, node, scope, ntype):
        self.update(node.exprs[-1], scope, ntype)

    @visitor.when(FunctionCallNode)
    def update(self, node, scope, ntype):
        self.inference(node.obj_method.ret_node, ntype)

    @visitor.when(MemberCallNode)
    def update(self, node, scope, ntype):
        self.inference(node.obj_method.ret_node, ntype)

    @visitor.when(IdNode)
    def update(self, node, scope, ntype):
        self.inference(scope.find_variable(node.lex).node, ntype)

    # Visit
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(Node)
    def visit(self, node, scope):
        super().visit(node, scope)

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        super().visit(node, scope) 

        infered = 0
        pending = []
        for (auto, sets) in self.variable.items():
            try:
                if (len(sets.D) + len(sets.S) == 1):
                    pending.append(auto)
                    continue
                ok, D1 = check_path(sets.D, OBJ)
                assert ok
                if len(sets.S):
                    candidate = LCA(sets.S)
                    assert LCA([candidate, D1]) == D1
                    D1 = candidate
                auto.type = D1.name
                self.context_update(auto, D1)
                infered += 1
            except AssertionError:
                self.errors.append((f'Bad use of AUTO_TYPE detected', auto.ttype))
        if not infered:
            for auto in pending:
                auto.type = OBJ.name
                self.context_update(auto, OBJ)
        self.variable.clear()
        return infered
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.attr_type, AutoType):
            self.inference(node, OBJ)

        if not node.expr:
            return

        expr, rtype = node.info
        if update_condition(rtype, expr):
            self.inference(node, expr, False)
        if update_condition(expr, rtype):
            self.update(node.expr, scope, rtype)			

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        super().visit(node, scope)   

        body, rtn = node.info
        if isinstance(rtn, AutoType):
            self.inference(node, OBJ)
        for ptype, pnode in zip(node.arg_types, node.arg_nodes):
            if isinstance(ptype, AutoType):
                self.inference(pnode, OBJ)
        if update_condition(rtn, body):
            self.inference(node, body, False)
        if update_condition(body, rtn):
            self.update(node.body, scope, rtn)
    
    @visitor.when(AssignNode)
    def visit(self, node, scope):
        super().visit(node, scope)
        
        node_type, var = node.info
        if update_condition(var, node_type):
            self.inference(scope.find_variable(node.id).node, node_type, False)
        if update_condition(node_type, var):
            self.update(node.expr, scope, var)

    @visitor.when(CaseExpressionNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.branch_type, AutoType):
            self.inference(node, OBJ)

    @visitor.when(LetAttributeNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.attr_type, AutoType):
            self.inference(node, OBJ)

        if not node.expr:
            return

        expr, rtype = node.info
        if update_condition(rtype, expr):
            self.inference(scope.find_variable(node.id).node, expr, False)
        if update_condition(expr, rtype):
            self.update(node.expr, scope, rtype)			

    @visitor.when(IfThenElseNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.cond_type, AutoType):
            self.update(node.condition, scope, BOOL)
        
    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.cond_type, AutoType):
            self.update(node.condition, scope, BOOL)
    
    @visitor.when(FunctionCallNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        args, real = node.info
        if not real:
            return

        for idx, (atype, rtype) in enumerate(zip(args, real)):
            if update_condition(rtype, atype):
                self.inference(node.obj_method.nodes[idx], atype, False)
            if update_condition(atype, rtype):
                self.update(node.args[idx], scope, rtype)

    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        args, real = node.info
        if not real:
            return

        for idx, (atype, rtype) in enumerate(zip(args, real)):
            if update_condition(rtype, atype):
                self.inference(node.obj_method.nodes[idx], atype, False)
            if update_condition(atype, rtype):
                self.update(node.args[idx], scope, rtype)

    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        left, right = node.info
        if isinstance(left, AutoType):
            self.update(node.left, scope, INT)
        if isinstance(right, AutoType):
            self.update(node.right, scope, INT)
        
    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.expr_type, AutoType):
            self.update(node.expr, scope, INT)

    @visitor.when(NotNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        if isinstance(node.expr_type, AutoType):
            self.update(node.expr, scope, BOOL)
   
    @visitor.when(EqualNode)
    def visit(self, node, scope):
        super().visit(node, scope)

        left, right = node.info
        if update_condition(left, right) and right in [INT, BOOL, STRING]:
            self.update(node.left, scope, right)
        if update_condition(right, left) and left in [INT, BOOL, STRING]:
            self.update(node.right, scope, left)
        
