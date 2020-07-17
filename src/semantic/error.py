""" Defines the ContextError and SemanticError reported in Visitors """

class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class ContextError(Exception):
    @property
    def text(self):
        return self.args[0]

class ScopeError(Exception):
    @property
    def text(self):
        return self.args[0]