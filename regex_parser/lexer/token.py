from enum import Enum


class TokenType(Enum):
    EOF = 0  # end of file
    ANY = 1  # .
    AT_BOL = 2  # ^  # Beginning of line
    AT_EOL = 3  # $  # End of line
    CCL_END = 4  # ]
    CCL_START = 5  # [
    CLOSE_CURLY = 6  # }
    CLOSE_PAREN = 7  # )
    CLOSURE = 8  # *
    DASH = 9  # -
    L = 10  # 普通字符
    OPEN_CURLY = 11  # {
    OPEN_PAREN = 12  # (
    OR = 13  # |
    OPTIONAL = 14  # ?
    PLUS_CLOSE = 15  # +


Str2TokenDict = {
    '.': TokenType.ANY,
    '^': TokenType.AT_BOL,
    '$': TokenType.AT_EOL,
    ']': TokenType.CCL_END,
    '[': TokenType.CCL_START,
    '}': TokenType.CLOSE_CURLY,
    ')': TokenType.CLOSE_PAREN,
    '*': TokenType.CLOSURE,
    '-': TokenType.DASH,
    '{': TokenType.OPEN_CURLY,
    '(': TokenType.OPEN_PAREN,
    '|': TokenType.OR,
    '?': TokenType.OPTIONAL,
    '+': TokenType.PLUS_CLOSE,
}


def is_connector(token_type: TokenType):
    """
    判断token_type是否为连接符
    :param token_type: 待判断的token_type
    :return:
    """
    nc = [
        TokenType.OPEN_PAREN,
        TokenType.CLOSE_PAREN,
        TokenType.AT_EOL,
        TokenType.AT_BOL,
        TokenType.EOF,
        TokenType.CLOSURE,
        TokenType.PLUS_CLOSE,
        TokenType.CCL_END,
        TokenType.OR
    ]
    return token_type not in nc