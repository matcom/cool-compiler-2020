from ...visitors import visitor
from ...cmp import CoolUtils as cool

#AST Printer
class FormatVisitor:
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(cool.ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.declarations)
        return f'{ans}\n{statements}'
    
    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node, tabs=0):
        parent = '' if node.parent is None else f"inherits {node.parent}"
        ans = '\t' * tabs + f'\\__ClassDeclarationNode: class {node.id} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(self.visit(child, tabs + 1) for child in node.features)
        return f'{ans}\n{features}'
    
    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node, tabs=0):
        sons = [node.expr] if node.expr else []
        text = '<- <expr>' if node.expr else ''
        ans = '\t' * tabs + f'\\__{node.__class__.__name__}: {node.id} : {node.type} {text}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}' if body else f'{ans}'
    
    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(' : '.join(param) for param in node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: {node.id}({params}) : {node.type} {{<body>}}'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'
    
    @visitor.when(cool.IfThenElseNode)
    def visit(self, node, tabs=0):
        sons = [node.condition, node.if_body, node.else_body]
        ans = '\t' * tabs + f'\\__IfThenElseNode: if <cond> then <body> else <body> fi'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(cool.WhileLoopNode)
    def visit(self, node, tabs=0):
        sons = [node.condition, node.body]
        ans = '\t' * tabs + f'\\__WhileLoopNode: while <cond> loop <body> pool'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(cool.BlockNode)
    def visit(self, node, tabs=0):
        sons = node.exprs
        ans = '\t' * tabs + f'\\__BlockNode: {{<expr> ... <expr>}}'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(cool.LetInNode)
    def visit(self, node, tabs=0):
        sons = node.let_body + [node.in_body]
        ans = '\t' * tabs + f'\\__LetInNode: let {{<attr> ... <attr>}} in <expr>'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(cool.CaseOfNode)
    def visit(self, node, tabs=0):
        sons = [node.expr] + node.branches
        ans = '\t' * tabs + f'\\__CaseOfNode: case <expr> of {{<case> ... <case>}} esac'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(cool.CaseExpressionNode)
    def visit(self, node, tabs=0):
        sons = [node.expr]
        ans = '\t' * tabs + f'\\__CaseExpressionNode: {node.id} : {node.type} => <expr>'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(cool.AssignNode)
    def visit(self, node, tabs=0):
        sons = [node.expr]
        ans = '\t' * tabs + f'\\__AssignNode: {node.id} = <expr>'
        body = '\n'.join(self.visit(child, tabs + 1) for child in sons)
        return f'{ans}\n{body}'
    
    @visitor.when(cool.UnaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__}: {node.symbol.lex} <expr>'
        right = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{right}'
   
    @visitor.when(cool.BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__}: <expr> {node.symbol.lex} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(cool.AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
    
    @visitor.when(cool.FunctionCallNode)
    def visit(self, node, tabs=0):
        obj = self.visit(node.obj, tabs + 1)
        ans = '\t' * tabs + f'\\__FunctionCallNode: <obj>.{node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        ans = f'{ans}\n{obj}'
        if args: ans += f'\n{args}'
        return ans

    @visitor.when(cool.MemberCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MemberCallNode: {node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        if args: ans += f'\n{args}'
        return ans
    
    @visitor.when(cool.NewNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__NewNode: new {node.type}()'
