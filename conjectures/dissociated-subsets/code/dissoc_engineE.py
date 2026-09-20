#!/usr/bin/env python3
"""Engine E: enumeration of sets of positive reals with no dissociated k-subset (k = 5)
in the (k-1)-dimensional parameter space of a dissociated (k-1)-subset.

Lemma (signed sums).  If P has no dissociated k-subset and T = {t_1<...<t_{k-1}} ⊂ P is
dissociated, then every element of P is  e·t  for some sign vector e ∈ {-1,0,1}^{k-1}
(the elements of T are the unit vectors).  Since every 7-element set contains a
dissociated 4-subset (today's k=4 theorem), every P with |P| ≥ 7 and no dissociated
5-subset arises this way.

State: E = list of sign vectors (indices into the fixed list of the 3^{k-1}-1 nonzero
vectors; the units come first), W = list of ≤ k-2 independent integer "cut" vectors
(t is restricted to S = W^perp).  Constraints kept feasible (LP on ≤ k-1 variables with
exact Gordan certificates for every pruning): 0 < t_1 < ... < t_{k-1};  e·t > 0 for e ∈ E.
A k-subset U ⊂ E is BLOCKED iff some η ∈ {-1,0,1}^U \ 0 has w(η) = Σ η_i e_i ∈ span_Q(W)
(w = 0 is the structural case).  Adding a vector creates new k-subsets; each unblocked one
must be blocked by a new cut w(η) (branch over the distinct admissible w's: w ∉ span W,
w not itself a ±1-relation of T, cut feasible, no two chosen vectors forced equal).
When |W| = k-2 the parameter t is a fixed integer point and everything is checked
numerically (no further cuts possible).  Vectors are added in canonical index order, so
every set E is generated once per (T, order).  Records the maximum |E| found and all
maximal configurations; with `target` it stops at the first E of that size.
"""
import sys, itertools, time
from fractions import Fraction
from math import gcd
import numpy as np
from scipy.optimize import linprog


def rank_frac(vectors):
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
        rows.append((p, v))
    return len(rows)

def in_span(W, w):
    if all(x == 0 for x in w):
        return True
    if not W:
        return False
    return rank_frac(W + [w]) == rank_frac(W)


