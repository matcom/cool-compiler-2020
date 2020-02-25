from core.cmp.pycompiler import *
from core.cmp.automata import *
from core.cmp.utils import *

class BadTextFormatException(Exception):
    """
    Class for wrong format in texts
    used to convert to a grammar
    """
    pass

class GrammarTools:
    @staticmethod
    def grammar_from_text(text: str):
        """
        Transform a string in this format:

        S --> A B
        A --> a A | epsilon
        B --> b B | epsilon

        to a Grammar object
        """
        terminals, nonTerminals, productions = [], [], []

        try:
            lines = text.split('\n')

            for line in lines:
                head, bodies = line.split('-->')

                head, = head.split()
                nonTerminals.append(head)

                for body in bodies.split('|'):
                    productions.append({'Head': head, 'Body': list(body.split())})
                    terminals.extend(productions[-1]['Body'])

        except:
            raise BadTextFormatException()

        sterminals, snonTerminals = set(terminals).difference(nonTerminals + ['epsilon']), set(nonTerminals)

        data = json.dumps({
                            'NonTerminals': [nt for nt in nonTerminals if nt in snonTerminals and snonTerminals.discard(nt) is None],
                            'Terminals': [t for t in terminals if t in sterminals and sterminals.discard(t) is None],
                            'Productions': productions
                        })

        return Grammar.from_json(data)

    @staticmethod
    def is_not_null(G: Grammar):
        """
        Check if the given grammar genere
        the empty language
        """
        accepted = set()
        visited = set()

        def dfs(symbol):
            visited.add(symbol)
            acc = False

            if isinstance(symbol, Terminal):
                acc = True
            else:
                for production in symbol.productions:
                    for s in production.Right:
                        if s not in visited:
                            dfs(s)
                    acc |= all(s in accepted for s in production.Right)

            if acc:
                accepted.add(symbol)

        dfs(G.startSymbol)

        return G.startSymbol in accepted

    @staticmethod
    def clone_grammar(G: Grammar):
        NG = Grammar()
        symbols = {nonTerminal: NG.NonTerminal(nonTerminal.Name, nonTerminal == G.startSymbol) for nonTerminal in G.nonTerminals}
        symbols.update({terminal: NG.Terminal(terminal.Name) for terminal in G.terminals})
        for p in G.Productions:
            x = symbols[p.Left]
            if isinstance(p.Right, Epsilon):
                x %= NG.Epsilon
            else:
                x %= Sentence(*[symbols[symbol] for symbol in p.Right])

        return NG

    @staticmethod
    def remove_left_recursion(G: Grammar):
        """
        Transform G for remove inmediate
        left recursion
        """
        G.Productions = []

        for nonTerminal in G.nonTerminals:
            recursion = [p.Right[1:] for p in nonTerminal.productions if len(p.Right) > 0 and p.Right[0] == nonTerminal]
            no_recursion = [p.Right for p in nonTerminal.productions if len(p.Right) == 0 or p.Right[0] != nonTerminal]

            if len(recursion) > 0:
                nonTerminal.productions = []
                aux = G.NonTerminal(f'{nonTerminal.Name}0')

                for p in no_recursion:
                    nonTerminal %= Sentence(*p) + aux

                for p in recursion:
                    aux %= Sentence(*p) + aux

                aux %= G.Epsilon
            else:
                G.Productions.extend(nonTerminal.productions)

    @staticmethod
    def factorize_grammar(G: Grammar):
        """
        Transform G for remove common
        prefixes
        """
        G.Productions = []

        pending = G.nonTerminals.copy()

        while pending:
            nonTerminal = pending.pop()

            productions = nonTerminal.productions.copy()
            nonTerminal.productions = []

            visited = set()

            for i, p in enumerate(productions):
                if p not in visited:
                    n = len(p.Right)
                    same_prefix = []

                    for p2 in productions[i:]:
                        m = 0

                        for s1, s2 in zip(p.Right, p2.Right):
                            if s1 == s2:
                                m += 1
                            else:
                                break
                        
                        if m > 0:
                            same_prefix.append(p2)
                            n = min(n, m)

                    if len(same_prefix) > 1:
                        visited.update(same_prefix)
                        aux = G.NonTerminal(f'{nonTerminal.Name}{i + 1}')

                        nonTerminal %= Sentence(*p.Right[:n]) + aux
                        for p2 in same_prefix:
                            if n == len(p2.Right):
                                aux %= G.Epsilon
                            else:
                                aux %= Sentence(*p2.Right[n:])

                        pending.append(aux)
                    else:
                        visited.add(p)
                        nonTerminal %= p.Right
    
    @staticmethod
    def compute_local_first(firsts, alpha):
        """
        Computes First(alpha), given First(Vt) and First(Vn) 
        alpha in (Vt U Vn)*
        """
        first_alpha = ContainerSet()
        
        try:
            alpha_is_epsilon = alpha.IsEpsilon
        except:
            alpha_is_epsilon = False

        # alpha == epsilon ? First(alpha) = { epsilon }
        if alpha_is_epsilon:
            first_alpha.set_epsilon()

        # alpha = X1 ... XN
        # First(Xi) subset of First(alpha)
        # epsilon  in First(X1)...First(Xi) ? First(Xi+1) subset of First(X) & First(alpha)
        # epsilon in First(X1)...First(XN) ? epsilon in First(X) & First(alpha)
        else:
            for symbol in alpha:
                first_symbol = firsts[symbol]
                first_alpha.update(first_symbol)
                if not first_symbol.contains_epsilon:
                    break
            else:
                first_alpha.set_epsilon()

        return first_alpha

    @staticmethod
    def compute_firsts(G: Grammar):
        """
        Computes First(Vt) U First(Vn) U First(alpha)
        P: X -> alpha
        """
        firsts = {}
        change = True
        
        # init First(Vt)
        for terminal in G.terminals:
            firsts[terminal] = ContainerSet(terminal)
            
        # init First(Vn)
        for nonterminal in G.nonTerminals:
            firsts[nonterminal] = ContainerSet()
        
        while change:
            change = False
            
            # P: X -> alpha
            for production in G.Productions:
                X = production.Left
                alpha = production.Right
                
                # get current First(X)
                first_X = firsts[X]
                    
                # init First(alpha)
                try:
                    first_alpha = firsts[alpha]
                except:
                    first_alpha = firsts[alpha] = ContainerSet()
                
                # CurrentFirst(alpha)???
                local_first = GrammarTools.compute_local_first(firsts, alpha)
                
                # update First(X) and First(alpha) from CurrentFirst(alpha)
                change |= first_alpha.hard_update(local_first)
                change |= first_X.hard_update(local_first)
                        
        # First(Vt) + First(Vt) + First(RightSides)
        return firsts

    @staticmethod
    def compute_follows(G: Grammar, firsts):
        """
        Computes Follow(Vn)
        """
        follows = { }
        change = True
        
        local_firsts = {}
        
        # init Follow(Vn)
        for nonterminal in G.nonTerminals:
            follows[nonterminal] = ContainerSet()
        follows[G.startSymbol] = ContainerSet(G.EOF)
        
        while change:
            change = False
            
            # P: X -> alpha
            for production in G.Productions:
                X = production.Left
                alpha = production.Right
                
                follow_X = follows[X]
                
                # X -> zeta Y beta
                # First(beta) - { epsilon } subset of Follow(Y)
                # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
                for i, symbol in enumerate(alpha):
                    if symbol.IsNonTerminal:
                        follow_symbol = follows[symbol]
                        beta = alpha[i + 1:]
                        try:
                            first_beta = local_firsts[beta]
                        except KeyError:
                            first_beta = local_firsts[beta] = GrammarTools.compute_local_first(firsts, beta)
                        change |= follow_symbol.update(first_beta)
                        if first_beta.contains_epsilon or len(beta) == 0:
                            change |= follow_symbol.update(follow_X)
        
        return follows

    @staticmethod
    def _register(table, state, symbol, value):
        if state not in table:
            table[state] = dict()

        row = table[state]
        
        if symbol not in row:
            row[symbol] = set()

        cell = row[symbol]

        cell.add(value)

        return len(cell) == 1

    @staticmethod
    def build_ll1_table(G: Grammar, firsts, follows):
        """
        Computes Parsing Table for a
        Parser LL(1)
        """
        # init parsing table
        M = {}
        is_ll1 = True
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            # working with symbols on First(alpha) ...
            first_alpha = firsts[alpha]
            for symbol in first_alpha:
                is_ll1 &= GrammarTools._register(M, X, symbol, production)
            
            # working with epsilon...
            if first_alpha.contains_epsilon:
                for symbol in follows[X]:
                    is_ll1 &= GrammarTools._register(M, X, symbol, production)
            
        # parsing table is ready!!!
        return M, is_ll1

    @staticmethod
    def build_automaton(G: Grammar):
        """
        Build the finite automaton for
        a regular grammar
        """
        states = { nonTerminal: State(nonTerminal.Name) for nonTerminal in G.nonTerminals }
        final_state = State('F\'', True)

        start_in_right = False
        epsilon_production = False

        for nonTerminal in G.nonTerminals:
            for production in nonTerminal.productions:
                right = production.Right

                # Start Symbol produces epsilon
                if isinstance(right, Epsilon) and nonTerminal == G.startSymbol:
                    epsilon_production = True
                    continue
                    
                start_in_right |= G.startSymbol in right
                n = len(right)

                # X --> w
                if n == 1 and isinstance(right[0], Terminal):
                    states[nonTerminal].add_transition(right[0].Name, final_state)
                    continue

                # X --> w Y
                if n == 2 and isinstance(right[0], Terminal) and isinstance(right[1], NonTerminal):
                    states[nonTerminal].add_transition(right[0].Name, states[right[1]])
                    continue

                return states[G.startSymbol], False

        states[G.startSymbol].final = epsilon_production
        return states[G.startSymbol], not (start_in_right and epsilon_production)

    epsilon = 'ε'
    
    @staticmethod 
    def regex_union(regex, other):
        if regex is None:
            return other

        if other is None:
            return regex

        if regex == other:
            return regex

        return f'({regex}|{other})'

    @staticmethod 
    def regex_concat(regex, other):
        if regex is None or other is None:
            return None

        if regex is GrammarTools.epsilon:
            return other

        if other is GrammarTools.epsilon:
            return regex

        return f'{regex}{other}'

    @staticmethod 
    def regex_star(regex):
        if regex is None or regex is GrammarTools.epsilon:
            return regex

        return f'({regex})*'

    @staticmethod
    def regexp_from_automaton(automaton):
        """
        Build the  regular expresion for
        a NFA
        """
        states = list(automaton)
        states_index = {state: i for i, state in enumerate(states)}
        n = len(states)

        R = [[[None for k in range(n + 1)] for j in range(n)] for i in range(n)]

        for i in range(n):
            R[i][i][0] = GrammarTools.epsilon

        for i, state in enumerate(states):
            for symbol, transitions in state.transitions.items():
                for state2 in transitions:
                    j = states_index[state2]
                    R[i][j][0] = GrammarTools.regex_union(R[i][j][0], symbol)

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    R[i][j][k + 1] = GrammarTools.regex_union(R[i][j][k], GrammarTools.regex_concat(R[i][k][k], GrammarTools.regex_concat(GrammarTools.regex_star(R[k][k][k]), R[k][j][k])))

        e = None
        for i in range(n):
            if states[i].final:
                e = GrammarTools.regex_union(e, R[0][i][n])

        return e


