from .formatter import COOL_FORMATTER
from ..errors import SemanticError

class COOL_CHECKER:
    def __init__(self):
        self.errors = []

    def check_semantics(self, program):
        self.errors.clear()
        # All semantics checks here
        print(COOL_FORMATTER().visit(program))
        return not len(self.errors) > 0
