from cmp.pycompiler import Production, Sentence, Symbol, EOF, Epsilon

class ContainerSet:
    def __init__(self, *values, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def extend(self, values):
        change = False
        for value in values:
            change |= self.add(value)
        return change

    def set_epsilon(self, value=True):
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    def update(self, other):
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other):
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)

    def hard_update(self, other):
        return self.update(other) | self.epsilon_update(other)

    def find_match(self, match):
        for item in self.set:
            if item == match:
                return item
        return None

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        return '%s-%s' % (str(self.set), self.contains_epsilon)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.set)

    def __nonzero__(self):
        return len(self) > 0

    def __eq__(self, other):
        if isinstance(other, set):
            return self.set == other
        return isinstance(other, ContainerSet) and self.set == other.set and self.contains_epsilon == other.contains_epsilon


def inspect(item, grammar_name='G', mapper=None):
    try:
        return mapper[item]
    except (TypeError, KeyError ):
        if isinstance(item, dict):
            items = ',\n   '.join(f'{inspect(key, grammar_name, mapper)}: {inspect(value, grammar_name, mapper)}' for key, value in item.items() )
            return f'{{\n   {items} \n}}'
        elif isinstance(item, ContainerSet):
            args = f'{ ", ".join(inspect(x, grammar_name, mapper) for x in item.set) } ,' if item.set else ''
            return f'ContainerSet({args} contains_epsilon={item.contains_epsilon})'
        elif isinstance(item, EOF):
            return f'{grammar_name}.EOF'
        elif isinstance(item, Epsilon):
            return f'{grammar_name}.Epsilon'
        elif isinstance(item, Symbol):
            return f"G['{item.Name}']"
        elif isinstance(item, Sentence):
            items = ', '.join(inspect(s, grammar_name, mapper) for s in item._symbols)
            return f'Sentence({items})'
        elif isinstance(item, Production):
            left = inspect(item.Left, grammar_name, mapper)
            right = inspect(item.Right, grammar_name, mapper)
            return f'Production({left}, {right})'
        elif isinstance(item, tuple) or isinstance(item, list):
            ctor = ('(', ')') if isinstance(item, tuple) else ('[',']')
            return f'{ctor[0]} {("%s, " * len(item)) % tuple(inspect(x, grammar_name, mapper) for x in item)}{ctor[1]}'
        else:
            raise ValueError(f'Invalid: {item}')

def pprint(item, header=""):
    if header:
        print(header)

    if isinstance(item, dict):
        for key, value in item.items():
            print(f'{key}  --->  {value}')
    elif isinstance(item, list):
        print('[')
        for x in item:
            print(f'   {repr(x)}')
        print(']')
    else:
        print(item)

class Token:
    """
    Basic token class.

    Parameters
    ----------
    lex : str
        Token's lexeme.
    token_type : Enum
        Token's type.
    """

    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def __str__(self):
        return f'{self.token_type}: {self.lex}'

    def __repr__(self):
        return str(self)

    @property
    def is_valid(self):
        return True

class UnknownToken(Token):
    def __init__(self, lex):
        Token.__init__(self, lex, None)

    def transform_to(self, token_type):
        return Token(self.lex, token_type)

    @property
    def is_valid(self):
        return False

def tokenizer(G, fixed_tokens):
    def decorate(func):
        def tokenize_text(text):
            tokens = []
            for lex in text.split():
                try:
                    token = fixed_tokens[lex]
                except KeyError:
                    token = UnknownToken(lex)
                    try:
                        token = func(token)
                    except TypeError:
                        pass
                tokens.append(token)
            tokens.append(Token('$', G.EOF))
            return tokens

        if hasattr(func, '__call__'):
            return tokenize_text
        elif isinstance(func, str):
            return tokenize_text(func)
        else:
            raise TypeError('Argument must be "str" or a callable object.')
    return decorate

class DisjointSet:
    def __init__(self, *items):
        self.nodes = { x: DisjointNode(x) for x in items }

    def merge(self, items):
        items = (self.nodes[x] for x in items)
        try:
            head, *others = items
            for other in others:
                head.merge(other)
        except ValueError:
            pass

    @property
    def representatives(self):
        return { n.representative for n in self.nodes.values() }

    @property
    def groups(self):
        return [[n for n in self.nodes.values() if n.representative == r] for r in self.representatives]

    def __len__(self):
        return len(self.representatives)

    def __getitem__(self, item):
        return self.nodes[item]

    def __str__(self):
        return str(self.groups)

    def __repr__(self):
        return str(self)

class DisjointNode:
    def __init__(self, value):
        self.value = value
        self.parent = self

    @property
    def representative(self):
        if self.parent != self:
            self.parent = self.parent.representative
        return self.parent

    def merge(self, other):
        other.representative.parent = self.representative

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)