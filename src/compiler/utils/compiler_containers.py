from dependency_injector import containers, providers
from compiler.components.dummy_component import dummy_component 
import lexer_definitions
from compiler.components.lexer_analyzer import lexer_analyzer

class component_container (containers.DeclarativeContainer):
    dummy_lexer = providers.Factory(dummy_component, "Lexer")
    cool_lexer = providers.Factory(lexer_analyzer)
    dummy_parser = providers.Factory(dummy_component, "Parser")


container_dict = { 
    'lexer_options': { 'd': component_container.dummy_lexer },
    'parser_options': {'d' : component_container.dummy_parser}  
    }    

class lexer_analyzer_dependency_container (containers.DeclarativeContainer):
    #This is just readonly properties
    reserved_keywords_cool = lexer_definitions.basic_keywords
    tokens_collection_cool = lexer_definitions.tokens_collection
    simple_rules_cool = lexer_definitions.simple_rules
    complex_rules_cool = lexer_definitions.complex_rules
    error_handlers_cool = lexer_definitions.error_handlers
    #----------------

    

