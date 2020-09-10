class Visitor:
    def visit(self, node):
        fn = getattr(self, 'visit_' + node.__class__.__name__)
        return fn(node)