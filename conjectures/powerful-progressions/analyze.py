#!/usr/bin/env python3
"""Structural analysis of consecutive-powerful-number AP3 triples.

Reads AP3 lines from a census file (census.cpp / census_seg.cpp output) and,
with exact integer arithmetic throughout:

  1. computes each element's unique representation n = a^2 * b^3, b squarefree;
  2. groups triples into scaling chains: T' ~ T iff T' = c*T componentwise
     for some rational c (union-find over all pairs); the chain's smallest
     member is its primitive;
  3. for each chain, computes the admissible multiplier set
        A(T, K) = { k <= K : k*T is again a triple of powerful numbers }
     via Lemma 1 (k admissible iff v_p(k) + min_w v_p(w) >= 2 for every
     prime p | k) and reports whether the chain is saturated below X,
     i.e. whether every admissible multiple is again *consecutive*;
  4. prints per-decade counts of triples and primitives.

Usage: python3 analyze.py data/census_1e18.txt
"""
import re, sys, math
from fractions import Fraction


def factor(n):
    """Trial division; fine for powerful n <= 1e19 (prime factors <= 1e6.33,
    or a leftover p^2, p <= ~3.2e9)."""
    f = {}
    m = n
    p = 2
    while p * p * p <= m:
        while m % p == 0:
            f[p] = f.get(p, 0) + 1
            m //= p
        p += 1 if p == 2 else 2
    if m > 1:
        r = math.isqrt(m)
        if r * r == m:
            f[r] = f.get(r, 0) + 2
        else:
            f[m] = f.get(m, 0) + 1
    chk = 1
    for q, e in f.items():
        chk *= q ** e
    assert chk == n, f"factorization failed for {n}"
    return f


def ab_rep(n):
    """n = a^2 b^3 with b squarefree; asserts n is powerful."""
    f = factor(n)
    a, b = 1, 1
    for q, e in f.items():
        assert e >= 2, f"{n} not powerful (prime {q} exponent {e})"
        if e % 2 == 1:
            b *= q
            a *= q ** ((e - 3) // 2)
        else:
            a *= q ** (e // 2)
    assert a * a * b ** 3 == n
    return a, b


def pretty(n):
    a, b = ab_rep(n)
    if b == 1:
        return f"{a}^2"
    if a == 1:
        return f"{b}^3"
    return f"{a}^2*{b}^3"


def min_valuations(triple):
    """{p: min_w v_p(w)} over the union of primes of the three elements."""
    facs = [factor(w) for w in triple]
    primes = set().union(*facs)
    return {p: min(f.get(p, 0) for f in facs) for p in primes}


def is_admissible(k, mv):
    """Lemma 1 test: v_p(k) + min_w v_p(w) >= 2 for every prime p | k."""
    kk = k
    p = 2
    while p * p <= kk:
        if kk % p == 0:
            e = 0
            while kk % p == 0:
                e += 1
                kk //= p
            if e + mv.get(p, 0) < 2:
                return False
        p += 1 if p == 2 else 2
    if kk > 1 and 1 + mv.get(kk, 0) < 2:
        return False
    return True


def saturation_scan(triple, K, observed, cap=200000):
    """Ascending scan of admissible multipliers k <= min(K, cap):
    returns (n_admissible_scanned, first_missing or None, scanned_to).
    'missing' = admissible by Lemma 1 (so k*T is an AP of powerful numbers)
    but absent from the census, i.e. an intruder broke consecutiveness."""
    mv = min_valuations(triple)
    obs = set(observed)
    nadm = 0
    first_missing = None
    upto = min(K, cap)
    for k in range(1, upto + 1):
        if is_admissible(k, mv):
            nadm += 1
            if k not in obs and first_missing is None:
                first_missing = k
                break
    return nadm, first_missing, upto


def main(path):
    triples = []
    X = 0
    for line in open(path):
        m = re.match(r"AP3 #\d+: (\d+) (\d+) (\d+)", line)
        if m:
            x, y, z = map(int, m.groups())
            assert y - x == z - y
            triples.append((x, y, z))
        m = re.match(r"X = (\d+)", line)
        if m:
            X = int(m.group(1))
    print(f"{len(triples)} triples loaded, X = {X}")

    parent = list(range(len(triples)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(triples)):
        for j in range(i + 1, len(triples)):
            c = Fraction(triples[j][0], triples[i][0])
            if all(Fraction(triples[j][t], triples[i][t]) == c for t in (1, 2)):
                pi, pj = find(i), find(j)
                if pi != pj:
                    parent[max(pi, pj)] = min(pi, pj)

    chains = {}
    for i in range(len(triples)):
        chains.setdefault(find(i), []).append(i)

    print(f"{len(chains)} scaling chains (primitives up to rational scaling)\n")
    dens = 2.17325
    nsquares_hist = {}
    for root in sorted(chains):
        idxs = chains[root]
        x, y, z = triples[idxs[0]]
        d = y - x
        tight = d / (2 * math.sqrt(x) / dens)
        nsq = sum(1 for w in (x, y, z) if ab_rep(w)[1] == 1)
        nsquares_hist[nsq] = nsquares_hist.get(nsq, 0) + 1
        print(f"chain of {len(idxs)}: primitive #{idxs[0]+1}")
        print(f"  ({x}, {y}, {z})  d = {d}" + (" [odd d]" if d % 2 else ""))
        print(f"  = ({pretty(x)}, {pretty(y)}, {pretty(z)})")
        print(f"  tightness d/meangap = {tight:.4f}; d/sqrt(x) = {d/math.sqrt(x):.4f}; "
              f"perfect squares among elements: {nsq}")
        obs = sorted(Fraction(triples[j][0], x) for j in idxs)
        assert all(f.denominator == 1 for f in obs), \
            "chain primitive is not integrally minimal"
        obs_int = [int(f) for f in obs]
        if X:
            K = X // z  # need k*z <= X for the scaled triple to lie in range
            mv = min_valuations((x, y, z))
            extra = [k for k in obs_int if not is_admissible(k, mv)]
            nadm, first_missing, upto = saturation_scan((x, y, z), K, obs_int)
            if first_missing is None:
                print(f"  SATURATED: all {nadm} admissible k <= min(X/z, cap) = {upto} "
                      f"occur as consecutive triples")
            else:
                print(f"  first missing admissible k = {first_missing} "
                      f"(k*T is a powerful AP but not consecutive); "
                      f"observed {len(obs_int)} of admissible k <= X/z = {K}")
            if extra:
                print(f"  WARNING: observed multiplier not admissible by Lemma 1: {extra}")
        if len(idxs) > 1:
            print(f"  scalings: {', '.join('x' + str(int(f)) for f in obs[1:])}")
        print()
    print(f"squares-per-primitive histogram: {nsquares_hist}")

    print("\ndecade | triples | primitives")
    prims = sorted(triples[chains[r][0]][0] for r in chains)
    firsts = sorted(t[0] for t in triples)
    for k in range(3, len(str(X))):
        nt = sum(1 for v in firsts if v < 10 ** k)
        np_ = sum(1 for v in prims if v < 10 ** k)
        print(f"10^{k:<2} | {nt:7} | {np_}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/census_1e18.txt")
