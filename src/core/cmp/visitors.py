import core.cmp.visitor as visitor
from core.cmp.CoolUtils import *
from core.cmp.semantic import SemanticError
from core.cmp.semantic import Attribute, Method, Type
from core.cmp.semantic import ErrorType, IntType, StringType, BoolType, IOType, VoidType
from core.cmp.semantic import Context, Scope

WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined.'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
CONDITION_NOT_BOOL = '"%s" conditions return type must be Bool not "%s"'

sealed = ['Int', 'String', 'Bool', 'SELF_TYPE', 'AUTO_TYPE']
build_in_types = [ 'Int', 'String', 'Bool', 'IO', 'SELF_TYPE', 'AUTO_TYPE', 'Object']

#AST Printer
class FormatVisitor(object):
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
        ans = '\t' * tabs + f'\\__AttrDeclarationNode: {node.id} : {node.type} {text}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}' if body else f'{ans}'
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(':'.join(param) for param in node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: {node.id}({params}) : {node.type} {{<body>}}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in node.body)
        return f'{ans}\n{body}'
    
    @visitor.when(IfThenElseNode)
    def visit(self, node, tabs=0):
        sons = [node.condition, node.if_body]
        text = ''
        if node.else_body:
            sons.append(node.else_body)
            text += 'else <body>'
        ans = '\t' * tabs + f'\\__IfThenElseNode: if <cond> then <body> {text} fi'
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

    @visitor.when(LetAttributeNode)
    def visit(self, node, tabs=0):
        sons = [node.expr] if node.expr else []
        text = '<- <expr>' if node.expr else ''
        ans = '\t' * tabs + f'\\__LetAttributeNode: {node.id} : {node.type} {text}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}' if body else f'{ans}'
    
    @visitor.when(AssignNode)
    def visit(self, node, tabs=0):
        sons = [node.expr]
        ans = '\t' * tabs + f'\\__AssignNode: {node.id} = <expr>'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(UnaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__} <expr>'
        right = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{right}'
   
    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
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
        return f'{ans}\n{obj}\n{args}'

    @visitor.when(MemberCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MemberCallNode: {node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'
    
    @visitor.when(NewNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__NewNode: new {node.type}()'

# Type Collector
class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
        self.type_level = {}
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        obj = self.context.create_type('Object')
        self.context.create_type('Int').set_parent(obj)
        self.context.create_type('String').set_parent(obj)
        self.context.create_type('Bool').set_parent(obj)
        self.context.create_type('IO').set_parent(obj)
        #self.context.create_type('SELF_TYPE')
        self.context.create_type('AUTO_TYPE')
        
        for def_class in node.declarations:
            self.visit(def_class)
             
        # comparison for sort node.declarations
        def get_type_level(typex):
            try:
                parent = self.type_level[typex]
            except KeyError:
                return 0
            
            if parent == 0:
                self.errors.append('Cyclic heritage.')
            elif type(parent) is not int:
                self.type_level[typex] = 0 if parent else 1
                if type(parent) is str:
                    self.type_level[typex] = get_type_level(parent) + 1
                
            return self.type_level[typex]
        
        node.declarations.sort(key = lambda node: get_type_level(node.id))               
                
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        if node.id not in build_in_types:
            try:
                self.context.create_type(node.id)
                self.type_level[node.id] = node.parent
            except SemanticError as ex:
                self.errors.append(ex.text)
        else:
            self.errors.append(f'{node.id} is an invalid class name')

# Type Builder
class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for def_class in node.declarations:
            self.visit(def_class)
            
        try:
            main = self.context.get_type('Main')
            main.get_method('main')
            if main.parent.name != 'Object':
                self.errors.append('The class "Main" cannot inherits from any type.')
        except SemanticError:
            self.errors.append('The class "Main" and his method "main" are needed.')
            
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        
        if node.parent:
            if node.parent in sealed:
                self.errors.append(f'Is not possible to inherits from "{node.parent}"')
                node.parent = 'Object'
            try:
                parent_type = self.context.get_type(node.parent)
                self.current_type.set_parent(parent_type)
            except SemanticError as ex:
                self.errors.append(ex.text)
        
        for feature in node.features:
            self.visit(feature)
            
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type) if node.type != 'SELF_TYPE' else self.current_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            attr_type = ErrorType()
            
        try:
            self.current_type.define_attribute(node.id, attr_type)
        except SemanticError as ex:
            self.errors.append(ex.text)
        
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        arg_names, arg_types = [], []
        for idx, typex in node.params:
            try:
                arg_type = self.context.get_type(typex) if node.type != 'SELF_TYPE' else self.current_type
            except SemanticError as ex:
                self.errors.append(ex.text)
                arg_type = ErrorType()
                
            arg_names.append(idx)
            arg_types.append(arg_type)
        
        try:
            ret_type = self.context.get_type(node.type) if node.type != 'SELF_TYPE' else self.current_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            ret_type = ErrorType()
        
        try:
            self.current_type.define_method(node.id, arg_names, arg_types, ret_type)
        except SemanticError as ex:
            self.errors.append(ex.text)

# Compute the Lowest Common Ancestor in
# the type hierarchy tree
def LCA(type_list, context):
    known_types = set()
    counter = {}

    type_list = [ context.get_type(tp.name) for tp in type_list ]
    for typex in type_list:
        node = typex
        while True:
            try:
                counter[node.name] += 1
                if counter[node.name] == len(type_list):
                    return [t for t in known_types if t.name == node.name][0]
            except KeyError:
                counter[node.name] = 1
                known_types.add(node)
            if node.parent:
                node = node.parent
            else:
                break

    raise Exception('El LCA se partio')

def IsAuto(name):
    return name == 'AUTO_TYPE' or IsVoid(name)

def IsVoid(name):
    return name == 'void'

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
        for attr in self.current_type.attributes:
            scope.define_variable(attr.name, attr.type)
            
        for feature in node.features:
            self.visit(feature, scope.create_child())
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type) if node.type != 'SELF_TYPE' else self.current_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()

        if not node.expr:
            node.computed_type = node_type 
            return

        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type

        if not (IsAuto(expr_type.name) or expr_type.conforms_to(node_type)):
            self.errors.append(INCOMPATIBLE_TYPES.replace('%s', expr_type.name, 1).replace('%s', node_type.name, 1))
        
        node.computed_type = node_type 
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)
        
        for pname, ptype in zip(self.current_method.param_names, self.current_method.param_types):
            scope.define_variable(pname, ptype)
            
        # for expr in node.body:
        self.visit(node.body, scope)
            
        last_expr = node.body
        last_expr_type = last_expr.computed_type
        method_rtn_type = self.current_method.return_type

        if not last_expr_type.conforms_to(method_rtn_type):
            self.errors.append(INCOMPATIBLE_TYPES.replace('%s', last_expr_type.name, 1).replace('%s', method_rtn_type.name, 1))
            
    @visitor.when(AssignNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        
        if scope.is_defined(node.id):
            var = scope.find_variable(node.id)
            node_type = var.type       
            
            if var.name == 'self':
                self.errors.append(SELF_IS_READONLY)
            elif not (IsAuto(expr_type.name) or expr_type.conforms_to(node_type)): 
                self.errors.append(INCOMPATIBLE_TYPES.replace('%s', expr_type.name, 1).replace('%s', node_type.name, 1))
        else:
            self.errors.append(VARIABLE_NOT_DEFINED.replace('%s', node.id, 1))
            node_type = ErrorType()
        
        node.computed_type = node_type
        
    @visitor.when(CaseOfNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        has_auto = has_error = False
        
        types_list = []
        for case in node.branches:
            self.visit(case.expr, scope)
            has_auto |= IsAuto(case.expr.computed_type.name)
            has_error |= case.expr.computed_type.name == '<error>'
            types_list.append(case.expr.computed_type)

        if has_error:
            node.computed_type = ErrorType()
        elif has_auto:
            node.computed_type = self.context.get_type('AUTO_TYPE')
        else:
            node.computed_type = LCA(types_list, self.context)

    @visitor.when(CaseExpressionNode)
    def visit(self, node, scope):
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
            node_type = self.context.get_type(node.type) if node.type != 'SELF_TYPE' else self.current_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()

        if not scope.is_local(node.id):
            scope.define_variable(node.id, node_type)
        else:
            self.errors.append(LOCAL_ALREADY_DEFINED.replace('%s', node.id, 1).replace('%s', self.current_method.name, 1))
        
        if not node.expr:
            node.computed_type = node.type
            return
            
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        
        if not(IsAuto(expr_type.name) or expr_type.conforms_to(node_type)):
            self.errors.append(INCOMPATIBLE_TYPES.replace('%s', expr_type.name, 1).replace('%s', node_type.name, 1))
          
        
        node.computed_type = node_type
        
    @visitor.when(IfThenElseNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        expr_type = node.condition.computed_type

        if not expr_type.name in ['Bool', 'AUTO_TYPE']:
            self.errors.append(CONDITION_NOT_BOOL.replace('%s', 'If', 1).replace('%s', expr_type.name, 1))

        self.visit(node.if_body, scope)
        node.computed_type = node.if_body.computed_type
        
        if node.else_body:
            self.visit(node.else_body, scope)
            if IsAuto(node.if_body.computed_type.name) or IsAuto(node.else_body.computed_type.name):
                node.computed_type = self.context.get_type('AUTO_TYPE')
            elif '<error>' in [node.if_body.computed_type.name, node.else_body.computed_type.name]:
                node.computed_type = ErrorType()
            else:
                node.computed_type = LCA([node.if_body.computed_type, node.else_body.computed_type], self.context)
            
    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.exprs:
            self.visit(expr, scope)

        last_expr = node.exprs[-1]
        node.computed_type = last_expr.computed_type    
            
    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        expr_type = node.condition.computed_type

        if not expr_type.name in ['Bool', 'AUTO_TYPE']:
            self.errors.append(CONDITION_NOT_BOOL.replace('%s', 'While', 1).replace('%s', expr_type.name, 1))

        self.visit(node.body, scope)
        node.computed_type = VoidType()
    
    @visitor.when(FunctionCallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope)
        obj_type = node.obj.computed_type
        
        if node.type:
            try:
                if IsAuto(node.type):
                    raise SemanticError('Is not possible to use AUTO_TYPE in a cast')
                if not obj_type.conforms_to(self.context.get_type(node.type)):
                    self.errors.append(INCOMPATIBLE_TYPES.replace('%s', obj_type.name, 1).replace('%s', node.type, 1))
            except SemanticError as ex:
                self.errors.append(ex.text)

        try:
            if node.type:
                obj_method = self.context.get_type(node.type).get_method(node.id)
            else:
                obj_method = obj_type.get_method(node.id)
            
            if len(node.args) == len(obj_method.param_types):
                for arg, param_type in zip(node.args, obj_method.param_types):
                    self.visit(arg, scope)
                    arg_type = arg.computed_type
                    
                    if not (IsAuto(arg_type.name) or arg_type.conforms_to(param_type)):
                        self.errors.append(INCOMPATIBLE_TYPES.replace('%s', arg_type.name, 1).replace('%s', param_type.name, 1))
            else:
                self.errors.append(f'Method "{obj_method.name}" of "{obj_type.name}" only accepts {len(obj_method.param_types)} argument(s)')
            
            node_type = obj_method.return_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()
            
        node.computed_type = node_type

    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        obj_type = self.current_type
        
        try:
            obj_method = obj_type.get_method(node.id)
        
            if len(node.args) == len(obj_method.param_types):
                for arg, param_type in zip(node.args, obj_method.param_types):
                    self.visit(arg, scope)
                    arg_type = arg.computed_type
                    
                    if not (IsAuto(arg_type.name) or arg_type.conforms_to(param_type)):
                        self.errors.append(INCOMPATIBLE_TYPES.replace('%s', arg_type.name, 1).replace('%s', param_type.name, 1))
            else:
                self.errors.append(f'Method "{obj_method.name}" of "{obj_type.name}" only accepts {len(obj_method.param_types)} argument(s)')
            
            node_type = obj_method.return_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()
            
        node.computed_type = node_type
    
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.computed_type
        
        self.visit(node.right, scope)
        right_type = node.right.computed_type
        
        if not (IsAuto(left_type.name) or left_type.conforms_to(IntType())) or not (IsAuto(right_type.name) or right_type.conforms_to(IntType())):
            self.errors.append(INVALID_OPERATION.replace('%s', left_type.name, 1).replace('%s', right_type.name, 1))
            node_type = ErrorType()
        else:
            node_type = IntType()
            
        node.computed_type = node_type
    
    @visitor.when(IntegerNode)
    def visit(self, node, scope):
        node.computed_type = IntType()
        
    @visitor.when(StringNode)
    def visit(self, node, scope):
        node.computed_type = StringType()
        
    @visitor.when(BoolNode)
    def visit(self, node, scope):
        node.computed_type = BoolType()

    @visitor.when(IdNode)
    def visit(self, node, scope):
        if scope.is_defined(node.lex):
            var = scope.find_variable(node.lex)
            node_type = var.type       
        else:
            self.errors.append(VARIABLE_NOT_DEFINED.replace('%s', node.lex, 1))
            node_type = ErrorType()
        
        node.computed_type = node_type

    @visitor.when(NewNode)
    def visit(self, node, scope):
        if node.type in build_in_types:
            self.errors.append(f'It cannot be initialized a {node.type} with the new keyword')
            node.computed_type = ErrorType()
        else:
            try:
                node_type = self.context.get_type(node.type)
            except SemanticError as ex:
                self.errors.append(ex.text)
                node_type = ErrorType()
                
            node.computed_type = node_type

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.computed_type = self.context.get_type('Bool')

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        if not (IsAuto(node.expr.computed_type.name) or node.expr.computed_type.name != 'Int'):
            self.errors.append("Complement works only for Int")
            node.computed_type = ErrorType()
        else:
            node.computed_type = self.context.get_type('Int')

    @visitor.when(NotNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        if not (IsAuto(node.expr.computed_type.name) or node.expr.computed_type.name != 'Bool'):
            self.errors.append("Not operator works only for Bool")
            node.computed_type = ErrorType()
        else:
            node.computed_type = self.context.get_type('Bool')

# Type Inference Visitor
class InferenceVisitor(object):
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def update(self, node, scope, ntype):
    	pass

    @visitor.when(Node)
    def update(self, node, scope, ntype):
    	pass

    @visitor.when(FunctionCallNode)
    def update(self, node, scope, ntype):
        obj_type = node.obj.computed_type

        obj_type.get_method(node.id).return_type = ntype
        node.computed_type = ntype

    @visitor.when(MemberCallNode)
    def update(self, node, scope, ntype):
        obj_type = self.current_type

        obj_type.get_method(node.id).return_type = ntype
        node.computed_type = ntype

    @visitor.when(AttrDeclarationNode)
    def update(self, node, scope, ntype):
    	scope.find_variable(node.id).type = ntype
    	node.computed_type = ntype

    @visitor.when(IdNode)
    def update(self, node, scope, ntype):
    	scope.find_variable(node.lex).type = ntype
    	node.computed_type = ntype

    @visitor.when(IfThenElseNode)
    def update(self, node, scope, ntype):
        if IsAuto(node.if_body.computed_type.name):
            self.update(node.if_body, scope, ntype)

        node.computed_type = node.if_body.computed_type

        if node.else_body:
            if IsAuto(node.else_body.computed_type.name):
                self.update(node.else_body, scope, ntype)

            names = [node.if_body.computed_type.name, node.else_body.computed_type.name]
            if 'AUTO_TYPE' not in names and '<error>' not in names:
                node.computed_type = LCA([node.if_body.computed_type, node.else_body.computed_type], self.context)
            else:
                if '<error>' in names:
                    node.computed_type = ErrorType()
                else:
                    node.computed_type = self.context.get_type('AUTO_TYPE')
    
    @visitor.when(CaseOfNode)
    def update(self, node, scope, ntype):
        types_list = []
        has_auto = has_error = False

        for case in node.branches:
            if IsAuto(case.computed_type.name):
                self.update(branch, scope, ntype)
                has_auto |= IsAuto(case.expr.computed_type.name)
                has_error |= case.expr.computed_type.name == '<error>'
                types_list.append(case.expr.computed_type)
        
        if has_error:
            node.computed_type = ErrorType()
        elif has_auto:
            node.computed_type = self.context.get_type('AUTO_TYPE')
        else:
            node.computed_type = LCA(types_list)

    @visitor.when(CaseExpressionNode)
    def update(self, node, scope, ntype):
        self.update(node.expr, scope, ntype)
        node.computed_type = node.expr.computed_type

    @visitor.when(LetInNode)
    def update(self, node, scope, ntype):
        self.update(node.in_body, node.scope, ntype)
        node.computed_type = node.in_body.computed_type

    @visitor.when(BlockNode)
    def update(self, node, scope, ntype):
        self.update(node.exprs[-1], scope, ntype)
        node.computed_type = node.exprs[-1].computed_type

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
        for attr in self.current_type.attributes:
            scope.define_variable(attr.name, attr.type)
            
        for feature in node.features:
            self.visit(feature, scope.create_child())

        for idx, attr in enumerate(self.current_type.attributes):
            actual_type = scope.find_variable(attr.name).type
            if IsAuto(attr.type.name):
                self.current_type.attributes[idx].type = actual_type
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        node.scope = scope
        if node.expr:
            self.visit(node.expr, scope)
            if IsAuto(node.type):
                if not IsAuto(node.expr.computed_type.name):
                    scope.find_variable(node.id).type = node.expr.computed_type
            else:
                if IsAuto(node.expr.computed_type.name):
                    self.update(node.expr, scope, node.type)
                else:
                    if not node.expr.computed_type.conforms_to(node.computed_type):
                        self.errors.append(INCOMPATIBLE_TYPES.replace('%s', node.expr.computed_type.name, 1).replace('%s', node.computed_type.name, 1))
                        node.computed_type = ErrorType()
                        return

            node.computed_type = node.expr.computed_type			

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)
        node.method = self.current_method

        for pname, ptype in zip(self.current_method.param_names, self.current_method.param_types):
            scope.define_variable(pname, ptype)

        # for expr in node.body:
        self.visit(node.body, scope)

        last_expr = node.body
        last_expr_type = last_expr.computed_type
        method_rtn_type = self.current_method.return_type    

        if IsAuto(method_rtn_type.name):
            if not IsAuto(last_expr_type.name):
                self.current_method.return_type = last_expr_type
                method_rtn_type = last_expr_type
        else:
            if IsAuto(last_expr_type.name):
                self.update(last_expr, scope, method_rtn_type)
            else:
                if not last_expr_type.conforms_to(method_rtn_type):
                    self.errors.append(INCOMPATIBLE_TYPES.replace('%s', last_expr_type.name, 1).replace('%s', method_rtn_type.name, 1))
            
        for idx, pname in enumerate(self.current_method.param_names):
            actual_type = scope.find_variable(pname).type
            if self.current_method.param_types[idx].name != actual_type.name:
                self.current_method.param_types[idx] = actual_type
    
    @visitor.when(IfThenElseNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        expr_type = node.condition.computed_type

        if IsAuto(expr_type.name):
            self.update(node.condition, scope, self.context.get_type('Bool'))
            expr_type = node.condition.computed_type
        if expr_type.name not in ['Bool', 'AUTO_TYPE']:
            self.errors.append(CONDITION_NOT_BOOL.replace('%s', 'If', 1).replace('%s', expr_type.name, 1))

        self.visit(node.if_body, scope)
        node.computed_type = node.if_body.computed_type

        if node.else_body:
            self.visit(node.else_body, scope)
            names = [node.if_body.computed_type.name, node.else_body.computed_type.name]
            if 'AUTO_TYPE' not in names and '<error>' not in names:
                node.computed_type = LCA([node.if_body.computed_type, node.else_body.computed_type], self.context)
            else:
                if '<error>' in names:
                    node.computed_type = ErrorType()
                else:
                    node.computed_type = self.context.get_type('AUTO_TYPE')
    
    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        expr_type = node.condition.computed_type
        if IsAuto(expr_type.name):
            self.update(node.condition, scope, self.context.get_type('Bool'))
            expr_type = node.condition.computed_type

        if expr_type.name not in ['Bool', 'AUTO_TYPE']:
            self.errors.append(CONDITION_NOT_BOOL.replace('%s', 'If', 1).replace('%s', expr_type.name, 1))

        self.visit(node.body, scope)
        node.computed_type = VoidType()
    
    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.exprs:
            self.visit(expr, scope)

        last_expr = node.exprs[-1]
        node.computed_type = last_expr.computed_type

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        child = scope.create_child()
        node.scope = child

        for attr in node.let_body:
            self.visit(attr, child)
            
        self.visit(node.in_body, child)
        node.computed_type = node.in_body.computed_type

        for attr in node.let_body:
            type_name = attr.type
            if attr.computed_type.name == '<error>':
                continue
            actual_type = child.find_variable(attr.id).type
            if type_name != actual_type.name:
                attr.type = actual_type.name

    @visitor.when(LetAttributeNode)
    def visit(self, node, scope):
        node.scope = scope
        try:
            node_type = self.context.get_type(node.type) if node.type != 'SELF_TYPE' else self.current_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()
          
        if not scope.is_local(node.id):
            scope.define_variable(node.id, node_type)
        else:
            self.errors.append(LOCAL_ALREADY_DEFINED.replace('%s', node.id, 1).replace('%s', self.current_method.name, 1))
        
        if not node.expr:
            node.computed_type = node_type
            return

        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type

        if IsAuto(node_type.name):
        	if not IsAuto(expr_type.name):
        		node.type = expr_type.name
        		scope.find_variable(node.id).type = expr_type
        		node.computed_type = expr_type
        else:
            if not IsAuto(expr_type.name):
                if not expr_type.conforms_to(node_type):
                    self.errors.append(INCOMPATIBLE_TYPES.replace('%s', expr_type.name, 1).replace('%s', node_type.name, 1))
            else:
                self.update(node.expr, scope, node_type)
                node.computed_type = node.expr.computed_type

    @visitor.when(CaseOfNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        has_auto = has_error = False
        
        types_list = []
        for case in node.branches:
            self.visit(case.expr, scope)
            has_auto |= IsAuto(case.expr.computed_type.name)
            has_error |= case.expr.computed_type.name == '<error>'
            types_list.append(case.expr.computed_type)

        if has_error:
            node.computed_type = ErrorType()
        elif has_auto:
            node.computed_type = self.context.get_type('AUTO_TYPE')
        else:
            node.computed_type = LCA(types_list, self.context)
        
    @visitor.when(CaseExpressionNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.computed_type = node.expr.computed_type

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type

        if scope.is_defined(node.id):
            var = scope.find_variable(node.id)
            node_type = var.type       
            
            if var.name == 'self':
                self.errors.append(SELF_IS_READONLY)
            else: 
                if IsAuto(node_type.name):
                    if not IsAuto(expr_type.name):
                        node.type = expr_type.name
                        scope.find_variable(node.id).type = expr_type
                        node.computed_type = expr_type
                else:
                    if not IsAuto(expr_type.name):
                        if not expr_type.conforms_to(node_type):
                            self.errors.append(INCOMPATIBLE_TYPES.replace('%s', expr_type.name, 1).replace('%s', node_type.name, 1))
                    else:
                        self.update(node.expr, scope, node_type)
                        node.computed_type = node.expr.computed_type
        else:
            self.errors.append(VARIABLE_NOT_DEFINED.replace('%s', node.id, 1))
            node.computed_type = ErrorType()
        
    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.computed_type = self.context.get_type('Bool')

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        if IsAuto(node.expr.computed_type.name):
            self.update(node.expr, scope, self.context.get_type('Int'))
            node.computed_type = node.expr.computed_type
        else:
            if node.expr.computed_type.name != 'Int':
                self.errors.append("Complement works only for Int")
                node.computed_type = ErrorType()
            else:
                node.computed_type = self.context.get_type('Int')

    @visitor.when(NotNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        if IsAuto(node.expr.computed_type.name):
            self.update(node.expr, scope, self.context.get_type('Bool'))
            node.computed_type = node.expr.computed_type
        else:
            if node.expr.computed_type.name != 'Bool':
                self.errors.append("Not operator works only for Bool")
                node.computed_type = ErrorType()
            else:
                node.computed_type = self.context.get_type('Bool')
   
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.computed_type
        
        self.visit(node.right, scope)
        right_type = node.right.computed_type

        if IsAuto(left_type.name):
        	self.update(node.left, scope, self.context.get_type('Int'))
        	left_type = node.left.computed_type

        if IsAuto(right_type.name):
        	self.update(node.right, scope, self.context.get_type('Int'))
        	right_type = node.right.computed_type
        
        if not (IsAuto(left_type.name) or left_type.conforms_to(IntType())) or not (IsAuto(right_type.name) or right_type.conforms_to(IntType())):
            self.errors.append(INVALID_OPERATION.replace('%s', left_type.name, 1).replace('%s', right_type.name, 1))
            node_type = ErrorType()
        else:
            node_type = IntType()
            
        node.computed_type = node_type
        
    @visitor.when(FunctionCallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope)
        obj_type = node.obj.computed_type
        
        if node.type:
            try:
                if IsAuto(node.type):
                    raise SemanticError('Is not possible to use AUTO_TYPE in a cast')
                if not obj_type.conforms_to(self.context.get_type(node.type)):
                    self.errors.append(INCOMPATIBLE_TYPES.replace('%s', obj_type.name, 1).replace('%s', node.type, 1))
            except SemanticError as ex:
                self.errors.append(ex.text)
                
        try:
            if node.type:
                obj_method = self.context.get_type(node.type).get_method(node.id)
            else:
                obj_method = obj_type.get_method(node.id)
            
            if len(node.args) == len(obj_method.param_types):
                for idx, arg in enumerate(node.args):
                    self.visit(arg, scope)
                    arg_type = arg.computed_type
                    param_type = obj_method.param_types[idx]
                    
                    if IsAuto(param_type.name):
                    	if not IsAuto(arg_type.name):
                    		obj_method.param_types[idx] = arg_type
                    else:
                    	if IsAuto(arg_type.name):
                    		self.update(arg, scope, param_type)
                    	else:
		                    if not arg_type.conforms_to(param_type):
		                        self.errors.append(INCOMPATIBLE_TYPES.replace('%s', arg_type.name, 1).replace('%s', param_type.name, 1))
            else:
                self.errors.append(f'Method "{obj_method.name}" of "{obj_type.name}" only accepts {len(obj_method.param_types)} argument(s)')
            
            node_type = obj_method.return_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()
            
        node.computed_type = node_type
    
    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        obj_type = self.current_type
        
        try:
            obj_method = obj_type.get_method(node.id)
            
            if len(node.args) == len(obj_method.param_types):
                for idx, arg in enumerate(node.args):
                    self.visit(arg, scope)
                    arg_type = arg.computed_type
                    param_type = obj_method.param_types[idx]
                    
                    if IsAuto(param_type.name):
                    	if not IsAuto(arg_type.name):
                    		obj_method.param_types[idx] = arg_type
                    else:
                    	if IsAuto(arg_type.name):
                    		self.update(arg, scope, param_type)
                    	else:
		                    if not arg_type.conforms_to(param_type):
		                        self.errors.append(INCOMPATIBLE_TYPES.replace('%s', arg_type.name, 1).replace('%s', param_type.name, 1))
            else:
                self.errors.append(f'Method "{obj_method.name}" of "{obj_type.name}" only accepts {len(obj_method.param_types)} argument(s)')
            
            node_type = obj_method.return_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()
            
        node.computed_type = node_type
    
    @visitor.when(IntegerNode)
    def visit(self, node, scope):
        node.computed_type = IntType()
        
    @visitor.when(StringNode)
    def visit(self, node, scope):
        node.computed_type = StringType()
        
    @visitor.when(BoolNode)
    def visit(self, node, scope):
        node.computed_type = BoolType()

    @visitor.when(IdNode)
    def visit(self, node, scope):
        if scope.is_defined(node.lex):
            var = scope.find_variable(node.lex)
            node_type = var.type       
        else:
            self.errors.append(VARIABLE_NOT_DEFINED.replace('%s', node.lex, 1))
            node_type = ErrorType()
        
        node.computed_type = node_type

    @visitor.when(NewNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            node_type = ErrorType()
            
        node.computed_type = node_type

class ComputedVisitor(FormatVisitor):
    def replace_auto(self, name):
        return 'Object' if IsAuto(name) else name

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
        real_type = self.replace_auto(node.scope.find_variable(node.id).type.name)
        ans = '\t' * tabs + f'\\__AttrDeclarationNode: {node.id} : {real_type} {text}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}' if body else f'{ans}'
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(':'.join(param) for param in node.params)
        real_type = self.replace_auto(node.method.return_type.name)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: {node.id}({params}) : {real_type} {{<body>}}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in node.body)
        return f'{ans}\n{body}'
    
    @visitor.when(IfThenElseNode)
    def visit(self, node, tabs=0):
        sons = [node.condition, node.if_body]
        text = ''
        if node.else_body:
            sons.append(node.else_body)
            text += 'else <body>'
        ans = '\t' * tabs + f'\\__IfThenElseNode: if <cond> then <body> {text} fi'
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

    @visitor.when(LetAttributeNode)
    def visit(self, node, tabs=0):
        sons = [node.expr] if node.expr else []
        text = '<- <expr>' if node.expr else ''
        real_type = self.replace_auto(node.scope.find_variable(node.id).type.name)
        ans = '\t' * tabs + f'\\__LetAttributeNode: {node.id} : {real_type} {text}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}' if body else f'{ans}'
    
    @visitor.when(AssignNode)
    def visit(self, node, tabs=0):
        sons = [node.expr]
        ans = '\t' * tabs + f'\\__AssignNode: {node.id} <- <expr>'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(UnaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__} <expr>'
        right = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{right}'
   
    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
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
        return f'{ans}\n{obj}\n{args}'

    @visitor.when(MemberCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MemberCallNode: {node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'
    
    @visitor.when(NewNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__NewNode: new {node.type}()'