class Action(tuple):
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __str__(self):
        try:
            action, tag = self
            return f"{'S' if action == Action.SHIFT else 'OK' if action == Action.OK else ''}{tag}"
        except:
            return str(tuple(self))

    __repr__ = __str__

class ShiftReduceParser:  
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, w[cursor:])
                
            # (Detect error)
            try:
                print(type(state), type(lookahead))
                action, tag = list(self.action[state][lookahead])[0]
                # (Shift case)
                if action == Action.SHIFT:
                    stack.append(tag)
                    cursor += 1
                # (Reduce case)
                elif action == Action.REDUCE:
                    for _ in range(len(tag.Right)): stack.pop()
                    stack.append(self.goto[stack[-1]][tag.Left])
                    output.append(tag)
                # (OK case)
                elif action == Action.OK:
                    return output
                # (Invalid case)
                else:
                    assert False, 'Must be something wrong!'
            except KeyError:
                raise Exception('Aborting parsing, item is not viable.')

class SLR1Parser(ShiftReduceParser):
    def build_LR0_automaton(self):
        G = self.augmentedG = self.G.AugmentedGrammar(True)

        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0)

        automaton = State(start_item, True)

        pending = [ start_item ]
        visited = { start_item: automaton }

        while pending:
            current_item = pending.pop()
            if current_item.IsReduceItem:
                continue
            
            # (Decide which transitions to add)
            next_symbol = current_item.NextSymbol
            
            next_item = current_item.NextItem()
            if not next_item in visited:
                pending.append(next_item)
                visited[next_item] = State(next_item, True)
            
            if next_symbol.IsNonTerminal:
                for prod in next_symbol.productions:
                        next_item = Item(prod, 0)
                        if not next_item in visited:
                            pending.append(next_item)
                            visited[next_item] = State(next_item, True) 

            current_state = visited[current_item]
            
            # (Add the decided transitions)
            current_state.add_transition(next_symbol.Name, visited[current_item.NextItem()])
            
            if next_symbol.IsNonTerminal:
                for prod in next_symbol.productions:
                        current_state.add_epsilon_transition(visited[Item(prod, 0)])
            
        self.automaton = automaton.to_deterministic()

    def _build_parsing_table(self):
        self.is_slr1 = True
        self.build_LR0_automaton()

        firsts = GrammarTools.compute_firsts(self.augmentedG)
        follows = GrammarTools.compute_follows(self.augmentedG, firsts)
        
        for i, node in enumerate(self.automaton):
            if self.verbose: print(i, node)
            node.idx = i
            node.tag = f'I{i}'

        for node in self.automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == self.augmentedG.startSymbol:
                        self.is_slr1 &= GrammarTools._register(self.action, idx, self.augmentedG.EOF, 
                                                            Action((Action.OK, '')))
                    else:
                        for symbol in follows[prod.Left]:
                            self.is_slr1 &= GrammarTools._register(self.action, idx, symbol, 
                                                                Action((Action.REDUCE, prod)))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.is_slr1 &= GrammarTools._register(self.action, idx, next_symbol, 
                                                            Action((Action.SHIFT, node[next_symbol.Name][0].idx)))
                    else:
                        self.is_slr1 &= GrammarTools._register(self.goto, idx, next_symbol, 
                                                            node[next_symbol.Name][0].idx)

