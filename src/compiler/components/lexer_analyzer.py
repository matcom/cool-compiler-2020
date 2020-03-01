from .abstract_component import Component
from ..utils.compiler_containers import lexer_analyzer_dependency_container as injector
from ply import lex

class lexer_analyzer(Component):
    def __init__(self,
                tokens_collection,
                basic_keywords,
                simple_rules,
                complex_rules,
                *args,
                **kwargs):                
        self.inject_complex_rules(complex_rules)
        self.tokens_collection = tokens_collection
        self.basic_keywords = basic_keywords
        super().__init__(*args, **kwargs)

    def inject_complex_rules(self, complex_rules):
        for x in complex_rules:
            super().__setattr__(x.__name__, x)

    
    def build_component(self):
        self.reserved = self.basic_keywords.keys()
        self.tokens = self.tokens_collection + tuple(self.basic_keywords.values())
        self.lexer = lex.lex(module = self)
        
    def input_lexer(self, cool_program_source_code):
        self.lexer.input(cool_program_source_code)
        

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token
