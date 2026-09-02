#!/usr/bin/env python3
"""
Segment-budget SAT encoding (v2) for the maximum number of triangular faces in a simple
Euclidean arrangement of n pseudolines (a^s_3(n) of Bartholdi-Blanc-Loisel 2008).

Same signotope core as kobon_sat.py (sigma(ijk) = + iff line j passes above the crossing
of lines i and k; "a crosses r before b" <=> sigma(sorted{r,a,b}) = -), but the objective is
expressed through SEGMENTS instead of a global triangle count:

  * every line carries exactly n-2 bounded segments, one per adjacent pair of crossings;
    n(n-2) segments in total;
  * a segment is a side of at most one triangle, and a triangle has three sides, so
        #triangles >= t   <=>   #unused segments <= n(n-2) - 3t;
  * the segment {a,b} on line r is USED iff, in addition, a and b are adjacent to r on lines
    a and b respectively (then i<j<k pairwise adjacent = a triangular face; no fourth line
    can enter a bounded region without crossing its boundary).

Variables: sigma(ijk); Adj(r;{a,b}) <-> no other line crosses r between a and b (full
equivalence via auxiliary conjunction variables); U(r;{a,b}) "segment exists and is unused":
      U -> Adj,   Adj & ~U -> Adj(a;{r,b}),   Adj & ~U -> Adj(b;{r,a}),
      Adj(r;{a,b}) & Adj(a;{r,b}) & Adj(b;{r,a}) -> ~U;
and  sum U <= budget  (pysat sequential counter / totalizer).

Soundness.  (SAT side) a model is a genuine arrangement (signotope theorem); Adj equals real
adjacency (both directions encoded); every real segment not marked U has its two partner
adjacencies, hence is a real triangle side; so at most `budget` real segments are unused and
the arrangement has >= t triangles.  (UNSAT side) any arrangement with >= t triangles gives
a model: sigma from the arrangement, Adj = real adjacency, U = real unused segments.

Symmetry breaking: the dihedral group of order 4n of kobon_sym.py (re-sweeping + mirror),
validated exhaustively for n <= 7 there; lex-leader constraints on a prefix of the sigma
variables, plus sigma(1,2,3) = - (the 180-degree rotation is the global sign flip).
"""
import argparse
import itertools
import os
import sys

from pysat.card import CardEnc, EncType

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kobon_sym import group  # noqa: E402


