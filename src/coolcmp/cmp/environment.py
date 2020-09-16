class Environment:
    def __init__(self, parent=None):
        self.map = {}
        self.parent = parent

    def define(self, name, ref):
        self.map[name] = ref

    def get(self, name):
        if name in self.map:
            return self.map[name]
            
        if self.parent:
            return self.parent.get(name)

        return None