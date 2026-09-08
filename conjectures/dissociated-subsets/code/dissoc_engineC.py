#!/usr/bin/env python3
"""Engine C: fail-first branching (as engine A) + certified LP pruning at every child
(as engine B), vectorised blocking tests.  Same problem, same certificate format.

State: integer basis (rows) of the subspace S of R^m cut out by the chosen relations.
Node: relations matrix R (all patterns of all k-subsets) times basis^T -> blocked flags.
Branch: among the first `scan` unblocked subsets in prefix order, the one with the fewest
children surviving the cheap forced-equality test; each surviving child is then tested by
a float LP whose "infeasible" verdict is accepted only with an exactly verified Gordan
multiplier vector (else exact Fourier-Motzkin decides).  Leaves: exact FM certificate.
"""
import sys, itertools, time, json
from fractions import Fraction
from math import gcd
import numpy as np
from scipy.optimize import linprog

# --- exact FM with multiplier tracking (independent copy; small) -------------------
def fm_certificate(rows):
    n = len(rows)
    if n == 0:
        return None
    nvar = len(rows[0])
    cur = []
    for i, r in enumerate(rows):
        mult = [Fraction(0)] * n; mult[i] = Fraction(1)
        cur.append((tuple(Fraction(x) for x in r), mult))
    for v in range(nvar):
        P, N, Z = [], [], []
        for r, mu in cur:
            c = r[v]
            (P if c > 0 else N if c < 0 else Z).append((r, mu))
        new = list(Z)
        for p, mp in P:
            for q, mq in N:
                a, b = -q[v], p[v]
                new.append((tuple(a * p[i] + b * q[i] for i in range(nvar)),
                            [a * x + b * y for x, y in zip(mp, mq)]))
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

def patterns(k):
    pats = []
    for eps in itertools.product((-1, 0, 1), repeat=k):
        nz = [e for e in eps if e != 0]
        if not nz or nz[0] != 1:
            continue
        j = next(i for i, e in enumerate(eps) if e != 0)
        idx = [i for i in range(k) if i != j]
        def restrict(row):
            return tuple(Fraction(row[i]) - Fraction(row[j]) * Fraction(eps[i], eps[j]) for i in idx)
        rows = []
        e = [0] * k; e[0] = 1; rows.append(restrict(e))
        for i in range(k - 1):
            e = [0] * k; e[i + 1] = 1; e[i] = -1; rows.append(restrict(e))
        if fm_certificate(rows) is None:
            pats.append(eps)
    return pats

