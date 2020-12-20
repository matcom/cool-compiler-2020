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
                'uncompatible types': lambda type1, type2, row_and_col= (0,0): error (
                    error_type='TypeError',
                    row_and_col= row_and_col,
                    message= 'Bad assign %s to %s' %(type1, type2)
                ),
                'repeated attr': lambda idName, row_and_col=(0,0):error(
                      error_type='TypeError',
                      row_and_col=row_and_col,
                      message="The attribute %s is already defined in the current context" %idName
                ),
                'repeated method': lambda idName, row_and_col=(0,0):error(
                      error_type='TypeError',
                      row_and_col=row_and_col,
                      message="The method %s is already defined in the current context" %idName
                ),
                'built-in inheritance': lambda idName, idParent, row_and_col=(0,0): error (
                    error_type='SemanticError',
                    row_and_col=row_and_col,
                    message="Class %s cannot inherit class %s." %(idName, idParent)
                ),
                'inheritance from child': lambda idChild, idParent, row_and_col=(0,0): error (
                    error_type='TypeError',
                    row_and_col=row_and_col,
                    message="The class %s is an ancestor of %s class" %(idParent, idChild)
                ),
                 'Inherit from itself': lambda idName, row_and_col=(0,0): error (
                    error_type='TypeError',
                    row_and_col=row_and_col,
                    message="The class %s  can't inherit from itself" %(idName)
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
                )
                }

def interceptError(validationFunc, errorOption: str, **argumentsConstructor):
    return (not validationFunc()) and errorSelector[errorOption](**argumentsConstructor)
