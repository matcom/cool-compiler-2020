LEXER_ERRORS = []
PARSER_ERRORS = []


def add_lexer_error(line, column, message):
    LEXER_ERRORS.append(f'({line}, {column}) - LexicographicError: {message}')
