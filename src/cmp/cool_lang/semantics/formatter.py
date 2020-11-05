from ..utils import on, when
from ..ast import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode, \
                    BinaryNode, UnaryNode, IfThenElseNode, WhileLoopNode, BlockNode, LetInNode,\
                    CaseOfNode, LetNode, CaseNode, AssignNode, FunctionCallNode, NewNode,      \
                    AtomicNode, MemberCallNode


class COOL_FORMATTER(object):
    @on('node')
    def visit(self, node, tabs):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode, tabs=0):
        ans = '\t' * tabs + '\\_ProgramNode [class, ..., class]'
        class_list = '\n'.join([ self.visit(xclass, tabs + 1) for xclass in node.classes])
        return f'{ans}\n{class_list}'

    @when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, tabs=0):
        inherits = f'child of {node.parent} ' if node.parent else ''
        ans = '\t' * tabs + f'\\_ClassDeclarationNode {node.id} {inherits}[feature, ..., feature]'
        features = '\n'.join([ self.visit(feature, tabs + 1) for feature in node.features])
        return f'{ans}\n{features}'

    @when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, tabs=0):
        expr = f'\n{self.visit(node.expression, tabs + 1)}' if node.expression else ''
        return '\t' * tabs + f'\\_AttrDeclarationNode {node.id}: {node.type}{expr}'

    @when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, tabs=0):
        params = ', '.join([f'{param.id}:{param.type}' for param in node.params ])
        ans = '\t' * tabs + f'\\_FuncDeclarationNode {node.id} ({params}) {node.type}'
        expr = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{expr}'

    @when(IfThenElseNode)
    def visit(self, node: IfThenElseNode, tabs=0):
        ans = '\t' * tabs + '\\_IfThenElseNode'
        cond = self.visit(node.condition, tabs + 1)
        then = self.visit(node.if_body, tabs + 1)
        xelse = self.visit(node.else_body, tabs + 1)
        return f'{ans}\n{cond}\n{then}\n{xelse}'

    @when(WhileLoopNode)
    def visit(self, node: WhileLoopNode, tabs=0):
        ans = '\t' * tabs + f'\\_WhileLoopNode'
        cond = self.visit(node.condition, tabs + 1)
        do = '\t' * tabs + 'DO'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{cond}\n{do}\n{body}'

    @when(BlockNode)
    def visit(self, node: BlockNode, tabs=0):
        ans = '\t' * tabs + '\\_BlockNode'
        exprs = '\n'.join([ self.visit(expr, tabs + 1) for expr in node.expressions ])
        return f'{ans}\n{exprs}'

    @when(LetNode)
    def visit(self, node: LetNode, tabs=0):
        ans = '\t' * tabs + f'\\_LetNode var {node.id} of type {node.type}'
        expr = ''
        if node.expression:
            expr = f' equal to\n {self.visit(node.expression, tabs + 1)}'
        return f'{ans}{expr}'
        
    @when(LetInNode)
    def visit(self, node: LetInNode, tabs=0):
        ans = '\t' * tabs + '\\_LetInNode'
        lets = '\n'.join([ self.visit(let, tabs + 1) for let in node.let_body ])
        xin = '\t' * tabs + 'IN'
        body = self.visit(node.in_body, tabs + 1)
        return f'{ans}\n{lets}\n{xin}\n{body}'

    @when(CaseNode)
    def visit(self, node: CaseNode, tabs=0):
        ans = '\t' * tabs + f'\\_CaseNode case {node.id} of type {node.type} equal to'
        expr = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{expr}'

    @when(CaseOfNode)
    def visit(self, node: CaseOfNode, tabs=0):
        ans = '\t' * tabs + '\\_CaseOfNode'
        expr = self.visit(node.expression, tabs + 1)
        of = '\t' * tabs + 'OF'
        body = '\n'.join([ self.visit(case, tabs + 1) for case in node.cases ])
        return f'{ans}\n{expr}\n{of}\n{body}'

    @when(AssignNode)
    def visit(self, node: AssignNode, tabs=0):
        ans = '\t' * tabs + f'\\_AssignNode var {node.id} equal to'
        expr = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{expr}'

    @when(MemberCallNode)
    def visit(self, node: MemberCallNode, tabs=0):
        ans = '\t' * tabs + f'\\MemberCallNode {node.id} with args'
        args = '\n'.join([ self.visit(arg, tabs + 1) for arg in node.args ])
        return f'{ans}\n{args}'

    @when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, tabs=0):
        ans = '\t' * tabs + '\\_FunctionCallNode from object'
        obj = self.visit(node.obj, tabs + 1)
        xid = '\t' * tabs + f'Calling function {node.id}{f" as type {node.type}" if node.type else ""}'
        args = '\n'.join([ self.visit(arg, tabs + 1) for arg in node.args ])
        return f'{ans}\n{obj}\n{xid}\n{args}'

    @when(NewNode)
    def visit(self, node: NewNode, tabs=0):
        ans = '\t' * tabs + f'\\_NewNode of Type {node.type}'
        return f'{ans}'

    @when(AtomicNode)
    def visit(self, node: AtomicNode, tabs=0):
        ans = '\t' * tabs + f'\\_{node.__class__.__name__} {node.token}'
        return f'{ans}'

    @when(UnaryNode)
    def visit(self, node: UnaryNode, tabs=0):
        ans = '\t' * tabs + f'\\_{node.__class__.__name__}'
        expr = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{expr}'

    
    @when(BinaryNode)
    def visit(self, node: BinaryNode, tabs=0):
        ans = '\t' * tabs + f'\\_{node.__class__.__name__}'
        expr1 = self.visit(node.left, tabs + 1)
        expr2 = self.visit(node.right, tabs + 1)
        return f'{ans}\n{expr1}\n{expr2}'
