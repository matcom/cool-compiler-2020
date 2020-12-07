class error:
    def __init__(self, error_type, row_and_col, message):
        self.error_type = error_type
        self.row_and_col = row_and_col
        self.message = message

    def __str__(self):
        return '(%d, %d) - %s: %s' %(self.row_and_col[0], self.row_and_col[1], self.error_type, self.message)

    __repr__ = __str__


errorSelector = {'repeated class': lambda idName, row_and_col=(0,0):error(
                      error_type= 'Semantic error',
                      row_and_col= row_and_col,
                      message= 'Class %s already exist' %idName
                    ),
                'undefined type': lambda idName, row_and_col=(0,0):error(
                      error_type='Semantic error',
                      row_and_col= row_and_col,
                      message= "The type %s doesn't exist in the current context" %idName,
                ),
                'repeated attr': lambda idName, row_and_col=(0,0):error(
                      error_type='Semantic error',
                      row_and_col=row_and_col,
                      message="The attribute %s is already defined in the current context" %idName
                ),
                'repeated method': lambda idName, row_and_col=(0,0):error(
                      error_type='Semantic error',
                      row_and_col=row_and_col,
                      message="The method %s is already defined in the current context" %idName
                ),
                'built-in inheritance': lambda idName, row_and_col=(0,0): error (
                    error_type='Semantic error',
                    row_and_col=row_and_col,
                    message="The class %s is sealed. You can't inherit from it" %idName
                ),
                'inheritance from child': lambda idChild, idParent, row_and_col=(0,0): error (
                    error_type='Semantic error',
                    row_and_col=row_and_col,
                    message="The class %s is an ancestor of %s class" %(idParent, idChild)
                ),
                 'Inherit from itself': lambda idName, row_and_col=(0,0): error (
                    error_type='Semantic error',
                    row_and_col=row_and_col,
                    message="The class %s  can't inherit from itself" %(idName)
                ),
                'undefined method in class': lambda idName, className, row_and_col=(0,0): error (
                    error_type= 'Semantic error',
                    row_and_col= row_and_col,
                    message="The class %s has no method called %s" %(idName, className)
                ),
                'undefined arguments for method in class': lambda idName, className, undefinedArgs, row_and_col=(0,0): error (
                    error_type= 'Semantic error',
                    row_and_col= row_and_col,
                    message="The arguments %s does not exists in method %s in class %s " %(undefinedArgs, idName, className)
                ),
                'uncompatible types': lambda type1, type2, row_and_col=(0,0): error (
                    error_type= 'Semantic error',
                    row_and_col= row_and_col,
                    message="Uncompatible types %s and %s in %s " %(type1, type2, row_and_col)
                ),
                'undefined symbol': lambda symbolName, row_and_col=(0,0): error (
                    error_type= 'Semantic error',
                    row_and_col= row_and_col,
                    message="Undefined symbol %s at %s" %(symbolName, row_and_col)
                )
                }

def interceptError(validationFunc, errorType: str, **argumentsConstructor):
    return (not validationFunc()) and errorSelector[errorType](**argumentsConstructor)
