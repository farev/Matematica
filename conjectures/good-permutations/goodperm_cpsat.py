#!/usr/bin/env python3
"""goodperm_cpsat.py — third, independent method: CP-SAT (OR-Tools) model over the
triangular bit-functions of NOTE.md Lemma 2, with one modular constraint per
proper block of odd length (even lengths are automatic, Lemma 3).

Usage: python3 goodperm_cpsat.py n [time_limit_s] [workers] [enumerate]
  n = 2^m - 1.  With enumerate=1 all solutions are enumerated (single worker,
  needed for exact counts); otherwise the solver decides feasibility.
Prints status, count (if enumerating), wall time, and the first solutions found,
each re-verified by an independent from-definition check inside this script.
"""
import sys, time
from ortools.sat.python import cp_model


def is_good(p):
    n = len(p)
    pre = [0]
    for x in p:
        pre.append(pre[-1] + x)
    for L in range(2, n):
        for s in range(0, n - L + 1):
            if (pre[s + L] - pre[s]) % L == 0:
                return False
    return sorted(p) == list(range(1, n + 1))


def build(n):
    m = (n + 1).bit_length() - 1
    assert (1 << m) - 1 == n
    md = cp_model.CpModel()
    # b[k][r] for k = 1..m-1, r in [1, 2^k) ; b_k(0) = 0 and b_0 = 0 are constants
    b = {}
    for k in range(1, m):
        for r in range(1, 1 << k):
            b[(k, r)] = md.NewBoolVar(f"b_{k}_{r}")

    def a_expr(t):
        terms = []
        const = t & 1  # bit 0 of a_t equals bit 0 of t
        for k in range(1, m):
            r = t & ((1 << k) - 1)
            tb = (t >> k) & 1
            if r == 0:
                const += (1 << k) * tb
            else:
                v = b[(k, r)]
                if tb == 0:
                    terms.append((1 << k, v))
                else:
                    const += (1 << k)
                    terms.append((-(1 << k), v))
        return terms, const

    A = [None] + [a_expr(t) for t in range(1, n + 1)]
    nblocks = 0
    for L in range(3, n, 2):
        for s in range(0, n - L + 1):
            lin = {}
            const = 0
            for t in range(s + 1, s + L + 1):
                terms, c = A[t]
                const += c
                for coef, v in terms:
                    lin[v] = lin.get(v, 0) + coef
            # sum = L*quot + rem, rem in [1, L-1]
            maxsum = L * n
            quot = md.NewIntVar(0, maxsum // L + 1, f"q_{s}_{L}")
            rem = md.NewIntVar(1, L - 1, f"r_{s}_{L}")
            md.Add(sum(coef * v for v, coef in lin.items()) + const == L * quot + rem)
            nblocks += 1
    return md, b, m, nblocks, A


def decode(sol, b, m, n):
    p = []
    for t in range(1, n + 1):
        v = t & 1
        for k in range(1, m):
            r = t & ((1 << k) - 1)
            tb = (t >> k) & 1
            bit = 0 if r == 0 else sol.Value(b[(k, r)])
            v |= ((bit ^ tb) << k)
        p.append(v)
    return p


class Collector(cp_model.CpSolverSolutionCallback):
    def __init__(self, b, m, n, maxprint=10):
        super().__init__()
        self.b, self.m, self.n, self.maxprint = b, m, n, maxprint
        self.count = 0
    def on_solution_callback(self):
        self.count += 1
        p = decode(self, self.b, self.m, self.n)
        ok = is_good(p)
        if self.count <= self.maxprint:
            print(("GOOD " if ok else "BAD!! ") + " ".join(map(str, p)), flush=True)
        if not ok:
            print("DEFECT: solver returned a non-good permutation", flush=True)


def main():
    n = int(sys.argv[1])
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 600.0
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    enum = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    t0 = time.time()
    md, b, m, nblocks, A = build(n)
    print(f"n={n} m={m} bool_vars={len(b)} odd_blocks={nblocks} build={time.time()-t0:.1f}s", flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_workers = 1 if enum else workers
    if enum:
        solver.parameters.enumerate_all_solutions = True
    cb = Collector(b, m, n)
    status = solver.Solve(md, cb) if enum else solver.Solve(md)
    name = solver.StatusName(status)
    if not enum and status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        p = decode(solver, b, m, n)
        print(("GOOD " if is_good(p) else "BAD!! ") + " ".join(map(str, p)))
    print(f"n={n} status={name} count={cb.count if enum else 'n/a'} wall={time.time()-t0:.1f}s "
          f"conflicts={solver.NumConflicts()} branches={solver.NumBranches()}", flush=True)


if __name__ == "__main__":
    main()
