from engine.cp import ErrorType, SelfType, SemanticError, visitor
from engine.parser import AttrDeclarationNode, FuncDeclarationNode, ProgramNode, ClassDeclarationNode
from engine.semantic_errors import ERROR_ON_LN_COL

class Builder:
    def __init__(self, context, errors = []):
        self.context = context
        self.current_type = None
        self.errors = errors

        #Construyendo tipos Build-In

        self.object_type = self.context.get_type('Object')
        
        self.io_type = self.context.get_type('IO')
        self.io_type.set_parent(self.object_type)

        self.int_type = self.context.get_type('Int')
        self.int_type.set_parent(self.object_type)
        self.int_type.sealed = True

        self.string_type = self.context.get_type('String')
        self.string_type.set_parent(self.object_type)
        self.string_type.sealed = True

        self.bool_type = self.context.get_type('Bool')
        self.bool_type.set_parent(self.object_type)
        self.bool_type.sealed = True

        self.object_type.define_method('abort', [], [], self.object_type)
        self.object_type.define_method('type_name', [], [], self.string_type)
        self.object_type.define_method('copy', [], [], SelfType())
        
        self.io_type.define_method('out_string', ['x'], [self.string_type], SelfType())
        self.io_type.define_method('out_int', ['x'], [self.int_type], SelfType())
        self.io_type.define_method('in_string', [], [], self.string_type)
        self.io_type.define_method('in_int', [], [], self.int_type)

        self.string_type.define_method('length', [], [], self.int_type)
        self.string_type.define_method('concat', ['s'], [self.string_type], self.string_type)
        self.string_type.define_method('substr', ['i', 'l'], [self.int_type, self.int_type], self.string_type)

    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for class_def in node.declarations:
            self.visit(class_def)
        try:
            self.context.get_type('Main').get_method('main')
        except SemanticError:
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "SemanticError: Class Main and feature main needed")

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id.lex)

        parent = node.parent
        if parent:
            parent_type = None
            try:
                parent_type = self.context.get_type(parent.lex)
                self.current_type.set_parent(parent_type)
            except SemanticError as se:
                if self.current_type and parent_type != None and parent_type.sealed:
                    self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "SemanticError: " + se.text)
                else:
                    self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "TypeError: " + se.text)
                self.current_type.set_parent(self.object_type)
        else:
            self.current_type.set_parent(self.object_type)

        for feature in node.features:
            self.visit(feature)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type.lex)
        except SemanticError as se:
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "TypeError: " + se.text)
            attr_type = ErrorType()

        try:
            self.current_type.define_attribute(node.id.lex, attr_type)
        except SemanticError as se:
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "SemanticError: " + se.text)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        arg_names, arg_types = [], []
        for ids, types in node.params:
            try:
                arg_type = self.context.get_type(types.lex)
            except SemanticError as se:
                self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "TypeError: " + se.text)
                arg_type = ErrorType()
            else:
                if isinstance(arg_type, SelfType):
                    self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "SemanticError: " + f'Type "{arg_type.name}" can not be used as a parameter type')
                    arg_type = ErrorType()
            
            arg_names.append(ids.lex)
            arg_types.append(arg_type)
    
        try:
            ret_type = self.context.get_type(node.type.lex)
        except SemanticError as se:
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "TypeError: " + se.text)
            ret_type = ErrorType()
        
        try:
            self.current_type.define_method(node.id.lex, arg_names, arg_types, ret_type)
        except SemanticError as se:
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "SemanticError: " + se.text)