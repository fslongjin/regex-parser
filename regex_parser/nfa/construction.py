from regex_parser.lexer.token import TokenType, is_connector
from regex_parser.lexer.lexer import Lexer
from regex_parser.nfa.nfa import Nfa, NfaPair, EdgeType

# 声明lexer为全局变量
lexer = Lexer('')


def construct(pattern_str):
    """
    构造NFA
    :param pattern_str: 正则表达式字符串
    :return:
    """
    global lexer
    lexer = Lexer(pattern_str)
    lexer.advance()
    nfa_pair = NfaPair()
    group(nfa_pair)

    return nfa_pair.start_node


def group(pair_out: NfaPair):
    """
    递归地构造NFA
    :param pair_out: 输出的NFA pair
    :return:
    """
    # 遇到开括号，构建子表达式
    if lexer.match(TokenType.OPEN_PAREN):
        lexer.advance()
        expr(pair_out)
        # 吞掉闭括号
        if lexer.match(TokenType.CLOSE_PAREN):
            lexer.advance()
    elif lexer.match(TokenType.EOF):
        return False
    else:
        # 构造单个字符的NFA
        expr(pair_out)

    while True:
        pair = NfaPair()
        if lexer.match(TokenType.OPEN_PAREN):
            lexer.advance()
            expr(pair)
            pair_out.end_node.next_state.append(pair.start_node)
            pair_out.end_node = pair.end_node
            if lexer.match(TokenType.CLOSE_PAREN):
                lexer.advance()
        elif lexer.match(TokenType.EOF):
            return False
        else:
            expr(pair)
            pair_out.end_node.next_state.append(pair.start_node)
            pair_out.end_node = pair.end_node


def expr(pair_out: NfaPair):
    """
    构造单独的，不包含括号的表达式的NFA
    :param pair_out: 输出的NFA pair
    :return:

                                       expression:  a|b

      ┌───────────────────────────────────────┐
      │                                       │
┌─────┴──┐                                    │
│        │       ┌───────────────┐        ┌───▼───────────────────┐      ┌────────────┐
│ start  │       │               │        │                       │      │            │
│        ├──────►│  Expression A ├────────►   Expression b        ├──────►  End       │
│        │       │               │        │                       │      │            │
└────┬───┘       └─────────┬─────┘        └───────────────────────┘      └──▲─────────┘
     │                     │                                                │ ▲
     │                     └────────────────────────────────────────────────┘ │
     │                                                                        │
     └────────────────────────────────────────────────────────────────────────┘
    """
    factor_connect(pair_out)
    pair = NfaPair()

    # 解析 | , 相当于在内部表达式外面都加上start和end节点，并更新pair_out，使其能包括整个nfa
    while lexer.match(TokenType.OR):
        lexer.advance()
        factor_connect(pair)
        start = Nfa()
        start.next_state.append(pair.start_node)
        start.next_state.append(pair_out.start_node)
        pair_out.start_node = start

        end = Nfa()
        pair.end_node.next_state.append(end)
        pair_out.end_node.next_state.append(end)
        pair_out.end_node = end

    return True


def factor_connect(pair_out: NfaPair):
    """
    构造普通字符连接的nfa
    :param pair_out: 输出的NFA pair
    :return:
    """
    if is_connector(lexer.current_token):
        factor(pair_out)

    while is_connector(lexer.current_token):
        pair = NfaPair()
        factor(pair)
        pair_out.end_node.next_state.append(pair.start_node)
        pair_out.end_node = pair.end_node

    return True


def factor(pair_out: NfaPair):
    """
    使用汤姆逊构造法，构造 * + ? 闭包的NFA
    :param pair_out: 输出的NFA pair
    :return:
    """

    term(pair_out)
    if lexer.match(TokenType.CLOSURE):
        nfa_star_closure(pair_out)
    elif lexer.match(TokenType.PLUS_CLOSE):
        nfa_plus_closure(pair_out)
    elif lexer.match(TokenType.OPTIONAL):
        nfa_option_closure(pair_out)


def term(pair_out: NfaPair):
    """
    对 . （单个字符） []进行匹配
    :param pair_out: 输出的NFA pair
    :return:
    """

    if lexer.match(TokenType.L):
        nfa_parse_single_char(pair_out)
    elif lexer.match(TokenType.ANY):
        nfa_parse_dot_char(pair_out)
    elif lexer.match(TokenType.CCL_START):
        nfa_parse_set_negative_char(pair_out)


