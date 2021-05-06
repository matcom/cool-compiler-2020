# Generic Error
ERROR = '(%d, %d) - %s: %s'

def LexicographicError(line, col, message):
    return ERROR % (line, col, "LexicographicError", message)

def SyntacticError(line, col, message):
    return ERROR % (line, col, "SyntacticError", message)