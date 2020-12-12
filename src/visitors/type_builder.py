from semantic import *

import visitors.visitor as visitor
from pipeline import State
from cl_ast import *
from tools.cmp_errors import *

class TypeBuilder(State):
    def __init__(self, name):
        super().__init__(name)

    def run(self, inputx):
        ast, context = inputx
        self.context = context
        self.visit(ast)
        return ast, self.context

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        builder = Builder(self.context)
        inherit = InheritBuilder(self.context)
        builder.visit(node)
        inherit.visit(node)
        self.errors = builder.errors + inherit.errors

class Builder:
    def __init__(self, context):
        self.errors = [ ]
        self.context = context
        self.current_type = None
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for dec in node.declarations:
            self.visit(dec)   
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        # set current type for this class declaration
        self.current_type = self.context.get_type(node.id)
        # visit func declarations and attr declarations for this class
        for feature in node.features:
            self.visit(feature)
        # compute parent
        if node.parent:
            try:
                parent = self.context.get_type(node.parent)
                current = parent
                while current:
                    if current.name == self.current_type.name:
                        self.errors.append(CSemanticError(node.parent_pos[0], node.parent_pos[1], (f'{current.name} is involved in inheritance cycle')))
                        break
                    current = current.parent
            except ContextError as e:
                parent = ErrorType()
                self.errors.append(CTypeError(node.parent_pos[0], node.parent_pos[1], e.text)) # parent type missing
            
            if node.parent in ['Int', 'String', 'Bool']:
                self.errors.append(CSemanticError(node.parent_pos[0], node.parent_pos[1], 'Invalid inherit in basic classes'))

            self.current_type.set_parent(parent)
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        args_ids = []
        args_types = []
        for param in node.params:
            args_ids.append(param.id)
            try:
                args_types.append(self.context.get_type(param.type))
            except ContextError as e:
                args_types.append(ErrorType())
                self.errors.append(CTypeError(param.row, param.col, e.text))
        try:
            ret_type = self.context.get_type(node.type)
        except ContextError as e:
            ret_type = ErrorType()
            self.errors.append(CTypeError(node.type_pos[0], node.type_pos[1], e.text))
        try:
            self.current_type.define_method(node.id, args_ids, args_types, ret_type)
        except SemanticError as e:
            self.errors.append(CSemanticError(node.row, node.col, e.text))

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except ContextError as e:
            attr_type = ErrorType()
            self.errors.append(CTypeError(node.type_pos[0], node.type_pos[1], e.text))
        try:
            self.current_type.define_attribute(node.id, attr_type)
        except SemanticError as e:
            self.errors.append(CSemanticError(node.row, node.col, e.text))

class InheritBuilder:
    def __init__(self, context):
        self.errors = []
        self.context = context
        self.current_type = None
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for dec in node.declarations:
            self.visit(dec)   
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        # set current type for this class declaration
        self.current_type = self.context.get_type(node.id)
        parent = self.current_type.parent
        # visit func declarations and attr declarations for this class
        if node.parent and parent is not ErrorType():
            for feature in node.features:
                self.visit(feature)
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        # check correct override 
        parent = self.current_type.parent
        cmeth = self.current_type.get_method(node.id)
        
        try:
            pmeth = parent.get_method(node.id)
            if len(node.params) != len(pmeth.param_names):
                self.errors.append(CSemanticError(node.row, node.col, f"Incompatible number of formal parameters in redefined {node.id}"))
                raise SemanticError()    
            
            for param, base in zip(node.params, zip(pmeth.param_names, pmeth.param_types)):
                if param.type != base[1].name:
                    self.errors.append(CSemanticError(param.row, param.col, WRONG_SIGNATURE % (node.id, parent.name)))   

            # Return Type compare and report error
            if pmeth.return_type.name != node.type:
                self.errors.append(CSemanticError(node.type_pos[0], node.type_pos[1], WRONG_SIGNATURE % (node.id, parent.name)))

        except SemanticError:
            pass
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        parent = self.current_type.parent
        
        try:
            pattr = parent.get_attribute(node.id)
            if pattr:
                self.errors.append(CSemanticError(node.row, node.col, f"Cannot override attribute {node.id} in {self.current_type.name} from {parent.name}"))
        except SemanticError:
            pass