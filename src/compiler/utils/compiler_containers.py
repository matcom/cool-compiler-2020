from dependency_injector import containers, providers
from compiler.components.dummy_component import dummy_component 
import lexer_definitions


class component_container (containers.DeclarativeContainer):
    dummy_lexer = providers.Factory(dummy_component, "Lexer")
    dummy_parser = providers.Factory(dummy_component, "Parser")


container_dict = { 
    'lexer_options': { 'd': component_container.dummy_lexer },
    'parser_options': {'d' : component_container.dummy_parser}  
    }    

class lexer_analyzer_dependency_container (containers.DeclarativeContainer):
    reserved_keywords_cool = providers.Callable(lambda value: value, lexer_definitions.basic_keywords)
    tokens_collection_cool = providers.Callable(lambda value: value, lexer_definitions.tokens_collection)
    simple_rules_cool = providers.Callable(lambda value: value, lexer_definitions.simple_rules_cool)


