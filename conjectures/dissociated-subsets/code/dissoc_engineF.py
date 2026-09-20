#!/usr/bin/env python3
"""Engine F: engine E's parameter-space enumeration with the SEVEN-SMALLEST normalisation.

Let P (|P| ≥ 2k-3) have no dissociated k-subset and let S be its 2k-3 smallest elements.
By the (k-1)-theorem (every 2k-3 = 7 elements contain a dissociated 4-subset when k = 5),
S contains a dissociated (k-1)-subset T; write S \ T = {s_1, ..., s_{k-2}} and
μ = max S.  Every element of P is a signed sum of T (Lemma 3.3), and every element of
P \ S exceeds μ.  So:

  phase 1: choose the k-2 "small" vectors s_i (any signed sums; all k-subsets of
           T ∪ {s_i} must be blocked, by structure or by cuts);
  phase 2: choose which of T ∪ {s_i} is the maximum μ (k-1 + ... cases), impose
           μ > every other element of S, and then add further vectors e with e·t > μ·t,
           in canonical index order, blocking every new k-subset as in engine E.

Every P is enumerated at least once (once per dissociated T ⊂ S), and the phase-2
candidates are only the sign vectors that can exceed μ.  Exactness as in engine E.
"""
import sys, itertools, time
from fractions import Fraction
import numpy as np
from dissoc_engineE import EngineE


