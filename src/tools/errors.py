

class CoolError(Exception):
    @property
    def error_type(self):
        return 'CoolError'

    @property
    def text(self):
        return self.args[0]

class CompilerError(CoolError):
    'Se reporta al presentar alguna anomalia con la entrada del compilador'

    UNKNOWN_FILE = 'The file "%s" does not exist'
    
    @property
    def error_type(self):
        return 'CompilerError'
    
class LexicographicError(CoolError):
    'Errores detectados por el lexer'

    UNKNOWN_TOKEN = 'Invalid token "%s"'
    
    @property
    def error_type(self):
        return 'CompilerError'
    
class SyntaticError(CoolError):
    'Errores detectados en el parser'

    @property
    def error_type(self):
        return 'CompilerError'
    
class NameError(CoolError):
    'Se reporta al referenciar a un identificador en un ambito en el que no es visible'

    USED_BEFORE_ASSIGNMENT = 'Variable "%s" used before being assigned'
    
    @property
    def error_type(self):
        return 'CompilerError'
    

class TypeError(CoolError):
    'Se reporta al detectar un problema de tipos'

    INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
    INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
    #? INCORRECT_TYPE = 'Incorrect type "%s" waiting "%s"'
    BOPERATION_NOT_DEFINED = '%s operations are not defined between "%s" and "%s"'
    UOPERATION_NOT_DEFINED = '%s operations are not defined for "%s"'
    
    @property
    def error_type(self):
        return 'CompilerError'
    

class AttributeError(CoolError):
    'Se reporta cuando un atributo o método se referencia pero no está definido'

    VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
    WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
    
    @property
    def error_type(self):
        return 'CompilerError'
    
class SemanticError(CoolError):
    'Otros errores semanticos'

    SELF_IS_READONLY = 'Variable "self" is read-only.'
    LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
    CIRCULAR_DEPENDENCY = 'Circular dependency between %s and %s'
    MISSING_PARAMETER = 'Missing argument "%s" in function call "%s"'
    TOO_MANY_ARGUMENTS = 'Too many arguments for function call "%s"'
   
    @property
    def error_type(self):
        return 'CompilerError'
    