class CoolError(Exception):
    def __init__(self, text, line, column):
        super().__init__(text)
        self.line = line
        self.column = column

    @property
    def error_type(self):
        return 'CoolError'

    @property
    def text(self):
        return self.args[0]

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.error_type}: {self.text}'

    def __repr__(self):
        return str(self)


class CompilerError(CoolError):
    'Se reporta al presentar alguna anomalia con la entrada del compilador'

    UNKNOWN_FILE = 'The file "%s" does not exist'
    
    @property
    def error_type(self):
        return 'CompilerError'
    

class LexicographicError(CoolError):
    'Errores detectados por el lexer'

    UNKNOWN_TOKEN = 'ERROR "%s"'
    UNDETERMINATED_STRING = 'Undeterminated string constant'
    EOF_COMMENT = 'EOF in comment'
    EOF_STRING = 'EOF in string constant'
    NULL_STRING = 'String contains null character'

    @property
    def error_type(self):
        return 'LexicographicError'
    

class SyntaticError(CoolError):
    'Errores detectados en el parser'

    ERROR = 'ERROR at or near "%s"'

    @property
    def error_type(self):
        return 'SyntacticError'
    

class SemanticError(CoolError):
    'Otros errores semanticos'

    SELF_IS_READONLY = 'Variable "self" is read-only.'
    LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
    MISSING_PARAMETER = 'Missing argument "%s" in function call "%s"'
    TOO_MANY_ARGUMENTS = 'Too many arguments for function call "%s"'
    
    @property
    def error_type(self):
        return 'SemanticError'


class NamesError(SemanticError):
    'Se reporta al referenciar a un identificador en un ambito en el que no es visible'

    USED_BEFORE_ASSIGNMENT = 'Variable "%s" used before being assigned'
    VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
    
    @property
    def error_type(self):
        return 'NameError'
    

class TypesError(SemanticError):
    'Se reporta al detectar un problema de tipos'

    INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
    INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
    INCORRECT_TYPE = 'Incorrect type "%s" waiting "%s"'
    BOPERATION_NOT_DEFINED = '%s operations are not defined between "%s" and "%s"'
    UOPERATION_NOT_DEFINED = '%s operations are not defined for "%s"'
    CIRCULAR_DEPENDENCY = 'Circular dependency between %s and %s'    

    PARENT_ALREADY_DEFINED = 'Parent type is already set for "%s"'
    TYPE_ALREADY_DEFINED = 'Type with the same name (%s) already in context.'
    TYPE_NOT_DEFINED = 'Type "%s" is not defined.'

    @property
    def error_type(self):
        return 'TypeError'
    

class AttributesError(SemanticError):
    'Se reporta cuando un atributo o método se referencia pero no está definido'

    WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
    
    METHOD_ALREADY_DEFINED = 'Method "%s" is already defined in class "%s"'
    METHOD_NOT_DEFINED = 'Method "%s" is not defined in "%s"'
    ATTRIBUTE_ALREADY_DEFINED = 'Attribute "%s" is already defined in %s'
    ATTRIBUTE_NOT_DEFINED = 'Attribute "%s" is not defined in %s'

    @property
    def error_type(self):
        return 'AttributeError'
    