#%%
from grammar.grammar import Grammar
from automatons.nondeterministic import NFA
from automatons.transformation import nfa_to_deterministic
from lexer.regexgenerator import Regex
from automatons.deterministic import DFA

class AlgebraicRegex:
    
    def __init__(self, string):
        self.string = string
        
    @property
    def is_void(self):
        return self.string == ''
    
    @property
    def empt(self):
        return self.string == 'ε'
    
    def __str__(self):
        return self.string
    
    def __repr__(self):
        return str(self)
        
    def __or__(self, other):
        assert isinstance(other, AlgebraicRegex)
        if self.is_void and other.is_void:
            return self
        elif self.is_void: return other
        elif other.is_void: return self
        if self.empt and other.empt: return self
        
        return AlgebraicRegex(f'(({self.string}|{other.string}))')
    
    def __gt__(self, other):
        assert isinstance(other, AlgebraicRegex)
        if self.is_void and other.is_void: return self
        elif self.is_void or other.is_void: return other
        
        if self.empt: return other
        if other.empt: return self

        return AlgebraicRegex(f'(({self.string})({other.string}))')
    
    def star(self):
        if self.empt or self.is_void: return self
        if len(self.string) == 1: return AlgebraicRegex(f'({self.string})*')
        
        return AlgebraicRegex(f'({self.string})*')
            

def assert_regular(G: Grammar):
    for production in G.Productions:
        if len(production.Right) > 2:
            return False
        if len(production.Right) == 2 and (production.Right[0].IsNonTerminal or production.Right[1].IsTerminal):
            return False
    return True

def grammar_to_automaton(G:Grammar):
    d = {sym.Name: i for i,sym in enumerate(G.nonTerminals)}
    s = {i:sym for i,sym in enumerate(G.nonTerminals)}
    if assert_regular(G):
        states = len(G.nonTerminals)
        transitions = {}
        finals = []
        for i in range(states):
            sym = s[i]
            for production in sym.productions:
                if len(production.Right) == 1:
                    next_sym = production.Right[0]
                    if next_sym.IsTerminal:
                        try:
                            transitions[(i,next_sym.Name)].append(i)
                        except:    
                            transitions[(i,next_sym.Name)] = [i]
                        finals.append(i)
                    else:
                        try:
                            transitions[(i,'')].append(d[next_sym.Name])
                        except:
                            transitions[(i,'')] = [d[next_sym.Name]]
                if len(production.Right) == 2:
                    next_sym = production.Right[0]
                    next_state = d[production.Right[1].Name]
                    try:
                        transitions[(i,next_sym.Name)].append(next_state)
                    except:
                        transitions[(i,next_sym.Name)] = [next_state]
                if len(production.Right) == 0:
                    finals.append(i)
        start = d[G.startSymbol.Name]
        return nfa_to_deterministic(NFA(states,finals, transitions, start=start))
    else:
        print('La Gramatica no es regular')

def regex_to_grammar(regex:Regex):
    automaton = regex.automaton
    G = Grammar()
    start = G.NonTerminal(f'A{automaton.start}',True)
    n = {}
    n[automaton.start] = start
    for i in range(automaton.states):
        if i != automaton.start:
            n[i] = G.NonTerminal(f'A{i}')
    t = {}
    for sym in automaton.vocabulary:
        t[sym] = G.Terminal(sym)

    for src, d in automaton.transitions.items():
        for sym, dest in d.items():
            nt = n[src]
            nt1 = n[dest[0]]
            s = t[sym]
            nt %= s + nt1 if nt1 != nt else s
    for f in automaton.finals:
        nt = n[f]
        nt %= G.Epsilon
    return G

def grammar_to_regex(G:Grammar,aut = None):
    if assert_regular(G):
        automaton = grammar_to_automaton(G) if not aut else aut
        n = automaton.states
        
        # Crear la tabla para la dinamica: tener en cuenta que el caracter $ indica
        # la cadena vacia, que luego habra que simplificar de acuerdo a las reglas
        # algebraicas de las expresiones regulares
        dp = {(i,j,k): AlgebraicRegex('') for i in range(1,n+1) for j in range(1,n+1) for k in range(n+1)}
        
        # Construir el caso BASE de la dinamica dp[i,j,0]
        for i, dest in automaton.transitions.items():
            i = i + 1
            for sym,l in dest.items():
                j = l[0] + 1
                if i != j:
                    dp[i,j,0] = AlgebraicRegex(sym)
                else:
                    dp[i,j,0] = AlgebraicRegex(sym)|AlgebraicRegex('ε')
                
        
        # aplicar el paso inductivo de la dinamica:
        # dp[i,j,k] = dp[i,j,k-1]|dp[i,k-1,k-1]dp[k,k,k-1]*dp[k,j,k-1] para todo k >= 1
        
        for k in range(1,n+1):
            for i in range(1,n+1):
                for j in range(1,n+1):
                    right = dp[i,k,k-1]>dp[k,k,k-1].star()
                    right = right >dp[k,j,k-1]
                    dp[i,j,k] = dp[i,j,k-1]|right
                                        
                    
        # La expresion regular del automata es el resultado de concatenar todos los pares dp[i,j,n] tales que j
        # sea un estado final
        finals = [dp[automaton.start+1,j+1,n] for j in automaton.finals]
        
        result = finals[0]
        for s in finals[1::]:
            result = result | s
        return result
    
    else:
        print('La gramatica no es regular')
                                        
        
# #%%
# G = Grammar()
# A = G.NonTerminal('A',True)
# B, C, D = G.NonTerminals('B C D')
# a,b = G.Terminals('a b')

# A %= a + A | b + A | a + B
# B %= b + C
# C %= b + D
# D %= G.Epsilon

# aut = DFA(2,[0],{(0,'a'):0,(0,'b'):1,(1,'a'):1,(1,'b'):0})
# display(aut)
# print(grammar_to_regex(G,aut=aut))
# display(Regex(grammar_to_regex(G,aut=aut).string).automaton)

# #%%

# print(grammar_to_regex(G))
# regex = Regex(grammar_to_regex(G).string)
# a = grammar_to_automaton(G)
# display(a)
# display(regex.automaton)
# print(a.recognize('abababaaaaabb'))
# print(regex('abababaaaaabb'))

# #%%
# print(G)
# print(assert_regular(G))

# #%%
# a = grammar_to_automaton(G)
# display(a)

# #%%
# r = Regex('(a|b)+')
# g = regex_to_grammar(r)
# print(g)
# display(grammar_to_automaton(g))