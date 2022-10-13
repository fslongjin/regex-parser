from enum import Enum


# 特殊的边的类型
class EdgeType(Enum):
    EPSILON = -1  # epsilon边
    CCL = -2  # 边对应的是字符集
    EMPTY = -3  # 一条ε边


class Nfa:
    # NFA总共有多少个状态
    NFA_TOTAL_STATUS_NUM = 0

    def __init__(self):
        # 使用负值表示特殊的边，使用正值表示字符
        self.edge_type = EdgeType.EPSILON
        self.next_state = []

        # 当前节点支持的输入的字符集
        self.input_set = set()
        self.status_num = 0
        self._set_status_num()

    def _set_status_num(self):
        """
        初始化状态编号
        :return:
        """
        self.status_num = Nfa.NFA_TOTAL_STATUS_NUM
        Nfa.NFA_TOTAL_STATUS_NUM += 1

    def set_input_set(self):
        for i in range(int(127)):
            self.input_set.add(chr(i))


class NfaPair:
    def __init__(self, start_node=None, end_node=None):
        self.start_node = start_node
        self.end_node = end_node
