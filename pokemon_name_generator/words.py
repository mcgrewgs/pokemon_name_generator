from typing import List, Dict, Set
from functools import lru_cache
from sys import argv


# @lru_cache(maxsize=1_048_576, typed=False)
def damerau_levenshtein(a: str, b: str, a_index: int = 0, b_index: int = 0) -> int:
    distances = [0]

    if a_index == len(a):
        return len(b) - b_index
    elif b_index == len(b):
        return len(a) - a_index
    elif a_index == len(a) - 1 or b_index == len(b) - 1:
        distances = [
            1 + damerau_levenshtein(a, b, a_index + 1, b_index),
            1 + damerau_levenshtein(a, b, a_index, b_index + 1),
            (
                damerau_levenshtein(a, b, a_index + 1, b_index + 1)
                + (0 if a[a_index] == b[b_index] else 1)
            ),
        ]
    else:
        distances = [
            1 + damerau_levenshtein(a, b, a_index + 1, b_index),
            1 + damerau_levenshtein(a, b, a_index, b_index + 1),
            (
                damerau_levenshtein(a, b, a_index + 1, b_index + 1)
                + (0 if a[a_index] == b[b_index] else 1)
            ),
        ]
        if a[a_index] == b[b_index + 1] and a[a_index + 1] == b[b_index]:
            distances.append(1 + damerau_levenshtein(a, b, a_index + 2, b_index + 2))

    return min(distances)


# @lru_cache(maxsize=1_073_741_824, typed=False)
def damerau_levenshtein_shortcut(a: str, b: str) -> int:
    if a == b:
        return 0
    elif len(a) == 0:
        return len(b)
    elif len(b) == 0:
        return len(a)
    elif len(a) == 1:
        if a in b:
            return len(b) - 1
        else:
            return len(b)
    elif len(b) == 1:
        if b in a:
            return len(a) - 1
        else:
            return len(a)
    elif a[0] == b[0]:
        return damerau_levenshtein_shortcut(a[1:], b[1:])
    elif a[0] == b[1] and a[1] == b[0]:
        return 1 + damerau_levenshtein_shortcut(a[2:], b[2:])
    else:
        return 1 + min(
            damerau_levenshtein_shortcut(a[1:], b),
            damerau_levenshtein_shortcut(a, b[1:]),
            damerau_levenshtein_shortcut(a[1:], b[1:]),
        )


def hamming_distance(a: str, b: str) -> int:
    return len(list(filter(lambda i: a[i] != b[i], range(len(a)))))


def hamming_distance2(a: str, b: str) -> int:
    return len(list(filter(lambda i: a[i] != b[i], range(len(a)))))


CONSONANTS: Set[str] = set(
    [
        "b",
        "c",
        "d",
        "f",
        "g",
        # "h",
        "j",
        "k",
        "l",
        "m",
        "n",
        "p",
        "q",
        "r",
        "s",
        "t",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
)

WORD_LIST: List[str] = []

with open("/Users/mcgrewgs/words") as f:
    WORD_LIST = f.read().lower().split("\n")

WORD_SET: Set[str] = set(WORD_LIST)

WORDS_BY_LENGTH: Dict[int, List[str]] = {}
for word in WORD_LIST:
    if len(word) > 1 and word[0] in CONSONANTS and word[-1] in CONSONANTS:
        if len(word) not in WORDS_BY_LENGTH:
            WORDS_BY_LENGTH[len(word)] = []
        WORDS_BY_LENGTH[len(word)].append(word)


def substrings(s: str) -> Set[str]:
    to_return: Set[str] = set([])

    for i in range(len(s) - 1):
        for j in range(i + 1, len(s)):
            to_return.add(s[i : j + 1])

    return to_return


def subwords(s: str) -> Set[str]:
    to_return: Set[str] = set([])

    for i in range(len(s) - 1):
        for j in range(i + 1, len(s)):
            st = s[i : j + 1]
            if st in WORD_SET:
                to_return.add(st)

    return to_return


def replaceable_subwords(s: str) -> Set[str]:
    return set(
        filter(lambda w: w[0] in CONSONANTS and w[-1] in CONSONANTS, subwords(s))
    )


def subword_replacements(s: str) -> Set[str]:
    return set(
        filter(
            lambda x: x[1:-1] == s[1:-1] and (x[0] == s[0] or x[-1] == s[-1]),
            WORDS_BY_LENGTH[len(s)],
        )
    )


def suggested_names(s: str) -> Set[str]:
    to_return: Set[str] = set([])
    for sw in replaceable_subwords(s):
        for r in subword_replacements(sw):
            to_return.add(s.replace(sw, r))

    return to_return


def main():
    name = argv[1].strip().lower()
    names = sorted(list(suggested_names(name)))
    print(name.capitalize())
    for n in names:
        print(f"  {n.capitalize()}")


if __name__ == "__main__":
    main()

# CLOSE_WORDS: Dict[str, List[str]] = {}
# for wl in WORDS_BY_LENGTH.values():
#     if len(wl[0]) < 4:
#         for w in wl:
#             CLOSE_WORDS[w] = list(
#                 filter(
#                     lambda x: (w[0] == x[0] or w[-1] == x[-1])
#                     and hamming_distance(w, x) == 1,
#                     wl,
#                 )
#             )
