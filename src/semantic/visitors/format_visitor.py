from utils import visitor 
from utils.ast import *

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__}'
        return ans
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.declarations)
        return f'{ans}\n{statements}'
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tabs=0):
        parent = '' if node.parent is None else f": {node.parent}"
        ans = '\t' * tabs + f'\\__ClassDeclarationNode: class {node.id} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(self.visit(child, tabs + 1) for child in node.features)
        return f'{ans}\n{features}'
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AttrDeclarationNode: {node.id} : {node.type}'
        return f'{ans}'
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: {node.id} : {node.type} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(AssignNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssignNode: {node.id} <- <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(':'.join(param) for param in node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: {node.id}({params}) : {node.type} -> <body>'
        body = f'{self.visit(node.body, tabs + 1)}'
        # body = f'\n'#{self.visit(node.body, tabs + 1)}' #.join(self.visit(child, tabs + 1) for child in node.body)
        return f'{ans}\n{body}'

    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(UnaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__} <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(WhileNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__}: while <cond> loop <expr> pool'
        cond = self.visit(node.cond, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{cond}\n{expr}'
    
    @visitor.when(ConditionalNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ {node.__class__.__name__}: if <cond> then <expr> else <expr> fi'
        cond = self.visit(node.cond, tabs + 1)
        stm = self.visit(node.stm, tabs + 1)
        else_stm = self.visit(node.else_stm, tabs + 1)
        return f'{ans}\n{cond}\n{stm}\n{else_stm}'

    @visitor.when(CaseNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ {node.__class__.__name__}: case <expr> of <case-list> esac'
        expr = self.visit(node.expr, tabs + 1)
        case_list = '\n'.join(self.visit(child, tabs + 1) for child in node.case_list)
        return f'{ans}\n{expr}\n{case_list}'

    @visitor.when(OptionNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.id} : {node.typex} -> <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(BlockNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ {node.__class__.__name__} ' + '{ <expr_list> }'
        expr = '\n'.join(self.visit(child, tabs + 1) for child in node.expr_list)
        return f'{ans}\n{expr}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
    
    @visitor.when(BaseCallNode)
    def visit(self, node, tabs=0):
        obj = self.visit(node.obj, tabs + 1)
        ans = '\t' * tabs + f'\\__BaseCallNode: <obj>@{node.type}.{node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{obj}\n{args}'

    @visitor.when(CallNode)
    def visit(self, node, tabs=0):
        obj = self.visit(node.obj, tabs + 1)
        ans = '\t' * tabs + f'\\__CallNode: <obj>.{node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{obj}\n{args}'
    
    @visitor.when(StaticCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__StaticCallNode: {node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'

    @visitor.when(InstantiateNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ InstantiateNode: new {node.lex}()'

    @visitor.when(LetNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ {node.__class__.__name__} let <init_list> in <expr>'
        init_list = '\n'.join(self.visit(arg, tabs + 1) for arg in node.init_list)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{init_list}\n{expr}'
