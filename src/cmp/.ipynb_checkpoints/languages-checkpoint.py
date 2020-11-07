from cmp.pycompiler import Sentence, Production
from cmp.utils import ContainerSet, Token, UnknownToken
from cmp.tools import build_parsing_table, metodo_predictivo_no_recursivo

class BasicXCool:
    def __init__(self, G):
        self.G = G
        self.fixed_tokens = { lex: Token(lex, G[lex]) for lex in '+ - * / ( )'.split() }

    @property
    def firsts(self):
        G = self.G
        return {
            G['+']: ContainerSet(G['+'] , contains_epsilon=False),
            G['-']: ContainerSet(G['-'] , contains_epsilon=False),
            G['*']: ContainerSet(G['*'] , contains_epsilon=False),
            G['/']: ContainerSet(G['/'] , contains_epsilon=False),
            G['(']: ContainerSet(G['('] , contains_epsilon=False),
            G[')']: ContainerSet(G[')'] , contains_epsilon=False),
            G['num']: ContainerSet(G['num'] , contains_epsilon=False),
            G['E']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
            G['T']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
            G['F']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
            G['X']: ContainerSet(G['-'], G['+'] , contains_epsilon=True),
            G['Y']: ContainerSet(G['/'], G['*'] , contains_epsilon=True),
            Sentence(G['T'], G['X']): ContainerSet(G['num'], G['('] , contains_epsilon=False),
            Sentence(G['+'], G['T'], G['X']): ContainerSet(G['+'] , contains_epsilon=False),
            Sentence(G['-'], G['T'], G['X']): ContainerSet(G['-'] , contains_epsilon=False),
            G.Epsilon: ContainerSet( contains_epsilon=True),
            Sentence(G['F'], G['Y']): ContainerSet(G['num'], G['('] , contains_epsilon=False),
            Sentence(G['*'], G['F'], G['Y']): ContainerSet(G['*'] , contains_epsilon=False),
            Sentence(G['/'], G['F'], G['Y']): ContainerSet(G['/'] , contains_epsilon=False),
            Sentence(G['num']): ContainerSet(G['num'] , contains_epsilon=False),
            Sentence(G['('], G['E'], G[')']): ContainerSet(G['('] , contains_epsilon=False)
        }

    @property
    def follows(self):
        G = self.G
        return {
            G['E']: ContainerSet(G[')'], G.EOF , contains_epsilon=False),
            G['T']: ContainerSet(G[')'], G['-'], G.EOF, G['+'] , contains_epsilon=False),
            G['F']: ContainerSet(G['-'], G.EOF, G['*'], G['/'], G[')'], G['+'] , contains_epsilon=False),
            G['X']: ContainerSet(G[')'], G.EOF , contains_epsilon=False),
            G['Y']: ContainerSet(G[')'], G['-'], G.EOF, G['+'] , contains_epsilon=False)
        }

    @property
    def table(self):
        G = self.G
        return {
            ( G['E'], G['num'], ): [ Production(G['E'], Sentence(G['T'], G['X'])), ],
            ( G['E'], G['('], ): [ Production(G['E'], Sentence(G['T'], G['X'])), ],
            ( G['X'], G['+'], ): [ Production(G['X'], Sentence(G['+'], G['T'], G['X'])), ],
            ( G['X'], G['-'], ): [ Production(G['X'], Sentence(G['-'], G['T'], G['X'])), ],
            ( G['X'], G[')'], ): [ Production(G['X'], G.Epsilon), ],
            ( G['X'], G.EOF, ): [ Production(G['X'], G.Epsilon), ],
            ( G['T'], G['num'], ): [ Production(G['T'], Sentence(G['F'], G['Y'])), ],
            ( G['T'], G['('], ): [ Production(G['T'], Sentence(G['F'], G['Y'])), ],
            ( G['Y'], G['*'], ): [ Production(G['Y'], Sentence(G['*'], G['F'], G['Y'])), ],
            ( G['Y'], G['/'], ): [ Production(G['Y'], Sentence(G['/'], G['F'], G['Y'])), ],
            ( G['Y'], G[')'], ): [ Production(G['Y'], G.Epsilon), ],
            ( G['Y'], G['-'], ): [ Production(G['Y'], G.Epsilon), ],
            ( G['Y'], G.EOF, ): [ Production(G['Y'], G.Epsilon), ],
            ( G['Y'], G['+'], ): [ Production(G['Y'], G.Epsilon), ],
            ( G['F'], G['num'], ): [ Production(G['F'], Sentence(G['num'])), ],
            ( G['F'], G['('], ): [ Production(G['F'], Sentence(G['('], G['E'], G[')'])), ]
        }

    @property
    def tokenizer(self):
        G = self.G
        fixed_tokens = self.fixed_tokens

        def tokenize_text(text):
            tokens = []
            for item in text.split():
                try:
                    float(item)
                    token = Token(item, G['num'])
                except ValueError:
                    try:
                        token = fixed_tokens[item]
                    except:
                        token = UnknownToken(item)
                tokens.append(token)
            eof = Token('$', G.EOF)
            tokens.append(eof)
            return tokens

        return tokenize_text

