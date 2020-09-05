from print_tree import PrintTree

class PrintAst(PrintTree):
    def get_children(self, node):
        return node.get_children()

    def get_node_str(self, node):
        return repr(node)
