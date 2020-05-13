from ..errors import SemanticError

class COOL_CHECKER:
    def __init__(self):
        self.errors = []

    def check_semantics(self, program):
        self.errors.clear()
        # All semantics checks here
        return len(self.errors) > 0
        return not len(self.errors) > 0
