#!/usr/bin/env python3
"""Aggregate the verify_grc.c result files into the per-prime summary table
and re-assert the Burnside cross-check for every (p,t) cell on the way.

Usage: python3 summarize.py [p ...]   (default: all results_p*.txt present)
"""
import glob
import re
import sys
from math import comb

from burnside import orbits

def main(primes):
    print(f"{'p':>3} {'layers':>6} {'orbits':>13} {'subsets':>16} "
          f"{'hard':>5} {'adjud':>5} {'fail':>4} {'wall_s':>8}")
    G_orb = G_sub = 0
    for p in primes:
        rows = []
        for line in open(f"data/results_p{p}.txt"):
            m = re.match(
                r"RESULT p=(\d+) t=(\d+) reps=(\d+) hard=(\d+) t3=(\d+) "
                r"t4=(\d+) adjud=(\d+) fail=(\d+) maxnodes=(\d+) "
                r"time=([\d.]+)s", line)
            if m:
                rows.append([int(x) if i < 9 else float(x)
                             for i, x in enumerate(m.groups())])
        assert rows, f"no rows for p={p}"
        ts = [r[1] for r in rows]
        assert ts == list(range(2, p)), f"p={p}: layers {ts[0]}..{ts[-1]}"
        n_orb = n_sub = n_hard = n_adj = n_fail = 0
        wall = 0.0
        for (pp, t, reps, hard, t3, t4, adj, fail, mx, secs) in rows:
            want = orbits(pp, t)
            assert reps == want, f"BURNSIDE MISMATCH p={pp} t={t}: {reps} != {want}"
            n_orb += reps
            n_sub += comb(pp - 1, t)
            n_hard += hard
            n_adj += adj
            n_fail += fail
            wall += secs
        print(f"{p:>3} {len(rows):>6} {n_orb:>13,} {n_sub:>16,} "
              f"{n_hard:>5} {n_adj:>5} {n_fail:>4} {wall:>8.1f}")
        G_orb += n_orb
        G_sub += n_sub
    print(f"{'all':>3} {'':>6} {G_orb:>13,} {G_sub:>16,}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        primes = [int(x) for x in sys.argv[1:]]
    else:
        primes = sorted(int(re.search(r"_p(\d+)\.txt", f).group(1))
                        for f in glob.glob("data/results_p*.txt"))
    main(primes)
