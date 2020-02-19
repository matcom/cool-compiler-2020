class Error:
    def __init__(self, error_name, description):
        self.error_name = error_name
        self.description = description

    def __str__(self):
        return f'{self.error_name}: {self.description}'


class LocalizedError(Error):
    def __init__(self, error_name, row, column, description):
        Error.__init__(self, 'SyntacticError', description)
        self.row = row
        self.column = column

    def __str__(self):
        return f'({self.row},{self.column}) - {self.error_name}: {self.description}'


class LexicographicError(LocalizedError):
    def __init__(self, row, column):
        LocalizedError.__init__(self, 'LexicographicError', row, column, 'Invalid character')


class SyntacticError(LocalizedError):
    def __init__(self, row, column, description):
        LocalizedError.__init__(self, 'SyntacticError', row, column, description)


class NameError(LocalizedError):
    def __init__(self, row, column, description):
        LocalizedError.__init__(self, 'NameError', row, column, description)


class TypeError(LocalizedError):
    def __init__(self, row, column, description):
        LocalizedError.__init__(self, 'TypeError', row, column, description)


class AttributeError(LocalizedError):
    def __init__(self, row, column, description):
        LocalizedError.__init__(self, 'AttributeError', row, column, description)


class SemanticError(LocalizedError):
    def LocalizedError(self, row, column, description):
        LocalizedError.__init__(self, 'SemanticError', row, column, description)        


class CompilationError(LocalizedError):
    def __init__(self, row, column, description):
        LocalizedError.__init__(self, 'CompilationError', row, column, description)        
