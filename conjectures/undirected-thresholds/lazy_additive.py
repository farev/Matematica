"""Offline additive-structure scan of deep canonical words.

Given a canonical U-free word C (from probe.py DFS), for each k test
whether some injection nu: letters(C) -> Z_n makes nu(C) additive:
nu(C[q]) = nu(C[q//k]) + nu(C[q%k]) (mod n), nu(C[0]) = 0.

Solve by symbolic digit-sum forms over free vars x_j = nu of the canonical
letter first occurring at position j < k (dedup: one var per canonical
letter), then Gaussian-style consistency over Z_n via CRT (n = 2 * 11 for
n = 22; general: reduce mod each prime power factor).

This is a NECESSARY-condition scan on one branch of the language tree; a
negative here does not exclude the ansatz on other branches.
"""

import sys
from math import gcd

import numpy as np

from urt import UInc


def probe_canonical(n, num, den, target, seed=0):
    import random
    rng = random.Random(seed)
    inc = UInc(num, den, target + 2)
    word = []
    used = 0
    stack = []
    bt = 0
    while len(word) < target and bt < 500000:
        recent = set(word[-(n - 3):]) if len(word) >= n - 3 else set(word)
        cands = [c for c in range(min(used + 1, n)) if c not in recent]
        rng.shuffle(cands)
        placed = False
        for ci, c in enumerate(cands):
            if inc.push(c):
                word.append(c)
                stack.append(cands[ci + 1:])
                used = max(used, c + 1)
                placed = True
                break
            inc.pop()
        if not placed:
            while stack:
                bt += 1
                rest = stack.pop()
                word.pop()
                inc.pop()
                used = max([0] + [x + 1 for x in word])
                pl2 = False
                for ci, c in enumerate(rest):
                    if inc.push(c):
                        word.append(c)
                        stack.append(rest[ci + 1:])
                        used = max(used, c + 1)
                        pl2 = True
                        break
                    inc.pop()
                if pl2:
                    break
            else:
                break
    return word


def additive_check(C, n, k):
    """Return (consistent, message). Letters of C get symbolic values; the
    letters first occurring at q < k are free vars; every position q has
    value form(q) = sum over base-k digits of q of x_{letter at digit pos}.
    Constraints: same letter -> same value; different letters -> different
    values (checked when forms are constant-difference); nu(C[0]) = 0.
    Consistency over Z_n handled by scanning solutions mod prime powers?
    Here: collect linear equations E x = 0 (mod n) and check solvability
    with injectivity via randomized + exhaustive-on-small-null-space search.
    """
    L = len(C)
    letters = sorted(set(C))
    # free vars: letters by first occurrence among positions < k
    first = {}
    for q, c in enumerate(C):
        if c not in first:
            first[c] = q
    freevars = [c for c in letters if first[c] < k]
    lidx = {c: i for i, c in enumerate(freevars)}
    V = len(freevars)
    # symbolic value of each position: vector of digit multiplicities
    # value(q) = sum_j mult[j] * x_j where digits of q index into C's first
    # k positions -> letters -> vars
    # compute per-position form by recursion: form(q) = form(q//k)+form(q%k)
    forms = np.zeros((L, V), dtype=np.int64)
    for q in range(L):
        if q < k:
            c = C[q]
            if first[c] < k:
                forms[q, lidx[c]] = 1
            else:
                return False, "letter first occurs >= k but q < k?"
        else:
            forms[q] = forms[q // k] + forms[q % k]
            if forms[q].max() > 10**9:
                return False, "overflow"
    # constraints: for each letter, all positions with that letter share a
    # form value -> differences must vanish (mod n); pick first occurrence
    # as representative
    eqs = []
    for q in range(L):
        d = forms[q] - forms[first[C[q]]]
        if d.any():
            eqs.append(d % n)
    # nu(C[0]) = 0: C[0] is a var; x_{C[0]} = 0
    z = np.zeros(V, dtype=np.int64)
    z[lidx[C[0]]] = 1
    eqs.append(z)
    # solve: enumerate assignments of free vars mod n satisfying all eqs and
    # injectivity.  V can be up to 22 -> enumeration too big; but eqs
    # usually pin everything.  Use: iterate over assignments of a small
    # basis via elimination mod prime factors.
    # cheap route: find any solution by randomized search guided by
    # elimination mod 2 and mod 11 (n = 22); here use brute elimination:
    A = (np.array(eqs) % n).astype(np.int64)
    # eliminate mod n with gcd pivoting (Smith-lite)
    A = A.copy()
    ncols = V
    pivots = {}
    r = 0
    Ared = A.tolist()
    # simple Hermite-style reduction mod n
    import itertools
    # fall back: solve by DFS over vars with constraint propagation
    # order vars; maintain partial assignment; check each eq when fully
    # assigned; prune via eqs with single unassigned var
    eqlist = [tuple(int(v) for v in row) for row in A]
    eqlist = list(set(eqlist))
    sol = {}

    def consistent_eq(row, assign):
        s = 0
        unk = None
        cnt = 0
        for j in range(V):
            if row[j] == 0:
                continue
            if j in assign:
                s += row[j] * assign[j]
            else:
                unk = j
                cnt += 1
                if cnt > 1:
                    return True, None, None
        if cnt == 0:
            return (s % n == 0), None, None
        # one unknown: row[unk]*x = -s (mod n)
        a = row[unk] % n
        b = (-s) % n
        g = gcd(a, n)
        if b % g:
            return False, None, None
        # solutions exist; don't force (may be multiple); just report
        return True, unk, (a, b)

    def dfs(i, assign, usedvals):
        if i == V:
            return dict(assign)
        j = order[i]
        for v in range(n):
            if v in usedvals:
                continue
            assign[j] = v
            ok = True
            for row in eqlist:
                res, _, _ = consistent_eq(row, assign)
                if not res:
                    ok = False
                    break
            if ok:
                usedvals.add(v)
                r = dfs(i + 1, assign, usedvals)
                if r is not None:
                    return r
                usedvals.discard(v)
            del assign[j]
        return None

    order = sorted(range(V), key=lambda j: -sum(1 for row in eqlist if row[j]))
    res = dfs(0, {}, set())
    if res is None:
        return False, f"no injective nu (V={V}, eqs={len(eqlist)})"
    B0 = [res[lidx[C[j]]] for j in range(k)]
    return True, ("nu found", res, B0)


if __name__ == "__main__":
    n, num, den, target = 22, 21, 20, int(sys.argv[1]) if len(sys.argv) > 1 else 700
    seeds = [int(s) for s in sys.argv[2].split(",")] if len(sys.argv) > 2 else [0, 1, 2]
    for seed in seeds:
        C = probe_canonical(n, num, den, target, seed=seed)
        print(f"seed {seed}: canonical word length {len(C)}")
        hits = []
        for k in range(20, 67):
            ok, msg = additive_check(C[: min(len(C), 12 * k)], n, k)
            if ok:
                hits.append((k, msg))
                print(f"  k={k}: ADDITIVE-CONSISTENT  B0={msg[2]}")
        if not hits:
            print("  no additive k in [20,66] on this branch")
