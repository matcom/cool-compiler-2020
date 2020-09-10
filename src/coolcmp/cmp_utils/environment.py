class Environment:
    def __init__(self):
        self.vars = {}
        self.parent = None

    def define(self, name, value=None): ...
    def is_defined(self, name): ...
    def get(self, name): ...

class SemanticsEnv(Environment):
    def define(self, name, value=None):
        assert(not self.is_defined(name))
        self.vars[name] = True

    def is_defined(self, name):
        return name in self.vars

    def get(self, name):
        if self.is_defined(name):
            return True
            
        if self.parent:
            return self.parent.get(name)

        return False