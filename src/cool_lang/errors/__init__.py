class Error:
    def __init__(self, error_name, row, column, description):
        self.error_name = error_name
        self.row = row
        self.column = column
        self.description = description

    def __str__(self):
        return f'({self.row},{self.column}) - {self.error_name}: {self.description}'

class LexicographicError(Error):
    def __init__(self, row, column):
        Error.__init__(self, 'LexicographicError', row, column, 'Invalid character')

class SyntacticError(Error):
    def __init__(self, row, column, description):
        Error.__init__(self, 'SyntacticError', row, column, description)

class NameError(Error):
    def __init__(self, row, column, description):
        Error.__init__(self, 'NameError', row, column, description)

class TypeError(Error):
    def __init__(self, row, column, description):
        Error.__init__(self, 'TypeError', row, column, description)

class AttributeError(Error):
    def __init__(self, row, column, description):
        Error.__init__(self, 'AttributeError', row, column, description)

class SemanticError(Error):
    def __init__(self, row, column, description):
        Error.__init__(self, 'SemanticError', row, column, description)        
