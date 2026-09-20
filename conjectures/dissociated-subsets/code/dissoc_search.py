#!/usr/bin/env python3
"""Engine A: exact search for sets of m distinct positive reals with no dissociated k-subset.

A set B of reals is dissociated iff all 2^|B| subset sums are distinct, i.e. iff no
nonzero eps in {-1,0,1}^B has sum eps_b b = 0.

We look for a point a = (a_1 < a_2 < ... < a_m), all a_i > 0, such that EVERY k-subset
carries at least one relation  sum eps_i a_i = 0.  The set of relations a sorted
positive k-subset can carry is finite (sign patterns feasible on the open cone); for
k = 4 it is exactly six, for k = 5 exactly 26 (the generator uses an exact test).

Search: depth-first over the hyperplane arrangement.  State = a rational linear
subspace S of R^m (all relations chosen so far), kept as an integer basis matrix.
  * A k-subset Q is BLOCKED on S if one of its relations vanishes identically on S.
  * If every Q is blocked: S is a leaf; decide exactly (Fourier-Motzkin over Q) whether
    S meets the open cone {0 < a_1 < ... < a_m}.  If yes: counterexample family found.
  * Otherwise pick an unblocked Q (fail-first) and branch on its relations r:
    S' = S ∩ r^perp (dimension drops by exactly one since r does not vanish on S).
    Children on which some a_i = 0 or a_i = a_j is forced are pruned (no valid point).
Soundness: any valid point in S lies on one of Q's relations, hence in one child.
Exact integer/rational arithmetic throughout.  Optionally writes a JSON certificate
(the case tree with a Gordan multiplier vector at every infeasible leaf) for checker.py.
"""
import sys, itertools, time, json
from fractions import Fraction
from math import gcd

# ---------------------------------------------------------------- exact FM feasibility
def fm_certificate(rows):
    """rows: list of tuples (Fractions/ints), strict system row . y > 0 for every row.
    Returns None if feasible; otherwise a Gordan certificate lambda (list of nonnegative
    Fractions, not all zero) with sum_i lambda_i * row_i == 0."""
    n = len(rows)
    if n == 0:
        return None
    nvar = len(rows[0])
    # augment every row with its multiplier vector over the original rows
    cur = []
    for i, r in enumerate(rows):
        mult = [Fraction(0)] * n; mult[i] = Fraction(1)
        cur.append((tuple(Fraction(x) for x in r), mult))
    for v in range(nvar):
        P, N, Z = [], [], []
        for r, mu in cur:
            c = r[v]
            if c > 0: P.append((r, mu))
            elif c < 0: N.append((r, mu))
            else: Z.append((r, mu))
        new = list(Z)
        for p, mp in P:
            for q, mq in N:
                a, b = -q[v], p[v]           # both > 0
                comb = tuple(a * p[i] + b * q[i] for i in range(nvar))
                mult = [a * x + b * y for x, y in zip(mp, mq)]
                new.append((comb, mult))
        for r, mu in new:
            if all(x == 0 for x in r):
                return mu
        cur = new
        if not cur:
            return None
        seen = set(); ded = []
        for r, mu in cur:
            piv = next(x for x in r if x != 0)
            key = tuple(x / abs(piv) for x in r)
            if key not in seen:
                seen.add(key); ded.append((r, mu))
        cur = ded
    return None

def fm_feasible(rows):
    return fm_certificate(rows) is None


# ---------------------------------------------------------------- relation generation
def relations_for_pattern(k):
    """All sign patterns eps in {-1,0,1}^k (first nonzero = +1) such that
    sum eps_i a_i = 0 is feasible for some 0 < a_1 < ... < a_k."""
    pats = []
    for eps in itertools.product((-1, 0, 1), repeat=k):
        if all(e == 0 for e in eps):
            continue
        first = next(e for e in eps if e != 0)
        if first != 1:
            continue
        j = next(i for i, e in enumerate(eps) if e != 0)
        idx = [i for i in range(k) if i != j]
        def restrict(row):
            return tuple(Fraction(row[i]) - Fraction(row[j]) * Fraction(eps[i], eps[j]) for i in idx)
        rows = []
        e = [0] * k; e[0] = 1; rows.append(restrict(e))
        for i in range(k - 1):
            e = [0] * k; e[i + 1] = 1; e[i] = -1; rows.append(restrict(e))
        if fm_feasible(rows):
            pats.append(eps)
    return pats


