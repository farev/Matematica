"""Enumerate U-code-free bit words at (n, alpha=(n-1)/(n-2)).

Usage: python3 enumerate_lang.py <n> <maxlen> [--palin <k>]

Without --palin: DFS count of U-code-free words per bit-length up to maxlen.
With --palin k: enumerate U-code-free palindromic blocks of odd length k in
the two boundary classes (phi0-type: starts/ends 0, middle 0; phi1-type:
starts/ends 1, middle 1), report monodromy cycle types, and dump candidates
whose type matches tau_0's (1,21)... for phi0 resp. tau_1's (n,) for phi1
to data/palin_n<n>_k<k>.txt.
"""

import sys
import time

from urt import UInc, decode, g_of, cycle_type, make_taus


def seed_inc(n, num, den, maxlen):
    inc = UInc(num, den, maxlen)
    for ch in decode([], n):
        ok = inc.push(ch)
        assert ok
    return inc


def count_words(n, num, den, maxlen):
    inc = seed_inc(n, num, den, maxlen + n + 2)
    counts = [0] * (maxlen + 1)
    state0 = list(range(n))
    stack = [(state0, 0)]  # iterative DFS: (state, next branch index)
    sys.setrecursionlimit(1000000)

    def rec(st, depth):
        counts[depth] += 1
        if depth == maxlen:
            return
        for b in (0, 1):
            if b == 0:
                x = st[0]
                ns = st[1 : n - 1] + [st[0], st[n - 1]]
            else:
                x = st[n - 1]
                ns = st[1 : n - 1] + [st[n - 1], st[0]]
            if inc.push(x):
                rec(ns, depth + 1)
            inc.pop()

    t0 = time.time()
    rec(state0, 0)
    dt = time.time() - t0
    return counts, dt


def palin_candidates(n, num, den, k, kind):
    """Enumerate U-code-free palindromes V of odd length k.

    kind 0: V[0] = V[k-1] = 0, V[(k-1)//2] = 0   (phi_0 candidates)
    kind 1: V[0] = V[k-1] = 1, V[(k-1)//2] = 1   (phi_1 candidates)
    Prefix-prune with UInc; full check at completion (the mirror half can
    introduce violations not visible in the prefix).
    Returns (n_checked_leaves, [(bits, gtype)]) for all completed U-code-free
    palindromes, and the sublist whose cycle type matches the target
    ((1, n-1) for kind 0, (n,) for kind 1).
    """
    assert k % 2 == 1
    h = (k + 1) // 2
    inc = seed_inc(n, num, den, k + n + 2)
    out = []
    leaves = 0
    target = tuple(sorted([1, n - 1])) if kind == 0 else (n,)

    def full_check(half):
        nonlocal leaves
        leaves += 1
        bits = half + half[-2::-1]
        inc2 = seed_inc(n, num, den, k + n + 2)
        st = list(range(n))
        ok = True
        for b in bits:
            if b == 0:
                x = st[0]
                st = st[1 : n - 1] + [st[0], st[n - 1]]
            else:
                x = st[n - 1]
                st = st[1 : n - 1] + [st[n - 1], st[0]]
            if not inc2.push(x):
                ok = False
                break
        if ok:
            g = g_of(bits, n)
            out.append((tuple(bits), cycle_type(g)))

    def rec(st, half, depth):
        if depth == h:
            full_check(half)
            return
        choices = (0, 1)
        if depth == 0:
            choices = (kind,)
        if depth == h - 1:
            choices = (0,) if kind == 0 else (1,)
        for b in choices:
            if b == 0:
                x = st[0]
                ns = st[1 : n - 1] + [st[0], st[n - 1]]
            else:
                x = st[n - 1]
                ns = st[1 : n - 1] + [st[n - 1], st[0]]
            if inc.push(x):
                half.append(b)
                rec(ns, half, depth + 1)
                half.pop()
            inc.pop()

    t0 = time.time()
    rec(list(range(n)), [], 0)
    dt = time.time() - t0
    hits = [bt for bt in out if bt[1] == target]
    return leaves, out, hits, dt


if __name__ == "__main__":
    n = int(sys.argv[1])
    num, den = n - 1, n - 2
    if "--palin" in sys.argv:
        k = int(sys.argv[sys.argv.index("--palin") + 1])
        for kind in (0, 1):
            leaves, out, hits, dt = palin_candidates(n, num, den, k, kind)
            tt = "(1,n-1)" if kind == 0 else "(n,)"
            print(f"n={n} k={k} kind={kind}: {leaves} completed halves, "
                  f"{len(out)} U-code-free palindromes, {len(hits)} with "
                  f"cycle type {tt}  [{dt:.1f}s]")
            if hits:
                fn = f"data/palin_n{n}_k{k}_kind{kind}.txt"
                with open(fn, "w") as f:
                    for bits, _ in hits:
                        f.write("".join(map(str, bits)) + "\n")
                print(f"  wrote {fn}")
    else:
        maxlen = int(sys.argv[2])
        counts, dt = count_words(n, num, den, maxlen)
        for L in range(0, maxlen + 1, 5):
            print(f"len {L}: {counts[L]}")
        print(f"len {maxlen}: {counts[maxlen]}  [{dt:.1f}s]")
