#!/usr/bin/env python3
"""Independent checker for the case-tree certificates written by engines A and B.

Verifies, with exact rational arithmetic and no code shared with the engines, that the
tree proves:   "every set of m distinct positive reals contains a dissociated k-subset"
(when the tree has no feasible leaf), or exhibits explicit counterexamples (feasible
leaves with witnesses whose largest dissociated subset really has size < k).

What is checked at every node (relations along the path define the subspace S):
  * the pattern list in the certificate is exactly the set of sign patterns
    eps in {-1,0,1}^k, first nonzero +1, feasible on the open sorted cone
    (recomputed here by an exact LP certificate test) -- so the branching is exhaustive;
  * the branch subset Q has every pattern represented exactly once among its children;
  * a child pruned "forced": the given vector (a_i or a_i - a_j) lies in the span of the
    path relations plus the child relation -- so the child has no point with distinct
    positive coordinates; "dim0": the relations span all of Q^m;
  * a child pruned by LP or an infeasible leaf: a Gordan vector lambda >= 0, != 0, such
    that sum lambda_i c_i lies in the span of the relations, where the c_i are the cone
    rows a_1 and a_{i+1} - a_i; if no lambda is supplied the checker computes one itself
    (float LP, then exact rational verification; exact simplex as last resort);
  * a feasible leaf: the witness satisfies all path relations, is strictly increasing
    and positive, and its largest dissociated subset (brute force) has size < k.
"""
import sys, json, itertools
from fractions import Fraction

def rref(vectors, m):
    """exact RREF of the row space; returns list of (pivot, row)"""
    rows = []
    for v in vectors:
        v = [Fraction(x) for x in v]
        for p, r in rows:
            if v[p] != 0:
                c = v[p]; v = [a - c * b for a, b in zip(v, r)]
        nz = [i for i, x in enumerate(v) if x != 0]
        if not nz:
            continue
        p = nz[0]; v = [x / v[p] for x in v]
        rows = [(q, [a - r[p] * b for a, b in zip(r, v)] if r[p] != 0 else r) for q, r in rows]
        rows.append((p, v)); rows.sort()
    return rows

def in_span(rows, v):
    v = [Fraction(x) for x in v]
    for p, r in rows:
        if v[p] != 0:
            c = v[p]; v = [a - c * b for a, b in zip(v, r)]
    return all(x == 0 for x in v)

def kernel_basis(rows, m):
    pivs = [p for p, _ in rows]
    free = [j for j in range(m) if j not in pivs]
    B = []
    for f in free:
        vec = [Fraction(0)] * m; vec[f] = Fraction(1)
        for p, r in rows:
            vec[p] = -r[f]
        B.append(vec)
    return B

def cone_rows(m):
    C = []
    e = [0] * m; e[0] = 1; C.append(e)
    for i in range(m - 1):
        e = [0] * m; e[i + 1] = 1; e[i] = -1; C.append(e)
    return C

def gordan_ok(rows, lam, m):
    lam = [Fraction(x) for x in lam]
    if any(x < 0 for x in lam) or all(x == 0 for x in lam):
        return False
    C = cone_rows(m)
    comb = [sum(lam[i] * C[i][j] for i in range(len(C))) for j in range(m)]
    return in_span(rows, comb)

def find_gordan(rows, m, stats):
    """compute a Gordan certificate for infeasibility of S ∩ open cone, exactly verified;
    returns lambda or None (None means: feasible, or could not certify)."""
    import numpy as np
    from scipy.optimize import linprog
    B = kernel_basis(rows, m)
    d = len(B)
    if d == 0:
        # S = {0}: certificate lambda = e_1 (a_1 > 0 impossible): a_1 = 0 on S
        lam = [Fraction(0)] * m; lam[0] = Fraction(1)
        return lam if gordan_ok(rows, lam, m) else None
    C = cone_rows(m)
    M = [[sum(Fraction(C[i][j]) * B[t][j] for j in range(m)) for t in range(d)] for i in range(m)]
    Mf = np.array([[float(x) for x in r] for r in M])
    c = np.zeros(d + 1); c[-1] = -1.0
    A_ub = np.hstack([-Mf, np.ones((m, 1))]); b_ub = np.zeros(m)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(-1, 1)] * d + [(0, 1)], method="highs")
    if res.status == 0 and -res.fun <= 1e-9:
        lam = [-float(v) for v in res.ineqlin.marginals]
        for den in (8, 64, 1024, 10**5, 10**8):
            lq = [max(Fraction(v).limit_denominator(den), Fraction(0)) for v in lam]
            if gordan_ok(rows, lq, m):
                stats["gordan_computed"] += 1
                return lq
    stats["gordan_failed"] += 1
    return None

