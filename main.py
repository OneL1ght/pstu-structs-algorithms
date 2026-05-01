from typing import Callable, Any


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


def print_colored(color, text: str):
    print(color + text + bcolors.ENDC)


def print_test(*in_, out, fun: Callable, check = None):
    res = fun(*in_)
    txt = f"[TEST] {fun.__name__}: input: {in_}, target: {out} | res: {res}"
    if check is None:
        check = lambda a, b: a == b
    color = bcolors.OKGREEN if check(out, res) else bcolors.FAIL
    print_colored(color, txt)

def intersection(a: list, b: list):
    acount, bcount = {}, {}
    len_a, len_b = len(a), len(b)
    i = 0
    while i < max(len_a, len_b):
        curr_a = None if i >= len(a) else a[i]
        if curr_a and curr_a in acount.keys():
            acount[curr_a] += 1
        else:
            acount[curr_a] = 1

        curr_b = None if i >= len(b) else b[i]
        if curr_b and curr_b in bcount.keys():
            bcount[curr_b] += 1
        else:
            bcount[curr_b] = 1
        i += 1

    c = []
    long, short = bcount, acount
    for k in short.keys():
        if k not in long.keys():
            continue
        c += [k] * min(short[k], long[k])
    return c


def exc1():
    check = lambda a, b: set(a) == set(b)
    print_test([], [], out=[], fun=intersection, check=check)
    print_test([12], [13], out=[], fun=intersection, check=check)
    print_test([12, 13], [13], out=[13], fun=intersection, check=check)
    print_test([12, 13], [13, 15], out=[13], fun=intersection, check=check)
    print_test([11, 13, 15, 12, 13], [13, 15], out=[13, 15], fun=intersection, check=check)
    print_test([0, 1, 2], list(range(12)), out=[0, 1, 2], fun=intersection, check=check)
    print_test(
        list(range(23, 53)),
        list(range(23, 53)),
        out=list(range(23, 53)),
        fun=intersection, check=check)
    print_test(
        list(map(lambda x: abs(x), range(-10, 11))),
        list(range(11)),
        out=list(range(11)),
        fun=intersection, check=check)


def lab1():
    exc1()


def main():
    lab1()


if __name__ == "__main__":
    main()
