#%%
from tools.firsts import compute_firsts
from tools.follows import compute_follows
from automatons.state import State
from grammar.items import Item
from parserr.shiftreduce import ShiftReduceParser

class SLR1Parser(ShiftReduceParser):

    def build_LR0_automaton(self,G):
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0)

        automaton = State(start_item, True)

        pending = [ start_item ]
        visited = { start_item: automaton }

        while pending:
            current_item = pending.pop()
            if current_item.IsReduceItem:
                continue

            current_state = visited[current_item]
            symbol = current_item.NextSymbol
            try:
                next_state = visited[current_item.next_item()]
            except KeyError:
                next_state = State(current_item.next_item(),True)
                visited[current_item.next_item()] = next_state
                
            current_state.add_transition(symbol.Name,next_state)
            pending.append(current_item.next_item())
            if symbol.IsNonTerminal:
                for production in symbol.productions:
                    item = Item(production,0)
                    try:
                        state = visited[item]
                    except KeyError:
                        state = State(item,True)
                        visited[item] = state
                        pending.append(item)
                    current_state.add_epsilon_transition(state)
                
        return automaton


    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar()
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton = self.build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, node)
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                
                if item.IsReduceItem:
                    head  = item.production.Left
                    if head == G.startSymbol:
                        self._register(self.action,(idx,G.EOF),('OK',item.production))
                    else:
                        for c in follows[head]:
                            self._register(self.action,(idx,c),('REDUCE',item.production))
                else:
                    symbol = item.NextSymbol
                    try:
                        trans_idx = node.transitions[symbol.Name][0].idx
                        if symbol.IsNonTerminal:
                            self._register(self.goto,(idx,symbol),trans_idx)
                        else:
                            self._register(self.action,(idx,symbol),('SHIFT',trans_idx))
                    except KeyError:
                        pass
    
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value

#%%