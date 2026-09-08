#!/usr/bin/env python3
"""Engine D: exact search for m-sets of distinct positive reals with no dissociated
k-subset (k = 5 in practice), using the DISSOCIATION CASE SPLIT.

Key fact.  If Q is a dissociated (k-1)-subset of the point a and x is any other
coordinate, then Q ∪ {x} is not dissociated, and the relation it carries must involve x
(a relation inside Q is impossible).  So x is a signed sum of Q.  Hence, once one
(k-1)-subset is known to be dissociated, every other coordinate is cut down to at most
3^(k-1)-1 sign patterns and the subspace dimension collapses to k-1.

Search tree.  State = (integer basis of a subspace S ⊂ R^m, set `dis` of (k-1)-subsets
assumed dissociated).  Node types:
  * SPLIT on a (k-1)-subset Q ∉ dis: children = the feasible relations of Q (each cuts S)
    and one "dis" child (Q assumed dissociated).  Exhaustive: at any valid point either
    some relation of Q holds or Q is dissociated.
  * BRANCH on a k-subset U: children = the allowed patterns of U (all feasible patterns,
    minus those supported inside some Q ∈ dis with Q ⊂ U).  Exhaustive for points at which
    every Q ∈ dis is dissociated.
  * PRUNE: a child on which some coordinate is forced to 0 or two coordinates are forced
    equal; a child certified infeasible (Gordan multipliers); a node on which a relation of
    some Q ∈ dis holds identically (no point of this branch has Q dissociated).
  * LEAF: every k-subset blocked (by an allowed pattern) and S ∩ open cone ≠ ∅:
    every point of S ∩ cone has no dissociated k-subset -> witness.  Or infeasible.
Certificates: JSON DAG (same conventions as engine C) with the extra node type "split".
"""
import sys, itertools, time, json
from fractions import Fraction
from math import gcd
import numpy as np
from scipy.optimize import linprog

from dissoc_engineC import fm_certificate, patterns, normalise, intersect


