from deterministic import DFA
from nondeterministic import NFA
from tools.firsts import ContainerSet

def compute_epsilon_closure(automaton: NFA, states):
    pending = list(states)
    closure = set(states)

    while pending:
        state = pending.pop()
        for nstate in automaton.epsilon_transitions(state):
            closure.add(nstate)
            pending.append(nstate)

    return closure
