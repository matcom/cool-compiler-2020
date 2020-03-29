""" Defines the base Semantic Error reported in Visitors """

class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]