class PowXCool:
    def __init__(self, G):
        self.G = G

    @property
    def firsts(self):
        G = self.G
        return {
            G['+']: ContainerSet(G['+'] , contains_epsilon=False),
            G['-']: ContainerSet(G['-'] , contains_epsilon=False),
            G['*']: ContainerSet(G['*'] , contains_epsilon=False),
            G['/']: ContainerSet(G['/'] , contains_epsilon=False),
            G['^']: ContainerSet(G['^'] , contains_epsilon=False),
            G['(']: ContainerSet(G['('] , contains_epsilon=False),
            G[')']: ContainerSet(G[')'] , contains_epsilon=False),
            G['num']: ContainerSet(G['num'] , contains_epsilon=False),
            G['E']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
            G['T']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
            G['F']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
            G['A']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
            G['X']: ContainerSet(G['-'], G['+'] , contains_epsilon=True),
            G['Y']: ContainerSet(G['/'], G['*'] , contains_epsilon=True),
            G['Z']: ContainerSet(G['^'] , contains_epsilon=True),
            Sentence(G['T'], G['X']): ContainerSet(G['num'], G['('] , contains_epsilon=False),
            Sentence(G['+'], G['T'], G['X']): ContainerSet(G['+'] , contains_epsilon=False),
            Sentence(G['-'], G['T'], G['X']): ContainerSet(G['-'] , contains_epsilon=False),
            G.Epsilon: ContainerSet( contains_epsilon=True),
            Sentence(G['F'], G['Y']): ContainerSet(G['num'], G['('] , contains_epsilon=False),
            Sentence(G['*'], G['F'], G['Y']): ContainerSet(G['*'] , contains_epsilon=False),
            Sentence(G['/'], G['F'], G['Y']): ContainerSet(G['/'] , contains_epsilon=False),
            Sentence(G['A'], G['Z']): ContainerSet(G['num'], G['('] , contains_epsilon=False),
            Sentence(G['^'], G['F']): ContainerSet(G['^'] , contains_epsilon=False),
            Sentence(G['num']): ContainerSet(G['num'] , contains_epsilon=False),
            Sentence(G['('], G['E'], G[')']): ContainerSet(G['('] , contains_epsilon=False)
        }

    @property
    def follows(self):
        G = self.G
        return {
            G['E']: ContainerSet(G[')'], G.EOF , contains_epsilon=False),
            G['T']: ContainerSet(G['-'], G[')'], G.EOF, G['+'] , contains_epsilon=False),
            G['F']: ContainerSet(G['-'], G['*'], G['/'], G[')'], G.EOF, G['+'] , contains_epsilon=False),
            G['A']: ContainerSet(G['-'], G['*'], G['/'], G['^'], G[')'], G.EOF, G['+'] , contains_epsilon=False),
            G['X']: ContainerSet(G[')'], G.EOF , contains_epsilon=False),
            G['Y']: ContainerSet(G['-'], G[')'], G.EOF, G['+'] , contains_epsilon=False),
            G['Z']: ContainerSet(G['-'], G['*'], G['/'], G[')'], G.EOF, G['+'] , contains_epsilon=False)
        }

