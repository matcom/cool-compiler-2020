from .utils import *
from ...visitors import visitor
from ...cmp import cool_ast as cool, empty_token, Context, SemanticError
from ...cmp import IntType, StringType, BoolType, IOType, VoidType, AutoType, SelfType

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
    st = context.append_type(SelfType())
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
    
    @visitor.when(cool.ProgramNode)
    def visit(self, node):
        self.context = Context()
        define_built_in_types(self.context)
        
        for def_class in node.declarations:
            self.visit(def_class)
             
        # comparison for sort node.declarations
        def get_type_level(typex, error_token=empty_token):
            try:
                parent = self.type_level[typex]
            except KeyError:
                return 0
            
            if parent == 0:
                node = self.parent[typex]
                node.parent = "Object"
                self.errors.append((SemanticError('Cyclic heritage.'), error_token))
            elif type(parent) is not int:
                self.type_level[typex] = 0 if parent else 1
                if type(parent) is str:
                    self.type_level[typex] = get_type_level(parent, self.parent[typex].tid) + 1
            
            return self.type_level[typex]
        
        node.declarations.sort(key = lambda node: get_type_level(node.id))               
                
    @visitor.when(cool.ClassDeclarationNode)
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
                self.errors.append((ex, node.tid))
                make_a_duplicate()
        else:
            self.errors.append((SemanticError(f'{node.id} is an invalid class name'), node.tid))
            make_a_duplicate()
