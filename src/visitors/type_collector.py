from semantic import *

import visitors.visitor as visitor
from pipeline import State
from cl_ast import *

class TypeCollector(State):
    def __init__(self):
        self.context = None

    def run(self, inputx):
        pass

    # Visit Node Functions