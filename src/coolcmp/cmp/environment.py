class Environment:
    def __init__(self, parent=None):
        self.map = {}
        self.parent = parent
        self.definitions = 0

    def define(self, name, ref):
        self.map[name] = ref
        self.definitions += 1

    def get(self, name):
        if name in self.map:
            return self.map[name]
            
        if self.parent:
            return self.parent.get(name)

        return None