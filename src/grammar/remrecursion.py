#%%
from grammar.grammar import Grammar
from grammar.symbols import NonTerminal
from grammar.symbols import Sentence
from trie.tree import Trie
#%%
def remove_left_recursion(G:Grammar):
    
    def find_recursive_production(t:NonTerminal):
        recursives, non_recursives = list(), list()
        for production in t.productions:
            head, body = production
            if len(body) > 1 and head == body[0]:
                recursives.append(production)
            else:
                non_recursives.append(production)
        return recursives, non_recursives

    def remove_redundant_productions(G:Grammar):
        for production in G.Productions:
            while G.Productions.count(production) > 1:
                G.Productions.remove(production)
            

    for nt in G.nonTerminals:
        recursives, non_recursives = find_recursive_production(nt)
        if recursives:
            new_symbol = G.NonTerminal(f'{nt}^')
            for production in non_recursives:
                G.Productions.remove(production)
                body = production.Right
                nt %= body + new_symbol
            for production in recursives:
                alpha = Sentence(*production.Right[1::])
                G.Productions.remove(production)
                new_symbol %= alpha + new_symbol | G.Epsilon
        
    remove_redundant_productions(G)

def factorize(G:Grammar):

    def lcp(sym):
        prefix_len, prefix = 0, None
        d = set()
        t = Trie([x for x in (G.terminals + G.nonTerminals)])
        for production in sym.productions:
            _, body = production
            p = t.prefix_query(body)
            if p:
                if len(p) > prefix_len:
                    prefix = p
                    prefix_len = len(p)
            t.insert(body)
        if prefix:
            for production in sym.productions:
                if all(prefix[i] == production.Right[i] for i in range(prefix_len)):
                    d.add(production)
        print(d)
        return prefix, d

    stack = [x for x in G.nonTerminals]
    while stack:
        sym = stack.pop()
        prefix, productions = lcp(sym)
        change = not prefix is None
        if change:
            new_t = G.NonTerminal(f'{sym.Name}^')
            sym %= prefix + new_t
            for p in productions:
                remainder = p.Right[len(prefix)::]
                remainder = Sentence(*remainder) if remainder else G.Epsilon
                new_t %= remainder
                G.Productions.remove(p)
                    
