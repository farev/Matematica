#!/usr/bin/env python3
"""dpm_brute.py — engine E3: from-definition brute force for tiny groups.

No sign-representative reduction, no incremental signed-sum state: extends
sequences over ALL nonzero elements (nondecreasing) and tests ±zero-sum-
freeness of each candidate directly, by recomputing the full signed-sum set
from scratch at every step. Cross-validates E1/E2 on every group it can
reach (|G| <= ~30). Exact integer arithmetic only.

Usage: python3 dpm_brute.py a [b]           one group
       python3 dpm_brute.py --selftest      the control battery
"""
import sys


def dpm(a, b=1, cap=10):
    n = a * b
    neg = [((-(i // b)) % a) * b + ((-(i % b)) % b) for i in range(n)]
    add = [[((i // b + j // b) % a) * b + ((i % b + j % b) % b)
            for j in range(n)] for i in range(n)]

    def pzsf(seq):
        T = set()
        for g in seq:
            Tn = set(T)
            Tn.add(g)
            Tn.add(neg[g])
            for t in T:
                Tn.add(add[t][g])
                Tn.add(add[t][neg[g]])
            if 0 in Tn:
                return False
            T = Tn
        return True

    best = 0

    def rec(seq, start):
        nonlocal best
        if len(seq) > best:
            best = len(seq)
        if len(seq) >= cap:
            return
        for g in range(start, n):
            if pzsf(seq + [g]):
                rec(seq + [g], g)

    rec([], 1)
    return best + 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        import math
        ok = True
        # cyclic: D± = floor(log2 n) + 1 (NOTE.md Lemma 4)
        for n in range(2, 25):
            got, want = dpm(n), int(math.log2(n)) + 1
            if got != want:
                ok = False
            print(f"C_{n}: brute={got} lemma4={want} {'ok' if got == want else 'MISMATCH'}")
        # rank 2 controls (values from E1/E2, and where marked from the
        # literature (secondary): C2+C4 = 4, C3+C3 = 3, C3+C9 = 5)
        for (a, b, want) in [(2, 2, 3), (2, 4, 4), (2, 6, 4), (3, 3, 3),
                             (3, 6, 5), (4, 4, 5), (2, 8, 5), (3, 9, 5),
                             (5, 5, 5), (2, 10, 5), (2, 12, 5), (4, 8, 6)]:
            got = dpm(a, b)
            if got != want:
                ok = False
            print(f"C_{a}+C_{b}: brute={got} expected={want} {'ok' if got == want else 'MISMATCH'}")
        sys.exit(0 if ok else 1)
    args = [int(x) for x in sys.argv[1:]]
    print(dpm(*args))
