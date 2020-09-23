from semantic.tools import *
from semantic.types import Type, Method
from utils import visitor
from utils.ast import *

class SelfTypeVisitor(object):
    def __init__(self, context:Context, errors=[]):
        self.context:Context =  context
        self.errors = errors
        self.current_type:Type = None
        self.current_method:Method = None

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope:Scope):
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)


    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):
        self.current_type = self.context.get_type(node.id, node.pos)

        fd = [feat for feat in node.features if isinstance(feat, FuncDeclarationNode)]

        for feat in node.features:
            if isinstance(feat, AttrDeclarationNode):
                self.visit(feat, scope)

        for feat, child_scope in zip(fd, scope.children):
            self.visit(feat, child_scope)        


    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode, scope:Scope):
        vinfo = scope.find_variable(node.id)
        if node.type == 'SELF_TYPE':
            vinfo.type = self.current_type


    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode, scope:Scope):
        self.current_method = self.current_type.get_method(node.id, node.pos)

        for pname, ptype in node.params:
            if ptype.value == 'SELF_TYPE':
                varinfo = scope.find_variable(pname)
                varinfo.type = self.current_type
                self.current_type.change_type(self.current_method, pname, self.current_type)

           
        if node.type == 'SELF_TYPE':
            self.current_method.return_type = self.current_type 
         
        self.visit(node.body, scope)


    @visitor.when(VarDeclarationNode)
    def visit(self, node:VarDeclarationNode, scope:Scope):
        varinfo = scope.find_variable(node.id)

        if node.type == 'SELF_TYPE':
            varinfo.type = self.current_type

    @visitor.when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        varinfo = scope.find_variable(node.id)

        if varinfo.type.name == 'SELF_TYPE':
            varinfo.type = self.current_type


    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, scope:Scope):
        for exp in node.expr_list:
            self.visit(exp, scope)


    @visitor.when(LetNode)
    def visit(self, node:LetNode, scope:Scope):
        child_scope = scope.expr_dict[node]
        for init in node.init_list:
            self.visit(init, child_scope)
        self.visit(node.expr, child_scope)

    @visitor.when(CaseNode) 
    def visit(self, node:CaseNode, scope:Scope):
        self.visit(node.expr, scope)

        new_scope = scope.expr_dict[node]
        for case, c_scope in zip(node.case_list, new_scope.children):
            self.visit(case, c_scope)
        

    @visitor.when(OptionNode)
    def visit(self, node:OptionNode, scope:Scope):
        var_info = scope.find_variable(node.id)
        self.visit(node.expr)

        if var_info.type.name == 'SELF_TYPE':
            var_info.type = self.current_type
    
    @visitor.when(InstantiateNode)
    def visit(self, node:InstantiateNode, scope:Scope):
        node.lex = self.current_type.name if node.lex == 'SELF_TYPE' else node.lex