from .semantic_utils import Context, SemanticException, Type, ErrorType, VoidType
from ..utils import on, when
from ..errors import SemanticError, CTypeError
from ..ast import ProgramNode, ClassDeclarationNode, FuncDeclarationNode, AttrDeclarationNode

class COOL_TYPE_BUILDER(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    def build_basic_types(self):
        strt = self.context.get_type('String')
        intt = self.context.get_type('Int')
        objt = self.context.get_type('Object')
        iot = self.context.get_type('IO')
        bt = self.context.get_type('Bool')
        # Int
        intt.set_parent(objt)
        # Bool
        bt.set_parent(objt)
        # Object
        objt.define_method('abort', [], [], objt)
        objt.define_method('type_name', [], [], strt)
        objt.define_method('copy', [], [], objt) # Is SELF_TYPE in the manual
        # IO
        iot.define_method('in_string', [], [], strt)
        iot.define_method('out_string', ['x'], [strt], iot) # Is SELF_TYPE in the manual
        iot.define_method('in_int', [], [], intt)
        iot.define_method('out_int', ['x'], [intt], iot) # Is SELF_TYPE in the manual
        iot.set_parent(objt)
        # String
        strt.define_method('length', [], [], intt)
        strt.define_method('concat', ['s'], [strt], strt)
        strt.define_method('substr', ['i', 'l'], [intt, intt], strt)
        strt.set_parent(objt)

    @on('node')
    def visit(self, node):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.build_basic_types()
        for class_def in node.classes:
            self.visit(class_def)
        try:
            self.context.get_type('Main')
            try:
                self.context.get_type('Main').get_method('main')
            except SemanticException as e:
                self.errors.append(SemanticError(node.line, node.column, e.text))
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))
    
    @when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        try:
            typex = self.context.get_type(node.id)
            self.current_type = typex
            parent_type = self.context.get_type(node.parent) if node.parent is not None else self.context.get_type('Object')
            typex.set_parent(parent_type)
        except SemanticException as e:
            if self.current_type and  node.parent in ['Int', 'String', 'Bool']:
                self.errors.append(SemanticError(node.line, node.column, e.text))
            else:
                self.errors.append(CTypeError(node.line, node.column, e.text))
        for feature in node.features:
            self.visit(feature)
    
    @when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode):
        atype = None
        try:
            atype = self.context.get_type(node.type)
        except SemanticException as e:
            atype = ErrorType()
            self.errors.append(CTypeError(node.line, node.column, e.text))
        try:
            self.current_type.define_attribute(node.id, atype)
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))
    
    @when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode):
        ret_type = ErrorType()
        params_type = [ErrorType()]*len(node.params)
        params_id = []
        try:
            ret_type = self.context.get_type(node.type) if node.type != 'void' else VoidType()
        except SemanticException as e:
            self.errors.append(CTypeError(node.line, node.column, e.text))
        for ind, param in enumerate(node.params):
            try:
                params_id.append(param.id)
                params_type[ind] = self.context.get_type(param.type)
            except SemanticException as e:
                self.errors.append(CTypeError(param.line, param.column, e.text))
        try:
            self.current_type.define_method(node.id, params_id, params_type, ret_type)
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))
