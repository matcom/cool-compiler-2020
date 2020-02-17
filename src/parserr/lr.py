from grammar.items import Item
from tools.firsts import ContainerSet
from automatons.state import State
from parserr.shiftreduce import ShiftReduceParser
from tools.firsts import compute_firsts, compute_local_first
from progressbar.progressbar import ProgressBar


def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()

    for remainder in item.Preview():
        for lookahead in compute_local_first(firsts=firsts, alpha=remainder):
            lookaheads.update(ContainerSet(lookahead))

    assert not lookaheads.contains_epsilon
    expanded = [
        Item(production, 0, lookaheads)
        for production in next_symbol.productions
    ]
    return expanded


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {
        Item(x.production, x.pos, set(lookahead))
        for x, lookahead in centers.items()
    }


def closure_lr1(items, firsts):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()

        for item in closure:
            new_items.update(ContainerSet(*expand(item, firsts)))

        changed = closure.update(new_items)

    return compress(closure)


def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.next_item() for item in items
                      if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)


def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF, ))
    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.nonTerminals:
            next_item = goto_lr1(current_state.state, symbol, just_kernel=True)
            if next_item:
                try:
                    next_state = visited[next_item]
                except KeyError:
                    next_state = State(
                        frozenset(closure_lr1(next_item, firsts)), True)
                    visited[next_item] = next_state
                    pending += [next_item]

                current_state.add_transition(symbol.Name, next_state)

    return automaton


def build_lalr_automaton(G):
    def centers(items: [Item]):
        return frozenset(item.Center() for item in items)

    def lookaheads(items: [Item]):
        return {item.Center(): item.lookaheads for item in items}

    def subset(items1, items2):
        return all(items1[i] <= items2[i] for i in items1)

    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, (G.EOF, ))

    start = State((closure_lr1(start_item, firsts)), True)

    pending = [start_item]
    visisted_centers = {centers(start.state): start}
    visited = {start_item: start}

    while pending:
        # if len(pending) > 124:
        #     print('ss')
        current_state = visited[pending.pop()]
        for symbol in G.terminals + G.nonTerminals:
            next_item = frozenset(goto_lr1(current_state.state, symbol,
                                           firsts))

            if next_item:
                # Caso en que pueda mezclar el nuevo item
                try:
                    next_state = visisted_centers[centers(next_item)]
                    if not subset(lookaheads(next_item),
                                  lookaheads(next_state.state)):
                        next_state.state = compress(
                            list(next_state.state) + list(next_item))
                        pending.append(frozenset(next_state.state))
                        visited[frozenset(next_state.state)] = next_state
                except KeyError:
                    next_state = State(next_item, True)
                    pending += [next_item]
                    visisted_centers[centers(next_item)] = next_state
                    visited[next_item] = next_state
                current_state.add_transition(symbol.Name, next_state)

    return start


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        # G = self.G.AugmentedGrammar() if not self.G.IsAugmentedGrammar else self.G

        automaton = build_LR1_automaton(self.G)
        for i, node in enumerate(automaton):
            node.idx = i
        progress = ProgressBar(term_width=30)
        for node in progress(automaton):
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    if item.production.Left == self.G.startSymbol:
                        self._register(self.action, (idx, self.G.EOF),
                                       ('OK', item.production))
                    else:
                        for lookahead in item.lookaheads:
                            self._register(self.action, (idx, lookahead),
                                           ('REDUCE', item.production))
                else:
                    next_symbol = item.NextSymbol
                    try:
                        if next_symbol.IsNonTerminal:
                            next_state = node.transitions[next_symbol.Name][0]
                            self._register(self.goto, (idx, next_symbol),
                                           next_state.idx)
                        else:
                            next_state = node.transitions[next_symbol.Name][0]
                            self._register(self.action, (idx, next_symbol),
                                           ('SHIFT', next_state.idx))
                    except KeyError:
                        pass

    @staticmethod
    def _register(table, key, value):
        # assert key not in table or table[key] == value, f'Shift-Reduce or Reduce-Reduce conflict!!!\n tried to put {value} in {key} already exist with value  {table[key]}'
        if not (key not in table or table[key] == value):
            print(
                f'Shift-Reduce or Reduce-Reduce conflict!!!\n tried to put {value} in {key} already exist with value  {table[key]}'
            )
            print(table)
            assert False
        table[key] = value


class LALRParser(ShiftReduceParser):
    def _build_parsing_table(self):
        register = LR1Parser._register
        G = self.G.AugmentedGrammar()
        automaton = build_lalr_automaton(G)
        for i, node in enumerate(automaton):
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        register(self.action, (idx, G.EOF),
                                 ('OK', item.production))
                    else:
                        for lookahead in item.lookaheads:
                            register(self.action, (idx, lookahead),
                                     ('REDUCE', item.production))
                else:
                    next_symbol = item.NextSymbol
                    try:
                        if next_symbol.IsNonTerminal:
                            next_state = node.transitions[next_symbol.Name][0]
                            register(self.goto, (idx, next_symbol),
                                     next_state.idx)
                        else:
                            next_state = node.transitions[next_symbol.Name][0]
                            register(self.action, (idx, next_symbol),
                                     ('SHIFT', next_state.idx))
                    except KeyError:
                        pass
