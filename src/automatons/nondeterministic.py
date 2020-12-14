class NFA:
    """
    Un autómata finito (determinista o no determinista) es un quíntuplo $A = <Q,q_0,V,F,f>$ con
    las siguientes características:

    -Q es un conjunto finito de estados Q = { q_0, .... , q_n }, de ahí el adjetivo de **finito**.
    -q_0 in Q es el estado inicial.
    -V es un conjunto finito de símbolos que pueden aparecer en la cinta.
    -F Q es un subconjunto de estados que denominaremos *estados finales*.
    -f es una *función de transición*, que determina, para cada par posible de estados y símbolos,
     cuál es el estado de destino. En la forma de esta función radica justamente la diferencia entre
     AF determinista y no determinista:
    -f: Q * V -> Q denota un autómata **determinista** justamente porque en un estado particular,
     para un símbolo particular, existe solamente un estado posible de destino (o ninguno),
     por lo tanto, siempre existe una única decisión que tomar.
    -f: Q *(V U e) -> 2^Q denota un autómata **no determinista** porque en un estado particular,
     para un símbolo particular, existen potencialmente múltiples estados de destino (o ninguno).
     Incluso permite realizar epsilon-transiciones (transiciones que no consumen símbolos de la cinta)
     lo cual resalta aún más el carácter no determinista de estos autómatas.
    """
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = {state: {} for state in range(states)}

        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations,
                           '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)

        self.vocabulary.discard('')

    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
