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


def root_constraints(root):
    """For a gcd-1 integer triple T0 (not necessarily powerful), the set of
    m >= 1 with m*T0 componentwise powerful is, by Lemma 1':
      (i)  every prime p with v_p(w) = 1 for some component w divides m, and
      (ii) for every prime p | m,  v_p(m) >= 2 - min_w v_p(w).
    Returns (mandatory, mu): the mandatory prime set and {p: min_w v_p(w)}
    over all primes appearing in any component with valuation 1, plus those
    needed for lookups (absent p means mu = 0 for new primes of m)."""
    facs = [factor(w) for w in root]
    primes = set().union(*facs)
    mu = {p: min(f.get(p, 0) for f in facs) for p in primes}
    mandatory = {p for p in primes if any(f.get(p, 0) == 1 for f in facs)}
    return mandatory, mu


def is_admissible_root(m, mandatory, mu):
    """Lemma 1' test for a gcd-1 root triple."""
    mm = m
    seen = set()
    p = 2
    while p * p <= mm:
        if mm % p == 0:
            e = 0
            while mm % p == 0:
                e += 1
                mm //= p
            seen.add(p)
            if e < 2 - mu.get(p, 0):
                return False
        p += 1 if p == 2 else 2
    if mm > 1:
        seen.add(mm)
        if 1 < 2 - mu.get(mm, 0):
            return False
    return mandatory <= seen


def saturation_scan(root, K, observed, cap=200000):
    """Ascending scan of admissible multipliers m <= min(K, cap) for the
    gcd-1 root: returns (first_missing or None, scanned_to). 'missing' =
    admissible by Lemma 1' (so m*T0 is an AP of powerful numbers) but absent
    from the census, i.e. an intruder broke consecutiveness."""
    mandatory, mu = root_constraints(root)
    obs = set(observed)
    upto = min(K, cap)
    nadm = 0
    for m in range(1, upto + 1):
        if is_admissible_root(m, mandatory, mu):
            nadm += 1
            if m not in obs:
                return m, upto, nadm
    return None, upto, nadm


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
        # gcd-1 root of the chain: any member divided by the gcd of its
        # components; every member is an integer multiple of it.
        g0 = math.gcd(x, math.gcd(y, z))
        root = (x // g0, y // g0, z // g0)
        obs_m = sorted(math.gcd(triples[j][0], math.gcd(triples[j][1], triples[j][2]))
                       for j in idxs)
        for j in idxs:
            gj = math.gcd(triples[j][0], math.gcd(triples[j][1], triples[j][2]))
            assert tuple(v // gj for v in triples[j]) == root, "chain root mismatch"
        root_powerful = all(
            all(e >= 2 for e in factor(w).values()) for w in root)
        if g0 > 1:
            print(f"  root T0 = {root} (primitive = {g0}*T0; root powerful: "
                  f"{'yes' if root_powerful else 'NO'})")
        if X:
            K = X // root[2]  # need m*z0 <= X to lie in range
            mandatory, mu = root_constraints(root)
            extra = [m for m in obs_m if not is_admissible_root(m, mandatory, mu)]
            first_missing, upto, nadm = saturation_scan(root, K, obs_m)
            if first_missing is None and nadm == 0:
                print(f"  (no admissible m <= scan cap {upto}; smallest "
                      f"observed multiplier is {obs_m[0]})")
            elif first_missing is None:
                print(f"  SATURATED: all {nadm} admissible m <= min(X/z0, cap) = {upto} "
                      f"occur as consecutive triples")
            else:
                print(f"  first missing admissible m = {first_missing} "
                      f"(m*T0 is a powerful AP but not consecutive); "
                      f"observed {len(obs_m)} multipliers, m-range <= X/z0 = {K}")
            if extra:
                print(f"  WARNING: observed multiplier fails Lemma 1': {extra}")
        if len(idxs) > 1:
            base = obs_m[0]
            rel = [Fraction(m, base) for m in obs_m[1:]]
            print(f"  multipliers of T0: {obs_m}")
            print(f"  scalings of primitive: "
                  f"{', '.join('x' + str(f) for f in rel)}")
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
