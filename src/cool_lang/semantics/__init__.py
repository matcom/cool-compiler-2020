from .formatter import COOL_FORMATTER
from .type_collector import COOL_TYPE_COLLECTOR
from .type_builder import COOL_TYPE_BUILDER
from .type_checker import COOL_TYPE_CHECKER
from ..errors import SemanticError

class COOL_CHECKER:
    def __init__(self):
        self.errors = []

    def check_semantics(self, program, verbose=False):
        self.errors.clear()
        # All semantics checks here
        if verbose:
            print(COOL_FORMATTER().visit(program, tabs=0))
        context = COOL_TYPE_COLLECTOR(errors=self.errors).visit(program)
        COOL_TYPE_BUILDER(context=context, errors=self.errors).visit(program)
        COOL_TYPE_CHECKER(context, errors=self.errors).visit(program)
        if verbose:
            print(context)
        return not len(self.errors) > 0
