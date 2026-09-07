#!/usr/bin/env python3
"""Empirical check of the 2-adic structure on known good permutations.

For a permutation a_1..a_n (n = 2^m - 1), with a_0 := 0, checks:
  (L1) te4/Bisceanu: a_{t+2^k} = a_t (mod 2^k) whenever 2^k < n, 1 <= t <= n-2^k.
  (L2) sum of any 2^k consecutive terms (2^k < n) is an odd multiple of 2^{k-1}.
  (L3) v_2(a_t) = v_2(t) for all t.
  (L4) full 2-adic isometry: for all 0 <= x < y <= n, v_2(a_y - a_x) = v_2(y - x).
  (L5) the pair {a_t, a_{t+q}} = {r, r+q} with q = 2^{m-1}, r = a_t mod q, a_q = q.
Also prints the 'flip pattern': bit k of a_t XOR bit k of t as a function of
t mod 2^k (must be well defined for a tree automorphism).

Usage: python3 lemma_check.py FILE   (one permutation per line)
"""
import sys


def v2(x):
    assert x != 0
    c = 0
    while x % 2 == 0:
        x //= 2
        c += 1
    return c


def check(a):
    n = len(a)
    m = n.bit_length()
    assert n == 2 ** m - 1, "n must be 2^m - 1"
    s = [0] + a  # s[0] = 0
    P = [0] * (n + 1)
    for i in range(1, n + 1):
        P[i] = P[i - 1] + s[i]
    res = {}
    # L1
    ok = True
    for k in range(1, m):
        if 2 ** k >= n:
            break
        for t in range(1, n - 2 ** k + 1):
            if (s[t + 2 ** k] - s[t]) % 2 ** k != 0:
                ok = False
    res["L1 a_{t+2^k} = a_t mod 2^k"] = ok
    # L2
    ok = True
    for k in range(1, m):
        if 2 ** k >= n:
            break
        for i in range(0, n - 2 ** k + 1):
            S = P[i + 2 ** k] - P[i]
            if S % 2 ** (k - 1) != 0 or (S // 2 ** (k - 1)) % 2 == 0:
                ok = False
    res["L2 sum of 2^k consecutive = odd * 2^(k-1)"] = ok
    # L3
    res["L3 v2(a_t) = v2(t)"] = all(v2(s[t]) == v2(t) for t in range(1, n + 1))
    # L4
    ok = True
    for x in range(0, n + 1):
        for y in range(x + 1, n + 1):
            if v2(s[y] - s[x]) != v2(y - x):
                ok = False
    res["L4 2-adic isometry incl. a_0=0"] = ok
    # L5
    q = 2 ** (m - 1)
    ok = s[q] == q
    for t in range(1, q):
        r = s[t] % q
        if sorted([s[t], s[t + q]]) != [r, r + q]:
            ok = False
    res["L5 pairs {a_t,a_{t+q}}={r,r+q}, a_q=q"] = ok
    # flip pattern
    flips = {}
    consistent = True
    for k in range(0, m):
        table = {}
        for t in range(0, n + 1):
            key = t % 2 ** k
            bit = ((s[t] >> k) ^ (t >> k)) & 1
            if key in table and table[key] != bit:
                consistent = False
            table[key] = bit
        flips[k] = table
    res["flip pattern f_k(t mod 2^k) well defined"] = consistent
    return res, flips


if __name__ == "__main__":
    for line in open(sys.argv[1]):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        a = [int(x) for x in line.replace(",", " ").split()]
        res, flips = check(a)
        print("perm:", " ".join(map(str, a)))
        for k, v in res.items():
            print("   ", "OK " if v else "FAIL", k)
        for k in sorted(flips):
            tab = flips[k]
            print("    bit %d flipped for t mod %d in %s" % (k, 2 ** k, sorted(r for r in tab if tab[r])))
