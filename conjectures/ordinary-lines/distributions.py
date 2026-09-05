#!/usr/bin/env python3
"""Enumerate line-type distributions (t_k)_{k>=2} of an n-point configuration with exactly
t_2 = m ordinary lines that are compatible with
   (C)  sum_k C(k,2) t_k = C(n,2)          (every pair of points spans exactly one line)
   (M)  t_2 >= 3 + sum_{k>=4} (k-3) t_k    (Melchior's inequality)
Used to justify the cube split: every configuration with t_2 <= m has one of these
distributions, so fixing the lines of size >= 4 (up to relabeling) is exhaustive.
"""
import sys
from math import comb


def distributions(n, m):
    """all dicts {k: t_k} (k>=3) with t_2 = m satisfying (C) and (M)"""
    budget = m - 3  # sum (k-3) t_k <= budget
    if budget < 0:
        return []
    target = comb(n, 2) - m  # sum_{k>=3} C(k,2) t_k
    out = []

    def rec(k, remaining_budget, remaining_pairs, acc):
        if k == 3:
            if remaining_pairs % 3 == 0:
                d = dict(acc)
                d[3] = remaining_pairs // 3
                out.append(d)
            return
        maxt = remaining_budget // (k - 3)
        for t in range(0, maxt + 1):
            pairs = comb(k, 2) * t
            if pairs > remaining_pairs:
                break
            acc2 = dict(acc)
            if t:
                acc2[k] = t
            rec(k - 1, remaining_budget - (k - 3) * t, remaining_pairs - pairs, acc2)

    rec(n, budget, target, {})
    return out


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    for m in range(0, M + 1):
        ds = distributions(n, m)
        print(f"n={n} t_2={m}: {len(ds)} distribution(s)")
        for d in ds:
            big = {k: v for k, v in d.items() if k >= 4}
            print(f"    t_3={d[3]:3d}  big lines: {big if big else 'none'}")