def normalise(v):
    g = 0
    for x in v:
        g = gcd(g, int(abs(x)))
    if g > 1:
        v = [int(x) // g for x in v]
    return [int(x) for x in v]

def intersect(basis, r):
    vals = [int(np.dot(r, s)) for s in basis]
    p = next(i for i, x in enumerate(vals) if x != 0)
    s0, v0 = basis[p], vals[p]
    new = []
    for i, s in enumerate(basis):
        if i == p:
            continue
        new.append(normalise([v0 * int(a) - vals[i] * int(b) for a, b in zip(s, s0)]))
    return new


class EngineC:
    def __init__(self, m, k, max_solutions=1, scan=24, certificate=False, verbose=False):
        self.m, self.k = m, k
        self.pats = patterns(k)
        self.P = len(self.pats)
        subs = list(itertools.combinations(range(m), k))
        subs.sort(key=lambda Q: (Q[-1], Q))
        self.subsets = subs
        R = np.zeros((len(subs) * self.P, m), dtype=np.int64)
        for qi, Q in enumerate(subs):
            for pi, eps in enumerate(self.pats):
                for e, i in zip(eps, Q):
                    R[qi * self.P + pi, i] = e
        self.R = R
        F = []
        for i in range(m):
            v = [0] * m; v[i] = 1; F.append(v)
        for i in range(m):
            for j in range(i + 1, m):
                v = [0] * m; v[i] = 1; v[j] = -1; F.append(v)
        self.F = np.array(F, dtype=np.int64)
        self.cone = np.zeros((m, m), dtype=np.int64)
        self.cone[0, 0] = 1
        for i in range(m - 1):
            self.cone[i + 1, i + 1] = 1; self.cone[i + 1, i] = -1
        self.scan = scan
        self.max_solutions = max_solutions
        self.certificate = certificate
        self.verbose = verbose
        self.nodes = 0; self.leaves = 0; self.leaves_infeasible = 0
        self.pruned_forced = 0; self.pruned_lp = 0; self.lp_unverified = 0; self.fm_calls = 0
        self.solutions = []
        self.memo = {}          # canonical subspace key -> node id (subtree fully explored, no solution)
        self.next_id = 0
        self.memo_hits = 0

    @staticmethod
    def canonical(basis):
        """RREF of the basis rows over Q -> hashable canonical form of the subspace."""
        rows = []
        for v in basis:
            v = [Fraction(int(x)) for x in v]
            for p, r in rows:
                if v[p] != 0:
                    c = v[p]; v = [a - c * b for a, b in zip(v, r)]
            nz = [i for i, x in enumerate(v) if x != 0]
            if not nz:
                continue
            p = nz[0]; v = [x / v[p] for x in v]
            rows = [(q, [a - r[p] * b for a, b in zip(r, v)] if r[p] != 0 else r) for q, r in rows]
            rows.append((p, v)); rows.sort()
        return tuple((p, tuple(r)) for p, r in rows)

    # ----- exact feasibility of S ∩ open cone, S given by integer basis
    def cone_rows(self, basis):
        B = np.array(basis, dtype=object)
        C = []
        for i in range(self.m):
            C.append(tuple(int(sum(int(self.cone[i, j]) * int(B[t, j]) for j in range(self.m))) for t in range(len(basis))))
        return C

    def gordan_ok(self, C, lam):
        if any(x < 0 for x in lam) or all(x == 0 for x in lam):
            return False
        d = len(C[0])
        return all(sum(lam[i] * C[i][t] for i in range(len(C))) == 0 for t in range(d))

    def prune_child(self, basis):
        """returns None if (LP says) feasible, else an exact Gordan certificate."""
        C = self.cone_rows(basis)
        d = len(C[0])
        Mf = np.array(C, dtype=float)
        c = np.zeros(d + 1); c[-1] = -1.0
        A_ub = np.hstack([-Mf, np.ones((self.m, 1))]); b_ub = np.zeros(self.m)
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(-1, 1)] * d + [(0, 1)], method="highs")
        if res.status == 0 and -res.fun > 1e-9:
            return None
        if res.status == 0:
            lam = [-float(v) for v in res.ineqlin.marginals]
            for den in (8, 64, 1024, 10**5, 10**8):
                lq = [max(Fraction(v).limit_denominator(den), Fraction(0)) for v in lam]
                if self.gordan_ok(C, lq):
                    return lq
        self.lp_unverified += 1
        self.fm_calls += 1
        return fm_certificate(C)

    def witness(self, basis):
        C = self.cone_rows(basis)
        d = len(C[0])
        Mf = np.array(C, dtype=float)
        c = np.zeros(d + 1); c[-1] = -1.0
        A_ub = np.hstack([-Mf, np.ones((self.m, 1))]); b_ub = np.zeros(self.m)
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(-1, 1)] * d + [(0, 1)], method="highs")
        y = res.x[:d]
        for den in (8, 64, 1024, 10**5, 10**8):
            yq = [Fraction(v).limit_denominator(den) for v in y]
            a = [sum(yq[t] * int(basis[t][i]) for t in range(d)) for i in range(self.m)]
            if a[0] > 0 and all(a[i + 1] > a[i] for i in range(self.m - 1)):
                L = 1
                for x in a:
                    L = L * x.denominator // gcd(L, x.denominator)
                return [int(x * L) for x in a]
        return None

    def dfs(self, basis):
        key = self.canonical(basis)
        if key in self.memo:
            self.memo_hits += 1
            return False, ({"ref": self.memo[key]} if self.certificate else None)
        my_id = self.next_id; self.next_id += 1
        stop, node = self.dfs_body(basis, my_id)
        if not stop:
            self.memo[key] = my_id
        return stop, node

    def dfs_body(self, basis, my_id):
        self.nodes += 1
        B = np.array(basis, dtype=np.int64)
        assert np.abs(B).max() < 2**40, "basis entries too large for int64 safety"
        prod = self.R @ B.T                       # (nsub*P, d)
        zero = ~np.any(prod, axis=1)              # relation vanishes on S
        blocked = zero.reshape(-1, self.P).any(axis=1)
        unblocked = np.flatnonzero(~blocked)
        if len(unblocked) == 0:
            self.leaves += 1
            lam = fm_certificate(self.cone_rows(basis)); self.fm_calls += 1
            if lam is None:
                w = self.witness(basis)
                assert w is not None
                self.solutions.append(w)
                if self.verbose:
                    print("  FOUND family dim", len(basis), "witness", w, flush=True)
                return len(self.solutions) >= self.max_solutions, ({"id": my_id, "Q": None, "leaf": {"feasible": True, "witness": w}} if self.certificate else None)
            self.leaves_infeasible += 1
            return False, ({"id": my_id, "Q": None, "leaf": {"feasible": False, "gordan": [str(x) for x in lam]}} if self.certificate else None)
        best = None
        for qi in unblocked[: self.scan]:
            children = []
            for pi in range(self.P):
                r = self.R[qi * self.P + pi]
                nb = intersect(basis, r)
                forced = None
                if not nb:
                    forced = "dim0"
                else:
                    NB = np.array(nb, dtype=np.int64)
                    z = ~np.any(self.F @ NB.T, axis=1)
                    if z.any():
                        forced = [int(x) for x in self.F[int(np.flatnonzero(z)[0])]]
                children.append((r, nb, forced))
            live = sum(1 for _, _, f in children if f is None)
            if best is None or live < best[2]:
                best = (int(qi), children, live)
                if live == 0:
                    break
        qi, children, live = best
        self.pruned_forced += len(children) - live
        cert = []
        stop = False
        for r, nb, forced in children:
            if forced is not None:
                if self.certificate:
                    cert.append({"r": [int(x) for x in r], "type": "pruned", "why": {"forced": forced}})
                continue
            lam = self.prune_child(nb)
            if lam is not None:
                self.pruned_lp += 1
                if self.certificate:
                    cert.append({"r": [int(x) for x in r], "type": "pruned", "why": {"gordan": [str(x) for x in lam]}})
                continue
            stop, sub = self.dfs(nb)
            if self.certificate:
                cert.append({"r": [int(x) for x in r], "type": "child", "node": sub})
            if stop:
                break
        return stop, ({"id": my_id, "Q": list(self.subsets[qi]), "children": cert} if self.certificate else None)

    def run(self):
        t0 = time.time()
        basis = [[1 if i == j else 0 for j in range(self.m)] for i in range(self.m)]
        found, root = self.dfs(basis)
        self.time = time.time() - t0
        self.root = root
        return found

    def write_certificate(self, path):
        doc = {"engine": "C", "k": self.k, "m": self.m, "patterns": [list(p) for p in self.pats],
               "nodes": self.nodes, "complete": not self.solutions, "root": self.root}
        with open(path, "w") as f:
            json.dump(doc, f)


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
    certpath = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "-" else None
    scan = int(sys.argv[5]) if len(sys.argv) > 5 else 24
    E = EngineC(m, k, max_solutions=maxsol, scan=scan, certificate=certpath is not None, verbose=True)
    print(f"[C] k={k} m={m}: {E.P} patterns; scan={scan}", flush=True)
    found = E.run()
    print(f"[C] nodes={E.nodes} leaves={E.leaves} leaves_infeasible={E.leaves_infeasible} pruned_forced={E.pruned_forced} "
          f"pruned_lp={E.pruned_lp} lp_unverified={E.lp_unverified} fm_calls={E.fm_calls} memo_hits={E.memo_hits} time={E.time:.2f}s", flush=True)
    if certpath:
        E.write_certificate(certpath); print("[C] certificate written to", certpath)
    if found:
        for w in E.solutions:
            print("[C] SOLUTION witness", w, "d(witness) =", d_of(w))
        print(f"[C] RESULT: there IS a set of {m} distinct positive reals with no dissociated {k}-subset => g({m}) <= {k-1}")
    else:
        print(f"[C] RESULT: every set of {m} distinct positive reals has a dissociated {k}-subset => g({m}) >= {k}")
