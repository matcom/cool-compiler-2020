#(Row, Col) - ErrorType: Message
ERROR_FORMAT = "(%d, %d) - %s: %s"

# Error Types
COMPILER_ERR = 'CompilerError'
LEXICOGRAPHIC_ERR = 'LexicographicError'
SYNTACTIC_ERR = 'SyntacticError'
NAME_ERR = 'NameError'
TYPE_ERR = 'TypeError'
ATTRIBUTE_ERR = 'AttributeError'
SEMANTIC_ERR = 'SemanticError'

# Semantic Messages
WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
FORMAL_ERROR_SELF = '"self" identifier cannot be used as formal parameter'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
INCORRECT_TYPE = 'Incorrect type "%s" waiting "%s"'
USED_BEFORE_ASSIGNMENT = 'Variable "%s" used before being assigned'
CIRCULAR_DEPENDENCY = 'Circular dependency between %s and %s'
BOPERATION_NOT_DEFINED = '%s operations are not defined between "%s" and "%s"'
UOPERATION_NOT_DEFINED = '%s operations are not defined for "%s"'
MISSING_PARAMETER = 'Missing argument "%s" in function call "%s"'
TOO_MANY_ARGUMENTS = 'Too many arguments for function call "%s"'

class Error(object):
    def __init__(self, row, col, typex, message):
        self.row = row
        self.col = col
        self.type = typex
        self.message = message

    def __str__(self):
        return ERROR_FORMAT % (self.row, self.col, self.type, self.message)

class CompilerError(Error):
    def __init__(self, row, col, message):
        super().__init__(row, col, COMPILER_ERR, message)

class LexicographicError(Error):
    def __init__(self, row, col, message):
        super().__init__(row, col, LEXICOGRAPHIC_ERR, message)

class SyntacticError(Error):
    def __init__(self, row, col, message):
        super().__init__(row, col, SYNTACTIC_ERR, message)

class NameError(Error):
    def __init__(self, row, col, message):
        super().__init__(row, col, NAME_ERR, message)

class TypeError(Error):
    def __init__(self, row, col, message):
        super().__init__(row, col, TYPE_ERR, message)

# Base Semantic for others Errors, redefine constructor      
class BaseSemanticError(Error):
    def __init__(self, row, col, message):
        super().__init__(row, col, SEMANTIC_ERR, message)