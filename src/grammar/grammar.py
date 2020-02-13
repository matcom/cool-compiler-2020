from grammar.symbols import (NonTerminal, Terminal, Sentence,
                             Epsilon, EOF, AttributeProduction)
import json


class Grammar():

    def __init__(self):

        self.Productions = []
        self.nonTerminals = []
        self.terminals = []
        self.startSymbol = None
        # production type
        self.pType = None
        self.Epsilon = Epsilon(self)
        self.EOF = EOF(self)

        self.symbDict = {}

    def NonTerminal(self, name, startSymbol=False):

        name = name.strip()
        if not name:
            raise Exception("Empty name")

        term = NonTerminal(name, self)

        if startSymbol:

            if self.startSymbol is None:
                self.startSymbol = term
            else:
                raise Exception("Cannot define more than one start symbol.")

        self.nonTerminals.append(term)
        self.symbDict[name] = term
        return term

    def NonTerminals(self, names):

        ans = tuple((self.NonTerminal(x) for x in names.strip().split()))

        return ans

    def Add_Production(self, production):

        if len(self.Productions) == 0:
            self.pType = type(production)

        assert type(
            production) == self.pType, "The Productions most be of only 1 type."

        production.Left.productions.append(production)
        self.Productions.append(production)

    def Terminal(self, name):

        name = name.strip()
        if not name:
            raise Exception("Empty name")

        term = Terminal(name, self)
        self.terminals.append(term)
        self.symbDict[name] = term
        return term

    def Terminals(self, names):

        ans = tuple((self.Terminal(x) for x in names.strip().split()))

        return ans

    def __str__(self):

        mul = '%s, '

        ans = 'Non-Terminals:\n\t'

        nonterminals = mul * (len(self.nonTerminals) - 1) + '%s\n'

        ans += nonterminals % tuple(self.nonTerminals)

        ans += 'Terminals:\n\t'

        terminals = mul * (len(self.terminals) - 1) + '%s\n'

        ans += terminals % tuple(self.terminals)

        ans += 'Productions:\n\t'

        ans += str(self.Productions)

        return ans

    @property
    def to_json(self):

        productions = []

        for p in self.Productions:
            head = p.Left.Name

            body = []

            for s in p.Right:
                body.append(s.Name)

            productions.append({'Head': head, 'Body': body})

        d = {'NonTerminals': [symb.Name for symb in self.nonTerminals if symb != self.startSymbol], 'Terminals':
             [symb.Name for symb in self.terminals],
             'Productions': productions}
        d['StartSymbol'] = self.startSymbol.Name

        return json.dumps(d)

    @staticmethod
    def from_json(data):
        data = json.loads(data)

        G = Grammar()
        dic = {'epsilon': G.Epsilon}
        dic[data['StartSymbol']] = G.NonTerminal(data['StartSymbol'], True)

        for term in data['Terminals']:
            dic[term] = G.Terminal(term)

        for noTerm in data['NonTerminals']:
            dic[noTerm] = G.NonTerminal(noTerm)

        for p in data['Productions']:
            head = p['Head']
            dic[head] %= Sentence(*[dic[term] for term in p['Body']])

        return G

    def copy(self):
        G = Grammar()
        G.Productions = self.Productions.copy()
        G.nonTerminals = self.nonTerminals.copy()
        G.terminals = self.terminals.copy()
        G.pType = self.pType
        G.startSymbol = self.startSymbol
        G.Epsilon = self.Epsilon
        G.EOF = self.EOF
        G.symbDict = self.symbDict.copy()

        return G

    @property
    def IsAugmentedGrammar(self):
        augmented = 0
        for left, right in self.Productions:
            if self.startSymbol == left:
                augmented += 1
        if augmented <= 1:
            return True
        else:
            return False

    def AugmentedGrammar(self):
        if not self.IsAugmentedGrammar:

            G = self.copy()
            S = G.startSymbol
            G.startSymbol = None
            SS = G.NonTerminal('S\'', True)
            if G.pType is AttributeProduction:
                SS %= S + G.Epsilon, lambda x: x
            else:
                SS %= S + G.Epsilon

            return G
        else:
            return self.copy()
