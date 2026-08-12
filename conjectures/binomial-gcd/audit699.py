#!/usr/bin/env python3
"""Deep-sample audit of the C sweep engine for Erdos #699.

Draws pseudorandom (seeded) n from [4, N], computes g(n) = n - prevprime(n)
independently (sympy), and for every level i <= min(g, n/2-1) re-decides
tight/counterexample status via a fully independent path:

    C engine (sweep699.c)          this audit (family699.py core)
    -----------------------        ------------------------------
    segmented sieve factoring      sympy factorint (rho/p-1)
    CRT candidate enumeration      Lucas dominated-set enumeration
    C, uint64                      Python bignums

Any disagreement with the committed census (extra hit, missing hit) is a
FAIL. Levels whose dominated sets blow past the cap are SKIPPED and counted
(reported honestly); everything else is a hard check.

Usage: audit699.py N SAMPLES SEED [--include-census]
"""
import sys
import random
from sympy import isprime, prevprime
import family699 as F


def main():
    N = int(sys.argv[1])
    samples = int(sys.argv[2])
    seed = int(sys.argv[3])
    census_file = sys.argv[4] if len(sys.argv) > 4 else None
    census = set()
    if census_file:
        for line in open(census_file):
            if line.startswith("#"):
                continue
            kind, n, i, j = line.strip().split(",")
            census.add((kind, int(n), int(i), int(j)))
    rng = random.Random(seed)
    checked = skipped = 0
    fails = []
    hits = []
    # always include the census rows' n themselves plus random n
    ns = sorted({int(n) for (_, n, _, _) in census if n <= N} |
                {rng.randrange(4, N + 1) for _ in range(samples)})
    for idx, n in enumerate(ns):
        try:
            g, imax, res = F.family_entry(n, f"audit-n={n}")
        except RuntimeError as e:
            skipped += 1
            print(f"  SKIP n={n}: {e}")
            continue
        checked += 1
        for (kind, nn, ii, jj) in res:
            hits.append((kind, nn, ii, jj))
            if (kind, nn, ii, jj) not in census:
                fails.append(("extra", kind, nn, ii, jj))
        if idx % 200 == 0:
            print(f"  ...{idx}/{len(ns)} n checked", flush=True)
    # census rows for sampled n must all have been found
    sampled_n = set(ns)
    for row in census:
        if row[1] in sampled_n and row not in set(hits):
            # row = (kind, n, i, j); hits entries are tuples same shape
            if (row[0], row[1], row[2], row[3]) not in hits:
                fails.append(("missing",) + row)
    print(f"\nAUDIT: {checked} n fully re-decided, {skipped} skipped (blowup), "
          f"{len(hits)} hits reproduced, {len(fails)} FAILURES")
    for f_ in fails:
        print("  FAIL", f_)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
