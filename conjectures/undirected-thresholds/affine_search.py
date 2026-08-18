"""Exhaustive search for additive-ansatz witnesses in canonical space.

Ansatz: W[0]=0, W[q] = W[q//k] + W[q%k] (mod n) — the fixed point of the
uniform morphism phi(x) = x + B0 with B0 = W[0..k).  We DFS over the
CANONICAL word (letters named by first occurrence) and carry the concrete
letter values symbolically: each canonical letter c has a form V(c) =
integer vector over free variables (one per canonical letter first seen at
a free position q < k).  Constraints:

  * position q >= k: value(C[q]) must equal V(C[q//k]) + V(C[q%k]) (mod n)
    -> asserting C[q] = c adds the homogeneous row V(c) - f to the system;
  * x_{C[0]} = 0 (W[0] = 0);
  * injectivity: no two distinct canonical letters may have forms forced
    equal modulo the system (checked in GF(2) and GF(11), n = 22 = 2*11).

Homogeneous systems never contradict; ALL pruning is injectivity + the
U-freeness checker (UInc) on the canonical word.  At forced positions the
system usually pins the letter uniquely, so the tree stays thin.

Usage: python3 affine_search.py <kmin> <kmax> <depth> [maxnodes]
(n, num, den fixed at 22, 21, 20 here.)
"""

import sys
import time

import numpy as np

from urt import UInc

N = 22
PRIMES = (2, 11)


class FieldElim:
    """Gaussian elimination over GF(p), snapshot-copy semantics."""

    def __init__(self, p, ncols):
        self.p = p
        self.ncols = ncols
        self.rows = []  # list of np arrays, row-echelon (pivot cols sorted)

    def copy(self):
        e = FieldElim(self.p, self.ncols)
        e.rows = [r.copy() for r in self.rows]
        return e

    def reduce(self, v):
        v = v % self.p
        for r in self.rows:
            pc = np.argmax(r != 0)
            if v[pc]:
                inv = pow(int(r[pc]), self.p - 2, self.p)
                v = (v - (int(v[pc]) * inv) * r) % self.p
        return v

    def insert(self, v):
        """Reduce and insert if independent, maintaining full RREF."""
        v = self.reduce(v)
        if not v.any():
            return False
        pc = int(np.argmax(v != 0))
        inv = pow(int(v[pc]), self.p - 2, self.p)
        v = (v * inv) % self.p
        # back-reduce existing rows against the new pivot
        for i, r in enumerate(self.rows):
            if r[pc]:
                self.rows[i] = (r - int(r[pc]) * v) % self.p
        self.rows.append(v)
        self.rows.sort(key=lambda r: int(np.argmax(r != 0)))
        return True


class System:
    """Forms + elimination in both fields + injectivity check."""

    MAXV = 24

    def __init__(self):
        self.elims = [FieldElim(p, self.MAXV) for p in PRIMES]
        self.forms = {}    # canonical letter -> integer vector mod N
        self.nvars = 0

    def copy(self):
        s = System()
        s.elims = [e.copy() for e in self.elims]
        s.forms = {c: v.copy() for c, v in self.forms.items()}
        s.nvars = self.nvars
        return s

    def new_letter_free(self, c):
        v = np.zeros(self.MAXV, dtype=np.int64)
        v[self.nvars] = 1
        self.nvars += 1
        self.forms[c] = v

    def new_letter_forced(self, c, f):
        self.forms[c] = f % N

    def add_equation(self, v):
        for e in self.elims:
            e.insert(v)

    def forced_equal(self, a, b):
        d = (self.forms[a] - self.forms[b]) % N
        for e in self.elims:
            if e.reduce(d).any():
                return False
        return True

    def injectivity_ok(self):
        # any pair of distinct letters with forms forced equal in BOTH
        # fields kills injectivity
        letters = list(self.forms)
        reduced = {}
        for c in letters:
            key = tuple(
                int(x) for e in self.elims for x in e.reduce(self.forms[c])
            )
            if key in reduced:
                return False
            reduced[key] = c
        return True


