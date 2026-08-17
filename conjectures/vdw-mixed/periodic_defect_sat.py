#!/usr/bin/env python3
"""Complete SAT search for near-periodic good partitions:
x_i = b_{((i-1) mod p)+1} XOR d_i with at most k defect bits d_i set.

Complete per (n, p, k): UNSAT means no p-periodic-with-<=k-defects witness
of length n exists. SAT witnesses are expanded and re-verified independently.

Encoding:
  block vars  b_c   c = 1..p
  defect vars d_i   i = 1..n
  value vars  x_i   i = 1..n   with x_i <-> b_{class(i)} XOR d_i  (4 clauses)
  AP clauses over x as usual; sequential counter enforces sum(d) <= k.

Usage:
  python3 periodic_defect_sat.py s t n p k [budget_conflicts]
  python3 periodic_defect_sat.py s t n pmin-pmax k [budget_conflicts]
"""
import os
import sys
import time

from pysat.solvers import Glucose42

from vdw_cnf import aps, coloring_is_good

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def build(n, s, t, p, k):
    B = lambda c: c                    # 1..p
    D = lambda i: p + i                # p+1..p+n
    X = lambda i: p + n + i            # p+n+1..p+2n
    top = p + 2 * n
    cls = []
    for i in range(1, n + 1):
        b, d, x = B(((i - 1) % p) + 1), D(i), X(i)
        # x <-> b xor d
        cls += [[-x, b, d], [-x, -b, -d], [x, -b, d], [x, b, -d]]
    for ap in aps(n, s):
        cls.append([X(i) for i in ap])
    for ap in aps(n, t):
        cls.append([-X(i) for i in ap])
    # sequential counter: sum d_i <= k
    # s_{i,j}: among d_1..d_i at least j are set; vars laid out after top
    S = lambda i, j: top + (i - 1) * k + j    # i=1..n, j=1..k
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            # s_{i,j} <- s_{i-1,j}
            if i > 1:
                cls.append([-S(i - 1, j), S(i, j)])
            # s_{i,j} <- s_{i-1,j-1} & d_i
            if j == 1:
                cls.append([-D(i), S(i, 1)])
            elif i > 1:
                cls.append([-S(i - 1, j - 1), -D(i), S(i, j)])
        # forbid k+1: d_i & s_{i-1,k} -> false
        if i > 1:
            cls.append([-D(i), -S(i - 1, k)])
    nvars = top + n * k
    return cls, B, D, X, nvars


def solve(n, s, t, p, k, budget=None, verbose=True):
    cls, B, D, X, nv = build(n, s, t, p, k)
    t0 = time.time()
    with Glucose42(bootstrap_with=cls) as SO:
        if budget:
            SO.conf_budget(budget)
            res = SO.solve_limited()
        else:
            res = SO.solve()
        el = time.time() - t0
        if res is None:
            return "UNKNOWN", el, None, None
        if not res:
            return "unsat", el, None, None
        model = set(l for l in SO.get_model() if l > 0)
    col = [0] * (n + 1)
    for i in range(1, n + 1):
        col[i] = 1 if (p + n + i) in model else 0
    ndef = sum(1 for i in range(1, n + 1) if (p + i) in model)
    if not coloring_is_good(col, s, t):
        raise RuntimeError("defect-periodic witness FAILED independent check")
    return "SAT", el, col, ndef


def main():
    s, t, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    prange = sys.argv[4]
    k = int(sys.argv[5])
    budget = int(sys.argv[6]) if len(sys.argv) > 6 else 300000
    if "-" in prange:
        pmin, pmax = map(int, prange.split("-"))
    else:
        pmin = pmax = int(prange)
    for p in range(pmin, pmax + 1):
        res, el, col, ndef = solve(n, s, t, p, k, budget)
        print(f"  p={p} k<={k}: {res}"
              + (f" ({ndef} defects)" if res == "SAT" else "")
              + f" ({el:.1f}s)", flush=True)
        if res == "SAT":
            os.makedirs(DATA, exist_ok=True)
            path = os.path.join(
                DATA, f"witness_{s}_{t}_n{n}_perdef_p{p}k{ndef}.txt")
            with open(path, "w") as f:
                f.write(f"# good partition of [1,{n}] for ({s},{t}); "
                        f"{p}-periodic with {ndef} defects (complete SAT "
                        f"search at k<={k}), verified\n")
                f.write("".join(str(col[i]) for i in range(1, n + 1)) + "\n")
            print(f"WITNESS -> {path}")
            return 0
    return 3


if __name__ == "__main__":
    sys.exit(main())
