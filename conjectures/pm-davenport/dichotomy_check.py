#!/usr/bin/env python3
"""Split-dichotomy check over the census.

Conjecture A' (split dichotomy): for every finite abelian G, either
    mu(G) = floor(log2 |G|)                (G "attains"), or
    mu(G) = max over proper direct decompositions G = A + B of
            mu(A) + mu(B)                  (G "split-sharp").

Every direct decomposition of a finite abelian group corresponds to a
partition of its multiset of primary cyclic factors (Krull-Schmidt), so
the best split is computable from census values of smaller groups.

Reads sweep.csv; recursively computes best-split values (memoized by
multiset of primary factors, using census mu where available and the
proved formulas mu(C_n) = floor(log2 n) for cyclic factors of prime-power
order when the census lacks an entry).  Reports every group violating
the dichotomy (none expected), and the census split into attained /
split-sharp / both.

Usage: python3 dichotomy_check.py [sweep.csv]
"""

import csv
import sys
from functools import lru_cache
from itertools import combinations


def flog2(n):
    return n.bit_length() - 1


def primary_factors(inv):
    """Invariant factors -> sorted tuple of prime-power cyclic orders."""
    out = []
    for d in inv:
        n = d
        p = 2
        while n > 1:
            if n % p == 0:
                q = 1
                while n % p == 0:
                    n //= p
                    q *= p
                out.append(q)
            p += 1 if p == 2 else 2
    return tuple(sorted(out))


def load(path):
    mu = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            inv = tuple(int(x) for x in row["invariant_factors"].split("x"))
            mu[primary_factors(inv)] = int(row["mu"])
    return mu


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sweep.csv"
    MU = load(path)

    @lru_cache(maxsize=None)
    def mu_of(pf):
        """mu of the group with primary factor multiset pf, from census
        or (for single cyclic prime-power factors) the proved formula."""
        if pf in MU:
            return MU[pf]
        if len(pf) == 1:
            return flog2(pf[0])
        raise KeyError(f"no census value for {pf}")

    @lru_cache(maxsize=None)
    def best_split(pf):
        """max over proper 2-partitions of pf of mu(A)+mu(B); None if
        indecomposable (single factor)."""
        if len(pf) == 1:
            return None
        best = 0
        n = len(pf)
        seen = set()
        for r in range(1, n // 2 + 1):
            for idx in combinations(range(n), r):
                A = tuple(sorted(pf[i] for i in idx))
                B = tuple(sorted(pf[i] for i in range(n) if i not in idx))
                if (A, B) in seen:
                    continue
                seen.add((A, B))
                best = max(best, mu_of(A) + mu_of(B))
        return best

    attained = split_sharp = both = neither = 0
    violations = []
    for pf, mu in sorted(MU.items(), key=lambda kv: (len(kv[0]), kv[0])):
        N = 1
        for q in pf:
            N *= q
        t = flog2(N)
        bs = best_split(pf)
        is_att = (mu == t)
        is_split = (bs is not None and mu == bs)
        if is_att and is_split:
            both += 1
        elif is_att:
            attained += 1
        elif is_split:
            split_sharp += 1
        else:
            neither += 1
            violations.append((pf, N, mu, t, bs))

    total = attained + split_sharp + both + neither
    print(f"groups checked: {total}")
    print(f"  attained only:     {attained}")
    print(f"  split-sharp only:  {split_sharp}")
    print(f"  both:              {both}")
    print(f"  NEITHER (dichotomy violations): {neither}")
    for pf, N, mu, t, bs in violations:
        print(f"  VIOLATION {pf}  N={N}  mu={mu}  t={t}  best_split={bs}")
    # sanity: superadditivity mu >= best_split must hold everywhere
    bad = [(pf, MU[pf], best_split(pf)) for pf in MU
           if best_split(pf) is not None and MU[pf] < best_split(pf)]
    print(f"superadditivity violations (must be 0): {len(bad)}")
    for pf, m, b in bad:
        print(f"  BAD {pf}: mu={m} < best_split={b}")


if __name__ == "__main__":
    main()
