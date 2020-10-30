class CILScope:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = []

    def add_var(self, var):
        self.vars.append(var)

    def get_full_name(self, var_name: str):
        for name in self.vars:
            if var_name == name.split('_')[2]:
                return name
        if self.parent:
            return self.parent.get_full_name(var_name)
        return ''