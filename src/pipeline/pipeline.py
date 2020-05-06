class Pipeline(object):
    def __init__(self, *args, **kwargs):
        self.states = []
        self.pipeline_errors = []

    def submit_state(self, state):
        self.states.append(state)

    def run_pipeline(self, inputx):
        self.pipeline_errors.clear() # clean old errors

        res = inputx
        for state in self.states:
            res = state.run(res)
            if state.stop:
                break

            # collect errors from current state
            self.pipeline_errors += state.errors

        return res

    def report_errors(self):
        for err in self.pipeline_errors:
            print(err) 