def exact_feasible(rows, m):
    from sympy import symbols, Rational
    from sympy.solvers.simplex import lpmax
    B = kernel_basis(rows, m); d = len(B)
    if d == 0:
        return False
    ys = symbols(f"y0:{d}"); t = symbols("t")
    C = cone_rows(m)
    cons = []
    for i in range(m):
        expr = sum(sum(Rational(C[i][j]) * Rational(B[t_][j].numerator, B[t_][j].denominator) for j in range(m)) * ys[t_] for t_ in range(d))
        cons.append(expr - t >= 0)
    for j in range(d):
        cons += [ys[j] <= 1, ys[j] >= -1]
    cons += [t <= 1, t >= 0]
    val, _ = lpmax(t, cons)
    return val > 0

def feasible_patterns(k, stats):
    pats = []
    for eps in itertools.product((-1, 0, 1), repeat=k):
        nz = [e for e in eps if e != 0]
        if not nz or nz[0] != 1:
            continue
        rows = rref([eps], k)
        lam = find_gordan(rows, k, stats)
        if lam is None:
            # not certified infeasible: decide exactly
            if exact_feasible(rows, k):
                pats.append(eps)
        # else infeasible: skip
    return pats

def dissociated(B):
    sums = set()
    for mask in range(1 << len(B)):
        s = sum(B[i] for i in range(len(B)) if mask >> i & 1)
        if s in sums: return False
        sums.add(s)
    return True

def largest_dissociated(A):
    for size in range(len(A), 0, -1):
        for B in itertools.combinations(A, size):
            if dissociated(B): return size
    return 0


