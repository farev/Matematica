#!/usr/bin/env python3
"""Engine B: independent exact search for m-sets of distinct positive reals with no
dissociated k-subset.  Written separately from dissoc_search.py (engine A):

  * state = reduced row echelon relation matrix over Q (rows = chosen relations),
    a relation r holds identically on the current subspace iff r reduces to 0 mod rows;
  * branching order: subsets sorted by (largest index, tuple) -- i.e. the set is built
    element by element and every k-subset inside a prefix is settled before the next
    element is used ("prefix-first"), no fail-first heuristic;
  * feasibility of  {a : rows.a = 0, 0 < a_1 < ... < a_m}  is decided at EVERY node by a
    floating LP whose verdict is accepted only after an exact rational certificate is
    verified: a rational point for "feasible", a Gordan vector lambda >= 0, lambda != 0,
    lambda^T C = 0 (mod the row space) for "infeasible"; when neither certificate can be
    rationalised, sympy's exact simplex (lpmax) decides.
Relation patterns are regenerated here by a different method (direct check of the sorted
cone via the exact simplex), not imported from engine A.
"""
import sys, itertools, time
from fractions import Fraction
from math import gcd
import numpy as np
from scipy.optimize import linprog
from sympy import symbols, Rational
from sympy.solvers.simplex import lpmax

# ------------------------------------------------------------------ exact rational RREF
class RelSpace:
    """Row-reduced list of rational relation vectors (pivot columns strictly increasing)."""
    def __init__(self, m):
        self.m = m
        self.rows = []      # list of (pivot, vector as list of Fraction), pivot value 1
    def reduce(self, v):
        v = [Fraction(x) for x in v]
        for piv, row in self.rows:
            c = v[piv]
            if c != 0:
                v = [a - c * b for a, b in zip(v, row)]
        return v
    def holds(self, v):
        return all(x == 0 for x in self.reduce(v))
    def add(self, v):
        """return a new RelSpace with v added (v must not already hold)."""
        w = self.reduce(v)
        piv = next(i for i, x in enumerate(w) if x != 0)
        w = [x / w[piv] for x in w]
        new = RelSpace(self.m)
        # keep fully reduced form: eliminate column piv from existing rows
        new.rows = []
        for p, row in self.rows:
            c = row[piv]
            if c != 0:
                row = [a - c * b for a, b in zip(row, w)]
            new.rows.append((p, row))
        new.rows.append((piv, w))
        new.rows.sort(key=lambda t: t[0])
        return new
    def dim_kernel(self):
        return self.m - len(self.rows)
    def kernel_basis(self):
        """rational basis of {a : rows.a = 0}: free columns parametrise."""
        pivs = [p for p, _ in self.rows]
        free = [j for j in range(self.m) if j not in pivs]
        basis = []
        for f in free:
            vec = [Fraction(0)] * self.m
            vec[f] = Fraction(1)
            for p, row in self.rows:
                vec[p] = -row[f]
            basis.append(vec)
        return basis

# ------------------------------------------------------------------ exact feasibility
def cone_matrix(basis, m):
    """rows of C: a_1 > 0 and a_{i+1}-a_i > 0 expressed in kernel coordinates y."""
    d = len(basis)
    C = [[basis[t][0] for t in range(d)]]
    for i in range(m - 1):
        C.append([basis[t][i + 1] - basis[t][i] for t in range(d)])
    return C

def exact_simplex_feasible(C):
    d = len(C[0]); n = len(C)
    ys = symbols(f"y0:{d}"); t = symbols("t")
    cons = []
    for row in C:
        cons.append(sum(Rational(row[j].numerator, row[j].denominator) * ys[j] for j in range(d)) - t >= 0)
    for j in range(d):
        cons += [ys[j] <= 1, ys[j] >= -1]
    cons += [t <= 1, t >= 0]
    val, _ = lpmax(t, cons)
    return val > 0

