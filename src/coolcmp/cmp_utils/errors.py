class CmpErrors(Exception):
    def __init__(self, line, column, msg):
        self.line = line
        self.column = column
        self.msg = msg
    
    def __str__(self):
        return '({},{}) - {}: {}'.format(self.line, self.column, self.__class__.__name__, self.msg)

class CompilerError(CmpErrors): pass
class LexicographicError(CmpErrors): pass
class SyntacticError(CmpErrors): pass
class NameError(CmpErrors): pass
class TypeError(CmpErrors): pass
class AttributeError(CmpErrors): pass
class SemanticError(CmpErrors): pass
