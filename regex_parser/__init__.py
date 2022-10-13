from regex_parser.nfa import construct
from regex_parser.parse.parse import match as reg_match


class Regex:
    def __init__(self, pattern):
        self.pattern = pattern
        self.input_str = ''
        self.__compiled_nfa = None

    def compile(self):
        self.__compiled_nfa = construct(self.pattern)

    def match(self, input_str):
        if self.__compiled_nfa is None:
            self.compile()
        self.input_str = input_str
        return reg_match(self.__compiled_nfa, self.input_str)

    
