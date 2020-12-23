class error:
    def __init__(self, error_type, row_and_col, message):
        self.error_type = error_type
        self.row_and_col = row_and_col
        self.message = message

    def __str__(self):
        return '(%d, %d) - %s: %s' %(self.row_and_col[0], self.row_and_col[1], self.error_type, self.message)

    __repr__ = __str__


errorSelector = {'repeated class basic': lambda idName, row_and_col=(0,0):error(
                      error_type= 'SemanticError',
                      row_and_col= row_and_col,
                      message= 'Redefinition of basic class %s' %idName
                    ),
                 'repeated class': lambda idName, row_and_col=(0,0):error(
                      error_type= 'SemanticError',
                      row_and_col= row_and_col,
                      message= 'Redefinition of basic class %s' %idName
                    ),
                'undefined type': lambda idName, row_and_col=(0,0):error(
                      error_type='TypeError',
                      row_and_col= row_and_col,
                      message= "The type %s doesn't exist in the current context" %idName,
                ),
                'undefined type in attr': lambda idAttr, idBadType, row_and_col= (0,0): error (
                    error_type='TypeError',
                    row_and_col= row_and_col,
                    message= 'Class %s of attribute %s is undefined.' %(idBadType, idAttr)
                ),
                'uncompatible types': lambda type1, type2, row_and_col= (0,0): error (
                    error_type='TypeError',
                    row_and_col= row_and_col,
                    message= 'Bad assign %s to %s' %(type1, type2)
                ),
                'repeated attr': lambda idName, row_and_col=(0,0):error(
                      error_type='SemanticError',
                      row_and_col=row_and_col,
                      message="Attribute %s is multiply defined in class." %idName
                ),
                'repeated method': lambda idName, row_and_col=(0,0):error(
                      error_type='SemanticError',
                      row_and_col=row_and_col,
                      message="Method %s is multiply defined." %idName
                ),
                'built-in inheritance': lambda idName, idParent, row_and_col=(0,0): error (
                    error_type='SemanticError',
                    row_and_col=row_and_col,
                    message="Class %s cannot inherit class %s." %(idName, idParent)
                ),
                'inheritance from child': lambda idChild, row_and_col=(0,0): error (
                    error_type='SemanticError',
                    row_and_col=row_and_col,
                    message="Class %s, or an ancestor of %s, is involved in an inheritance cycle." %(idChild, idChild)
                ),
                'undefined method in class': lambda idName, className, row_and_col=(0,0): error (
                    error_type= 'TypeError',
                    row_and_col= row_and_col,
                    message="The class %s has no method called %s" %(idName, className)
                ),
                'undefined arguments for method in class': lambda idName, className, undefinedArgs, row_and_col=(0,0): error (
                    error_type= 'TypeError',
                    row_and_col= row_and_col,
                    message="The arguments %s does not exists in method %s in class %s " %(undefinedArgs, idName, className)
                ),
                'arithmetic fail': lambda type1, type2, symbolOp, row_and_col=(0,0): error (
                    error_type= 'TypeError',
                    row_and_col= row_and_col,
                    message="non-Int arguments: %s %s %s." %(type1, symbolOp, type2)
                ),
                'undefined symbol': lambda symbolName, row_and_col=(0,0): error (
                    error_type= 'NameError',
                    row_and_col= row_and_col,
                    message="Undeclared identifier %s." %symbolName
                ),
                'not ancestor in dispatch': lambda idName, returnType, row_and_col=(0,0): error (
                    error_type= 'TypeError',
                    row_and_col= row_and_col,
                    message= 'Type %s is not subtype of %s at %s.' %(idName, returnType, row_and_col)
                ),
                'comparison fail': lambda row_and_col= (0,0): error(
                    error_type= 'TypeError',
                    row_and_col=row_and_col,
                    message= 'Illegal comparison with a basic type.'
                ),
                'uncompatible assing object': lambda idName, type1, type2, row_and_col = (0,0) : error (
                    error_type='TypeError',
                    row_and_col= row_and_col,
                    message= "Inferred type %s of initialization of %s does not conform to identifier's declared type %s." %(type1, idName, type2)
                ),
                'self parameter': lambda row_and_col = (0,0) : error (
                    error_type= 'SemanticError',
                    row_and_col= row_and_col,
                    message= "'self' cannot be the name of a formal parameter."
                ),
                'boolean fail': lambda type1, type2, row_and_col=(0,0): error (
                    error_type= 'TypeError',
                    row_and_col= row_and_col,
                    message="non-Bool arguments: %s + %s." %(type1, type2)
                ),
                'uncompatible assign attr': lambda idName, type1, type2, row_and_col = (0,0): error (
                    error_type='TypeError',
                    row_and_col= row_and_col,
                    message="Inferred type %s of initialization of attribute %s does not conform to declared type %s" %( type1, idName, type2)
                ),
                'bad ~': lambda type1, type2, row_and_col = (0,0): error (
                    error_type='TypeError',
                    row_and_col= row_and_col,
                    message="Argument of '~' has type %s instead of %s." %( type1, type2)
                ),
                'bad not': lambda type1, type2, row_and_col = (0,0): error (
                    error_type='TypeError',
                    row_and_col= row_and_col,
                    message="Argument of 'not' has type %s instead of %s." %( type1, type2)
                ),
                'not method in class': lambda idMethod, row_and_col= (0,0): error (
                    error_type='AttributeError',
                    row_and_col= row_and_col,
                    message= "Dispatch to undefined method %s." %(idMethod)
                ),
                'bad dispatch': lambda idMethod, badType, badArg, realType, row_and_col= (0,0): error(
                    error_type='TypeError',
                    row_and_col= row_and_col,
                    message= "In call of method %s, type %s of parameter %s does not conform to declared type %s." %(idMethod, badType, badArg, realType)
                ),
                'bad static dispatch': lambda typeLef, typeRight, row_and_col= (0,0): error(
                    error_type='TypeError',
                    row_and_col= row_and_col,
                    message="Expression type %s does not conform to declared static dispatch type %s." %(typeLef, typeRight)
                ),
                'self assign': lambda row_and_col= (0,0): error (
                    error_type= 'SemanticError',
                    row_and_col= row_and_col,
                    message= "Cannot assign to 'self'."
                ),
                'bad predicate': lambda row_and_col= (0,0): error (
                    error_type= 'TypeError',
                    row_and_col= row_and_col,
                    message= 'Loop condition does not have type Bool.'
                ),
                'bad redefine method': lambda methodName, badType, goodType, row_and_col= (0,0): error(
                    error_type= 'SemanticError',
                    row_and_col= row_and_col,
                    message ='In redefined method %s, parameter type %s is different from original type %s.' %(methodName, badType, goodType)
                ),
                'bad returnType in redefine method': lambda methodName, badType, goodType, row_and_col= (0,0): error (
                    error_type= 'SemanticError',
                    row_and_col= row_and_col,
                    message= 'In redefined method %s, return type %s is different from original return type %s.' %(methodName, badType, goodType)
                ),
                'bad length in redefine': lambda methodName, row_and_col= (0,0): error (
                    error_type='SemanticError',
                    row_and_col= row_and_col,
                    message= 'Incompatible number of formal parameters in redefined method %s.' %(methodName)
                ),
                'bad redefine attr': lambda badAttr, row_and_col= (0,0) : error(
                    error_type= 'SemanticError',
                    row_and_col= row_and_col,
                    message= 'Attribute %s is an attribute of an inherited class.' %(badAttr)
                )
                }

def interceptError(validationFunc, errorOption: str, **argumentsConstructor):
    return (not validationFunc()) and errorSelector[errorOption](**argumentsConstructor)
