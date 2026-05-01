"""
Реализация красно-черного дерева (неполная, только поиск + вставка)
"""

import random
import time
import sys


BLACK = False
RED = True
NAN = -sys.maxsize - 1


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Node:
    def __init__(self, v: int, red: bool, ) -> None:
        self.val = v
        self.red = red
        self.left:  Node | None = None
        self.right: Node | None = None


class RBTree:
    def __init__(self, v: int) -> None:
        self.root = Node(v, BLACK)

    def _assert_valid(self):
        assert not self.root.red,            "root is not red!"
        assert valid_colors_from(self.root), "detected wrong colors!"
        assert valid_order_from(self.root),  "detected wrong order!"

    def insert(self, val: int):
        _insert(self.root, val)
        # self._assert_valid() for debug use

    def has(self, val: int) -> bool:
        def has_in_children(n: Node | None, val: int) -> bool:
            if not n:
                return False
            elif n.val == val:
                return True
            elif val <= n.val:
                return has_in_children(n.left, val)
            else:
                return has_in_children(n.right, val)
        return has_in_children(self.root, val)

    def print(self):
        from collections import deque

        # — ширина ячейки по самому длинному значению
        all_nodes = []
        def gather(node):
            if node is None: return
            all_nodes.append(node)
            gather(node.left); gather(node.right)
        gather(self.root)
        if not all_nodes:
            return

        cell = max(len(str(n.val)) for n in all_nodes) + 2  # +1 пробел с каждой стороны

        # — inorder-позиция каждого узла (линейная ширина вместо 2^depth)
        slot = {}
        ctr  = [0]
        def inorder(node):
            if node is None: return
            inorder(node.left)
            slot[id(node)] = ctr[0]; ctr[0] += 1
            inorder(node.right)
        inorder(self.root)

        # — BFS по уровням
        levels = []
        q = deque([(self.root, 0)])
        while q:
            node, lvl = q.popleft()
            while len(levels) <= lvl:
                levels.append([])
            levels[lvl].append(node)
            if node.left:  q.append((node.left,  lvl + 1))
            if node.right: q.append((node.right, lvl + 1))

        for row in levels:
            line   = []
            cursor = 0
            for node in row:
                val = str(node.val)
                x   = slot[id(node)] * cell + (cell - len(val)) // 2
                line.append(' ' * max(0, x - cursor))
                if node.red:
                    line.append(bcolors.FAIL + val + bcolors.ENDC)
                else:
                    line.append(val)
                cursor = x + len(val)
            print(''.join(line))


def print_colored(color, text: str):
    print(color + text + bcolors.ENDC, end="")


def _insert(n: Node, val: int):
    if val <= n.val:
        if n.left is None:
            n.left = Node(val, not n.red)
        else:
            _insert(n.left, val)
    elif n.val < val:
        if n.right is None:
            n.right = Node(val, not n.red)
        else:
            _insert(n.right, val)


def _max_recur(node: Node | None) -> int:
    if node is None:
        return NAN
    return max(max(_max_recur(node.left), _max_recur(node.right)), node.val)


def valid_order_from(node: Node | None):
    if node is None:
        return True
    max_left  = _max_recur(node.left)
    max_right = _max_recur(node.right)
    left_smaller_or_eq = max_left <= node.val if max_left != NAN else True
    right_bigger       = max_right > node.val if max_right != NAN else True
    return (left_smaller_or_eq
            and right_bigger
            and valid_order_from(node.left)
            and valid_order_from(node.right))


def valid_colors_from(node: Node | None):
    if node is None:
        return True
    left_red  = node.left.red if node.left is not None else BLACK
    right_red = node.right.red if node.right is not None else BLACK
    return ((left_red == right_red == BLACK if node.red else True)
            and valid_colors_from(node.left)
            and valid_colors_from(node.right))


def demo_red_black_tree():
    t = RBTree(10)
    t.insert(5)
    t.insert(12)
    t.insert(16)
    t.insert(15)
    t.insert(13)
    t.insert(-13)
    t.insert(-1)
    t.insert(32)
    t.insert(2)
    t.insert(17)
    t.insert(1)
    t._assert_valid()
    t.print()


def task1():
    """
    Вывод для 10^5 элементов:

    Добавление в список 100000 элементов: 0.0010650157928466797sec
    Добавление в дерево 100000 элементов: 0.09037971496582031sec
    Разница добавления дерево/список: 84.86
    Поиск в списке 100000 элементов: 50.582088232040405sec
    Поиск в дереве 100000 элементов: 0.1436159610748291sec
    Разница поиска дерево/список: 0.0028392651646963417
    Результаты поиска элементов равны: True
    """
    N = 10**2
    random_int = lambda: random.randrange(-10**6, 10**6, 1)
    src  = [random_int() for _ in range(N)]
    lst  = []
    tree = RBTree(random_int())

    start = time.time()
    for num in src:
        lst.append(num)
    lst_dur = time.time() - start
    print(f"Добавление в список {N} элементов: {lst_dur}sec")

    start = time.time()
    for num in src:
        tree.insert(num)
    tree_dur = time.time() - start
    print(f"Добавление в дерево {N} элементов: {tree_dur}sec")
    print(f"Разница добавления дерево/список: {round(tree_dur/lst_dur, 2)}")

    cmp = [random_int() for _ in range(N)]

    lst_has = {}
    start = time.time()
    for num in cmp:
        lst_has[num] = num in lst
    lst_dur = time.time() - start
    print(f"Поиск в списке {N} элементов: {lst_dur}sec")

    tree_has = {}
    start = time.time()
    for num in cmp:
        tree_has[num] = tree.has(num)
    tree_dur = time.time() - start
    print(f"Поиск в дереве {N} элементов: {tree_dur}sec")
    print(f"Разница поиска дерево/список: {tree_dur/lst_dur}")
    print(f"Результаты поиска элементов равны: {tree_has == lst_has}")

def task2():
    def parse(s: str) -> list[int | str]:
        tokens = []
        i = 0
        while i < len(s):
            if s[i].isspace():
                i += 1
            elif s[i].isdigit():
                j = i
                while j < len(s) and s[j].isdigit():
                    j += 1
                tokens.append(int(s[i:j]))
                i = j
            else:
                tokens.append(s[i])
                i += 1
        return tokens

    def calculate_from_low(tokens: list, pos: int):
        val, pos = calculate_high(tokens, pos)
        while pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            right, pos = calculate_high(tokens, pos)
            val = val + right if op == '+' else val - right
        return val, pos

    def calculate_high(tokens: list, pos: int):
        val, pos = get_atom(tokens, pos)
        while pos < len(tokens) and tokens[pos] in ('*', '/'):
            op = tokens[pos]
            pos += 1
            right, pos = get_atom(tokens, pos)
            if op == '*':
                val = val * right
            else:
                val = int(val / right)
        return val, pos

    def get_atom(tokens: list, pos: int):
        tok = tokens[pos]
        if isinstance(tok, int):
            return tok, pos + 1
        if tok == '(':
            val, pos = calculate_from_low(tokens, pos + 1)
            assert tokens[pos] == ')', "не нашлась закрывающая скобка"
            return val, pos + 1
        raise ValueError(f"неожиданный токен: {tok!r}")

    while True:
        s = input("Введите выражение (или 'q' для выхода): ").strip()
        if s == 'q':
            break
        tokens = parse(s)
        result, _ = calculate_from_low(tokens, 0)
        print(f"= {result}")


def main():
    # demo_red_black_tree()
    task1()
    task2()


if __name__ == "__main__":
    main()
