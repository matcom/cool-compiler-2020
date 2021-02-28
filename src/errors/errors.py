"""
Copyright (c) 2020 School of Math and Computer Science, University of Havana

COOL compiler project
"""

LEXER_ERRORS = []
PARSER_ERRORS = []
SEMANTIC_ERRORS = []

ERR_TYPE = "TypeError"
ERR_SEMANTIC = "SemanticError"
ERR_ATTRIBUTE = "AttributeError"
ERR_NAME = "NameError"


def add_lexer_error(line, column, message):
    LEXER_ERRORS.append(f'({line}, {column}) - LexicographicError: {message}')


def add_parser_error(line, column, message):
    PARSER_ERRORS.append(f'({line}, {column}) - SyntacticError: {message}')


def add_semantic_error(line, column, message):
    SEMANTIC_ERRORS.append(f'({line}, {column}) - {message}')