def feasible_certified(C, m, stats):
    """decide {y : C y > 0} != empty with an exact certificate."""
    d = len(C[0]); n = len(C)
    Cf = np.array([[float(x) for x in row] for row in C])
    # max t: -C y + t <= 0 ; -1<=y<=1 ; 0<=t<=1
    c = np.zeros(d + 1); c[-1] = -1.0
    A_ub = np.hstack([-Cf, np.ones((n, 1))]); b_ub = np.zeros(n)
    bounds = [(-1, 1)] * d + [(0, 1)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if res.status == 0 and -res.fun > 1e-9:
        # try to certify feasibility with an exact rational point
        y = res.x[:d]
        for den in (8, 64, 1024, 10**5, 10**8):
            yq = [Fraction(v).limit_denominator(den) for v in y]
            if all(sum(C[i][j] * yq[j] for j in range(d)) > 0 for i in range(n)):
                stats["cert_point"] += 1
                return True, yq
    if res.status == 0 and -res.fun <= 1e-9:
        lam = res.ineqlin.marginals  # dual values for A_ub rows (<= 0 for a min problem)
        lam = [-float(v) for v in lam]
        for den in (8, 64, 1024, 10**5, 10**8):
            lq = [Fraction(v).limit_denominator(den) for v in lam]
            lq = [x if x > 0 else Fraction(0) for x in lq]
            if any(x > 0 for x in lq) and all(sum(lq[i] * C[i][j] for i in range(n)) == 0 for j in range(d)):
                stats["cert_gordan"] += 1
                return False, lq
    stats["fallback_simplex"] += 1
    ok = exact_simplex_feasible(C)
    return ok, None

# ------------------------------------------------------------------ relation patterns
def patterns(k, stats):
    pats = []
    for eps in itertools.product((1, 0, -1), repeat=k):
        nz = [e for e in eps if e != 0]
        if not nz or nz[0] != 1:
            continue
        R = RelSpace(k).add(eps)
        B = R.kernel_basis()
        C = cone_matrix(B, k)
        ok, _ = feasible_certified(C, k, stats)
        if ok:
            pats.append(eps)
    return pats

# ------------------------------------------------------------------ search
class EngineB:
    def __init__(self, m, k, max_solutions=1, verbose=False):
        self.m, self.k = m, k
        self.stats = {"cert_point": 0, "cert_gordan": 0, "fallback_simplex": 0}
        self.pats = patterns(k, self.stats)
        subs = list(itertools.combinations(range(m), k))
        subs.sort(key=lambda Q: (Q[-1], Q))   # prefix-first order
        self.subsets = subs
        self.rels = []
        for Q in subs:
            lst = []
            for eps in self.pats:
                v = [0] * m
                for e, i in zip(eps, Q):
                    v[i] = e
                lst.append(tuple(v))
            self.rels.append(lst)
        self.nodes = 0; self.leaves = 0; self.pruned_lp = 0
        self.solutions = []
        self.max_solutions = max_solutions
        self.verbose = verbose

    def dfs(self, R, chosen):
        self.nodes += 1
        B = R.kernel_basis()
        if not B:
            return False
        ok, cert = feasible_certified(cone_matrix(B, self.m), self.m, self.stats)
        if not ok:
            self.pruned_lp += 1
            return False
        # first unblocked subset in prefix-first order
        for qi, lst in enumerate(self.rels):
            if not any(R.holds(r) for r in lst):
                for r in lst:
                    chosen.append((self.subsets[qi], r))
                    if self.dfs(R.add(r), chosen):
                        return True
                    chosen.pop()
                return False
        # leaf: all subsets blocked and feasible => solution family
        self.leaves += 1
        # integer witness from the rational point cert
        d = len(B)
        a = [sum(cert[t] * B[t][i] for t in range(d)) for i in range(self.m)]
        L = 1
        for x in a:
            L = L * x.denominator // gcd(L, x.denominator)
        w = [int(x * L) for x in a]
        self.solutions.append((list(chosen), [[str(x) for x in b] for b in B], w))
        if self.verbose:
            print("  FOUND family dim", d, "witness", w, flush=True)
        return len(self.solutions) >= self.max_solutions

    def run(self):
        t0 = time.time()
        found = self.dfs(RelSpace(self.m), [])
        self.time = time.time() - t0
        return found


def d_of(A):
    A = list(A)
    def dissoc(Bs):
        sums = set()
        for mask in range(1 << len(Bs)):
            s = sum(Bs[i] for i in range(len(Bs)) if mask >> i & 1)
            if s in sums: return False
            sums.add(s)
        return True
    for size in range(len(A), 0, -1):
        for Bs in itertools.combinations(A, size):
            if dissoc(Bs): return size
    return 0


if __name__ == "__main__":
    k = int(sys.argv[1]); m = int(sys.argv[2])
    maxsol = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    E = EngineB(m, k, max_solutions=maxsol, verbose=True)
    print(f"[B] k={k} m={m}: {len(E.pats)} relation patterns: {E.pats}")
    found = E.run()
    print(f"[B] nodes={E.nodes} leaves={E.leaves} pruned_lp={E.pruned_lp} stats={E.stats} time={E.time:.2f}s")
    if found:
        for chosen, basis, w in E.solutions:
            print("[B] SOLUTION witness", w, "d(witness) =", d_of(w))
        print(f"[B] RESULT: there IS a set of {m} distinct positive reals with no dissociated {k}-subset => g({m}) <= {k-1}")
    else:
        print(f"[B] RESULT: every set of {m} distinct positive reals has a dissociated {k}-subset => g({m}) >= {k}")