# ---------------------------------------------------------------- integer basis utilities
def vec_gcd_normalise(v):
    g = 0
    for x in v:
        g = gcd(g, abs(x))
    if g > 1:
        v = [x // g for x in v]
    return v

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def intersect(basis, r):
    """basis: list of integer vectors spanning S. r: integer relation vector not vanishing
    on S. Returns integer basis of S ∩ r^perp."""
    vals = [dot(r, s) for s in basis]
    p = next(i for i, x in enumerate(vals) if x != 0)
    s0, v0 = basis[p], vals[p]
    new = []
    for i, s in enumerate(basis):
        if i == p:
            continue
        w = [v0 * a - vals[i] * b for a, b in zip(s, s0)]
        new.append(vec_gcd_normalise(w))
    return new


class Searcher:
    def __init__(self, m, k, verbose=False, max_solutions=1, certificate=False):
        self.m, self.k = m, k
        self.pats = relations_for_pattern(k)
        self.subsets = list(itertools.combinations(range(m), k))
        self.rels = []
        for Q in self.subsets:
            lst = []
            for eps in self.pats:
                v = [0] * m
                for e, i in zip(eps, Q):
                    v[i] = e
                lst.append(tuple(v))
            self.rels.append(lst)
        self.forbid = []
        for i in range(m):
            v = [0] * m; v[i] = 1; self.forbid.append(tuple(v))
        for i in range(m):
            for j in range(i + 1, m):
                v = [0] * m; v[i] = 1; v[j] = -1; self.forbid.append(tuple(v))
        self.nodes = 0; self.leaves = 0; self.pruned_forced = 0; self.leaves_infeasible = 0
        self.solutions = []
        self.verbose = verbose
        self.max_solutions = max_solutions
        self.certificate = certificate

    def vanishes(self, r, basis):
        return all(dot(r, s) == 0 for s in basis)

    def cone_rows(self, basis):
        d = len(basis)
        rows = [tuple(basis[t][0] for t in range(d))]
        for i in range(self.m - 1):
            rows.append(tuple(basis[t][i + 1] - basis[t][i] for t in range(d)))
        return rows

    def witness(self, basis):
        import numpy as np
        from scipy.optimize import linprog
        d = len(basis)
        rows = self.cone_rows(basis)
        c = [0] * d + [-1]
        A_ub = []; b_ub = []
        for r in rows:
            A_ub.append([-float(x) for x in r] + [1.0]); b_ub.append(0.0)
        bounds = [(-1, 1)] * d + [(0, None)]
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if res.status != 0:
            return None
        y = res.x[:d]
        for den in (10, 100, 1000, 10**4, 10**6, 10**9):
            yq = [Fraction(v).limit_denominator(den) for v in y]
            a = [sum(yq[t] * basis[t][i] for t in range(d)) for i in range(self.m)]
            if a[0] > 0 and all(a[i + 1] > a[i] for i in range(self.m - 1)):
                L = 1
                for x in a:
                    L = L * x.denominator // gcd(L, x.denominator)
                return [int(x * L) for x in a]
        return None

    def dfs(self, basis, chosen):
        """returns (stop, certnode)"""
        self.nodes += 1
        unblocked = [qi for qi, lst in enumerate(self.rels)
                     if not any(self.vanishes(r, basis) for r in lst)]
        if not unblocked:
            self.leaves += 1
            lam = fm_certificate(self.cone_rows(basis))
            if lam is None:
                w = self.witness(basis)
                assert w is not None, "feasible leaf but no rational witness found"
                self.solutions.append((list(chosen), [list(b) for b in basis], w))
                if self.verbose:
                    print("  FOUND family dim", len(basis), "witness", w, flush=True)
                node = {"Q": None, "leaf": {"feasible": True, "witness": w}} if self.certificate else None
                return len(self.solutions) >= self.max_solutions, node
            self.leaves_infeasible += 1
            node = {"Q": None, "leaf": {"feasible": False, "gordan": [str(x) for x in lam]}} if self.certificate else None
            return False, node
        best = None
        for qi in unblocked:
            children = []
            for r in self.rels[qi]:
                nb = intersect(basis, r)
                forced = None
                if not nb:
                    forced = "dim0"
                else:
                    for fv in self.forbid:
                        if self.vanishes(fv, nb):
                            forced = fv; break
                children.append((r, nb, forced))
            live = sum(1 for _, _, f in children if f is None)
            if best is None or live < best[2]:
                best = (qi, children, live)
                if live == 0:
                    break
        qi, children, live = best
        self.pruned_forced += len(children) - live
        certchildren = []
        stop = False
        for r, nb, forced in children:
            if forced is not None:
                if self.certificate:
                    certchildren.append({"r": list(r), "type": "pruned",
                                         "why": {"forced": list(forced) if forced != "dim0" else "dim0"}})
                continue
            chosen.append((self.subsets[qi], r))
            stop, sub = self.dfs(nb, chosen)
            chosen.pop()
            if self.certificate:
                certchildren.append({"r": list(r), "type": "child", "node": sub})
            if stop:
                break
        node = {"Q": list(self.subsets[qi]), "children": certchildren} if self.certificate else None
        return stop, node

    def run(self):
        t0 = time.time()
        basis = []
        for i in range(self.m):
            v = [0] * self.m; v[i] = 1; basis.append(v)
        found, root = self.dfs(basis, [])
        self.time = time.time() - t0
        self.root = root
        return found

    def write_certificate(self, path):
        doc = {"engine": "A", "k": self.k, "m": self.m, "patterns": [list(p) for p in self.pats],
               "nodes": self.nodes, "complete": len(self.solutions) < self.max_solutions or not self.solutions,
               "root": self.root}
        with open(path, "w") as f:
            json.dump(doc, f)


def check_dissociated(B):
    sums = set()
    for mask in range(1 << len(B)):
        s = sum(B[i] for i in range(len(B)) if mask >> i & 1)
        if s in sums:
            return False
        sums.add(s)
    return True

def d_of(A):
    A = list(A)
    for size in range(len(A), 0, -1):
        for B in itertools.combinations(A, size):
            if check_dissociated(B):
                return size
    return 0


if __name__ == "__main__":
    k = int(sys.argv[1]); m = int(sys.argv[2])
    maxsol = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    certpath = sys.argv[4] if len(sys.argv) > 4 else None
    S = Searcher(m, k, verbose=True, max_solutions=maxsol, certificate=certpath is not None)
    print(f"k={k} m={m}: {len(S.pats)} feasible relation patterns per sorted {k}-subset: {S.pats}")
    found = S.run()
    print(f"nodes={S.nodes} leaves={S.leaves} leaves_infeasible={S.leaves_infeasible} "
          f"pruned_forced_children={S.pruned_forced} time={S.time:.2f}s")
    if certpath:
        S.write_certificate(certpath)
        print("certificate written to", certpath)
    if found:
        for chosen, basis, w in S.solutions:
            print("SOLUTION family: basis", basis, "witness", w, "d(witness) =", d_of(w) if w else None)
        print(f"RESULT: there IS a set of {m} distinct positive reals with no dissociated {k}-subset  => g({m}) <= {k-1}")
    else:
        print(f"RESULT: every set of {m} distinct positive reals has a dissociated {k}-subset  => g({m}) >= {k}")
