from abstract_component import Component


class dummy_component (Component):
    def __init__(self, input, component_type: str):
        super().__init__(input)
        self.component_type = component_type


    def output(self):
        return "Sorry, this is just a dummy %s component" %(self.component_type)


