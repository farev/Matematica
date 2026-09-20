#!/usr/bin/env python3
"""Engine G: engine F with every LP replaced by exact extreme-ray arithmetic.

The feasible region of the parameter t is a pointed polyhedral cone in W^perp (the
sorted cone 0 < t_1 < ... cut by the strict rows e·t > 0, the ordering rows, and the
cut hyperplanes W).  We keep its extreme rays as primitive integer vectors and update
them by one double-description step per added constraint:
    strict row v >= 0 : keep rays with v·r >= 0, add (v·p) q - (v·q) p for p > 0 > q;
    cut       w  = 0 : keep rays with w·r  = 0, add the same combinations.
Then, exactly:
  * the open region is nonempty  iff  every strict row is > 0 on some ray;
  * a new strict row v is compatible iff  v > 0 on some ray;
  * a cut w meets the open region  iff  w takes both signs on the rays;
  * two chosen vectors are forced equal iff their difference vanishes on all rays.
Non-extreme rays produced by the naive step are removed by a rank test, so the ray
lists stay small.  All arithmetic is on Python integers.
"""
import sys, itertools, time
from math import gcd
from fractions import Fraction
import numpy as np
from dissoc_engineF import EngineF


def prim(v):
    g = 0
    for x in v:
        g = gcd(g, abs(int(x)))
    return tuple(int(x) // g for x in v) if g > 1 else tuple(int(x) for x in v)

def rank_int(rows):
    """rank of a small integer matrix, exact (fraction-free elimination)."""
    M = [list(map(Fraction, r)) for r in rows]
    rk = 0
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        piv = None
        for i in range(rk, len(M)):
            if M[i][c] != 0:
                piv = i; break
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


class Region:
    """pointed cone given by its rays; `rows` = all strict rows, `cuts` = equalities."""
    __slots__ = ("rays", "rows", "cuts", "dim")

    def __init__(self, rays, rows, cuts, dim):
        self.rays = rays; self.rows = rows; self.cuts = cuts; self.dim = dim

    @staticmethod
    def base(dim):
        rays = [tuple(1 if j >= i else 0 for j in range(dim)) for i in range(dim)]
        rows = []
        r = [0] * dim; r[0] = 1; rows.append(tuple(r))
        for i in range(dim - 1):
            r = [0] * dim; r[i + 1] = 1; r[i] = -1; rows.append(tuple(r))
        return Region(rays, rows, [], dim)

    def _step(self, v, eq):
        pos, neg, zero = [], [], []
        for r in self.rays:
            s = sum(a * b for a, b in zip(v, r))
            (pos if s > 0 else neg if s < 0 else zero).append((r, s))
        keep = [r for r, _ in zero] + ([] if eq else [r for r, _ in pos])
        for p, sp in pos:
            for q, sq in neg:
                keep.append(prim(tuple(sp * b - sq * a for a, b in zip(p, q))))
        # dedupe and drop non-extreme rays (tight constraints must have rank dim-1-|cuts|)
        seen = set(); out = []
        allrows = self.rows + ([tuple(v)] if not eq else [])
        allcuts = self.cuts + ([tuple(v)] if eq else [])
        need = self.dim - 1 - len(allcuts)
        for r in keep:
            if r in seen or all(x == 0 for x in r):
                continue
            seen.add(r)
            tight = [row for row in allrows if sum(a * b for a, b in zip(row, r)) == 0]
            if need <= 0 or rank_int(tight + allcuts) >= need + len(allcuts):
                out.append(r)
        return Region(out, allrows, allcuts, self.dim)

    def add_strict(self, v):
        return self._step(tuple(v), False)

    def add_cut(self, w):
        return self._step(tuple(w), True)

    def nonempty(self):
        if not self.rays:
            return False
        for row in self.rows:
            if not any(sum(a * b for a, b in zip(row, r)) > 0 for r in self.rays):
                return False
        return True

    def compatible(self, v):
        return any(sum(a * b for a, b in zip(v, r)) > 0 for r in self.rays)

    def cut_meets(self, w):
        pos = neg = False
        for r in self.rays:
            s = sum(a * b for a, b in zip(w, r))
            if s > 0: pos = True
            elif s < 0: neg = True
            if pos and neg:
                return True
        return False

    def vanishes(self, v):
        return all(sum(a * b for a, b in zip(v, r)) == 0 for r in self.rays)


class EngineG(EngineF):
    def __init__(self, k=5, target=None, verbose=True, max_records=50, reverse=False):
        super().__init__(k=k, target=target, verbose=verbose, max_records=max_records, reverse=reverse)
        self.ray_steps = 0; self.max_rays = 0

    # ---- exact region tests replacing the LP-based ones -----------------------------
    def T_dissociated_region(self, reg):
        return not any(reg.vanishes(r) for r in self.trel)

    def dup_region(self, reg, E, new=None):
        idx = E + ([new] if new is not None else [])
        for a, b in itertools.combinations(idx, 2):
            if reg.vanishes(tuple(x - y for x, y in zip(self.vecs[a], self.vecs[b]))):
                return True
        return False

    def step(self, reg, v, eq=False):
        self.ray_steps += 1
        r2 = reg.add_cut(v) if eq else reg.add_strict(v)
        if len(r2.rays) > self.max_rays:
            self.max_rays = len(r2.rays)
        return r2

    # ---- phase 1 ----------------------------------------------------------------------
    def run(self):
        t0 = time.time(); self.t0 = t0
        self.phase1(list(self.units), [], self.dim - 1, Region.base(self.dim))
        self.time = time.time() - t0
        return self.best

    def phase1(self, E, W, last, reg):
        if self.stop:
            return
        self.phase1_nodes += 1
        if len(E) - self.dim == self.nsmall_total:
            self.choose_max(E, W, reg)
            return
        for i in range(last + 1, self.n):
            if self.stop:
                return
            if self.always_neg[i]:
                continue
            if not reg.compatible(self.vecs[i]):
                continue
            reg2 = self.step(reg, self.vecs[i])
            if not reg2.nonempty():
                continue
            if self.dup_region(reg2, E, i):
                continue
            E2 = E + [i]
            pending = [tuple(sorted(c + (i,))) for c in itertools.combinations(E, self.k - 1)]
            self.resolve1(E2, W, pending, i, reg2)

    def resolve1(self, E, W, pending, last, reg):
        if self.stop:
            return
        for idx, U in enumerate(pending):
            if not self.blocked(U, W):
                if len(W) >= self.dim - 1:
                    return
                for w in self.cut_options(U, W):
                    if not reg.cut_meets(w):
                        continue
                    W2 = W + [list(w)]
                    reg2 = self.step(reg, w, eq=True)
                    if not reg2.nonempty():
                        continue
                    if not self.T_dissociated_region(reg2):
                        continue
                    if self.dup_region(reg2, E):
                        continue
                    self.cuts += 1
                    self.resolve1(E, W2, pending[idx + 1:], last, reg2)
                return
        self.phase1(E, W, last, reg)

    # ---- the maximum of the seven ----------------------------------------------------
    def choose_max(self, E, W, reg):
        for mu in E:
            if self.stop:
                return
            self.mu_cases += 1
            reg2 = reg
            ok = True
            for x in E:
                if x == mu:
                    continue
                dv = tuple(a - b for a, b in zip(self.vecs[mu], self.vecs[x]))
                if not reg2.compatible(dv):
                    ok = False; break
                reg2 = self.step(reg2, dv)
                if not reg2.nonempty():
                    ok = False; break
            if not ok:
                continue
            if len(W) == self.dim - 1:
                self.numericF(E, W, mu, -1)
            else:
                self.phase2(E, W, mu, self.dim - 1, reg2)

    # ---- phase 2 ----------------------------------------------------------------------
    def phase2(self, E, W, mu, last, reg):
        if self.stop:
            return
        self.phase2_nodes += 1
        self.nodes += 1
        if self.nodes % 5000 == 0:
            print(f"  progress: nodes={self.nodes} p1={self.phase1_nodes} mu={self.mu_cases} cuts={self.cuts} numeric={self.numeric_nodes} "
                  f"best={self.best} |E|={len(E)} W={W} rays<={self.max_rays} elapsed={time.time()-self.t0:.0f}s", flush=True)
        self.record(E, W)
        for i in range(last + 1, self.n):
            if self.stop:
                return
            if i in E or self.always_neg[i]:
                continue
            dv = tuple(a - b for a, b in zip(self.vecs[i], self.vecs[mu]))
            if not reg.compatible(dv):
                continue
            reg2 = self.step(reg, dv)
            if not reg2.nonempty():
                continue
            if self.dup_region(reg2, E, i):
                continue
            E2 = E + [i]
            pending = [tuple(sorted(c + (i,))) for c in itertools.combinations(E, self.k - 1)]
            self.resolve2(E2, W, mu, pending, i, reg2)

    def resolve2(self, E, W, mu, pending, last, reg):
        if self.stop:
            return
        for idx, U in enumerate(pending):
            if not self.blocked(U, W):
                if len(W) >= self.dim - 1:
                    return
                for w in self.cut_options(U, W):
                    if not reg.cut_meets(w):
                        continue
                    W2 = W + [list(w)]
                    reg2 = self.step(reg, w, eq=True)
                    if not reg2.nonempty():
                        continue
                    if not self.T_dissociated_region(reg2):
                        continue
                    if self.dup_region(reg2, E):
                        continue
                    self.cuts += 1
                    if len(W2) == self.dim - 1:
                        self.numericF(E, W2, mu, last)
                    else:
                        self.resolve2(E, W2, mu, pending[idx + 1:], last, reg2)
                return
        self.phase2(E, W, mu, last, reg)


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    target = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    reverse = len(sys.argv) > 3 and sys.argv[3] == "rev"
    G = EngineG(k=k, target=target, reverse=reverse)
    if len(sys.argv) > 3 and sys.argv[3].startswith("seed"):
        import random
        rng = random.Random(int(sys.argv[3][4:]))
        others = G.vecs[G.dim:]
        rng.shuffle(others)
        G.vecs = G.vecs[:G.dim] + others
        G.V = np.array(G.vecs, dtype=np.int64)
        d = G.dim
        G.always_pos = []; G.always_neg = []; G.small = []
        for v in G.vecs:
            suf = [sum(v[i:]) for i in range(d)]
            G.always_pos.append(all(s >= 0 for s in suf) and any(s > 0 for s in suf))
            G.always_neg.append(all(s <= 0 for s in suf) and any(s < 0 for s in suf))
            w = list(v); w[d - 1] -= 1
            suf = [sum(w[i:]) for i in range(d)]
            G.small.append(all(s <= 0 for s in suf) and any(s < 0 for s in suf))
        print(f"[G] shuffled candidate order with seed {sys.argv[3][4:]}", flush=True)
    print(f"[G] k={k}: {G.n} sign vectors; small vectors to choose: {G.nsmall_total}; target={target} reverse={reverse}", flush=True)
    best = G.run()
    print(f"[G] best |E| = {best}; nodes={G.nodes} phase1={G.phase1_nodes} mu_cases={G.mu_cases} cuts={G.cuts} numeric={G.numeric_nodes} "
          f"ray_steps={G.ray_steps} max_rays={G.max_rays} time={G.time:.1f}s stop={G.stop}", flush=True)
    for Eset, W, t in G.records[:10]:
        if t is None:
            print("   family: vectors", [G.vecs[i] for i in Eset], "cuts", W)
        else:
            vals = sorted(int(np.dot(G.vecs[i], t)) for i in Eset)
            print("   point t =", t, "set", vals)
    if target is not None and best >= target:
        print(f"[G] RESULT: found a set of {best} positive reals with no dissociated {k}-subset")
    elif target is None:
        print(f"[G] RESULT (exhaustive): the largest set of positive reals with no dissociated {k}-subset has {best} elements => m_{k} = {best+1}")
