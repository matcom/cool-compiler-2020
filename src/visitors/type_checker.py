from semantic import *

import visitor
from pipeline import State
from src.cl_ast import *

class TypeChecker(State):
    def __init__(self):
        self.context = None
        self.current_type = None
        self.current_method = None

    def run(self, inputx):
        # ast, context = inputx
        pass