def nfa_parse_single_char(pair_out: NfaPair):
    """
    为单个字符构造NFA节点
    :param pair_out: 输出的NFA pair
    :return:
    """
    if not lexer.match(TokenType.L):
        return False

    pair_out.start_node = Nfa()
    pair_out.end_node = Nfa()

    pair_out.start_node.next_state.append(pair_out.end_node)
    pair_out.start_node.edge_type = lexer.current_char
    lexer.advance()
    return True


def nfa_parse_dot_char(pair_out: NfaPair):
    """
    为字符 . 构造NFA节点
    :param pair_out: 输出的NFA pair
    :return:
    """
    if not lexer.match(TokenType.ANY):
        return False

    pair_out.start_node = Nfa()
    pair_out.end_node = Nfa()

    pair_out.start_node.next_state.append(pair_out.end_node)

    pair_out.start_node.edge_type = EdgeType.CCL
    pair_out.start_node.set_input_set()


def nfa_parse_set_negative_char(pair_out: NfaPair):
    if not lexer.match(TokenType.CCL_START):
        return False
    negation = False
    # 吃掉'['
    lexer.advance()

    if lexer.match(TokenType.AT_BOL):
        negation = True
    pair_out.start_node = Nfa()
    pair_out.end_node = Nfa()
    pair_out.start_node.next_state.append(pair_out.end_node)
    pair_out.start_node.edge_type = EdgeType.CCL

    do_dash(pair_out.start_node.input_set)

    if negation:
        # 对输入字符集取反
        char_set_inverse(pair_out.start_node.input_set)

    # 吃掉']'
    lexer.advance()
    return True


def nfa_parse_set_char(pair_out: NfaPair):
    """
    解析字符 [
    :param pair_out: 输出的NFA pair
    :return:
    """
    if not lexer.match(TokenType.CCL_START):
        return False

    pair_out.start_node = Nfa()
    pair_out.end_node = Nfa()

    pair_out.start_node.next_state.append(pair_out.end_node)

    pair_out.start_node.edge_type = EdgeType.CCL
    pair_out.start_node.input_set.clear()
    do_dash(pair_out.start_node.input_set)

    # 吃掉']'
    lexer.advance()
    return True


def nfa_star_closure(pair_out: NfaPair):
    """
    解析 * 闭包
    :param pair_out: 输出的NFA pair
    :return:
    """
    if not lexer.match(TokenType.CLOSURE):
        return False
    start = Nfa()
    end = Nfa()
    start.next_state.append(pair_out.start_node)
    start.next_state.append(pair_out.end_node)

    pair_out.end_node.next_state.append(end)
    pair_out.end_node.next_state.append(pair_out.start_node)

    pair_out.start_node = start
    pair_out.end_node = end

    lexer.advance()
    return True


def nfa_plus_closure(pair_out: NfaPair):
    """
    解析 + 闭包
    :param pair_out: 输出的NFA pair
    :return:
    """
    if not lexer.match(TokenType.PLUS_CLOSE):
        return False

    start = Nfa()
    end = Nfa()

    start.next_state.append(pair_out.start_node)

    pair_out.end_node.next_state.append(pair_out.start_node)
    pair_out.end_node.next_state.append(end)

    pair_out.start_node = start
    pair_out.end_node = end

    lexer.advance()
    return True


def nfa_option_closure(pair_out: NfaPair):
    """
    解析 | 闭包
    :param pair_out: 输出的NFA pair
    :return:
    """
    if not lexer.match(TokenType.OPTIONAL):
        return False

    start = Nfa()
    end = Nfa()

    start.next_state.append(pair_out.start_node)
    start.next_state.append(end)
    pair_out.end_node.next_state.append(end)

    pair_out.start_node = start
    pair_out.end_node = end

    lexer.advance()
    return True


def do_dash(input_set: set):
    first = ''
    while not lexer.match(TokenType.CCL_END):
        # 不是减号
        if not lexer.match(TokenType.DASH):
            first = lexer.current_char
            input_set.add(first)
        else:  # 是减号
            lexer.advance()
            # 添加开始到结尾的字符
            for c in range(ord(first), ord(lexer.current_char) + 1):
                input_set.add(chr(c))
        lexer.advance()


def char_set_inverse(input_set: set):
    """
    对输入的字符集取补集
    :param input_set:
    :return:
    """
    for i in range(127):
        c = chr(i)
        if c not in input_set:
            input_set.add(c)
        else:
            input_set.remove(c)
