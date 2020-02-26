from queue import Queue
from .pycompiler import Grammar, Item
from .automata import State
from .utils import ContainerSet

class GrammarTools:
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
            row[symbol] = []

        cell = row[symbol]

        if value not in cell:
            cell.append(value)

        return len(cell) == 1

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
        output, operations = [], []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor].token_type
            if self.verbose: print(stack, w[cursor:])
                
            # (Detect error)
            try:
                action, tag = self.action[state][lookahead][0]
                # (Shift case)
                if action == Action.SHIFT:
                    stack.append(tag)
                    cursor += 1
                    operations.append(action)
                # (Reduce case)
                elif action == Action.REDUCE:
                    for _ in range(len(tag.Right)): stack.pop()
                    stack.append(self.goto[stack[-1]][tag.Left][0])
                    output.append(tag)
                    operations.append(action)
                # (OK case)
                elif action == Action.OK:
                    # output.reverse()
                    return output, operations
                # (Invalid case)
                else:
                    assert False, 'Must be something wrong!'
            except KeyError:
                print('Parsing Error:', stack, w[cursor:])
                return w[cursor:][0], None

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
        
        # automaton.set_formatter(empty_formatter)
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