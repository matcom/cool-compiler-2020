from ast.base import Node, AtomicNode, UnaryNode, BinaryNode

class EpsilonNode(AtomicNode):
    def evaluate(self):
        automaton = NFA(states = 1, finals = [0],transitions = {} )
        return automaton

#%%
EPSILON = 'ε'
EpsilonNode(EPSILON).evaluate()
