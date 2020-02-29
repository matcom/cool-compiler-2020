from .abstract_component import Component
from ..utils.compiler_containers import lexer_analyzer_dependency_container as injector
from ply import lex

class lexer_analyzer(Component):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    @property
    def tokens_collection(self):
        return  injector.tokens_collection_cool
        
    @property
    def basic_reserved(self):
        return injector.reserved_keywords_cool

    def build_component(self):
        self.reserved = self.basic_reserved.keys()
        self.tokens = self.tokens_collection + tuple(self.basic_reserved.values())
        self.lexer = lex.lex(module = self)
        