import cmp.visitor as visitor

def get_printer(ConstantNumberNode, BinaryNode):

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node, tabs):
            pass

        @visitor.when(BinaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + '\\__' + '<expr> '+ node.__class__.__name__ +' <expr>\n' + self.visit(node.left, tabs +1) + '\n' + self.visit(node.right, tabs + 1)
            return ans

        @visitor.when(ConstantNumberNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + '\\__' + 'num: ' + node.lex

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))