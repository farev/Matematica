#!/usr/bin/env python3
"""Independent witness checker for reciprocal Rado colorings.

Reads a witness file:  line 1: "n r k",  line 2: n colors (0..r-1).
Confirms the coloring is total and NO color class contains a solution of
1/x_1 + ... + 1/x_k = 1/y with all of x_1..x_k, y in the class.

Deliberately not the encoder's method: the encoder enumerates all
solutions in [1,n] once and emits clauses; this checker re-derives
solutions *inside each class only*, walking the class as an explicit
sorted list with bisect bounds and testing the final term by direct
membership. Shares no code with recip.py.

Exit 0 and "WITNESS OK" iff valid; otherwise prints a violating tuple.
"""
import sys
from bisect import bisect_left
from math import gcd


def class_has_solution(C, k):
    """C sorted list. Return a violating (y, xs) or None."""
    Cset = set(C)
    for y in C:
        # DFS: j terms still to choose, all from C, each > y, nondecreasing,
        # remainder a/b to be met exactly.
        def dfs(j, lo_idx, a, b, acc):
            if j == 1:
                if a > 0 and b % a == 0:
                    x = b // a
                    if x in Cset and x > y and (not acc or x >= acc[-1]):
                        return acc + [x]
                return None
            # candidates x in C at index >= lo_idx, 1/x < a/b, j/x >= a/b
            start = max(lo_idx, bisect_left(C, b // a + 1))
            for idx in range(start, len(C)):
                x = C[idx]
                if a * x > j * b:          # 1/x < (a/b)/j  -> too small
                    break
                na, nb = a * x - b, b * x
                g = gcd(na, nb)
                if g:
                    na, nb = na // g, nb // g
                res = dfs(j - 1, idx, na, nb, acc + [x])
                if res:
                    return res
            return None
        i0 = bisect_left(C, y + 1)
        if i0 < len(C):
            res = dfs(k, i0, 1, y, [])
            if res:
                return (y, res)
    return None


def main(path):
    with open(path) as f:
        n, r, k = map(int, f.readline().split())
        col = list(map(int, f.readline().split()))
    if len(col) != n or any(not (0 <= c < r) for c in col):
        print(f"BAD WITNESS: coloring not total or colors out of range")
        return 1
    for c in range(r):
        C = [x for x in range(1, n + 1) if col[x - 1] == c]
        bad = class_has_solution(C, k)
        if bad:
            y, xs = bad
            s = " + ".join(f"1/{x}" for x in xs)
            print(f"VIOLATION in color {c}: {s} = 1/{y}  (all in class)")
            return 1
    print(f"WITNESS OK  (n={n}, r={r}, k={k})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
