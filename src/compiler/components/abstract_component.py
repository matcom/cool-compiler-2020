
class Component:
    def __init__(self, 
                input_info,
                component_name,
                debug_session = False,
                error_log_file = None,
                build_after_initialize = True):
        self.input_info = input_info
        self.component_name = component_name
        self.debug_session = debug_session
        self.error_log_file = error_log_file
        
        if build_after_initialize: self.build_component()


    def build_component (self):
        if self.debug_session: 
            print('Building %s component' %self.component_name)
    
