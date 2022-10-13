from regex_parser.nfa import construct


class Regex:
    def __init__(self, pattern):
        self.pattern = pattern
        self.input_str = ''
        self.compiled_nfa = None

    def compile(self):
        self.compiled_nfa = construct(self.pattern)

    def match(self, input_str):
        if self.compiled_nfa is None:
            self.compile()
        self.input_str = input_str
        pass

    
