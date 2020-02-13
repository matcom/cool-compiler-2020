#%%
from automatons.deterministic import DFA
from automatons.nondeterministic import NFA
from tools.firsts import ContainerSet

def compute_epsilon_closure(automaton: NFA, states):
    pending = list(states)
    closure = set(states)

    while pending:
        state = pending.pop()
        for nstate in automaton.epsilon_transitions(state):
            if nstate not in closure:
                closure.add(nstate)
                pending.append(nstate)

    return ContainerSet(*closure)


def nfa_to_deterministic(automaton: NFA):
    transitions = {}
    start = compute_epsilon_closure(automaton,[automaton.start])
    start.state = 0
    pending = [start]
    aut_states = [start]
    start.is_final = any(s in automaton.finals for s in start)
    n = 1
    while pending:
        state = pending.pop()
        for symbol in automaton.vocabulary:
            next_state = []
            for s in state:
                next_state+=[x for x in automaton.transitions.get(s,{}).get(symbol,[])]
            if next_state:
                try:
                    transitions[state.state,symbol]
                    assert False, "Automato Finito Determinista Invalido"
                except KeyError:
                    next_state = compute_epsilon_closure(automaton, next_state)
                    if not next_state in aut_states:
                        next_state.state = n
                        next_state.is_final = any(s in automaton.finals for s in next_state)
                        pending.append(next_state)
                        aut_states.append(next_state)
                        n+=1
                    else:
                        next_state = aut_states[aut_states.index(next_state)]
                    transitions[state.state, symbol] = next_state.state

    finals = [s.state for s in aut_states if s.is_final]
    dfa = DFA(n, finals, transitions)
    return dfa
