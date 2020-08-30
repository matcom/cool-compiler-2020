from grammar.symbols import Terminal


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
    def __init__(self,
                 lex: str,
                 token_type: Terminal,
                 token_column=None,
                 token_line=None):
        self.lex = lex
        self.token_type = token_type
        self.token_column = token_column
        self.token_line = token_line

    def __str__(self):
        return f'{self.token_type}: {self.lex}'

    def __repr__(self):
        return str(self)
