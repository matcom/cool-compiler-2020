from automatons.state import State
from lexer.regexgenerator import Regex
from lexer.tokens import Token
from grammar.grammar import Terminal


class TokenLine(Token):
    '''
    Clase para representar el token constante de cambio de Linea
    '''
    def __init__(self):
        super().__init__('\n', 'Line')


class Lexer:
    """
    El generador de lexer se basa en un conjunto de expresiones regulares.
    Cada una de ellas está asociada a un tipo de token.
    El lexer termina siendo un autómata finito determinista con ciertas peculiaridades:
    - Resulta de transformar el autómata unión entre todas las expresiones regulares del lenguaje,
      y convertirlo a determinista.
    - Cada estado final almacena los tipos de tokens que se reconocen al alcanzarlo.
      Se establece una prioridad entre ellos para poder desambiaguar.
    - Para tokenizar, la cadena de entrada viaja repetidas veces por el autómata.
    - Cada vez, se comienza por el estado inicial, pero se continúa a partir de la última sección de la
      cadena que fue reconocida.
    - Cuando el autómata se "traba" durante el reconocimiento de una cadena, se reporta la ocurrencia de un token.
      Su lexema está formado por la concatenación de los símbolos que fueron consumidos desde el inicio y hasta pasar
      por el último estado final antes de trabarse. Su tipo de token es el de mayor relevancia entre los anotados en el
      estado final.
    - Al finalizar de consumir toda la cadena, se reporta el token de fin de cadena.
    """
    def __init__(self, table, eof, ignore_white_space=False):
        self.eof = eof
        self.regexs = self._build_regexs(table, ignore_white_space)
        self.automaton = self._build_automaton()
        self.ignore_white_space = ignore_white_space
        self.line = 1
        self.column = 1

    def _build_regexs(self, table, ignore_white_space):
        regexs = []
        # fixed blank tokens
        fixed_line_token = Regex('\n', ignore_white_space=False)
        fixed_space_token = Regex(' ', ignore_white_space=False)

        for n, (token_type, regex) in enumerate(table):

            regex = Regex(regex, ignore_white_space)

            start = State.from_nfa(regex.automaton)

            for state in start:
                if state.final:
                    state.tag = (n, token_type)
            regexs.append(start)

        line_automaton = State.from_nfa(fixed_line_token.automaton)
        space_automaton = State.from_nfa(fixed_space_token.automaton)

        for state in line_automaton:
            if state.final:
                state.tag = (len(table) + 1, 'Line')

        for state in space_automaton:
            if state.final:
                state.tag = (len(table) + 2, 'Space')

        regexs.append(line_automaton)
        regexs.append(space_automaton)
        return regexs

    def _build_automaton(self):
        start = State('start')

        for regex in self.regexs:
            start.add_epsilon_transition(regex)
        return start.to_deterministic()

    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        lex = ''
        suffix = ''
        continues = 0

        for i, symbol in enumerate(string):
            # handle special character for regex !:
            if symbol == '!' and suffix and suffix[0] == '"':
                suffix += symbol
                self.column += 1
                continue
            if symbol == '\\':
                if suffix and suffix[0] == '"' and i < len(
                        string) - 1 and string[i + 1] not in ('n', '"'):
                    self.column += 1
                    continues += 1
                    continue
            # Handle spcial case with a newline in a string
            if symbol == '\n' and suffix and suffix[0] == '"':
                if string[i - 1] == '\\':
                    self.column = 1
                    self.line += 1
                    continues += 1
                    continue
            next_state = state.transitions.get(symbol, None)
            if next_state:
                suffix += symbol
                self.column += 1
                state = next_state[0]
                if state.final:
                    lex += suffix
                    suffix = ''
                    final = state
            else:
                break

        return final, lex, suffix, continues

    def _tokenize(self, text):
        while text:
            string = text
            final, lex, suffix, continues = self._walk(string)
            if final:
                n = 2**64
                token_type = None
                for state in final.state:
                    try:
                        priority, tt = state.tag
                        if priority < n:
                            n = priority
                            token_type = tt
                    except TypeError:
                        pass
                # suffix contains characters that didnt match
                # so they would be count twice. We must substract
                # them from column
                self.column -= (len(suffix) + continues)
                yield lex, token_type
                text = string[len(lex) + continues:]
            else:
                if len(text) == len(suffix) + continues and suffix[0] == '"':
                    raise SyntaxError(
                        f'({self.line},{self.column}) - LexicographicError: String contains EOF'
                    )
                raise SyntaxError(
                    f'({self.line},{self.column}) - LexicographicError: ERROR "%r"'
                    % text[len(suffix) + continues])

        yield '$', self.eof

    def __call__(self, text: str):
        tokens = []
        for lex, ttype in self._tokenize(text):
            if isinstance(ttype, str) and ttype == 'Line':
                self.line += 1
                self.column = 1
            elif isinstance(ttype, str) and ttype == 'Space':
                # IGNORE WHITE SPACE
                pass
            else:
                tok = Token(lex, ttype, self.column, self.line)
                tokens.append(tok)

        return tokens
