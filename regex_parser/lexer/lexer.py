from regex_parser.lexer.token import TokenType, Str2TokenDict


class Lexer:
    def __init__(self, pattern):
        self.pattern = pattern
        self.current_token = None
        self.current_char = ''
        self.pos = 0

    def advance(self):
        """
        读取下一个token
        :return: 下一个token
        """
        if self.pos >= len(self.pattern):
            self.current_token = TokenType.EOF
            return TokenType.EOF
        self.current_char = self.pattern[self.pos]
        self.pos += 1

        self.current_token = self.handle_semantic_lexical_analysis()

        return self.current_token

    def handle_semantic_lexical_analysis(self):
        if self.current_char in Str2TokenDict:
            return Str2TokenDict[self.current_char]
        else:
            return TokenType.L

    def match(self, token_type):
        """
        匹配当前token是否为token_type
        :param token_type: 指定的token类型
        :return: True -> 匹配成功
                    False -> 匹配失败
        """
        return self.current_token == token_type
