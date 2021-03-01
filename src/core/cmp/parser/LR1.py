from .shift_reduce import ShiftReduceParser
from .utils import build_LR1_automaton, upd_table

class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        self.ok = True
        G = self.Augmented = self.G.AugmentedGrammar(True)

        automaton = self.automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
            node.tag = f'I{i}'

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == G.startSymbol:
                        self.ok &= upd_table(self.action, idx, G.EOF, (ShiftReduceParser.OK, ''))
                    else:
                        for lookahead in item.lookaheads:
                            self.ok &= upd_table(self.action, idx, lookahead, (ShiftReduceParser.REDUCE, prod))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.ok &= upd_table(self.action, idx, next_symbol, (ShiftReduceParser.SHIFT, node[next_symbol.Name][0].idx))
                    else:
                        self.ok &= upd_table(self.goto, idx, next_symbol, node[next_symbol.Name][0].idx)