class LR1Parser(ShiftReduceParser):
    @staticmethod
    def expand(item, firsts):
        next_symbol = item.NextSymbol
        if next_symbol is None or not next_symbol.IsNonTerminal:
            return []
        
        lookaheads = ContainerSet()
        # (Compute lookahead for child items)
        for preview in item.Preview():
            lookaheads.hard_update(GrammarTools.compute_local_first(firsts, preview))
        
        assert not lookaheads.contains_epsilon
        # (Build and return child items)
        return [Item(prod, 0, lookaheads) for prod in next_symbol.productions]

    @staticmethod
    def compress(items):
        centers = {}

        for item in items:
            center = item.Center()
            try:
                lookaheads = centers[center]
            except KeyError:
                centers[center] = lookaheads = set()
            lookaheads.update(item.lookaheads)
        
        return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

    @staticmethod
    def closure_lr1(items, firsts):
        closure = ContainerSet(*items)
        
        changed = True
        while changed:
            changed = False
            
            new_items = ContainerSet()
            for item in closure:
                new_items.extend(LR1Parser.expand(item, firsts))

            changed = closure.update(new_items)
            
        return LR1Parser.compress(closure)
    
    @staticmethod
    def goto_lr1(items, symbol, firsts=None, just_kernel=False):
        assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
        items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
        return items if just_kernel else LR1Parser.closure_lr1(items, firsts)


    def build_LR1_automaton(self):
        G = self.augmentedG = self.G.AugmentedGrammar(True)

        firsts = GrammarTools.compute_firsts(G)
        firsts[G.EOF] = ContainerSet(G.EOF)
        
        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0, lookaheads=(G.EOF,))
        start = frozenset([start_item])
        
        closure = LR1Parser.closure_lr1(start, firsts)
        automaton = State(frozenset(closure), True)
        
        pending = [ start ]
        visited = { start: automaton }
        
        while pending:
            current = pending.pop()
            current_state = visited[current]
            
            for symbol in G.terminals + G.nonTerminals:
                # (Get/Build `next_state`)
                kernels = LR1Parser.goto_lr1(current_state.state, symbol, just_kernel=True)
                
                if not kernels:
                    continue
                
                try:
                    next_state = visited[kernels]
                except KeyError:
                    pending.append(kernels)
                    visited[pending[-1]] = next_state = State(frozenset(LR1Parser.goto_lr1(current_state.state, symbol, firsts)), True)
                
                current_state.add_transition(symbol.Name, next_state)
        
        self.automaton = automaton

    def _build_parsing_table(self):
        self.is_lr1 = True
        self.build_LR1_automaton()
        
        for i, node in enumerate(self.automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
            node.tag = f'I{i}'

        for node in self.automaton:
            idx = node.idx
            for item in node.state:
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == self.augmentedG.startSymbol:
                        self.is_lr1 &= GrammarTools._register(self.action, idx, self.augmentedG.EOF, 
                                                            Action((Action.OK, '')))
                    else:
                        for lookahead in item.lookaheads:
                            self.is_lr1 &= GrammarTools._register(self.action, idx, lookahead, 
                                                                Action((Action.REDUCE, prod)))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.is_lr1 &= GrammarTools._register(self.action, idx, next_symbol, 
                                                            Action((Action.SHIFT, node[next_symbol.Name][0].idx)))
                    else:
                        self.is_lr1 &= GrammarTools._register(self.goto, idx, next_symbol, 
                                                            node[next_symbol.Name][0].idx)
                pass

class LALR1Parser(LR1Parser):
    @staticmethod
    def mergue_items_lookaheads(items, others):
        if len(items) != len(others):
            return False

        new_lookaheads = []
        for item in items:
            for item2 in others:
                if item.Center() == item2.Center():
                    new_lookaheads.append(item2.lookaheads)
                    break
            else:
                return False

        for item, new_lookahead in zip(items, new_lookaheads):
            item.lookaheads = item.lookaheads.union(new_lookahead)

        return True

    def build_LR1_automaton(self):
        super().build_LR1_automaton()

        states = list(self.automaton)
        new_states = []
        visited = {}

        for i, state in enumerate(states):
            if state not in visited:
                # creates items
                items = [item.Center() for item in state.state]

                # check for states with same center
                for state2 in states[i:]:
                    if LALR1Parser.mergue_items_lookaheads(items, state2.state):
                        visited[state2] = len(new_states)

                # add new state
                new_states.append(State(frozenset(items), True))

        # making transitions
        for state in states:
            new_state = new_states[visited[state]]
            for symbol, transitions in state.transitions.items():
                for state2 in transitions:
                    new_state2 = new_states[visited[state2]]
                    # check if the transition already exists
                    if symbol not in new_state.transitions or new_state2 not in new_state.transitions[symbol]:
                        new_state.add_transition(symbol, new_state2)

        self.automaton = new_states[0]
