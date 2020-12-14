"""
Este modulo contiene la declaracion de la clase ShiftReduceParser, la cual
sirve de base para los parsers SLR, LALR y LR
"""
from typing import Dict, List, Literal, Tuple, Union
from grammar.grammar import EOF, Grammar
from grammar.symbols import Production, Terminal
from lexer.tokens import Token

Action = Union[Literal["SHIFT"], Literal["REDUCE"], Literal["OK"]]
Tag = Union[Production, int]
ActionTableEntry = Tuple[int, Terminal]


class ShiftReduceParser:
    """
    Clase base para los parsers SLR(1), LALR(1) y LR(1).
    No se debe instanciar directamente, en vez de eso, todo parser
    cuyo funcionamiento se base en las acciones shift reduce deben heredar
    de esta clase e implementar el metodo build_parsing_table.
    """

    SHIFT = "SHIFT"
    REDUCE = "REDUCE"
    OK = "OK"

    def __init__(self, G: Grammar, verbose: bool = False):
        self.G = G
        self.verbose = verbose
        self.action: Dict[ActionTableEntry, Tuple[Action, Tag]] = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, tokens: List[Token]):
        stack = [0]
        cursor = 0
        output = []

        if isinstance(tokens[0].token_type, EOF):
            raise SyntaxError("(0,0) - SyntacticError: Cool program must not be empty.")

        while True:
            state = stack[-1]
            lookahead = tokens[cursor].token_type
            try:
                action, tag = self.action[state, lookahead]
            except KeyError:
                col = tokens[cursor].token_column - len(tokens[cursor].lex)
                if lookahead.Name == "self" or (
                    lookahead.Name == "assign"
                    and tokens[cursor - 1].token_type.Name == "self"
                ):
                    raise SyntaxError(
                        f"({tokens[cursor].token_line},{col}) - "
                        + f' SemanticError: ERROR "%s"' % tokens[cursor].lex
                    )
                raise SyntaxError(
                    f"({tokens[cursor].token_line},{col}) - "
                    + f' SyntacticError: ERROR "%s"' % tokens[cursor]
                )

            if action == self.SHIFT:
                cursor += 1
                assert isinstance(tag, int)
                stack.append(tag)

            elif action == self.REDUCE:
                assert isinstance(tag, Production)
                head, body = tag

                for _ in range(len(body)):
                    stack.pop()

                output.append(tag)
                new_state = self.goto[stack[-1], head]
                stack.append(new_state)

            elif action == self.OK:
                output.append(tag)
                return output[::-1]

            else:
                raise Exception("La cadena no pertenece al lenguaje")

    def dumps_parser_state(self, file):
        """
        Devuelve un formato objeto de tipo bytes (o string)
        que sirve para guardar el estado del parser en un fichero
        para cargarlo posteriormente con load.
        """
        try:
            import cloudpickle  # type: ignore
        except ImportError:
            return False

        try:
            cloudpickle.dump(self, file)
            return True
        except Exception:
            return False

    @staticmethod
    def load_parser_state(file):
        try:
            import cloudpickle as pickle

            return pickle.load(file)
        except ImportError:
            return None
