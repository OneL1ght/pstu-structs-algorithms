import random
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


def txt2words(text: str) -> list:
    words = []
    current = []
    for ch in text:
        if ch.isalpha():
            current.append(ch.lower())
        else:
            if current:
                words.append(''.join(current))
                current = []
    if current:
        words.append(''.join(current))
    return words


def test_txt2words():
    print_test("", out=[], fun=txt2words)
    print_test("Hello, World!", out=["hello", "world"], fun=txt2words)
    print_test("one two\nthree", out=["one", "two", "three"], fun=txt2words)
    print_test("it's fine... really!", out=["it", "s", "fine", "really"], fun=txt2words)
    print_test("a1b2c3", out=["a", "b", "c"], fun=txt2words)
    print_test("Hello; world: how are you?", out=["hello", "world", "how", "are", "you"], fun=txt2words)
    with open("assets/lab1exc2.txt", 'r') as f:
        txt = "".join(f.readlines())
        print_test(
            txt,
            out=["we", "study", "programming", "languages", "c", "c", "go", "we", "are", "programmers"],
            fun=txt2words)


def words2bigrams(words: list) -> dict:
    bigrams = {}
    for i in range(len(words) - 1):
        key = words[i]
        if key not in bigrams:
            bigrams[key] = []
        bigrams[key].append(words[i + 1])
    return bigrams


def test_words2bigrams():
    check = lambda a, b: a == b
    print_test([], out={}, fun=words2bigrams, check=check)
    print_test(["hello"], out={}, fun=words2bigrams, check=check)
    print_test(
        ["we", "study"],
        out={"we": ["study"]},
        fun=words2bigrams, check=check)
    print_test(
        ["we", "study", "programming", "languages", "c", "c", "go", "we", "are", "programmers"],
        out={
            "we": ["study", "are"],
            "study": ["programming"],
            "programming": ["languages"],
            "languages": ["c"],
            "c": ["c", "go"],
            "go": ["we"],
            "are": ["programmers"],
        },
        fun=words2bigrams, check=check)
    print_test(
        ["a", "b", "a", "b"],
        out={"a": ["b", "b"], "b": ["a"]},
        fun=words2bigrams, check=check)


def continue_sentence(bigrams: dict, word: str, n: int = 100):
    word = word.lower()
    if word not in bigrams:
        print(f"Слово '{word}' не найдено в словаре")
        return
    result = [word]
    current = word
    for _ in range(n):
        if current not in bigrams:
            break
        current = random.choice(bigrams[current])
        result.append(current)
    print(" ".join(result))


def exc2():
    # test_txt2words()
    # print()
    # test_words2bigrams()
    # print()
    with open("assets/lab1exc2.txt", 'r') as f:
        bigrams = words2bigrams(txt2words(f.read()))
    word = input("Введите слово: ")
    continue_sentence(bigrams, word, 5)


def lab1():
    exc1()
    print()
    exc2()


def main():
    lab1()


if __name__ == "__main__":
    main()
