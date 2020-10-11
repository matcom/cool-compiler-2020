# Compute column.
#     input is the input text string
#     lexpos is a lex position in token instance
def find_column(input, lexpos):
    line_start = input.rfind('\n', 0, lexpos) + 1
    return (lexpos - line_start) + 1

class Singleton(type):
    """ Singleton Pattern using metaclasses """

    def __init__(cls, *args):
        cls._instance = None
        type.__init__(cls, *args)

    def __call__(cls, *args):
        if cls._instance is None:
            cls._instance = type.__call__(cls, *args)
        return cls._instance

    def __new__(cls, *args, **kwargs):
        return type.__new__(cls, *args, **kwargs)