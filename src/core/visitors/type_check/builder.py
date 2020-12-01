from .utils import *
from ...visitors import visitor
from ...cmp import CoolUtils as cool, SemanticError, empty_token, ErrorType

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
    
    @visitor.when(cool.ProgramNode)
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
                self.errors.append((SemanticError('Method "main" must takes no formal parameters'), tmethod))
        except TypeError:
            self.errors.append((SemanticError('No definition for class "Main"'), empty_token))
        except KeyError:
            self.errors.append((SemanticError('Class "Main" must have a method "main"'), main_token))         
    
    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        
        if node.parent:
            if node.parent in sealed:
                self.errors.append((SemanticError(f'Is not possible to inherits from "{node.parent}"'), node.tparent))
                node.parent = 'Object'
            try:
                parent_type = self.context.get_type(node.parent)
                self.current_type.set_parent(parent_type)
            except TypeError as ex:
                self.errors.append((ex, node.tparent))
        
        for feature in node.features:
            self.visit(feature)
            
    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except TypeError as ex:
            self.errors.append((ex, node.ttype))
            attr_type = ErrorType()
        node.attr_type = attr_type

        try:
            if node.id == 'self':
                raise SemanticError(SELF_IS_READONLY)
            attr = self.current_type.define_attribute(node.id, attr_type)
            attr.node = node
            node.attr = attr
        except SemanticError as ex:
            self.errors.append((ex, node.tid))
        
    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node):
        arg_names, arg_types, arg_nodes = [], [], []
        for i, arg in enumerate(node.params):
            idx, typex = arg
            try:
                assert typex != ST
                arg_type = self.context.get_type(typex)
            except TypeError as ex:
                self.errors.append((ex, node.params[i].ttype))
                arg_type = ErrorType()
            except AssertionError:
                self.errors.append((SemanticError(INVALID_PARAMETER % (idx)), node.params[i].ttype))
                arg_type = ErrorType()

            if idx == 'self':
                self.errors.append((SemanticError('"self" cannot be the name of a formal parameter'), node.params[i].ttype))
            if idx in arg_names:
                self.errors.append((SemanticError(f'Formal parameter {idx} redefined'), node.params[i].ttype))
            arg_names.append(idx)
            arg_types.append(arg_type)
            arg_nodes.append(arg)
            arg.idx = i
            arg.method_types = arg_types
        
        try:
            ret_type = self.context.get_type(node.type)
        except TypeError as ex:
            self.errors.append((ex, node.ttype))
            ret_type = ErrorType()
        node.ret_type = ret_type
        node.arg_types = arg_types
        node.arg_names = arg_names
        node.arg_nodes = arg_nodes

        try:
            if node.id == 'self':
                raise SemanticError('"self" is an invalid method name')
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
            self.errors.append((ex, node.tid))
