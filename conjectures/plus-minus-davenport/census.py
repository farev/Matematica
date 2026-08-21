#!/usr/bin/env python3
"""Census of lmax(G) = D_pm(G) - 1 over all abelian groups of order <= N.

Classification per group:
  pinned   LB == cap (sandwich): lmax = cap, PROVED; witness search as check.
  exp3     exponent-3 (elementary 3-group C3^r, r>=2): lmax = r by Theorem
           T3 (dissociated <=> F3-linearly independent); search verifies
           where affordable.
  search   LB < cap: the C engine decides; witness => cap-attainment,
           full exhaustion => deficiency (both CERTIFIED).

LB = best product bound = max over decompositions of the prime-power
factor multiset into cyclic factors (distinct primes within each part)
of sum floor(log2 part).

Output: census.csv with one row per group.
Usage: census.py N [jobs] [--python-verify M]
"""

import csv
import subprocess
import sys
import time
from itertools import product
from math import prod

from dissoc import Group, abelian_groups_of_order, lmax_dfs


def flog2(x):
    return x.bit_length() - 1


def best_product_bound(factors):
    """Max sum of floor(log2 .) over regroupings of prime-power factors
    into parts with pairwise-distinct primes."""
    # factors are prime powers; group by prime
    def prime_of(q):
        for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                  53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
                  109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167,
                  173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                  233, 239, 241, 251):
            if q % p == 0:
                return p
        return q
    byp = {}
    for q in factors:
        byp.setdefault(prime_of(q), []).append(q)
    primes = sorted(byp)
    for p in primes:
        byp[p].sort(reverse=True)  # descending prime powers
    # number of cyclic parts = max multiplicity; a part takes at most one
    # power of each prime.  Try all assignments of each prime's powers to
    # part slots (parts symmetric; fix slots 0..k-1, powers of a prime go
    # to distinct slots).  Small enough for our group sizes.
    k = max(len(v) for v in byp.values())
    from itertools import permutations

    best = -1

    def slot_choices(powers):
        # ways to place powers into distinct slots 0..k-1
        for pos in permutations(range(k), len(powers)):
            yield pos

    def rec(i, slots):
        nonlocal best
        if i == len(primes):
            val = sum(flog2(s) for s in slots if s > 1)
            best = max(best, val)
            return
        p = primes[i]
        for pos in slot_choices(byp[p]):
            new = list(slots)
            for q, j in zip(byp[p], pos):
                new[j] *= q
            rec(i + 1, new)

    rec(0, [1] * k)
    return best


def exponent(factors):
    from math import lcm
    return lcm(*factors)


def run_c_engine(binpath, factors, need=None, order=None, timeout=None):
    cmd = [binpath] + [str(f) for f in factors]
    if need:
        cmd.append(f"need={need}")
    if order:
        cmd.append(f"order={order}")
    t0 = time.time()
    out = subprocess.run(cmd, capture_output=True, text=True,
                         timeout=timeout).stdout
    dt = time.time() - t0
    lmax = nodes = None
    witness = ""
    for line in out.splitlines():
        if line.startswith("lmax = "):
            parts = line.split()
            lmax = int(parts[2])
            nodes = int(parts[5])
        if line.startswith("witness coords ="):
            witness = line.split("=", 1)[1].strip()
    return lmax, nodes, witness, dt


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    out = sys.argv[3] if len(sys.argv) > 3 else "census.csv"
    slow = []
    rows = []
    t_start = time.time()
    for n in range(start, N + 1):
        for factors in abelian_groups_of_order(n):
            cap = flog2(n)
            lb = best_product_bound(factors)
            exp = exponent(factors)
            rank = len(factors)
            name = "+".join(f"C{f}" for f in factors)
            if lb == cap:
                method = "pinned"
                # quick verification: witness search with need=cap
                lmax, nodes, wit, dt = run_c_engine("./dissoc", factors,
                                                    need=cap, timeout=60)
                assert lmax == cap, (name, lmax, cap)
            elif exp == 3:
                method = "theorem-T3"
                # verify by search only when modest
                if n <= 100:
                    lmax, nodes, wit, dt = run_c_engine("./dissoc", factors,
                                                        timeout=300)
                    assert lmax == rank, (name, lmax, rank)
                else:
                    lmax, nodes, wit, dt = rank, -1, "", 0.0
            else:
                method = "search"
                try:
                    lmax, nodes, wit, dt = run_c_engine("./dissoc", factors,
                                                        timeout=600)
                except subprocess.TimeoutExpired:
                    slow.append((n, factors))
                    rows.append(dict(order=n, group=name, lb=lb, cap=cap,
                                     lmax="TIMEOUT", dpm="", method="search",
                                     nodes="", seconds=">600", witness=""))
                    continue
            rows.append(dict(order=n, group=name, lb=lb, cap=cap, lmax=lmax,
                             dpm=lmax + 1, method=method, nodes=nodes,
                             seconds=f"{dt:.2f}", witness=wit))
            tag = ("DEFICIENT" if isinstance(lmax, int) and lmax < cap
                   else "")
            if method == "search" or tag:
                print(f"n={n:4d} {name:22s} lb={lb} cap={cap} "
                      f"lmax={lmax} {tag} ({dt:.2f}s, {nodes} nodes)",
                      flush=True)
    with open("census.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["order", "group", "lb", "cap",
                                          "lmax", "dpm", "method", "nodes",
                                          "seconds", "witness"])
        w.writeheader()
        w.writerows(rows)
    print(f"census to {N}: {len(rows)} groups, {time.time()-t_start:.1f}s "
          f"total, {len(slow)} timeouts: {slow}")


if __name__ == "__main__":
    main()
