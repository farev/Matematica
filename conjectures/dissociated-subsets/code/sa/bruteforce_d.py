#!/usr/bin/env python3
"""Independent brute-force evaluator for d(A) = size of the largest dissociated subset.

A finite set B is dissociated iff all 2^|B| subset sums are distinct.
This file shares no code with the C search program.

Method: for s = 1, 2, ...: enumerate ALL s-subsets of A, test each by building
the set of its subset sums and checking its size equals 2^s.  If no s-subset is
dissociated, d(A) = s-1 (every superset of a non-dissociated set is
non-dissociated, because the subset sums of the smaller set are among the
subset sums of the larger one, so no larger subset can be dissociated).

Optionally (--topdown, for small A) also enumerate subsets from the top,
size |A| downward, as a second independent confirmation.

Usage:  python3 bruteforce_d.py 1 2 3 4 5 6 7
        python3 bruteforce_d.py --topdown 1 2 3 4 5 6 7
        echo "1 2 3 4" | python3 bruteforce_d.py -
"""
import sys
from itertools import combinations


def is_dissociated(B):
    sums = set()
    for mask in range(1 << len(B)):
        s = 0
        for i, b in enumerate(B):
            if mask >> i & 1:
                s += b
        sums.add(s)
    return len(sums) == (1 << len(B))


def d_bottom_up(A):
    A = sorted(set(A))
    witness = ()
    s = 1
    while s <= len(A):
        found = None
        for T in combinations(A, s):
            if is_dissociated(T):
                found = T
                break
        if found is None:
            return s - 1, witness
        witness = found
        s += 1
    return len(A), witness


def d_top_down(A):
    A = sorted(set(A))
    for s in range(len(A), 0, -1):
        for T in combinations(A, s):
            if is_dissociated(T):
                return s, T
    return 0, ()


def main():
    args = sys.argv[1:]
    topdown = False
    if args and args[0] == '--topdown':
        topdown = True
        args = args[1:]
    if args == ['-']:
        A = [int(x) for x in sys.stdin.read().split()]
    else:
        A = [int(x) for x in args]
    assert len(A) == len(set(A)) and all(x > 0 for x in A), "need distinct positive integers"
    d, w = d_bottom_up(A)
    print(f"|A|={len(A)} d(A)={d} witness={list(w)} (bottom-up: no dissociated {d+1}-subset among all {len(A)}-choose-{d+1})")
    if topdown:
        d2, w2 = d_top_down(A)
        print(f"top-down: d(A)={d2} witness={list(w2)} agree={d2 == d}")


if __name__ == '__main__':
    main()
