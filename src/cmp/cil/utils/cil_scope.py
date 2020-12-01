from typing import Dict, Optional


class Var:
    def __init__(self, idx: str, local_name: str):
        self.id = idx
        self.local_name = local_name

    def __str__(self):
        return f"[var] {self.id}: {self.local_name}"

    def __repr__(self):
        return str(self)


class Scope:
    def __init__(self, parent: Optional["Scope"] = None):
        self.parent = parent
        self.vars: Dict[str, Var] = {}

    def child(self):
        return Scope(parent=self)

    def define_var(self, name: str, local_name: str) -> Var:
        var = self.vars[name] = Var(name, local_name)
        return var

    def get_var(self, name: str) -> Optional[Var]:
        try:
            return self.vars[name]
        except KeyError:
            if self.parent is not None:
                return self.parent.get_var(name)
            return None

    def __str__(self):
        cond = self.parent is None
        result = "{\n"
        result += "\t" if cond else "Parent:\n" + f"{self.parent}\n\t"
        result += "\n\t".join(str(x) for x in self.vars.values())
        result += "\n}"
        return result

    def __repr__(self):
        return str(self)
