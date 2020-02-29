from .abstract_component import Component


class lexer_analyzer(Component):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def tokens_collection():
        pass
    
    def build_component(self):
        super().build_component()        