
class ContainerSet:
    """
    Resulta conveniente manejar la pertenencia o no de epsilon a un conjunto como un caso extremo.
    Para ello usaremos la clase ContainerSet implementada a continuación.

    La clase funciona como un conjunto de símbolos.
    Permite consulta la pertenencia de epsilon al conjunto.
    Las operaciones que modifican el conjunto devuelven si hubo cambio o no.
    El conjunto puede ser actualizado con la adición de elementos individuales, add(...),
    o a partir de otro conjunto,update(...) y hard_update(...).
    La actualización sin epsilon (1), con epsilon (2) y de solo epsilon (3),
    ocurre a través de update(...), hard_update(...) y epsilon_update(...) respectivamente.
    """

    def __init__(self, *values, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def set_epsilon(self, value=True):
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    def update(self, other):
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other):
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)

    def hard_update(self, other):
        return self.update(other) | self.epsilon_update(other)

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        return '%s-%s' % (str(self.set), self.contains_epsilon)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.set)

    def __eq__(self, other):
        return isinstance(other, ContainerSet) and self.set == other.set and \
            self.contains_epsilon == other.contains_epsilon


def compute_local_first(firsts, alpha):

    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon()
    else:
        i = 0
        while i < len(alpha):
            sym = alpha[i]
            if sym.IsTerminal:
                first_alpha.add(sym)
                break
            else:
                first_alpha.update(firsts[sym])
                if firsts[sym].contains_epsilon:
                    first_alpha.set_epsilon()
                    i += 1
                else:
                    break

    return first_alpha


def compute_firsts(grammar):
    firsts = {}
    change = True

    for terminal in grammar.terminals:
        firsts[terminal] = ContainerSet(terminal)

    for nonterminal in grammar.nonTerminals:
        firsts[nonterminal] = ContainerSet()

    while change:
        change = False

        for production in grammar.Productions:
            X = production.Left
            alpha = production.Right

            first_X = firsts[X]

            try:
                first_alpha = firsts[alpha]
            except:
                first_alpha = firsts[alpha] = ContainerSet()

            local_first = compute_local_first(firsts, alpha)

            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)

    return firsts
