from semantic import *

import visitor
from pipeline import State
from src.cl_ast import *

class TypeCollector(State):
    def __init__(self):
        self.context = None

    def run(self, inputx):
        pass

    # Visit Node Functions