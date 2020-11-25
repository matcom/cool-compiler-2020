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
    'Errores detectados en el cool_parser'

    ERROR = 'ERROR at or near "%s"'

    @property
    def error_type(self):
        return 'SyntacticError'
    

class SemanticError(CoolError):
    'Otros errores semanticos'

    SELF_IS_READONLY = 'Cannot assign to \'self\'.'
    SELF_IN_LET = '\'self\' cannot be bound in a \'let\' expression.'
    SELF_PARAM = "'self' cannot be the name of a formal parameter."
    SELF_ATTR = "'self' cannot be the name of an attribute."

    LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
    ARGUMENT_ERROR = 'Method %s called with wrong number of arguments.'
    
    REDEFINITION_ERROR = 'Redefinition of basic class %s'
    INHERIT_ERROR = 'Class %s cannot inherit class %s.'

    @property
    def error_type(self):
        return 'SemanticError'


class NamesError(SemanticError):
    'Se reporta al referenciar a un identificador en un ambito en el que no es visible'

    VARIABLE_NOT_DEFINED = 'Undeclared identifier %s.'
    
    @property
    def error_type(self):
        return 'NameError'
    

class TypesError(SemanticError):
    'Se reporta al detectar un problema de tipos'

    INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'

    ATTR_TYPE_ERROR = 'Inferred type %s of initialization of attribute %s does not conform to declared type %s.'
    ATTR_TYPE_UNDEFINED = 'Class %s of attribute %s is undefined.'
    BOPERATION_NOT_DEFINED = 'non-Int arguments: %s %s %s.'
    COMPARISON_ERROR = 'Illegal comparison with a basic type.'
    UOPERATION_NOT_DEFINED = 'Argument of \'%s\' has type %s instead of %s.'
    CLASS_CASE_BRANCH_UNDEFINED  = 'Class %s of case branch is undefined.'
    TYPE_ALREADY_DEFINED = 'Classes may not be redefined.'
    PREDICATE_ERROR = 'Predicate of \'%s\' ddoes not have type %s.'
    INCOSISTENT_ARG_TYPE = 'In call of method %s, type %s of parameter %s does not conform to declared type %s.'
    INCOMPATIBLE_TYPES_DISPATCH = 'Expression type %s does not conform to declared static dispatch type %s.'
    INHERIT_UNDEFINED = 'Class %s inherits from an undefined class %s.'
    CIRCULAR_DEPENDENCY = 'Class %s, or an ancestor of %s, is involved in an inheritance cycle.'    
    UNCONFORMS_TYPE = 'Inferred type %s of initialization of %s does not conform to identifier\'s declared type %s.'
    UNDEFINED_TYPE_LET = 'Class %s of let-bound identifier %s is undefined.'
    LOOP_CONDITION_ERROR = 'Loop condition does not have type Bool.'
    PARAMETER_MULTY_DEFINED = 'Formal parameter %s is multiply defined.'
    RETURN_TYPE_ERROR = 'Inferred return type %s of method test does not conform to declared return type %s.'
    PARAMETER_UNDEFINED = 'Class %s of formal parameter %s is undefined.'
    RETURN_TYPE_UNDEFINED = 'Undefined return type %s in method %s.'
    NEW_UNDEFINED_CLASS = '\'new\' used with undefined class %s.'

    PARENT_ALREADY_DEFINED = 'Parent type is already set for "%s"'
    TYPE_NOT_DEFINED = 'Type "%s" is not defined.'

    @property
    def error_type(self):
        return 'TypeError'
    

class AttributesError(SemanticError):
    'Se reporta cuando un atributo o método se referencia pero no está definido'

    DISPATCH_UNDEFINED = 'Dispatch to undefined method %s.'
    METHOD_ALREADY_DEFINED = 'Method "%s" is multiply defined.'
    ATTRIBUTE_ALREADY_DEFINED = 'Attribute "%s" is multiply defined in class.'
    ATTR_DEFINED_PARENT = 'Attribute %s is an attribute of an inherited class.'
    WRONG_SIGNATURE_PARAMETER = 'In redefined method %s, parameter type %s is different from original type %s.'
    WRONG_SIGNATURE_RETURN = 'In redefined method %s, return type %s is different from original return type %s.'
    WRONG_NUMBER_PARAM = 'Incompatible number of formal parameters in redefined method %s.'
    
    METHOD_NOT_DEFINED = 'Method "%s" is not defined in "%s"'
    ATTRIBUTE_NOT_DEFINED = 'Attribute "%s" is not defined in %s'

    @property
    def error_type(self):
        return 'AttributeError'
    