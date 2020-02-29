from .abstract_component import Component


class dummy_component (Component):
    def __init__(self, component_name, *args, **kwargs):
        component_name = component_name + "dummy_"
        super().__init__(*args, component_name = component_name + "dummy_", **kwargs)
        


    def build_component(self):
        super().build_component()
        return "Sorry, this is just a %s component" %(self.component_name)