class Encoder2:
    def __init__(self, n, tmin, symbreak=True, lexdepth=60, card='seqcounter', budget=None, tight=False, t2=True):
        self.n = n
        self.nv = 0
        self.clauses = []
        self.sig, self.adj, self.uns = {}, {}, {}
        self.tight = tight
        self.t2 = t2   # include the (T2) extreme-endpoint clauses (only with tight=True)
        L = range(1, n + 1)
        for t in itertools.combinations(L, 3):
            self.sig[t] = self.new()
        self.nsig = self.nv
        for a, b, c, d in itertools.combinations(L, 4):
            s = [self.sig[(a, b, c)], self.sig[(a, b, d)], self.sig[(a, c, d)], self.sig[(b, c, d)]]
            for p, q, r in itertools.combinations(range(4), 3):
                self.clauses.append([-s[p], s[q], -s[r]])
                self.clauses.append([s[p], -s[q], s[r]])
        # adjacency with full equivalence
        for r in L:
            others = [x for x in L if x != r]
            for a, b in itertools.combinations(others, 2):
                v = self.new()
                self.adj[(r, a, b)] = v
                bts = []
                for l in others:
                    if l == a or l == b:
                        continue
                    self.clauses.append([-v, -self.before(r, a, l), -self.before(r, l, b)])
                    self.clauses.append([-v, -self.before(r, b, l), -self.before(r, l, a)])
                    p1 = self.new()
                    p2 = self.new()
                    self.clauses.append([-p1, self.before(r, a, l)])
                    self.clauses.append([-p1, self.before(r, l, b)])
                    self.clauses.append([-p2, self.before(r, b, l)])
                    self.clauses.append([-p2, self.before(r, l, a)])
                    bts += [p1, p2]
                self.clauses.append([v] + bts)
        # unused-segment variables
        for r in L:
            others = [x for x in L if x != r]
            for a, b in itertools.combinations(others, 2):
                u = self.new()
                self.uns[(r, a, b)] = u
                A = self.adj[(r, a, b)]
                A1 = self.adj[(a,) + tuple(sorted((r, b)))]
                A2 = self.adj[(b,) + tuple(sorted((r, a)))]
                self.clauses.append([-u, A])
                self.clauses.append([-A, u, A1])
                self.clauses.append([-A, u, A2])
                self.clauses.append([-A, -A1, -A2, -u])
        if symbreak and n >= 3:
            self.clauses.append([-self.sig[(1, 2, 3)]])
            G = group(n)
            for key, m in G.items():
                if key == (0, 0):
                    continue
                self.lex_leader(m, lexdepth)
        self.tmin = tmin
        self.budget = budget if budget is not None else (n * (n - 2) - 3 * tmin if tmin is not None else None)
        if tight:
            self.add_tight()
        if self.budget is not None:
            lits = [self.uns[t] for t in sorted(self.uns)]
            if self.budget < 0:
                v = self.new()
                self.clauses += [[v], [-v]]
            elif self.budget < len(lits):
                enc = {'seqcounter': EncType.seqcounter, 'totalizer': EncType.totalizer,
                       'cardnetwrk': EncType.cardnetwrk, 'sortnetwrk': EncType.sortnetwrk,
                       'kmtotalizer': EncType.kmtotalizer, 'mtotalizer': EncType.mtotalizer}[card]
                cnf = CardEnc.atmost(lits=lits, bound=self.budget, top_id=self.nv, encoding=enc)
                self.clauses += cnf.clauses
                self.nv = max(self.nv, cnf.nv)

    def new(self):
        self.nv += 1
        return self.nv

    def before(self, r, a, b):
        s = self.sig[tuple(sorted((r, a, b)))]
        return -s if a < b else s

    def add_tight(self):
        """Redundant clauses valid ONLY when t = n(n-7/3)/3 is an integer attained exactly
        (n = 18: t = 94, budget 6).  From Bartholdi-Blanc-Loisel's proof of Theorem 1.1:
        a perfect line L (all n-2 segments used) has an unused segment on the line through
        one of its two extreme crossings, starting at that crossing; a segment can serve at
        most two perfect lines.  With m perfect lines: used <= n(n-3)+m and unused >= m/2.
        At n = 18, used = 282 forces m >= 12 and m <= 12, so:
          (T1) exactly 12 perfect lines, the other 6 have exactly one unused segment;
          (T2) every unused segment {L,X} on line N has L and X perfect and the crossings
               N∩L, N∩X extreme (first or last) on L and on X respectively.
        Encoded as implications only (sound: any 94-arrangement supplies witnesses)."""
        n, L = self.n, range(1, self.n + 1)
        # t = n(3n-7)/9 exactly  <=>  9t = n(3n-7);  then budget = n(n-2) - 3t = n/3
        assert n % 2 == 0 and 9 * self.tmin == n * (3 * n - 7) and 3 * self.budget == n, \
            'tight constraints only apply when t = n(n-7/3)/3 exactly (even n)'
        perf = {}
        for r in L:
            p = self.new()
            perf[r] = p
            others = [x for x in L if x != r]
            segs = [self.uns[(r, a, b)] for a, b in itertools.combinations(others, 2)]
            for u in segs:
                self.clauses.append([-p, -u])
            # (T1) at most one unused segment per line
            cnf = CardEnc.atmost(lits=segs, bound=1, top_id=self.nv, encoding=EncType.seqcounter)
            self.clauses += cnf.clauses
            self.nv = max(self.nv, cnf.nv)
        first, last = {}, {}
        for r in L:
            for a in L:
                if a == r:
                    continue
                f, l = self.new(), self.new()
                first[(r, a)], last[(r, a)] = f, l
                for x in L:
                    if x in (r, a):
                        continue
                    self.clauses.append([-f, self.before(r, a, x)])
                    self.clauses.append([-l, self.before(r, x, a)])
        if self.t2:
            for (N, a, b), u in self.uns.items():
                for Lx in (a, b):
                    self.clauses.append([-u, perf[Lx]])
                    self.clauses.append([-u, first[(Lx, N)], last[(Lx, N)]])
        # (T1) exactly `budget` unused segments in total
        lits = [self.uns[t] for t in sorted(self.uns)]
        cnf = CardEnc.atleast(lits=lits, bound=self.budget, top_id=self.nv, encoding=EncType.seqcounter)
        self.clauses += cnf.clauses
        self.nv = max(self.nv, cnf.nv)

    def lex_leader(self, m, depth):
        """x <=_lex g(x) where (g.sigma)(t) = sign * sigma(old),  m[t] = (old, sign)."""
        triples = sorted(self.sig)[:depth]
        e_prev = None
        for t in triples:
            x = self.sig[t]
            old, sgn = m[t]
            y = self.sig[old] if sgn == 1 else -self.sig[old]
            if x == y:
                continue
            cl = [-x, y]
            if e_prev is not None:
                cl = [-e_prev] + cl
            self.clauses.append(cl)
            e = self.new()
            base = [] if e_prev is None else [-e_prev]
            self.clauses.append(base + [-x, -y, e])
            self.clauses.append(base + [x, y, e])
            e_prev = e

    def write(self, path, comment=''):
        with open(path, 'w') as f:
            for line in comment.splitlines():
                f.write('c ' + line + '\n')
            f.write(f'p cnf {self.nv} {len(self.clauses)}\n')
            for c in self.clauses:
                f.write(' '.join(map(str, c)) + ' 0\n')

    def decode(self, model):
        pos = set(l for l in model if l > 0)
        return {t: (1 if v in pos else -1) for t, v in self.sig.items()}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('tmin', type=int)
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--nosym', action='store_true')
    ap.add_argument('--lexdepth', type=int, default=60)
    ap.add_argument('--card', default='seqcounter')
    ap.add_argument('--tight', action='store_true')
    a = ap.parse_args()
    E = Encoder2(a.n, a.tmin, symbreak=not a.nosym, lexdepth=a.lexdepth, card=a.card, tight=a.tight)
    E.write(a.out, comment=f'kobon_sat2 n={a.n} tmin={a.tmin} budget={E.budget} sym={not a.nosym} '
                            f'lexdepth={a.lexdepth} card={a.card} tight={a.tight} nsig={E.nsig}')
    print(f'n={a.n} tmin={a.tmin} budget={E.budget}: {E.nv} vars, {len(E.clauses)} clauses -> {a.out}')