class Regex:
    def __init__(self, G):
        self.G = G

    @property
    def firsts(self):
        G = self.G
        return {
            G['|']: ContainerSet(G['|'] , contains_epsilon=False),
            G['*']: ContainerSet(G['*'] , contains_epsilon=False),
            G['(']: ContainerSet(G['('] , contains_epsilon=False),
            G[')']: ContainerSet(G[')'] , contains_epsilon=False),
            G['symbol']: ContainerSet(G['symbol'] , contains_epsilon=False),
            G['E']: ContainerSet(G['symbol'], G['('] , contains_epsilon=False),
            G['T']: ContainerSet(G['symbol'], G['('] , contains_epsilon=False),
            G['F']: ContainerSet(G['symbol'], G['('] , contains_epsilon=False),
            G['A']: ContainerSet(G['symbol'], G['('] , contains_epsilon=False),
            G['X']: ContainerSet(G['|'] , contains_epsilon=True),
            G['Y']: ContainerSet(G['symbol'], G['('] , contains_epsilon=True),
            G['Z']: ContainerSet(G['*'] , contains_epsilon=True),
            Sentence(G['T'], G['X']): ContainerSet(G['symbol'], G['('] , contains_epsilon=False),
            Sentence(G['|'], G['E']): ContainerSet(G['|'] , contains_epsilon=False),
            G.Epsilon: ContainerSet( contains_epsilon=True),
            Sentence(G['F'], G['Y']): ContainerSet(G['symbol'], G['('] , contains_epsilon=False),
            Sentence(G['T']): ContainerSet(G['symbol'], G['('] , contains_epsilon=False),
            Sentence(G['A'], G['Z']): ContainerSet(G['symbol'], G['('] , contains_epsilon=False),
            Sentence(G['*']): ContainerSet(G['*'] , contains_epsilon=False),
            Sentence(G['symbol']): ContainerSet(G['symbol'] , contains_epsilon=False),
            Sentence(G['('], G['E'], G[')']): ContainerSet(G['('] , contains_epsilon=False)
        }

    @property
    def follows(self):
        G = self.G
        return {
            G['E']: ContainerSet(G[')'], G.EOF , contains_epsilon=False),
            G['T']: ContainerSet(G['|'], G[')'], G.EOF , contains_epsilon=False),
            G['F']: ContainerSet(G['symbol'], G['|'], G['('], G[')'], G.EOF , contains_epsilon=False),
            G['A']: ContainerSet(G['symbol'], G.EOF, G['|'], G['*'], G['('], G[')'] , contains_epsilon=False),
            G['X']: ContainerSet(G[')'], G.EOF , contains_epsilon=False),
            G['Y']: ContainerSet(G['|'], G[')'], G.EOF , contains_epsilon=False),
            G['Z']: ContainerSet(G['symbol'], G.EOF, G['|'], G['('], G[')'] , contains_epsilon=False)
        }

    @property
    def table(self):
        G = self.G
        return {
            ( G['E'], G['symbol'], ): [ Production(G['E'], Sentence(G['T'], G['X'])), ],
            ( G['E'], G['('], ): [ Production(G['E'], Sentence(G['T'], G['X'])), ],
            ( G['X'], G['|'], ): [ Production(G['X'], Sentence(G['|'], G['E'])), ],
            ( G['X'], G[')'], ): [ Production(G['X'], G.Epsilon), ],
            ( G['X'], G.EOF, ): [ Production(G['X'], G.Epsilon), ],
            ( G['T'], G['symbol'], ): [ Production(G['T'], Sentence(G['F'], G['Y'])), ],
            ( G['T'], G['('], ): [ Production(G['T'], Sentence(G['F'], G['Y'])), ],
            ( G['Y'], G['symbol'], ): [ Production(G['Y'], Sentence(G['T'])), ],
            ( G['Y'], G['('], ): [ Production(G['Y'], Sentence(G['T'])), ],
            ( G['Y'], G['|'], ): [ Production(G['Y'], G.Epsilon), ],
            ( G['Y'], G[')'], ): [ Production(G['Y'], G.Epsilon), ],
            ( G['Y'], G.EOF, ): [ Production(G['Y'], G.Epsilon), ],
            ( G['F'], G['symbol'], ): [ Production(G['F'], Sentence(G['A'], G['Z'])), ],
            ( G['F'], G['('], ): [ Production(G['F'], Sentence(G['A'], G['Z'])), ],
            ( G['Z'], G['*'], ): [ Production(G['Z'], Sentence(G['*'])), ],
            ( G['Z'], G['symbol'], ): [ Production(G['Z'], G.Epsilon), ],
            ( G['Z'], G.EOF, ): [ Production(G['Z'], G.Epsilon), ],
            ( G['Z'], G['|'], ): [ Production(G['Z'], G.Epsilon), ],
            ( G['Z'], G['('], ): [ Production(G['Z'], G.Epsilon), ],
            ( G['Z'], G[')'], ): [ Production(G['Z'], G.Epsilon), ],
            ( G['A'], G['symbol'], ): [ Production(G['A'], Sentence(G['symbol'])), ],
            ( G['A'], G['('], ): [ Production(G['A'], Sentence(G['('], G['E'], G[')'])), ]
        }

    @property
    def parser(self):
        firsts = self.firsts
        follows = self.follows
        M = build_parsing_table(self.G, firsts, follows)
        parser = metodo_predictivo_no_recursivo(self.G, M)
        return parser