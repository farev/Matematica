#!/usr/bin/env python3
"""
SEARCH model (v3) for Kobon arrangements WITH triple points (no parallels, no 4-fold points).

A pseudoline arrangement whose only degeneracies are triple points is obtained from a simple
arrangement by collapsing a set of pairwise vertex-disjoint triangular faces (perturb each
triple point locally into a small triangle; conversely shrinking a triangular face to a point
keeps every pair of pseudolines crossing exactly once).  Collapsing a triangular face T
contracts its three sides; a face sharing an edge with T loses one side, so a quadrilateral
with exactly one collapsed edge-neighbour becomes a triangle (a pentagon with two, a hexagon
with three, likewise).  Vertex-disjointness of the collapsed set already forbids a
quadrilateral with two collapsed neighbours (they would share a vertex), so no digons arise.

This encoder counts:   surviving triangular faces  +  promoted quadrilaterals   >= t.
Promotions of pentagons and hexagons are NOT modelled, so the model is INCOMPLETE: a SAT
model is a genuine arrangement with >= t triangles (sound), an UNSAT answer proves nothing.
Use it as a construction search only.

Variables (on top of the v2 signotope/adjacency core, full Adj equivalence):
  T(ijk)  <-> Adj(i;{j,k}) & Adj(j;{i,k}) & Adj(k;{i,j})        (triangular face)
  C(ijk)   -> T(ijk); C(abc) & C(abd) forbidden for triples sharing two lines (vertex-disjoint)
  G(ijk)   -> T(ijk) & ~C(ijk)                                    (surviving triangle)
  Q(x,w,y,z) -> Adj(x;{z,w}) & Adj(w;{x,y}) & Adj(y;{w,z}) & Adj(z;{y,x})   (quadrilateral face,
              cyclic order x,w,y,z; three cyclic orders per 4-set)
  N(Q,edge)  -> Q & C(edge-triangle)      where the edge on line w between x and y has the
              triangle (x,w,y) as its other face
  sum G + sum N >= t.
"""
import argparse
import itertools
import os
import sys

from pysat.card import CardEnc, EncType

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kobon_sat2 import Encoder2


class Encoder3(Encoder2):
    def __init__(self, n, tmin, symbreak=False, card='kmtotalizer', max_collapse=None):
        # core without any budget/cardinality; flip-only symmetry breaking
        super().__init__(n, None, symbreak=False, tight=False)
        self.clauses.append([-self.sig[(1, 2, 3)]])
        L = range(1, n + 1)
        self.tri, self.col, self.sur, self.quad, self.prom = {}, {}, {}, {}, {}
        for i, j, k in itertools.combinations(L, 3):
            t = self.new()
            self.tri[(i, j, k)] = t
            a1, a2, a3 = self.adj[(i, j, k)], self.adj[(j, i, k)], self.adj[(k, i, j)]
            self.clauses += [[-t, a1], [-t, a2], [-t, a3], [t, -a1, -a2, -a3]]
            c = self.new()
            self.col[(i, j, k)] = c
            self.clauses.append([-c, t])
            g = self.new()
            self.sur[(i, j, k)] = g
            self.clauses += [[-g, t], [-g, -c]]
        # vertex-disjointness of collapsed triangles
        for (a, b) in itertools.combinations(L, 2):
            others = [x for x in L if x not in (a, b)]
            ts = [self.col[tuple(sorted((a, b, x)))] for x in others]
            for u, v in itertools.combinations(ts, 2):
                self.clauses.append([-u, -v])
        # quadrilateral faces and promotions
        for S in itertools.combinations(L, 4):
            a, b, c, d = S
            for cyc in ((a, b, c, d), (a, b, d, c), (a, c, b, d)):
                q = self.new()
                self.quad[cyc] = q
                for idx in range(4):
                    w = cyc[idx]
                    x, y = cyc[idx - 1], cyc[(idx + 1) % 4]
                    self.clauses.append([-q, self.adj[(w,) + tuple(sorted((x, y)))]])
                for idx in range(4):
                    w = cyc[idx]
                    x, y = cyc[idx - 1], cyc[(idx + 1) % 4]
                    p = self.new()
                    self.prom[(cyc, idx)] = p
                    self.clauses += [[-p, q], [-p, self.col[tuple(sorted((x, w, y)))]]]
        self.tmin = tmin
        lits = list(self.sur.values()) + list(self.prom.values())
        enc = {'totalizer': EncType.totalizer, 'seqcounter': EncType.seqcounter,
               'kmtotalizer': EncType.kmtotalizer}[card]
        cnf = CardEnc.atleast(lits=lits, bound=tmin, top_id=self.nv, encoding=enc)
        self.clauses += cnf.clauses
        self.nv = max(self.nv, cnf.nv)
        if max_collapse is not None:
            cnf = CardEnc.atmost(lits=list(self.col.values()), bound=max_collapse, top_id=self.nv,
                                 encoding=EncType.seqcounter)
            self.clauses += cnf.clauses
            self.nv = max(self.nv, cnf.nv)

    def decode_full(self, model):
        pos = set(l for l in model if l > 0)
        sigma = {t: (1 if v in pos else -1) for t, v in self.sig.items()}
        collapsed = [t for t, v in self.col.items() if v in pos]
        promoted = [(cyc, idx) for (cyc, idx), v in self.prom.items() if v in pos]
        surviving = [t for t, v in self.sur.items() if v in pos]
        return sigma, collapsed, promoted, surviving


def independent_check(n, sigma, collapsed, promoted):
    """Recount from the definition using only the local sequences derived from sigma."""
    from kobon_sat import local_sequences, triangles
    seqs = local_sequences(n, sigma)
    idx = {r: {x: p for p, x in enumerate(seqs[r])} for r in seqs}

    def adjacent(r, a, b):
        return abs(idx[r][a] - idx[r][b]) == 1
    tris = set(triangles(n, seqs))
    for t in collapsed:
        assert t in tris, f'collapsed {t} is not a triangular face'
    for t1, t2 in itertools.combinations(collapsed, 2):
        assert len(set(t1) & set(t2)) < 2, f'collapsed triangles {t1} {t2} share a vertex'
    new = set()
    for cyc, i in promoted:
        w, x, y = cyc[i], cyc[i - 1], cyc[(i + 1) % 4]
        for j in range(4):
            ww, xx, yy = cyc[j], cyc[j - 1], cyc[(j + 1) % 4]
            assert adjacent(ww, xx, yy), f'{cyc} is not a quadrilateral face'
        assert tuple(sorted((x, w, y))) in collapsed, f'promotion {cyc},{i} without collapsed neighbour'
        new.add(frozenset(cyc))
    surviving = [t for t in tris if t not in set(collapsed)]
    return len(surviving), len(new), len(surviving) + len(new)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('tmin', type=int)
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--card', default='kmtotalizer')
    ap.add_argument('--maxcol', type=int, default=None)
    a = ap.parse_args()
    E = Encoder3(a.n, a.tmin, card=a.card, max_collapse=a.maxcol)
    E.write(a.out, comment=f'kobon_sat3 n={a.n} tmin={a.tmin} card={a.card} maxcol={a.maxcol} nsig={E.nsig}')
    print(f'n={a.n} tmin={a.tmin}: {E.nv} vars, {len(E.clauses)} clauses -> {a.out}')
