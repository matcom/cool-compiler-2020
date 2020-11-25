class Var:
    def __init__(self, idx, local_name):
        self.id = idx
        self.local_name = local_name

    def __str__(self):
        return f'[var] {self.id}: {self.local_name}'

    def __repr__(self):
        return str(self)


class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}

    def child(self):
        return Scope(parent=self)

    def define_var(self, name, local_name):
        var = self.vars[name] = Var(name, local_name)
        return var

    def get_var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            if self.parent is not None:
                return self.parent.get_var(name)
            return None

    def __str__(self):
        return '{\n' + ('\t' if self.parent is None else 'Parent:\n' + f'{self.parent}\n\t') + '\n\t'.join(str(x) for x in self.vars.values()) + '\n}'

    def __repr__(self):
        return str(self)
