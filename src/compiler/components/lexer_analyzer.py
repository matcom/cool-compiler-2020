from .abstract_component import Component
from ..utils.compiler_containers import lexer_analyzer_dependency_container as injector
from ply import lex

class lexer_analyzer(Component):
    def __init__(self,
                tokens_collection,
                basic_keywords,
                simple_rules,
                complex_rules,
                error_handlers,
                *args,
                **kwargs):                
        self.inject(complex_rules)
        self.inject(error_handlers)
        self.tokens_collection = tokens_collection
        self.basic_keywords = basic_keywords
        super().__init__(*args, **kwargs)

    def inject(self, function_group):
        for function in function_group:
            super().__setattr__(function.__name__, function)

    
    def build_component(self):
        self.reserved = self.basic_keywords.keys()
        self.tokens = self.tokens_collection + tuple(self.basic_keywords.values())
        self.lexer = lex.lex(module = self)

        
    def input_lexer(self, cool_program_source_code):
        self.lexer.input(cool_program_source_code)
        

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token


    # A funny iterator here
    def __iter__(self):
        return self

    def __next__(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    def next(self):
        return self.__next__()
    # End of fun



if __name__ == "__main__":
    import sys

    input_info = sys.argv[1]
    with open(input_info, encoding = 'utf-8') as file:
        cool_program_source_code = file.read()
    
    lexer = lexer_analyzer(tokens_collection = injector.tokens_collection_cool,
                        basic_keywords = injector.reserved_keywords_cool, 
                        simple_rules = injector.simple_rules_cool, 
                        complex_rules = injector.complex_rules_cool,
                        error_handlers = injector.error_handlers_cool)
    lexer.input_lexer(cool_program_source_code)

    for token in lexer:
        print(token)