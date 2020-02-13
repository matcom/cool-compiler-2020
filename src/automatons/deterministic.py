from  automatons.nondeterministic import NFA

class DFA(NFA):
    """
    Esta clase extiende la clase `NFA` para:
    - Usar la función de transición propia de los autómatas finitos deterministas.
    - Implementar un algoritmo de reconocimiento de cadenas.
    """
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)

        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start


    def epsilon_transitions(self):
        raise TypeError()

    def _move(self, symbol):
        try:
            self.current = self.transitions[self.current][symbol][0]
            return True
        except KeyError:
            return False

    def _reset(self):
        self.current = self.start

    def recognize(self, string):
        self.current = self.start
        for c in string:
            if not self._move(c):
                return False
        return self.current in self.finals
