from utils import compiler_containers

class compiler:
    def __init__(self, lexer, parser):
        self.symbolTable = {}
        self.lexer = lexer
        self.parser = parser
        pass