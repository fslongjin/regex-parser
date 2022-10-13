from regex_parser.nfa.nfa import EdgeType


def match(compiled_nfa, input_str):
    """
    使用NFA进行正则匹配
    :param compiled_nfa: 构建好的nfa
    :param input_str: 输入的字符串
    :return:
    """

    start_node = compiled_nfa
    # 当前路径中的nfa的列表
    current_nfa_list = [start_node]
    next_nfa_list = epsilon_closure(current_nfa_list)

    for i, char in enumerate(input_str):
        current_nfa_list = next_step(next_nfa_list, char)
        next_nfa_list = epsilon_closure(current_nfa_list)

        if next_nfa_list is None:
            return False

        if has_acceptable_state(next_nfa_list) and i == len(input_str) - 1:
            return True

    return False


def epsilon_closure(input_list: list):
    """
    求出nfa的epsilon闭包
    :param input_list:输入的当前nfa节点的列表
    :return:
    """

    if len(input_list) == 0:
        return None

    nfa_stack = []
    for i in input_list:
        nfa_stack.append(i)

    while len(nfa_stack) > 0:
        nfa = nfa_stack.pop()
        for nxt in nfa.next_state:
            # 将epsilon边加入到图中
            if nxt is not None and nfa.edge_type == EdgeType.EPSILON:
                if nxt not in input_list:
                    input_list.append(nxt)
                    nfa_stack.append(nxt)
    return input_list


def next_step(input_list, char):
    """
    根据当前的epsilon闭包，求出下一个转移状态
    :param input_list: 当前的epsilon闭包
    :param char: 输入字符
    :return:
    """
    out_list = []
    for nfa in input_list:
        if nfa.edge_type == char or (nfa.edge_type == EdgeType.CCL and char in nfa.input_set):
            for n in nfa.next_state:
                out_list.append(n)
    return out_list


def has_acceptable_state(nfa_list: list):
    """
    当前nfa节点列表中是否有匹配的状态
    :param nfa_list: 要检查的nfa节点列表
    :return:
    """
    for nfa in nfa_list:
        if len(nfa.next_state) == 0:
            return True

        all_none = True
        for x in nfa.next_state:
            if x is not None:
                all_none = False
        if all_none:
            return True

    return False
