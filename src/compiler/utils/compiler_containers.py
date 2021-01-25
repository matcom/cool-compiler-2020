from dependency_injector import containers, providers
from ..components import dummy_component, lexer_analyzer
from ..utils import lexer_definitions

component_injector = { 
    'lexer_options': { 'dummy': dummy_component, 
                        'cool' : lexer_analyzer },
    'parser_options': {'dummy' : dummy_component}
    }

params_for_component = {
    'lexer' : {
        'cool' : {
             'basic_keywords': lexer_definitions.basic_keywords,
              'simple_rules' : lexer_definitions.simple_rules,
              'complex_rules' : lexer_definitions.complex_rules,
              'tokens_collection' : lexer_definitions.tokens_collection,
              'error_handlers' : lexer_definitions.error_handlers            
        }
    }
}