def is_space(char):
    return char == ' ' or char == '\t' or char == '\r'


def is_digit(char):
    return '0' <= char <= '9'


def is_letter(char):
    return 'a' <= char <= 'z' or 'A' <= char <= 'Z'


def is_alnum(char):
    """
    判断是否为数字或字母
    :param char:
    :return:
    """
    return is_letter(char) or is_digit(char)