def search_k(k, depth, maxnodes=3_000_000, num=21, den=20, first_only=True,
             log=None, m=1):
    """m: multiplier of the affine morphism phi(x) = m*x + B0 (gcd(m,N)=1);
    fixed point satisfies W[q] = m*W[q//k] + W[q%k]."""
    inc = UInc(num, den, depth + 2)
    C = []
    nodes = 0
    reached = 0
    survivors = []

    sys0 = System()

    def reduced_zero(S, d):
        d = d % N
        if not d.any():
            return True
        return all(not e.reduce(d).any() for e in S.elims)

    def rec(used, S):
        nonlocal nodes, reached
        q = len(C)
        reached = max(reached, q)
        if q == depth:
            survivors.append((list(C), S))
            return first_only
        if nodes >= maxnodes:
            return True
        f = None
        pinned = None
        if q >= k:
            f = (m * S.forms[C[q // k]] + S.forms[C[q % k]]) % N
            for c in range(min(used, N)):
                if reduced_zero(S, S.forms[c] - f):
                    pinned = c
                    break
        if pinned is not None:
            cands = [pinned]
        else:
            cands = list(range(min(used + 1, N)))
        for c in cands:
            nodes += 1
            fresh = c == used
            S2 = S
            if q == 0:
                S2 = S.copy()
                S2.new_letter_free(c)
                S2.add_equation(S2.forms[c].copy())  # x_{C[0]} = 0
                if not S2.injectivity_ok():
                    continue
            elif f is not None and pinned is None:
                if fresh:
                    S2 = S.copy()
                    S2.new_letter_forced(c, f)
                else:
                    d = (S.forms[c] - f) % N
                    if not reduced_zero(S, d):
                        S2 = S.copy()
                        S2.add_equation(d)
                if S2 is not S and not S2.injectivity_ok():
                    continue
            elif f is None and fresh and q < k:
                S2 = S.copy()
                S2.new_letter_free(c)
                if not S2.injectivity_ok():
                    continue
            if inc.push(c):
                C.append(c)
                stop = rec(used + 1 if fresh else used, S2)
                C.pop()
                inc.pop()
                if stop:
                    return True
            else:
                inc.pop()
        return False

    t0 = time.time()
    rec(0, sys0)
    dt = time.time() - t0
    return survivors, reached, nodes, dt


def concretize(C, S, k):
    """Enumerate concrete nu assignments (both fields' nullspaces, CRT),
    return list of B0 tuples that are injective on letters of C."""
    import itertools
    letters = sorted(set(C))
    Vn = S.nvars
    sols = []
    per_field = []
    for e, p in zip(S.elims, PRIMES):
        # free columns = those without pivot among first Vn columns
        pivots = {int(np.argmax(r != 0)) for r in e.rows}
        freecols = [j for j in range(Vn) if j not in pivots]
        per_field.append((e, p, freecols))
        if len(freecols) > 6 and p == 11:
            return []  # too many; caller should extend depth
    f2 = per_field[0]
    f11 = per_field[1]

    def field_solutions(e, p, freecols):
        outs = []
        for vals in itertools.product(range(p), repeat=len(freecols)):
            x = np.zeros(S.MAXV, dtype=np.int64)
            for j, v in zip(freecols, vals):
                x[j] = v
            # back-substitute rows (rows sorted by pivot; go reverse)
            for r in reversed(e.rows):
                pc = int(np.argmax(r != 0))
                s = int((r @ x - r[pc] * x[pc]) % p)
                x[pc] = (-s * pow(int(r[pc]), p - 2, p)) % p
            outs.append(x % p)
        return outs

    s2 = field_solutions(*f2)
    s11 = field_solutions(*f11)
    for x2 in s2:
        for x11 in s11:
            # CRT combine: value = 11*(x2*inv11mod2) + 2*(x11*inv2mod11)
            x = (11 * (x2 % 2) * 1 + 2 * (x11 * 6)) % N  # 2*6=12=1 mod 11
            vals = {}
            ok = True
            for c in letters:
                v = int((S.forms[c] @ x) % N)
                if v in vals.values():
                    ok = False
                    break
                vals[c] = v
            if ok and vals.get(C[0], None) == 0:
                B0 = tuple(vals[C[j]] for j in range(k))
                sols.append((B0, vals))
    return sols


if __name__ == "__main__":
    kmin, kmax, depth = map(int, sys.argv[1:4])
    maxnodes = int(sys.argv[4]) if len(sys.argv) > 4 else 3_000_000
    for k in range(kmin, kmax + 1):
        surv, reached, nodes, dt = search_k(k, depth)
        msg = f"k={k}: reach {reached}/{depth}, {nodes} nodes [{dt:.1f}s]"
        if surv:
            C, S = surv[0]
            sols = concretize(C, S, k)
            msg += f"  SURVIVOR (concrete nu: {len(sols)})"
            with open(f"data/affine_n22_k{k}.txt", "w") as fh:
                fh.write("C=" + ",".join(map(str, C)) + "\n")
                for B0, vals in sols[:50]:
                    fh.write("B0=" + ",".join(map(str, B0)) + "\n")
        print(msg, flush=True)
