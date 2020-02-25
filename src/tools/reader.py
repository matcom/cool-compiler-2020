from tools.cmp_errors import CompilerError
from pipeline import State

class Reader(State):
    def __init__(self, name):
        super().__init__(name)

    def run(self, path):
        try:
            raw = open(path).read()
            return raw
        except:
            self.errors.append(CompilerError(0, 0, 'Missing input file'))
            self.stop = True # stop pipeline