#%%
from baseNodeTree.base import Node, AtomicNode, UnaryNode, BinaryNode
from automatons.nondeterministic import NFA
from automatons.operations import (
    automata_union,
    automata_concatenation,
    automata_closure
)
from automatons.transformation import nfa_to_deterministic
from grammar.grammar import Grammar
from lexer.tokens import Token
from parserr.ll1 import build_ll1_parser
from tools.evaluate import evaluate_parse

#%%


class EpsilonNode(AtomicNode):
    def evaluate(self):
        automaton = NFA(states=1, finals=[0], transitions={})
        return automaton


class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        automaton = NFA(states=2, finals=[1], transitions={(0, s): [1]})
        return automaton


class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        automaton = value
        for state in automaton.finals:
            try:
                automaton.transitions[state][''].append(automaton.start)
            except KeyError:
                automaton.transitions[state][''] = [automaton.start]
            try:
                automaton.transitions[automaton.start][''].append(state)
            except KeyError:
                automaton.transitions[automaton.start][''] = [state]

        return automaton


class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        automata = automata_union(lvalue, rvalue)
        return automata


class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        automata = automata_concatenation(lvalue, rvalue)
        return automata


class RangeNode(Node):
    def __init__(self, iterable):
        self.rang = iterable

    def evaluate(self):
        it = iter(self.rang)
        node = SymbolNode(next(it))
        while 1:
            try:
                node = UnionNode(node, SymbolNode(next(it)))
            except StopIteration:
                automata = node.evaluate()
                return automata


class PositiveClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_concatenation(value, automata_closure(value))


class QuestionNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_union(value, EpsilonNode('').evaluate())
#%%


class Regex(object):

    def __init__(self, regex, ignore_white_space=True):
        self.regex = regex
        self.G = Grammar()
        E = self.G.NonTerminal('E', True)
        T, F, A, X, Y, Z = self.G.NonTerminals('T F A X Y Z')
        pipe, star, opar, cpar, symbol, epsilon, plus, minus, obrack, cbrack, question = self.G.Terminals(
            '| * ( ) symbol ε + - [ ] ?')

        E %= T + X, lambda h, s: s[2], None, lambda h, s: s[1]
        X %= pipe + E, lambda h, s: UnionNode(h[0], s[2])
        X %= self.G.Epsilon, lambda h, s: h[0]
        T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]
        Y %= T, lambda h, s: ConcatNode(h[0], s[1])
        Y %= self.G.Epsilon, lambda h, s: h[0]
        F %= A + Z, lambda h, s: s[2], None, lambda h, s: s[1]
        Z %= star, lambda h, s: ClosureNode(h[0])
        Z %= plus, lambda h, s: PositiveClosureNode(h[0])
        Z %= question, lambda h, s: QuestionNode(h[0])
        Z %= self.G.Epsilon, lambda h, s: h[0]
        A %= symbol, lambda h, s: SymbolNode(s[1])
        A %= epsilon, lambda h, s: EpsilonNode(s[1])
        A %= opar + E + cpar, lambda h, s: s[2]

        self.automaton = self._build_automaton(regex, ignore_white_space)

    def _build_automaton(self, regex, ignore_white_space):

        def regex_tokenizer(regex, ignore_white_space):
            d = {term.Name: term for term in self.G.terminals}
            tokens = []
            symbol_term = [
                term for term in self.G.terminals if term.Name == 'symbol'][0]
            fixed_tokens = {tok.Name: Token(tok.Name, tok)
                            for tok in [d['|'], d['*'],
                                        d['+'], d['?'],
                                        d['('], d[')'],
                                        d['['], d[']'],
                                        d['-'], d['ε']]}

            for i, c in enumerate(regex):
                if c == "\\" or \
                   (ignore_white_space and c.isspace()):
                    continue
                try:
                    token = fixed_tokens[c]
                    if regex[i - 1] == '\\':
                        raise KeyError
                except KeyError:
                    token = Token(c, symbol_term)
                tokens.append(token)
            tokens.append(Token('$', self.G.EOF))
            return tokens

        toks = regex_tokenizer(regex, ignore_white_space)
        parser = build_ll1_parser(self.G)
        left_parse = parser(toks)
        tree = evaluate_parse(left_parse, toks)
        automatom = tree.evaluate()
        automaton = nfa_to_deterministic(automatom)
        return automaton

    def __call__(self, w: str):
        return self.automaton.recognize(w)
