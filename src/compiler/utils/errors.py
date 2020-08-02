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
                )}

def interceptError(validationFunc, errorType: str, **argumentsConstructor):
    return (not validationFunc()) and errorSelector[errorType](**argumentsConstructor)