class EngineE:
    def __init__(self, k=5, target=None, verbose=True, max_records=50, reverse=False):
        self.k = k; self.dim = k - 1
        d = self.dim
        vecs = [v for v in itertools.product((-1, 0, 1), repeat=d) if any(v)]
        units = [tuple(1 if i == j else 0 for i in range(d)) for j in range(d)]
        others = [v for v in vecs if v not in units]
        if reverse:
            others = others[::-1]
        self.vecs = units + others          # units first: indices 0..d-1
        self.n = len(self.vecs)
        self.V = np.array(self.vecs, dtype=np.int64)
        self.units = list(range(d))
        # T-relations: sign patterns feasible on the sorted cone restricted to T (±1 vectors)
        self.trel = [v for v in vecs if self._first_nonzero_sign(v) == 1]  # all ±1/0 vectors up to sign
        # etas for k-subsets: nonzero, first nonzero +1
        self.etas = [e for e in itertools.product((-1, 0, 1), repeat=k) if any(e) and self._first_nonzero_sign(e) == 1]
        self.eta_arr = np.array(self.etas, dtype=np.int64)     # (121, k)
        # suffix-sum sign determinacy on the sorted cone
        self.always_pos = []; self.always_neg = []
        for v in self.vecs:
            suf = [sum(v[i:]) for i in range(d)]
            self.always_pos.append(all(s >= 0 for s in suf) and any(s > 0 for s in suf))
            self.always_neg.append(all(s <= 0 for s in suf) and any(s < 0 for s in suf))
        # "certainly small": e.t < t_{k-1} on the whole sorted cone (suffix sums of e - u_{k-1}
        # all <= 0, some < 0).  Normalisation: T is a dissociated (k-1)-subset of the 2k-3
        # smallest elements of P (exists by the k-1 theorem), hence at most k-2 elements of
        # P \ T lie below max T.  Only certainly-small vectors are counted (sound).
        self.small = []
        for v in self.vecs:
            w = list(v); w[d - 1] -= 1
            suf = [sum(w[i:]) for i in range(d)]
            self.small.append(all(s <= 0 for s in suf) and any(s < 0 for s in suf))
        self.max_small = k - 2
        self.target = target
        self.verbose = verbose
        self.best = 0; self.records = []; self.max_records = max_records
        self.nodes = 0; self.cuts = 0; self.numeric_nodes = 0; self.lp_calls = 0; self.lp_unverified = 0; self.cuts_by_samples = 0
        self.stop = False
        self.block_cache = {}
        self.K_cache = {}
        self.sample_cache = {}
        self.trel_arr = np.array(self.trel, dtype=np.int64)

    @staticmethod
    def _first_nonzero_sign(v):
        for x in v:
            if x != 0:
                return 1 if x > 0 else -1
        return 0

    # ------------------------------------------------------------ feasibility (exact)
    def constraint_rows(self, E):
        d = self.dim
        rows = []
        r = [0] * d; r[0] = 1; rows.append(r)
        for i in range(d - 1):
            r = [0] * d; r[i + 1] = 1; r[i] = -1; rows.append(r)
        for ei in E:
            if ei >= d:                       # units already covered by the cone rows
                rows.append(list(self.vecs[ei]))
        return rows

    def kernel_basis(self, W):
        """integer basis of W^perp in Z^d (exact, via Fractions)."""
        d = self.dim
        if not W:
            return [[1 if i == j else 0 for j in range(d)] for i in range(d)]
        # RREF of W, then free-variable basis, scaled to integers
        rows = []
        for v in W:
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
        pivs = [p for p, _ in rows]
        B = []
        for f in range(d):
            if f in pivs:
                continue
            vec = [Fraction(0)] * d; vec[f] = Fraction(1)
            for p, r in rows:
                vec[p] = -r[f]
            L = 1
            for x in vec:
                L = L * x.denominator // gcd(L, x.denominator)
            B.append([int(x * L) for x in vec])
        return B

    def feasible(self, E, W):
        """exact: is {t ∈ W^perp : all constraint rows > 0} nonempty?  Returns (bool, cert)."""
        rows = self.constraint_rows(E)
        B = self.kernel_basis(W)
        dd = len(B)
        if dd == 0:
            return False, None
        C = [[sum(r[j] * B[t][j] for j in range(self.dim)) for t in range(dd)] for r in rows]
        self.lp_calls += 1
        Cf = np.array(C, dtype=float)
        c = np.zeros(dd + 1); c[-1] = -1.0
        A_ub = np.hstack([-Cf, np.ones((len(C), 1))]); b_ub = np.zeros(len(C))
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(-1, 1)] * dd + [(0, 1)], method="highs")
        if res.status == 0 and -res.fun > 1e-9:
            y = res.x[:dd]
            for den in (8, 64, 1024, 10**5, 10**8):
                yq = [Fraction(v).limit_denominator(den) for v in y]
                if all(sum(C[i][t] * yq[t] for t in range(dd)) > 0 for i in range(len(C))):
                    return True, yq
            self.lp_unverified += 1
            return True, None          # treated as feasible (sound: never prunes)
        if res.status == 0:
            lam = [-float(v) for v in res.ineqlin.marginals]
            for den in (8, 64, 1024, 10**5, 10**8):
                lq = [max(Fraction(v).limit_denominator(den), Fraction(0)) for v in lam]
                if any(x > 0 for x in lq) and all(sum(lq[i] * C[i][t] for i in range(len(C))) == 0 for t in range(dd)):
                    return False, lq
        self.lp_unverified += 1
        return True, None              # could not certify infeasibility: keep (sound)

    def samples(self, E, W, nrand=4):
        """a few exact rational points of the region {t in W^perp: constraints > 0}
        (max-margin point + optima in random directions), cached per (E, W)."""
        key = (tuple(E), tuple(map(tuple, W)))
        if key in self.sample_cache:
            return self.sample_cache[key]
        rows = self.constraint_rows(E)
        B = self.kernel_basis(W)
        dd = len(B)
        pts = []
        if dd > 0:
            C = [[sum(r[j] * B[t][j] for j in range(self.dim)) for t in range(dd)] for r in rows]
            Cf = np.array(C, dtype=float)
            rng = np.random.default_rng(len(E) * 1000 + len(W))
            for trial in range(nrand + 1):
                if trial == 0:
                    c = np.zeros(dd + 1); c[-1] = -1.0
                else:
                    c = np.concatenate([rng.normal(size=dd), [0.0]])
                A_ub = np.hstack([-Cf, np.ones((len(C), 1))]); b_ub = np.zeros(len(C))
                bounds = [(-1, 1)] * dd + [(1e-3, 1)]
                self.lp_calls += 1
                res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
                if res.status != 0:
                    continue
                y = res.x[:dd]
                for den in (8, 64, 1024, 10**5):
                    yq = [Fraction(v).limit_denominator(den) for v in y]
                    if all(sum(C[i][t] * yq[t] for t in range(dd)) > 0 for i in range(len(C))):
                        pts.append([sum(yq[t] * B[t][j] for t in range(dd)) for j in range(self.dim)])
                        break
        self.sample_cache[key] = pts
        return pts

    # ------------------------------------------------------------ blocking
    def w_vectors(self, U):
        """all w(η) for the k-subset U (tuple of vector indices): array (121, d)."""
        M = self.V[list(U)]                    # (k, d)
        return self.eta_arr @ M                # (121, d)

    def K_of(self, W):
        """integer basis (numpy, dd x d) of W^perp; w ∈ span(W) iff K @ w == 0."""
        key = tuple(map(tuple, W))
        K = self.K_cache.get(key)
        if K is None:
            K = np.array(self.kernel_basis(W), dtype=np.int64).reshape(-1, self.dim)
            self.K_cache[key] = K
        return K

    def blocked(self, U, W):
        key = (U, tuple(map(tuple, W)))
        if key in self.block_cache:
            return self.block_cache[key]
        Ws = self.w_vectors(U)                      # (121, d)
        K = self.K_of(W)
        res = bool(np.any(~np.any(Ws @ K.T, axis=1)))   # some w(η) ⊥ K, i.e. in span(W)
        self.block_cache[key] = res
        return res

    def cut_options(self, U, W):
        """distinct admissible cut vectors for an unblocked k-subset U."""
        Ws = self.w_vectors(U)
        K = self.K_of(W)
        inspan = ~np.any(Ws @ K.T, axis=1)
        small = np.all(np.abs(Ws) <= 1, axis=1)     # ±1-relations of T (incl. zero): impossible
        opts = {}
        for w, s, small_ in zip(Ws, inspan, small):
            if s or small_:
                continue
            w = [int(x) for x in w]
            g = 0
            for x in w:
                g = gcd(g, abs(x))
            w = [x // g for x in w]
            if self._first_nonzero_sign(w) < 0:
                w = [-x for x in w]
            opts[tuple(w)] = True
        return list(opts.keys())

    def T_dissociated_on(self, W):
        K = self.K_of(W)
        return not bool(np.any(~np.any(self.trel_arr @ K.T, axis=1)))

    def duplicates_forced(self, E, W, new=None):
        idx = E + ([new] if new is not None else [])
        if len(idx) < 2:
            return False
        K = self.K_of(W)
        M = self.V[idx]                             # (s, d)
        # pairwise differences
        D = (M[:, None, :] - M[None, :, :]).reshape(-1, self.dim)
        iu = np.triu_indices(len(idx), 1)
        D = (M[iu[0]] - M[iu[1]])
        return bool(np.any(~np.any(D @ K.T, axis=1)))

    # ------------------------------------------------------------ search
    def record(self, E, W, t=None):
        if len(E) > self.best:
            self.best = len(E)
            self.records = []
            if self.verbose:
                print(f"  new best |E| = {len(E)}  W={W}  t={t}", flush=True)
        if len(E) == self.best and len(self.records) < self.max_records:
            self.records.append((list(E), [list(w) for w in W], t))
        if self.target is not None and len(E) >= self.target:
            self.stop = True

    def dfs(self, E, W, last, pts=None):
        if self.stop:
            return
        self.nodes += 1
        if self.nodes % 20000 == 0:
            print(f"  progress: nodes={self.nodes} cuts={self.cuts} numeric={self.numeric_nodes} best={self.best} |E|={len(E)} W={W} elapsed={time.time()-self.t0:.0f}s", flush=True)
        self.record(E, W)
        nsmall = sum(1 for e in E if self.small[e])
        if pts is None or len(pts) < 2:
            pts = self.samples(E, W)
            if not pts:
                okp, _ = self.feasible(E, W)
                if not okp:
                    return
        for i in range(last + 1, self.n):
            if self.stop:
                return
            if self.always_neg[i]:
                continue
            if self.small[i] and nsmall >= self.max_small:
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
            self.resolve(E2, W, pending, i, pts2)

    def resolve(self, E, W, pending, last, pts):
        """block every k-subset in `pending` (by existing W or new cuts), then continue."""
        if self.stop:
            return
        for idx, U in enumerate(pending):
            if not self.blocked(U, W):
                if len(W) >= self.dim - 1:
                    return                        # t already fixed: cannot block -> dead
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
                    else:
                        self.cuts_by_samples += 1
                    self.cuts += 1
                    if len(W2) == self.dim - 1:
                        self.numeric(E, W2, pending[idx + 1:], last)
                    else:
                        self.resolve(E, W2, pending[idx + 1:], last, [])
                return
        self.dfs(E, W, last, pts)

    def numeric(self, E, W, pending, last):
        """t is fixed (up to scale) by W: finish with integer arithmetic."""
        if self.stop:
            return
        self.numeric_nodes += 1
        B = self.kernel_basis(W)
        assert len(B) == 1
        t = B[0]
        if t[0] < 0:
            t = [-x for x in t]
        # sorted positive, T dissociated, chosen vectors positive & distinct
        if not (t[0] > 0 and all(t[i + 1] > t[i] for i in range(self.dim - 1))):
            return
        vals = [int(np.dot(self.vecs[e], t)) for e in range(self.n)]
        if not self.T_dissociated_numeric(t):
            return
        chosen = [vals[e] for e in E]
        if any(v <= 0 for v in chosen) or len(set(chosen)) < len(chosen):
            return
        # all pending (and, for safety, all) k-subsets of E must be numerically blocked
        for U in itertools.combinations(chosen, self.k):
            if self.dissociated(U):
                return
        self.record(E, W, t)
        # extend numerically with candidates of larger index
        cand = [i for i in range(last + 1, self.n) if vals[i] > 0 and vals[i] not in chosen]
        self.numeric_dfs(E, W, t, chosen, cand, 0, vals)

    def numeric_small_ok(self, E, i, vals, t):
        # numeric version of the normalisation: at most max_small chosen non-unit values below t_{k-1}
        cnt = sum(1 for e in E if e >= self.dim and vals[e] < t[self.dim - 1])
        return cnt + (1 if vals[i] < t[self.dim - 1] else 0) <= self.max_small

    def numeric_dfs(self, E, W, t, chosen, cand, start, vals):
        if self.stop:
            return
        for j in range(start, len(cand)):
            i = cand[j]
            v = vals[i]
            if v in chosen:
                continue
            if not self.numeric_small_ok(E, i, vals, t):
                continue
            ok = True
            for c4 in itertools.combinations(chosen, self.k - 1):
                if self.dissociated(c4 + (v,)):
                    ok = False; break
            if not ok:
                continue
            self.numeric_nodes += 1
            self.record(E + [i], W, t)
            self.numeric_dfs(E + [i], W, t, chosen + [v], cand, j + 1, vals)

    @staticmethod
    def dissociated(U):
        sums = set()
        for mask in range(1 << len(U)):
            s = sum(U[i] for i in range(len(U)) if mask >> i & 1)
            if s in sums:
                return False
            sums.add(s)
        return True

    def T_dissociated_numeric(self, t):
        return self.dissociated(tuple(t))

    def run(self):
        t0 = time.time(); self.t0 = t0
        self.dfs(list(self.units), [], self.dim - 1)
        self.time = time.time() - t0
        return self.best


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    target = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    reverse = len(sys.argv) > 3 and sys.argv[3] == "rev"
    E = EngineE(k=k, target=target, reverse=reverse)
    print(f"[E] k={k}: {E.n} sign vectors, {len(E.etas)} etas; target={target}", flush=True)
    best = E.run()
    print(f"[E] best |E| = {best}; nodes={E.nodes} cuts={E.cuts} numeric_nodes={E.numeric_nodes} lp_calls={E.lp_calls} "
          f"lp_unverified={E.lp_unverified} time={E.time:.1f}s stop={E.stop}", flush=True)
    for Eset, W, t in E.records[:10]:
        if t is None:
            print("   family: vectors", [E.vecs[i] for i in Eset], "cuts", W)
        else:
            vals = sorted(int(np.dot(E.vecs[i], t)) for i in Eset)
            print("   point t =", t, "set", vals)
    if target is not None and best >= target:
        print(f"[E] RESULT: found a set of {best} positive reals with no dissociated {k}-subset")
    elif target is None:
        print(f"[E] RESULT (exhaustive): the largest set of positive reals with no dissociated {k}-subset has {best} elements => m_{k} = {best+1}")
