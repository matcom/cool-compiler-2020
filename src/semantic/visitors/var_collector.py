from semantic.visitors import visitor
from semantic.tools import *
from semantic.types import Type, ErrorType
from utils.errors import SemanticError, AttributesError, TypesError, NamesError
from utils.ast import *

class VarCollector:
    def __init__(self, context=Context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope:Scope=None):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    
    def copy_scope(self, scope:Scope, parent:Type):
        if parent is None:
            return
        for attr in parent.attributes:
            if scope.find_variable(attr.name) is None:
                scope.define_attribute(attr)
        self.copy_scope(scope, parent.parent)


    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):
        self.current_type = self._get_type(node.id, node.pos)
        scope.define_variable('self', self.current_type)
        
        for feat in node.features:
            if isinstance(feat, AttrDeclarationNode):
                self.visit(feat, scope)
        
        self.copy_scope(scope, self.current_type.parent)
        
        for feat in node.features:
            if isinstance(feat, FuncDeclarationNode):
                self.visit(feat, scope)


        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode, scope:Scope):
        scope.define_attribute(self.current_type.get_attribute(node.id, node.pos))

        
    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode, scope:Scope):
        # Ver si el método está definido en el padre
        parent = self.current_type.parent 
        pnames = [param[0] for param in node.params]
        ptypes = [param[1] for param in node.params]

        self.current_method = self.current_type.get_method(node.id, node.pos)

        new_scope = scope.create_child()
        scope.functions[node.id] = new_scope

        # Añadir las variables de argumento
        for pname, ptype in node.params:
            new_scope.define_variable(pname, self._get_type(ptype.value, ptype.pos))
            
        self.visit(node.body, new_scope)
  
        
    def _get_type(self, ntype, pos):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()
        
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node:VarDeclarationNode, scope:Scope):
        if node.id == 'self':
            error_text = SemanticError.SELF_IS_READONLY
            self.errors.append(SemanticError(error_text, *node.pos))
            return
        
        if scope.is_defined(node.id):
            var = scope.find_variable(node.id)
            if var.type != ErrorType():
                error_text = SemanticError.LOCAL_ALREADY_DEFINED %(node.id, self.current_method.name) 
                self.errors.append(SemanticError(error_text, *node.pos))        
            return

        vtype = self._get_type(node.type, node.type_pos)
        var_info = scope.define_variable(node.id, vtype)
       
        if node.expr != None:
            self.visit(node.expr, scope)
            
        
    @visitor.when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        if node.id == 'self':
            error_text = SemanticError.SELF_IS_READONLY
            self.errors.append(SemanticError(error_text, *node.pos))
            return
    
        vinfo = scope.find_variable(node.id)
        if vinfo is None:
            error_text = NamesError.VARIABLE_NOT_DEFINED %(node.id, self.current_method.name)  
            self.errors.append(NamesError(error_text, *node.pos))
            vtype = ErrorType()
            scope.define_variable(node.id, vtype)
        else:
            vtype = vinfo.type
            
        self.visit(node.expr, scope)
    
    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, scope:Scope):
        for exp in node.expr_list:
            self.visit(exp, scope)
    

    @visitor.when(LetNode)
    def visit(self, node:LetNode, scope:Scope):
        n_scope = scope.create_child()
        scope.expr_dict[node] = n_scope
        for init in node.init_list:
            self.visit(init, n_scope)
        
        self.visit(node.expr, n_scope)

    #no necesario
    @visitor.when(BinaryNode)
    def visit(self, node:BinaryNode, scope:Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    
    @visitor.when(UnaryNode)
    def visit(self, node:UnaryNode, scope:Scope):
        self.visit(node.expr, scope)
     

    @visitor.when(VariableNode)
    def visit(self, node:VariableNode, scope:Scope):
        if not scope.is_defined(node.lex):
            error_text = NamesError.VARIABLE_NOT_DEFINED %(node.lex, self.current_method.name)
            self.errors.append(NamesError(error_text, *node.pos))
            vinfo = scope.define_variable(node.lex, ErrorType(node.pos))
        else:
            vinfo = scope.find_variable(node.lex)
        return vinfo.type


    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope:Scope):
        self.visit(node.cond, scope)
        self.visit(node.expr, scope)


    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope:Scope):
        self.visit(node.cond, scope)
        self.visit(node.stm, scope)
        self.visit(node.else_stm, scope)

    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode, scope:Scope):
        self.visit(node.expr, scope)
    
    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope:Scope):
        self.visit(node.obj, scope)
        for arg in node.args:
            self.visit(arg, scope)


    @visitor.when(BaseCallNode)
    def visit(self, node:BaseCallNode, scope:Scope):
        self.visit(node.obj, scope)
        for arg in node.args:
            self.visit(arg, scope)
    

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode, scope:Scope):
        for arg in node.args:
            self.visit(arg, scope)


    @visitor.when(CaseNode)
    def visit(self, node:CaseNode, scope:Scope):
        self.visit(node.expr, scope)

        new_scp = scope.create_child()
        scope.expr_dict[node] = new_scp

        for case in node.case_list:
            self.visit(case, new_scp.create_child())
        

    @visitor.when(OptionNode)
    def visit(self, node:OptionNode, scope:Scope):
        typex = self.context.get_type(node.typex, node.type_pos)
        
        self.visit(node.expr, scope)
        scope.define_variable(node.id, typex)


    