class Checker:
    def __init__(self, doc):
        self.k = doc["k"]; self.m = doc["m"]
        self.stats = {"nodes": 0, "leaves_infeasible": 0, "leaves_feasible": 0, "pruned_forced": 0,
                      "pruned_gordan": 0, "gordan_computed": 0, "gordan_failed": 0, "exact_simplex": 0,
                      "witness_ok": 0}
        pats = feasible_patterns(self.k, self.stats)
        cert_pats = sorted(tuple(p) for p in doc["patterns"])
        assert sorted(pats) == cert_pats, f"pattern list mismatch: mine {sorted(pats)} vs cert {cert_pats}"
        self.pats = sorted(pats)
        self.subpats = sorted(feasible_patterns(self.k - 1, self.stats)) if self.k >= 3 else []
        if "subpatterns" in doc:
            assert sorted(tuple(p) for p in doc["subpatterns"]) == self.subpats, "sub-pattern list mismatch"
        self.root = doc["root"]
        self.complete = bool(doc.get("complete", True))
        self.counterexamples = []
        self.verified = {}

    def check(self):
        self.walk(self.root, [])
        return self.stats

    def rels_of(self, Q):
        out = []
        for eps in self.pats:
            v = [0] * self.m
            for e, i in zip(eps, Q):
                v[i] = e
            out.append(tuple(v))
        return out

    def infeasible_ok(self, rows, lam):
        if lam is not None and gordan_ok(rows, lam, self.m):
            return True
        lam2 = find_gordan(rows, self.m, self.stats)
        if lam2 is not None:
            return True
        self.stats["exact_simplex"] += 1
        return not exact_feasible(rows, self.m)

    # ---- engine D extensions: (k-1)-subset split nodes and "dis" context ----------
    def subrels_of(self, Q):
        out = []
        for eps in self.subpats:
            v = [0] * self.m
            for e, i in zip(eps, Q):
                v[i] = e
            out.append(tuple(v))
        return out

    def allowed_rels(self, U, dis):
        """patterns of the k-subset U allowed under the dis context: a pattern supported
        inside a dissociated Q ⊂ U cannot hold, so it must involve every element of U∖Q."""
        out = []
        for eps in self.pats:
            ok = True
            for Q in dis:
                if set(Q) <= set(U):
                    for pos, i in enumerate(U):
                        if i not in Q and eps[pos] == 0:
                            ok = False
            if ok:
                v = [0] * self.m
                for e, i in zip(eps, U):
                    v[i] = e
                out.append(tuple(v))
        return out

    def walk(self, node, path, dis=()):
        rows = rref(path, self.m)
        if "split" in node:
            self.stats["nodes"] += 1
            self.stats["splits"] = self.stats.get("splits", 0) + 1
            Q = tuple(node["split"])
            assert len(Q) == self.k - 1
            expected = self.subrels_of(Q)
            seen = [tuple(ch["r"]) for ch in node["children"] if ch["type"] != "dis"]
            diss = [ch for ch in node["children"] if ch["type"] == "dis"]
            if self.complete:
                assert sorted(seen) == sorted(expected), f"split on {Q}: relation children incomplete"
                assert len(diss) == 1, f"split on {Q}: dissociated child missing"
            else:
                assert set(seen) <= set(expected) and len(diss) <= 1
            for ch in node["children"]:
                if ch["type"] == "dis":
                    self.walk(ch["node"], path, dis + (Q,))
                elif ch["type"] == "pruned":
                    self.check_pruned(ch, path, Q)
                else:
                    self.walk(ch["node"], path + [tuple(ch["r"])], dis)
            return
        if "ref" in node:
            # a subtree already verified for the same subspace: check the subspace matches
            key = (tuple((p, tuple(r)) for p, r in rows), dis)
            assert key in self.verified, "ref to an unverified or different subspace"
            assert self.verified[key] == node["ref"], "ref id mismatch"
            self.stats["refs"] = self.stats.get("refs", 0) + 1
            return
        self.stats["nodes"] += 1
        if "id" in node:
            self.verified[(tuple((p, tuple(r)) for p, r in rows), dis)] = node["id"]
        if node.get("Q") is None:
            leaf = node["leaf"]
            if "dis_violated" in leaf:
                # a relation of a subset assumed dissociated holds identically: no point here
                Qd = tuple(leaf["dis_violated"]["Q"]); r = tuple(leaf["dis_violated"]["r"])
                assert Qd in dis, "dis_violated names a subset not assumed dissociated"
                assert r in self.subrels_of(Qd), "dis_violated relation is not a relation of Q"
                assert in_span(rows, r), "dis_violated relation does not hold on the subspace"
                self.stats["pruned_dis"] = self.stats.get("pruned_dis", 0) + 1
                return
            if leaf["feasible"]:
                w = leaf["witness"]
                assert all(sum(Fraction(r[i]) * w[i] for i in range(self.m)) == 0 for r in path), "witness violates path relation"
                assert w[0] > 0 and all(w[i + 1] > w[i] for i in range(self.m - 1)), "witness not sorted positive"
                dd = largest_dissociated(w)
                assert dd < self.k, f"witness has a dissociated {dd}-subset"
                self.stats["leaves_feasible"] += 1; self.stats["witness_ok"] += 1
                self.counterexamples.append(w)
            else:
                lam = leaf.get("gordan")
                assert self.infeasible_ok(rows, lam), "infeasible leaf could not be certified"
                self.stats["leaves_infeasible"] += 1
            return
        Q = tuple(node["Q"])
        node_dis = tuple(tuple(q) for q in node.get("dis", [])) if "dis" in node else dis
        assert node_dis == dis, "dis context recorded in the node differs from the path context"
        expected = self.allowed_rels(Q, dis) if dis else self.rels_of(Q)
        seen = [tuple(ch["r"]) for ch in node["children"]]
        if self.complete:
            assert sorted(seen) == sorted(expected), f"children of {Q} do not cover all allowed patterns exactly once"
        else:
            assert set(seen) <= set(expected) and len(seen) == len(set(seen)), f"unknown or repeated child relation at {Q}"
        for ch in node["children"]:
            if ch["type"] == "pruned":
                self.check_pruned(ch, path, Q)
            else:
                self.walk(ch["node"], path + [tuple(ch["r"])], dis)

    def check_pruned(self, ch, path, Q):
        r = tuple(ch["r"])
        why = ch.get("why", {})
        rows2 = rref(path + [r], self.m)
        if "forced" in why:
            fv = why["forced"]
            if fv == "dim0":
                assert len(rows2) == self.m, "dim0 claim false"
            else:
                fv = [Fraction(x) for x in fv]
                nz = [x for x in fv if x != 0]
                assert (len(nz) == 1 and nz[0] == 1) or (len(nz) == 2 and sorted(nz) == [-1, 1]), "bad forced vector"
                assert in_span(rows2, fv), "forced vector not in span"
            self.stats["pruned_forced"] += 1
        else:
            lam = why.get("gordan")
            assert self.infeasible_ok(rows2, lam), f"LP-pruned child of {Q} could not be certified infeasible"
            self.stats["pruned_gordan"] += 1


if __name__ == "__main__":
    path = sys.argv[1]
    doc = json.load(open(path))
    C = Checker(doc)
    st = C.check()
    print(f"checker: engine {doc.get('engine')} k={C.k} m={C.m}: {st}")
    if C.counterexamples:
        print(f"VERIFIED: the certificate exhibits {len(C.counterexamples)} counterexample set(s), e.g. {C.counterexamples[0]}: g({C.m}) <= {C.k-1}")
    elif C.complete:
        print(f"VERIFIED: every set of {C.m} distinct positive reals contains a dissociated {C.k}-subset: g({C.m}) >= {C.k}")
    else:
        print("certificate is marked incomplete and exhibits no counterexample: nothing is established")
