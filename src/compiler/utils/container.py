from dependency_injector import containers, providers
from compiler.components.dummy_component import dummy_component 



class component_container (containers.DeclarativeContainer):
    dummy_lexer = providers.Factory(dummy_component, "Lexer")
    dummy_parser = providers.Factory(dummy_component, "Parser")


    




