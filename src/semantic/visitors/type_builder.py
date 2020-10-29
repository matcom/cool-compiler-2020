from utils.errors import SemanticError, AttributesError, TypesError, NamesError
from semantic.types import Type, VoidType, ErrorType, Attribute, Method
from semantic.tools import Context
from utils import visitor 
from utils.ast import *

class TypeBuilder:
    def __init__(self, context:Context, errors=[]):
        self.context:Context = context
        self.current_type:Type = None
        self.errors:list = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        for dec in node.declarations:
            self.visit(dec)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode):
        try:
            self.current_type = self.context.get_type(node.id, node.pos)
        except SemanticError as e:
            self.current_type = ErrorType()
            self.errors.append(e)
        
        if node.parent is not None:
            try:
                parent = self.context.get_type(node.parent, node.parent_pos)
                current = parent
                while current is not None:
                    if current.name == self.current_type.name:
                        error_text = TypesError.CIRCULAR_DEPENDENCY %(parent.name, self.current_type.name) 
                        raise TypesError(error_text, *node.pos)
                    current = current.parent
            except SemanticError as e:
                parent = ErrorType()
                self.errors.append(e)
            self.current_type.set_parent(parent)
        
        for feature in node.features:
            self.visit(feature)
    

    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode):
        args_names = []
        args_types = []
        for name, type_ in node.params:
            try:
                args_names.append(name)
                args_types.append(self.context.get_type(type_.value, type_.pos))
            except SemanticError as e:
                args_types.append(ErrorType(type_.pos))
                self.errors.append(e)
        
        try:
            return_type = self.context.get_type(node.type, node.type_pos)
        except SemanticError as e:
            return_type = ErrorType(node.type_pos)
            self.errors.append(e)
    
        try:
            self.current_type.define_method(node.id, args_names, args_types, return_type)
        except SemanticError as e:
            self.errors.append(e)
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode):
        try:
            attr_type = self.context.get_type(node.type, node.pos)
        except SemanticError as e:
            attr_type = ErrorType(node.type_pos)
            self.errors.append(e)
        
        try:
            self.current_type.define_attribute(node.id, attr_type, node.pos)
        except SemanticError as e:
            self.errors.append(e)