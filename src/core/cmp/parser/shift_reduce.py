class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w, get_shift_reduce=False):
        stack = [0]
        cursor = 0
        output = []
        operations = []

        while True:
            state = stack[-1]
            lookahead = w[cursor].token_type
            if self.verbose: print(stack, w[cursor:])

            # Your code here!!! (Detect error)
            if state not in self.action or lookahead not in self.action[state]:
                return None, (True, w[cursor]) #//TODO: Build the correct error using `w[cursor]`

            action, tag = list(self.action[state][lookahead])[0]
            # Your code here!!! (Shift case)
            if action is ShiftReduceParser.SHIFT:
                operations.append(ShiftReduceParser.SHIFT)
                stack.append(tag)
                cursor += 1
            # Your code here!!! (Reduce case)
            elif action is ShiftReduceParser.REDUCE:
                operations.append(ShiftReduceParser.REDUCE)
                if len(tag.Right):
                    stack = stack[:-len(tag.Right)]
                stack.append(list(self.goto[stack[-1]][tag.Left])[0])
                output.append(tag)
            # Your code here!!! (OK case)
            elif action is ShiftReduceParser.OK:
                return (output if not get_shift_reduce else(output,operations)), (False, None) 
            # Your code here!!! (Invalid case)
            else:
                raise ValueError
