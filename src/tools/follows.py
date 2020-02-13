#%%
from tools.firsts import ContainerSet, compute_firsts, compute_local_first
from grammar.grammar import Grammar
from grammar.symbols import Sentence
#%%
def compute_follows(G: Grammar,firsts):
    follows = {}
    change = True

    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)

    while change:
        change = False

        for production in G.Productions:

            X = production.Left
            alpha = production.Right

            i = 0
            while i < len(alpha):
                sym = alpha[i]
                if sym.IsNonTerminal:
                    if i == len(alpha)-1:
                        follows[sym].update(follows[X])
                    else:
                        try:
                            local = firsts[alpha[i+1::]]
                        except KeyError:
                            local = compute_local_first(firsts, alpha[i+1::])
                    
                        change |= follows[sym].update(local)
                        if local.contains_epsilon:
                            change |= follows[sym].update(follows[X])
                i+= 1
        
    return follows