class EngineD:
    def __init__(self, m, k, max_solutions=1, scan=16, certificate=False, verbose=False, split_range=None):
        self.m, self.k = m, k
        self.pats = patterns(k)                 # k-patterns (26 for k=5)
        self.subpats = patterns(k - 1)          # (k-1)-patterns (6 for k=4)
        self.P = len(self.pats)
        subs = list(itertools.combinations(range(m), k))
        subs.sort(key=lambda Q: (Q[-1], Q))
        self.subsets = subs
        self.sub_index = {Q: i for i, Q in enumerate(subs)}
        R = np.zeros((len(subs) * self.P, m), dtype=np.int64)
        for qi, Q in enumerate(subs):
            for pi, eps in enumerate(self.pats):
                for e, i in zip(eps, Q):
                    R[qi * self.P + pi, i] = e
        self.R = R
        # (k-1)-subsets that may be split on: by default those inside the first 2k-1... use split_range
        self.split_range = split_range if split_range is not None else m
        self.qsubsets = list(itertools.combinations(range(self.split_range), k - 1))
        self.qrels = {}
        for Q in self.qsubsets:
            lst = []
            for eps in self.subpats:
                v = [0] * m
                for e, i in zip(eps, Q):
                    v[i] = e
                lst.append(tuple(v))
            self.qrels[Q] = lst
        # pattern support masks: for pattern pi and subset position j, is eps_j nonzero
        self.pat_nz = np.array([[e != 0 for e in eps] for eps in self.pats])   # (P, k)
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
        self.pruned_forced = 0; self.pruned_lp = 0; self.pruned_dis = 0; self.lp_unverified = 0
        self.splits = 0; self.branches = 0
        self.solutions = []
        self.memo = {}; self.next_id = 0; self.memo_hits = 0

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def canonical(basis):
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

    def lp(self, C):
        d = len(C[0])
        Mf = np.array(C, dtype=float)
        c = np.zeros(d + 1); c[-1] = -1.0
        A_ub = np.hstack([-Mf, np.ones((self.m, 1))]); b_ub = np.zeros(self.m)
        return linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(-1, 1)] * d + [(0, 1)], method="highs")

    def prune_child(self, basis):
        C = self.cone_rows(basis)
        res = self.lp(C)
        if res.status == 0 and -res.fun > 1e-9:
            return None
        if res.status == 0:
            lam = [-float(v) for v in res.ineqlin.marginals]
            for den in (8, 64, 1024, 10**5, 10**8):
                lq = [max(Fraction(v).limit_denominator(den), Fraction(0)) for v in lam]
                if self.gordan_ok(C, lq):
                    return lq
        self.lp_unverified += 1
        return fm_certificate(C)

    def witness(self, basis, avoid):
        """rational point of S ∩ open cone avoiding the hyperplanes in `avoid` (relation vectors)."""
        C = self.cone_rows(basis)
        d = len(C[0])
        res = self.lp(C)
        y0 = res.x[:d]
        rng = np.random.default_rng(12345)
        for trial in range(200):
            y = y0 if trial == 0 else y0 + rng.normal(scale=0.05 * (-res.fun), size=d)
            for den in (8, 64, 1024, 10**5, 10**8):
                yq = [Fraction(v).limit_denominator(den) for v in y]
                a = [sum(yq[t] * int(basis[t][i]) for t in range(d)) for i in range(self.m)]
                if a[0] > 0 and all(a[i + 1] > a[i] for i in range(self.m - 1)) and \
                   all(sum(int(r[i]) * a[i] for i in range(self.m)) != 0 for r in avoid):
                    L = 1
                    for x in a:
                        L = L * x.denominator // gcd(L, x.denominator)
                    return [int(x * L) for x in a]
        return None

    def forced(self, nb):
        if not nb:
            return "dim0"
        NB = np.array(nb, dtype=np.int64)
        z = ~np.any(self.F @ NB.T, axis=1)
        if z.any():
            return [int(x) for x in self.F[int(np.flatnonzero(z)[0])]]
        return None

    # ---------------------------------------------------------------- search
    def allowed_mask(self, dis):
        """boolean (nsub, P): pattern allowed for subset (not supported inside a dis Q ⊂ U)."""
        allowed = np.ones((len(self.subsets), self.P), dtype=bool)
        for Q in dis:
            Qs = set(Q)
            for x in range(self.m):
                if x in Qs:
                    continue
                U = tuple(sorted(Qs | {x}))
                ui = self.sub_index[U]
                pos = U.index(x)
                allowed[ui] &= self.pat_nz[:, pos]     # must involve x
        return allowed

    def dfs(self, basis, dis):
        key = (self.canonical(basis), dis)
        if key in self.memo:
            self.memo_hits += 1
            return False, ({"ref": self.memo[key]} if self.certificate else None)
        my_id = self.next_id; self.next_id += 1
        stop, node = self.body(basis, dis, my_id)
        if not stop:
            self.memo[key] = my_id
        return stop, node

    def body(self, basis, dis, my_id):
        self.nodes += 1
        B = np.array(basis, dtype=np.int64)
        assert np.abs(B).max() < 2**40
        # consistency: no relation of a dis Q may hold identically
        for Q in dis:
            for r in self.qrels[Q]:
                if not np.any(B @ np.array(r, dtype=np.int64)):
                    self.pruned_dis += 1
                    return False, ({"id": my_id, "Q": None, "leaf": {"feasible": False, "dis_violated": {"Q": list(Q), "r": list(r)}}} if self.certificate else None)
        prod = self.R @ B.T
        zero = ~np.any(prod, axis=1)
        allowed = self.allowed_mask(dis)
        blocked = (zero.reshape(-1, self.P) & allowed).any(axis=1)
        unblocked = np.flatnonzero(~blocked)
        if len(unblocked) == 0:
            self.leaves += 1
            lam = fm_certificate(self.cone_rows(basis))
            if lam is None:
                avoid = [r for Q in dis for r in self.qrels[Q]]
                w = self.witness(basis, avoid)
                assert w is not None, "feasible leaf without rational witness"
                self.solutions.append(w)
                if self.verbose:
                    print("  FOUND family dim", len(basis), "dis", dis, "witness", w, flush=True)
                return len(self.solutions) >= self.max_solutions, ({"id": my_id, "Q": None, "leaf": {"feasible": True, "witness": w}} if self.certificate else None)
            self.leaves_infeasible += 1
            return False, ({"id": my_id, "Q": None, "leaf": {"feasible": False, "gordan": [str(x) for x in lam]}} if self.certificate else None)

        # ---- choose: SPLIT on a (k-1)-subset if no dis yet, else BRANCH on a k-subset
        if not dis:
            # split on the (k-1)-subset with fewest live relation-children among the first `scan`
            # candidates that are not already carrying a relation identically
            best = None
            for Q in self.qsubsets:
                rels = self.qrels[Q]
                if any(not np.any(B @ np.array(r, dtype=np.int64)) for r in rels):
                    continue   # Q already non-dissociated on S: splitting is pointless
                children = []
                for r in rels:
                    nb = intersect(basis, r)
                    children.append((r, nb, self.forced(nb)))
                live = sum(1 for _, _, f in children if f is None)
                if best is None or live < best[2]:
                    best = (Q, children, live)
                    if live == 0:
                        break
                if best is not None and len([1 for Q2 in self.qsubsets]) and False:
                    pass
            assert best is not None
            Q, children, live = best
            self.splits += 1
            cert = []
            stop = False
            for r, nb, f in children:
                if f is not None:
                    self.pruned_forced += 1
                    if self.certificate:
                        cert.append({"r": list(r), "type": "pruned", "why": {"forced": f}})
                    continue
                lam = self.prune_child(nb)
                if lam is not None:
                    self.pruned_lp += 1
                    if self.certificate:
                        cert.append({"r": list(r), "type": "pruned", "why": {"gordan": [str(x) for x in lam]}})
                    continue
                stop, sub = self.dfs(nb, dis)
                if self.certificate:
                    cert.append({"r": list(r), "type": "child", "node": sub})
                if stop:
                    break
            if not stop:
                stop, sub = self.dfs(basis, dis + (Q,))
                if self.certificate:
                    cert.append({"type": "dis", "node": sub})
            return stop, ({"id": my_id, "split": list(Q), "children": cert} if self.certificate else None)

        # BRANCH on an unblocked k-subset (fail-first among the first `scan` in prefix order,
        # preferring subsets that contain a dis Q)
        cand = list(unblocked[: self.scan])
        best = None
        for ui in cand:
            U = self.subsets[ui]
            children = []
            for pi in range(self.P):
                if not allowed[ui, pi]:
                    continue
                r = self.R[ui * self.P + pi]
                nb = intersect(basis, r)
                children.append((r, nb, self.forced(nb)))
            live = sum(1 for _, _, f in children if f is None)
            if best is None or live < best[2]:
                best = (int(ui), children, live)
                if live == 0:
                    break
        ui, children, live = best
        self.branches += 1
        cert = []
        stop = False
        for r, nb, f in children:
            if f is not None:
                self.pruned_forced += 1
                if self.certificate:
                    cert.append({"r": [int(x) for x in r], "type": "pruned", "why": {"forced": f}})
                continue
            lam = self.prune_child(nb)
            if lam is not None:
                self.pruned_lp += 1
                if self.certificate:
                    cert.append({"r": [int(x) for x in r], "type": "pruned", "why": {"gordan": [str(x) for x in lam]}})
                continue
            stop, sub = self.dfs(nb, dis)
            if self.certificate:
                cert.append({"r": [int(x) for x in r], "type": "child", "node": sub})
            if stop:
                break
        return stop, ({"id": my_id, "Q": list(self.subsets[ui]), "dis": [list(Q) for Q in dis], "children": cert} if self.certificate else None)

    def run(self):
        t0 = time.time()
        basis = [[1 if i == j else 0 for j in range(self.m)] for i in range(self.m)]
        found, root = self.dfs(basis, ())
        self.time = time.time() - t0
        self.root = root
        return found

    def write_certificate(self, path):
        doc = {"engine": "D", "k": self.k, "m": self.m, "patterns": [list(p) for p in self.pats],
               "subpatterns": [list(p) for p in self.subpats], "split_range": self.split_range,
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
    scan = int(sys.argv[5]) if len(sys.argv) > 5 else 16
    split_range = int(sys.argv[6]) if len(sys.argv) > 6 else min(m, 2 * k - 3)
    E = EngineD(m, k, max_solutions=maxsol, scan=scan, certificate=certpath is not None, verbose=True, split_range=split_range)
    print(f"[D] k={k} m={m}: {E.P} patterns, {len(E.subpats)} sub-patterns; scan={scan} split_range={split_range}", flush=True)
    found = E.run()
    print(f"[D] nodes={E.nodes} splits={E.splits} branches={E.branches} leaves={E.leaves} leaves_infeasible={E.leaves_infeasible} "
          f"pruned_forced={E.pruned_forced} pruned_lp={E.pruned_lp} pruned_dis={E.pruned_dis} lp_unverified={E.lp_unverified} "
          f"memo_hits={E.memo_hits} time={E.time:.2f}s", flush=True)
    if certpath:
        E.write_certificate(certpath); print("[D] certificate written to", certpath)
    if found:
        for w in E.solutions:
            print("[D] SOLUTION witness", w, "d(witness) =", d_of(w))
        print(f"[D] RESULT: there IS a set of {m} distinct positive reals with no dissociated {k}-subset => g({m}) <= {k-1}")
    else:
        print(f"[D] RESULT: every set of {m} distinct positive reals has a dissociated {k}-subset => g({m}) >= {k}")
