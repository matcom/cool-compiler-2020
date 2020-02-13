import tools.visitor as visitor

def get_printer(AtomicNode=(), UnaryNode=(), BinaryNode=(), ):

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node, tabs):
            pass

        @visitor.when(UnaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            child = self.visit(node.node, tabs + 1)
            return f'{ans}\n{child}'

        @visitor.when(BinaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(AtomicNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))