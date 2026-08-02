#!/usr/bin/env python3
"""Independent O(n^2) verifier for additive-square-freeness.

Deliberately written from the definition, not from afsf.c's incremental test,
so that it is a genuine cross-check of the C searcher rather than a restatement
of it.  Exact integer arithmetic throughout.

A word w contains an ADDITIVE SQUARE if it has a factor u v with |u| = |v| = k
and sum(u) = sum(v).

Usage:
    python3 verify_word.py "0,1,3,4,0,1,..."      # check one word
    python3 verify_word.py --file words.txt        # one word per line
    python3 verify_word.py --selftest
"""
import sys


def first_additive_square(w):
    """Return (start, k) of the first additive square found, or None.

    Brute force straight from the definition: every start position, every
    half-length.  O(n^3) naive, made O(n^2) with prefix sums but still
    structurally independent of the incremental end-of-word test.
    """
    n = len(w)
    pre = [0] * (n + 1)
    for i, x in enumerate(w):
        pre[i + 1] = pre[i] + x
    for start in range(n):
        for k in range(1, (n - start) // 2 + 1):
            s1 = pre[start + k] - pre[start]
            s2 = pre[start + 2 * k] - pre[start + k]
            if s1 == s2:
                return (start, k)
    return None


def is_additive_square_free(w):
    return first_additive_square(w) is None


def alphabet_of(w):
    return sorted(set(w))


def selftest():
    """Positive and negative controls."""
    ok = True

    # negative controls: words that DO contain an additive square
    for w, why in [
        ([0, 0], "00 is an additive square"),
        ([1, 2, 3, 3, 2, 1], "whole word: 1+2+3 = 3+2+1"),
        ([5, 1, 4, 2, 7], "1,4 vs 2,... -> check 1+4=5 vs 2+? no; 5 vs 1? no"),
        ([0, 1, 1, 0], "01|10 sums 1,1"),
        ([2, 7, 9], "2+7=9 is not a square (unequal lengths) -- see below"),
    ][:4]:
        if is_additive_square_free(w):
            print(f"FAIL negative control {w}: {why}")
            ok = False

    # positive controls: additive-square-free words
    for w in [
        [],
        [0],
        [0, 1],
        [0, 1, 0],
        [2, 7, 9],          # 2!=7, 7!=9, and 2+7=9 != 9+? (no 4th letter)
    ]:
        if not is_additive_square_free(w):
            print(f"FAIL positive control {w}")
            ok = False

    # an abelian square is always an additive square
    if is_additive_square_free([3, 5, 5, 3]):
        print("FAIL: abelian square 3,5|5,3 not detected")
        ok = False

    # exhaustive check of the binary case: no binary word of length 4 is afsf
    from itertools import product
    if any(is_additive_square_free(list(t)) for t in product([0, 1], repeat=4)):
        print("FAIL: some binary word of length 4 is additive-square-free")
        ok = False
    if not any(is_additive_square_free(list(t)) for t in product([0, 1], repeat=3)):
        print("FAIL: no binary word of length 3 is additive-square-free")
        ok = False

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def check_one(s):
    w = [int(x) for x in s.replace(" ", "").split(",") if x != ""]
    hit = first_additive_square(w)
    if hit is None:
        print(f"OK  len={len(w)} alphabet={alphabet_of(w)} additive-square-free")
        return 0
    start, k = hit
    print(f"BAD len={len(w)} additive square at start={start} halflen={k}: "
          f"{w[start:start+k]} | {w[start+k:start+2*k]}")
    return 1


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if sys.argv[1] == "--selftest":
        return selftest()
    if sys.argv[1] == "--file":
        rc = 0
        with open(sys.argv[2]) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                rc |= check_one(line)
        return rc
    return check_one(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
