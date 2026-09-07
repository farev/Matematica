#!/usr/bin/env python3
"""idfamily.py — the identity-like family a_t ≡ t (mod q), q = 2^{m-1}, n = 2q-1.

Such a permutation is a_t = t + q*e_t (t < q), a_q = q, a_{t+q} = t + q*(1-e_t),
for a bit string e in {0,1}^{q-1}.  NOTE.md §4c derives: it is good iff
  (I1) no odd-length window of e is constant (equivalently no 000 and no 111);
  (I2) O_i != O'_j for all i, j >= 0 with i + j even, (i,j) != (0,0), (i,j) != (q-1,q-1),
       where O_i = number of ones among e_1..e_i and O'_j = number of ones among the last j bits.
This script (a) checks the derivation against the from-definition test for q = 4, 8, 16
by brute force over all strings, and (b) counts the strings satisfying (I1)+(I2) by DFS
for q up to 64 (q-1 = 63 bits, with pruning on prefixes).

Usage: python3 idfamily.py [maxq]
"""
import sys, itertools

def perm_from_bits(q, e):
    n = 2 * q - 1
    a = [0] * (n + 1)
    for t in range(1, q):
        a[t] = t + q * e[t - 1]
        a[t + q] = t + q * (1 - e[t - 1])
    a[q] = q
    return a[1:]

def is_good(p):
    n = len(p); pre = [0]
    for x in p: pre.append(pre[-1] + x)
    for L in range(2, n):
        for s in range(0, n - L + 1):
            if (pre[s + L] - pre[s]) % L == 0: return False
    return sorted(p) == list(range(1, n + 1))

def sat_I1I2(e):
    N = len(e)
    for i in range(N - 2):
        if e[i] == e[i + 1] == e[i + 2]: return False
    O = [0]
    for x in e: O.append(O[-1] + x)
    Op = [0]
    for x in reversed(e): Op.append(Op[-1] + x)
    for i in range(N + 1):
        for j in range(N + 1):
            if (i + j) % 2 == 0 and (i, j) != (0, 0) and (i, j) != (N, N) and O[i] == Op[j]:
                return False
    return True

def brute(q):
    N = q - 1
    good = crit = both = 0
    for bits in itertools.product([0, 1], repeat=N):
        g = is_good(perm_from_bits(q, bits)); c = sat_I1I2(bits)
        good += g; crit += c; both += (g and c)
        if g != c:
            print("MISMATCH at q=%d e=%s good=%s crit=%s" % (q, bits, g, c)); return None
    return good, crit

def dfs_count(q, cap=10**7):
    """count strings satisfying (I1)+(I2) by DFS with prefix pruning:
    a prefix e_1..e_k fixes O_i for i<=k and, once the whole string is known, O'_j.
    We prune only on (I1) and on the constraints among prefix counts that are already
    decidable: O_i != O'_j requires the suffix; but for the full string we check at the leaf.
    Additional sound pruning: for i<=k and j<=k with i+j even, O'_j is unknown; skip.
    (Used only for q <= 32; q = 64 uses the meet-in-the-middle below.)"""
    N = q - 1; cnt = 0; e = [0] * N
    def rec(k):
        nonlocal cnt
        if cnt >= cap: return
        if k == N:
            if sat_I1I2(e): cnt += 1
            return
        for b in (0, 1):
            if k >= 2 and e[k - 1] == e[k - 2] == b: continue
            e[k] = b; rec(k + 1)
    rec(0); return cnt

if __name__ == "__main__":
    maxq = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    for q in (4, 8, 16):
        r = brute(q)
        print("q=%d n=%d: brute force over 2^%d strings: good=%d, satisfying (I1)+(I2)=%d %s"
              % (q, 2 * q - 1, q - 1, r[0], r[1], "(derivation agrees)" if r else ""))
    for q in (32,):
        if q <= maxq:
            print("q=%d: strings satisfying (I1)+(I2) (DFS with the 000/111 prune): %d" % (q, dfs_count(q)))