class EngineF(EngineE):
    def __init__(self, k=5, target=None, verbose=True, max_records=50, reverse=False):
        super().__init__(k=k, target=target, verbose=verbose, max_records=max_records, reverse=reverse)
        self.nsmall_total = k - 2            # |S \ T|
        self.extra = []                      # extra strict rows v (v·t > 0): ordering constraints
        self.phase1_nodes = 0; self.phase2_nodes = 0; self.mu_cases = 0

    # constraint rows now include the extra ordering rows
    def constraint_rows(self, E):
        rows = super().constraint_rows(E)
        for v in self.extra:
            rows.append(list(v))
        return rows

    def samples(self, E, W, nrand=4):
        # cache key must include the extra rows
        key = (tuple(E), tuple(map(tuple, W)), tuple(map(tuple, self.extra)))
        if key in self.sample_cache:
            return self.sample_cache[key]
        saved = self.sample_cache
        self.sample_cache = {}
        pts = super().samples(E, W, nrand)
        self.sample_cache = saved
        self.sample_cache[key] = pts
        return pts

    # ------------------------------------------------------------ phase 1
    def run(self):
        t0 = time.time(); self.t0 = t0
        self.phase1(list(self.units), [], self.dim - 1, [])
        self.time = time.time() - t0
        return self.best

    def phase1(self, E, W, last, pts):
        """choose the small vectors one at a time (index order), blocking new k-subsets."""
        if self.stop:
            return
        self.phase1_nodes += 1
        nsm = len(E) - self.dim
        if nsm == self.nsmall_total:
            self.choose_max(E, W, pts)
            return
        if not pts:
            pts = self.samples(E, W)
        for i in range(last + 1, self.n):
            if self.stop:
                return
            if self.always_neg[i]:
                continue
            if self.duplicates_forced(E, W, i):
                continue
            E2 = E + [i]
            pts2 = [q for q in pts if sum(self.vecs[i][j] * q[j] for j in range(self.dim)) > 0]
            if not self.always_pos[i] and not pts2:
                ok, p = self.feasible(E2, W)
                if not ok:
                    continue
                if p is not None:
                    B = self.kernel_basis(W)
                    pts2 = [[sum(p[t] * B[t][j] for t in range(len(B))) for j in range(self.dim)]]
            elif self.always_pos[i] and not pts2:
                pts2 = pts
            pending = [tuple(sorted(c + (i,))) for c in itertools.combinations(E, self.k - 1)]
            self.resolve1(E2, W, pending, i, pts2)

    def resolve1(self, E, W, pending, last, pts):
        if self.stop:
            return
        for idx, U in enumerate(pending):
            if not self.blocked(U, W):
                if len(W) >= self.dim - 1:
                    return
                for w in self.cut_options(U, W):
                    W2 = W + [list(w)]
                    if not self.T_dissociated_on(W2):
                        continue
                    if self.duplicates_forced(E, W2):
                        continue
                    signs = set()
                    for p in pts:
                        s = sum(w[j] * p[j] for j in range(self.dim))
                        signs.add(1 if s > 0 else -1 if s < 0 else 0)
                    if not ({1, -1} <= signs or 0 in signs):
                        ok, _ = self.feasible(E, W2)
                        if not ok:
                            continue
                    self.cuts += 1
                    self.resolve1(E, W2, pending[idx + 1:], last, self.samples(E, W2))
                return
        self.phase1(E, W, last, pts)

    # ------------------------------------------------------------ choose the maximum of S
    def choose_max(self, E, W, pts):
        """E = T ∪ small vectors (|E| = 2k-3).  Branch on which element is the maximum μ."""
        for mu in E:
            if self.stop:
                return
            self.mu_cases += 1
            saved = self.extra
            rows = []
            for x in E:
                if x != mu:
                    rows.append(tuple(a - b for a, b in zip(self.vecs[mu], self.vecs[x])))
            self.extra = saved + rows
            ok, p = self.feasible(E, W)
            if ok:
                if len(W) == self.dim - 1:
                    self.numericF(E, W, mu, -1)
                else:
                    self.phase2(E, W, mu, self.dim - 1, [])
            self.extra = saved

    # ------------------------------------------------------------ phase 2
    def phase2(self, E, W, mu, last, pts):
        if self.stop:
            return
        self.phase2_nodes += 1
        self.nodes += 1
        if self.nodes % 5000 == 0:
            print(f"  progress: nodes={self.nodes} p1={self.phase1_nodes} mu={self.mu_cases} cuts={self.cuts} numeric={self.numeric_nodes} "
                  f"best={self.best} |E|={len(E)} W={W} elapsed={time.time()-self.t0:.0f}s", flush=True)
        self.record(E, W)
        if not pts:
            pts = self.samples(E, W)
            if not pts:
                ok, _ = self.feasible(E, W)
                if not ok:
                    return
        for i in range(last + 1, self.n):
            if self.stop:
                return
            if i in E or self.always_neg[i]:
                continue
            # must exceed mu:  (e_i - mu)·t > 0 ; cheap exact rejection on the sorted cone
            dv = tuple(a - b for a, b in zip(self.vecs[i], self.vecs[mu]))
            suf = [sum(dv[j:]) for j in range(self.dim)]
            if all(s <= 0 for s in suf):
                continue                          # e_i·t <= mu·t everywhere on the cone
            if self.duplicates_forced(E, W, i):
                continue
            pts2 = [q for q in pts if sum(dv[j] * q[j] for j in range(self.dim)) > 0]
            saved = self.extra
            self.extra = saved + [dv]
            E2 = E + [i]
            if not pts2:
                ok, p = self.feasible(E2, W)
                if not ok:
                    self.extra = saved
                    continue
                if p is not None:
                    B = self.kernel_basis(W)
                    pts2 = [[sum(p[t] * B[t][j] for t in range(len(B))) for j in range(self.dim)]]
            pending = [tuple(sorted(c + (i,))) for c in itertools.combinations(E, self.k - 1)]
            self.resolve2(E2, W, mu, pending, i, pts2)
            self.extra = saved

    def resolve2(self, E, W, mu, pending, last, pts):
        if self.stop:
            return
        for idx, U in enumerate(pending):
            if not self.blocked(U, W):
                if len(W) >= self.dim - 1:
                    return
                for w in self.cut_options(U, W):
                    W2 = W + [list(w)]
                    if not self.T_dissociated_on(W2):
                        continue
                    if self.duplicates_forced(E, W2):
                        continue
                    signs = set()
                    for p in pts:
                        s = sum(w[j] * p[j] for j in range(self.dim))
                        signs.add(1 if s > 0 else -1 if s < 0 else 0)
                    if not ({1, -1} <= signs or 0 in signs):
                        ok, _ = self.feasible(E, W2)
                        if not ok:
                            continue
                    self.cuts += 1
                    if len(W2) == self.dim - 1:
                        self.numericF(E, W2, mu, last)
                    else:
                        self.resolve2(E, W2, mu, pending[idx + 1:], last, self.samples(E, W2))
                return
        self.phase2(E, W, mu, last, pts)

    # ------------------------------------------------------------ numeric mode with the ordering
    def numericF(self, E, W, mu, last):
        if self.stop:
            return
        self.numeric_nodes += 1
        B = self.kernel_basis(W)
        assert len(B) == 1
        t = B[0]
        if t[0] < 0:
            t = [-x for x in t]
        if not (t[0] > 0 and all(t[i + 1] > t[i] for i in range(self.dim - 1))):
            return
        if not self.T_dissociated_numeric(t):
            return
        vals = [int(np.dot(self.vecs[e], t)) for e in range(self.n)]
        chosen = [vals[e] for e in E]
        if any(v <= 0 for v in chosen) or len(set(chosen)) < len(chosen):
            return
        muv = vals[mu]
        # ordering: mu is the max of the first 2k-3 elements, later ones exceed mu
        first = chosen[: 2 * self.k - 3]
        if max(first) != muv or any(v <= muv for v in chosen[2 * self.k - 3:]):
            return
        for U in itertools.combinations(chosen, self.k):
            if self.dissociated(U):
                return
        self.record(E, W, t)
        cand = [i for i in range(last + 1, self.n) if i not in E and vals[i] > muv and vals[i] not in chosen]
        self.numeric_dfs(E, W, t, chosen, cand, 0, vals)


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    target = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    reverse = len(sys.argv) > 3 and sys.argv[3] == "rev"
    F = EngineF(k=k, target=target, reverse=reverse)
    print(f"[F] k={k}: {F.n} sign vectors; small vectors to choose: {F.nsmall_total}; target={target} reverse={reverse}", flush=True)
    best = F.run()
    print(f"[F] best |E| = {best}; nodes={F.nodes} phase1={F.phase1_nodes} mu_cases={F.mu_cases} cuts={F.cuts} numeric={F.numeric_nodes} "
          f"lp_calls={F.lp_calls} lp_unverified={F.lp_unverified} time={F.time:.1f}s stop={F.stop}", flush=True)
    for Eset, W, t in F.records[:10]:
        if t is None:
            print("   family: vectors", [F.vecs[i] for i in Eset], "cuts", W)
        else:
            vals = sorted(int(np.dot(F.vecs[i], t)) for i in Eset)
            print("   point t =", t, "set", vals)
    if target is not None and best >= target:
        print(f"[F] RESULT: found a set of {best} positive reals with no dissociated {k}-subset")
    elif target is None:
        print(f"[F] RESULT (exhaustive): the largest set of positive reals with no dissociated {k}-subset has {best} elements => m_{k} = {best+1}")
