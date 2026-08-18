"""Deep probes into the undirected-free language over Sigma_n.

Randomized DFS with restarts; also lexicographic-least mode.  Emits the
letter word and its 3-symbol choice code (0: repeat distance n-2,
1: repeat distance n-1, 2: other/fresh letter).

Usage: python3 probe.py <n> <num> <den> <target_len> <restarts> [--lex] [--seed S]
"""

import random
import sys
import time

from urt import UInc


def choices_at(word, n):
    """Legal next letters: those not among the last (n-2)... i.e. letters
    whose last occurrence is at distance >= n-2 (gap rule for alpha =
    (n-1)/(n-2): forbidden distance d <= n-3+... see NOTE; here we just
    return all letters not in the last window that the U-checker would
    instantly reject, plus we let UInc do the real work)."""
    # cheap prefilter: letters in the last 19 (for n=22) are hopeless
    recent = set(word[-(n - 3):]) if len(word) >= n - 3 else set(word)
    return [c for c in range(n) if c not in recent]


def probe(n, num, den, target, rng, lex=False, maxbacktrack=200000):
    inc = UInc(num, den, target + 2)
    word = []
    used = 0
    stack = []  # (choices list, idx)
    backtracks = 0

    def legal(c):
        return c <= used  # canonical: new letter must be `used`

    while len(word) < target and backtracks < maxbacktrack:
        cands = [c for c in choices_at(word, n) if c <= used]
        if not lex:
            rng.shuffle(cands)
        placed = False
        for c in cands:
            if inc.push(c):
                word.append(c)
                stack.append(cands[cands.index(c) + 1:])
                if c == used:
                    pass
                used = max(used, c + 1)
                placed = True
                break
            inc.pop()
        if not placed:
            # backtrack
            while stack:
                backtracks += 1
                rest = stack.pop()
                word.pop()
                inc.pop()
                used = max([0] + [x + 1 for x in word])
                placed2 = False
                for c in rest:
                    if inc.push(c):
                        word.append(c)
                        stack.append(rest[rest.index(c) + 1:])
                        used = max(used, c + 1)
                        placed2 = True
                        break
                    inc.pop()
                if placed2:
                    break
            else:
                return word, backtracks  # tree exhausted
    return word, backtracks


def choice_code(word, n):
    code = []
    for i in range(len(word)):
        c = word[i]
        if i >= n - 2 and word[i - (n - 2)] == c:
            code.append(0)
        elif i >= n - 1 and word[i - (n - 1)] == c:
            code.append(1)
        else:
            code.append(2)
    return code


if __name__ == "__main__":
    n, num, den, target, restarts = map(int, sys.argv[1:6])
    lex = "--lex" in sys.argv
    seed = 12345
    if "--seed" in sys.argv:
        seed = int(sys.argv[sys.argv.index("--seed") + 1])
    rng = random.Random(seed)
    best = []
    t0 = time.time()
    for r in range(restarts):
        w, bt = probe(n, num, den, target, rng, lex=lex)
        if len(w) > len(best):
            best = w
        print(f"restart {r}: reached {len(w)} (backtracks {bt}) "
              f"[{time.time()-t0:.0f}s]")
        if len(w) >= target:
            break
    w = best
    print("length:", len(w))
    print("word:", "".join(f"{c:02d}" for c in w))
    cc = choice_code(w, n)
    print("code:", "".join(map(str, cc)))
