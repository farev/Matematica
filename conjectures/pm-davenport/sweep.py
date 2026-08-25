#!/usr/bin/env python3
"""Sweep d_pm (= max dissociated set size mu(G)) over ALL finite abelian
groups of order <= MAXN, via the C engine (dpm_fast), recording for each:

    group (invariant factors), |G|, t = floor(log2 |G|),
    concat = sum of floor(log2 d_i) over cyclic factors (lower bound),
    mu = d_pm, attained = (mu == t), n_extremal, nodes.

Also runs every group in a second presentation (prime-power factors) when it
differs from the invariant-factor presentation, and asserts that mu,
n_extremal and nodes agree — an isomorphism-invariance cross-check of the
engine (node count = number of nonempty pm-zsf sets, an invariant).

Output: sweep.csv (one row per group, invariant-factor presentation).

Usage: python3 sweep.py MAXN [--engine ./dpm_fast]
"""

import subprocess
import sys
import csv
from functools import lru_cache


def primes_upto(n):
    s = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if s[i] == i:
            for j in range(i * i, n + 1, i):
                if s[j] == j:
                    s[j] = i
    return s


def factor(n, small):
    f = {}
    while n > 1:
        p = small[n]
        f[p] = f.get(p, 0) + 1
        n //= p
    return f


def partitions(n):
    if n == 0:
        yield []
        return
    for first in range(n, 0, -1):
        for rest in partitions(n - first):
            if not rest or rest[0] <= first:
                yield [first] + rest


def abelian_groups(N, small):
    """All abelian groups of order N as sorted lists of prime-power cyclic
    factors [(p, e), ...]."""
    f = factor(N, small)
    groups = [[]]
    for p, e in sorted(f.items()):
        new = []
        for part in partitions(e):
            for g in groups:
                new.append(g + [(p, k) for k in part])
        groups = new
    return groups


def invariant_factors(pp):
    """Convert prime-power factor list [(p,e),...] to invariant factors
    d_1 | d_2 | ... (largest last)."""
    from collections import defaultdict
    byp = defaultdict(list)
    for p, e in pp:
        byp[p].append(p ** e)
    for p in byp:
        byp[p].sort(reverse=True)
    r = max(len(v) for v in byp.values())
    inv = []
    for i in range(r):
        d = 1
        for p in byp:
            if i < len(byp[p]):
                d *= byp[p][i]
        inv.append(d)
    inv.sort()
    return inv


def flog2(n):
    return n.bit_length() - 1


def run_engine(engine, orders):
    out = subprocess.run([engine] + [str(o) for o in orders],
                         capture_output=True, text=True, check=True).stdout
    mu = next(int(l.split()[2]) for l in out.splitlines() if l.startswith("d_pm"))
    line = next(l for l in out.splitlines() if l.startswith("d_pm"))
    parts = line.replace("=", " ").split()
    # d_pm X D_pm Y n_extremal Z nodes W
    mu = int(parts[1])
    next_ = int(parts[5])
    nodes = int(parts[7])
    wit = next(l for l in out.splitlines() if l.startswith("witness:"))
    return mu, next_, nodes, wit[9:].strip()


def main():
    maxn = int(sys.argv[1])
    engine = "./dpm_fast"
    if "--engine" in sys.argv:
        engine = sys.argv[sys.argv.index("--engine") + 1]
    small = primes_upto(maxn)
    rows = []
    for N in range(2, maxn + 1):
        for pp in abelian_groups(N, small):
            inv = invariant_factors(pp)
            ppo = sorted(p ** e for p, e in pp)
            mu, nex, nodes, wit = run_engine(engine, inv)
            if ppo != inv:
                mu2, nex2, nodes2, _ = run_engine(engine, ppo)
                assert (mu, nex, nodes) == (mu2, nex2, nodes2), \
                    f"presentation mismatch for {inv} vs {ppo}: " \
                    f"{(mu, nex, nodes)} != {(mu2, nex2, nodes2)}"
            t = flog2(N)
            concat = sum(flog2(d) for d in inv)
            rows.append({
                "invariant_factors": "x".join(map(str, inv)),
                "N": N,
                "t_log2N": t,
                "concat_lb": concat,
                "mu": mu,
                "attained": int(mu == t),
                "deficiency": t - mu,
                "n_extremal": nex,
                "nodes": nodes,
                "witness": wit,
            })
            print(f"Z_{'xZ_'.join(map(str, inv))}  N={N}  mu={mu}  t={t}  "
                  f"{'ATTAINED' if mu == t else 'DEFICIENT by ' + str(t - mu)}"
                  f"  extremal={nex}")
    with open("sweep.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote sweep.csv with {len(rows)} groups")
    def_rows = [r for r in rows if r["deficiency"] > 0]
    print(f"deficient groups: {len(def_rows)}")
    for r in def_rows:
        print(f"  {r['invariant_factors']}  N={r['N']}  mu={r['mu']}  "
              f"t={r['t_log2N']}  def={r['deficiency']}")


if __name__ == "__main__":
    main()
