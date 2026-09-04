#!/usr/bin/env python3
"""
Signotope SAT encoding for the maximum number of (bounded, triangular) faces in a
simple Euclidean arrangement of n pseudolines -- the quantity a^s_3(n) of
Bartholdi-Blanc-Loisel (2008) and, for straight lines, the Kobon triangle number.

Model.  A simple Euclidean pseudoline arrangement with lines labelled 1..n by their
vertical order at x = -infinity (bottom to top) is encoded by a rank-3 signotope
(Felsner-Weil 2001): a sign sigma(i,j,k) for every i<j<k, with the axiom that for every
a<b<c<d the sequence sigma(abc), sigma(abd), sigma(acd), sigma(bcd) has at most one
sign change.  Semantics used here: sigma(ijk) = + iff line j passes ABOVE the crossing
point of lines i and k.  Consequently, for any line r and two other lines a<b,
        "a crosses r before b (left to right)"  <=>  sigma(sorted{r,a,b}) = -   (*)
(checked for r the bottom, middle and top line of the triple; see NOTE.md).

A bounded triangular face with sides on lines i<j<k exists iff the crossings with j and k
are adjacent along i, the crossings with i and k adjacent along j, and the crossings with
i and j adjacent along k (no fourth line can enter a bounded region without crossing its
boundary).

Variables: sigma(i,j,k); Adj(r;{a,b}) -> "no other line crosses r between a and b";
T(i,j,k) -> Adj(i;{j,k}) & Adj(j;{i,k}) & Adj(k;{i,j}); cardinality sum T >= t.
Only the implication directions needed for soundness are emitted by default:
a model yields a genuine arrangement with >= t triangles, and any arrangement with >= t
triangles yields a model.  --full adds the converse implications (redundant, may help).

Symmetry breaking (--symbreak): rotation by 180 degrees is the global sign flip, so
sigma(1,2,3) = - is forced; reflection in a horizontal axis is the label reversal
i -> n+1-i with sign flip, and its composition with the rotation is the plain label
reversal; both are broken by lex-leader prefix constraints (Crawford et al. style).
"""
import argparse
import itertools
import sys

from pysat.card import CardEnc, EncType
from pysat.formula import CNF


class Encoder:
    def __init__(self, n, tmin=None, full=False, symbreak=True, lexdepth=40, card='totalizer'):
        self.n = n
        self.nv = 0
        self.clauses = []
        self.sig = {}
        self.adj = {}
        self.tri = {}
        L = range(1, n + 1)
        for t in itertools.combinations(L, 3):
            self.sig[t] = self.new()
        self.nsig = self.nv
        # --- signotope axiom -------------------------------------------------
        for a, b, c, d in itertools.combinations(L, 4):
            s = [self.sig[(a, b, c)], self.sig[(a, b, d)], self.sig[(a, c, d)], self.sig[(b, c, d)]]
            for p, q, r in itertools.combinations(range(4), 3):
                # forbid s_p = s_r != s_q
                self.clauses.append([-s[p], s[q], -s[r]])
                self.clauses.append([s[p], -s[q], s[r]])
        # --- adjacency / segment variables ------------------------------------
        for r in L:
            others = [x for x in L if x != r]
            for a, b in itertools.combinations(others, 2):
                v = self.new()
                self.adj[(r, a, b)] = v
                for l in others:
                    if l == a or l == b:
                        continue
                    # l between a and b along r  (a before l before b, or b before l before a)
                    self.clauses.append([-v, -self.before(r, a, l), -self.before(r, l, b)])
                    self.clauses.append([-v, -self.before(r, b, l), -self.before(r, l, a)])
                if full:
                    # (no l between) -> Adj :  Adj or OR_l Bt_l ; Bt_l -> between
                    bts = []
                    for l in others:
                        if l == a or l == b:
                            continue
                        p1 = self.new()  # a before l before b
                        p2 = self.new()  # b before l before a
                        self.clauses.append([-p1, self.before(r, a, l)])
                        self.clauses.append([-p1, self.before(r, l, b)])
                        self.clauses.append([-p2, self.before(r, b, l)])
                        self.clauses.append([-p2, self.before(r, l, a)])
                        bts += [p1, p2]
                    self.clauses.append([v] + bts)
        # --- triangle variables ---------------------------------------------
        for i, j, k in itertools.combinations(L, 3):
            v = self.new()
            self.tri[(i, j, k)] = v
            a1, a2, a3 = self.adj[(i, j, k)], self.adj[(j, i, k)], self.adj[(k, i, j)]
            self.clauses.append([-v, a1])
            self.clauses.append([-v, a2])
            self.clauses.append([-v, a3])
            if full:
                self.clauses.append([v, -a1, -a2, -a3])
        # --- symmetry breaking ------------------------------------------------
        if symbreak and n >= 3:
            self.clauses.append([-self.sig[(1, 2, 3)]])
            if n >= 4:
                self.lex_leader(lambda t: (self.sig[self.rev(t)], True), lexdepth)   # rev
                self.lex_leader(lambda t: (self.sig[self.rev(t)], False), lexdepth)  # rev o flip
        # --- cardinality ------------------------------------------------------
        self.tmin = tmin
        if tmin is not None:
            lits = [self.tri[t] for t in sorted(self.tri)]
            enc = {'totalizer': EncType.totalizer, 'seqcounter': EncType.seqcounter,
                   'sortnetwrk': EncType.sortnetwrk, 'cardnetwrk': EncType.cardnetwrk,
                   'kmtotalizer': EncType.kmtotalizer, 'mtotalizer': EncType.mtotalizer}[card]
            if tmin > len(lits):
                v = self.new()          # trivially unsatisfiable: more triangles than triples
                self.clauses += [[v], [-v]]
            elif tmin > 0:
                cnf = CardEnc.atleast(lits=lits, bound=tmin, top_id=self.nv, encoding=enc)
                self.clauses += cnf.clauses
                self.nv = max(self.nv, cnf.nv)

    def new(self):
        self.nv += 1
        return self.nv

    def rev(self, t):
        n = self.n
        return tuple(sorted(n + 1 - x for x in t))

    def before(self, r, a, b):
        """literal: 'a crosses r before b' (a != b, both != r)."""
        s = self.sig[tuple(sorted((r, a, b)))]
        return -s if a < b else s

    def lex_leader(self, image, depth):
        """x <=_lex g(x) on the first `depth` sigma variables (sorted-triple order).
        image(t) -> (var, same_sign): g maps sigma(t) to var (if same_sign) or -var."""
        triples = sorted(self.sig)[:depth]
        e_prev = None
        for t in triples:
            x = self.sig[t]
            v, same = image(t)
            y = v if same else -v
            if x == y:
                continue
            # if equal so far: x <= y
            cl = [-x, y]
            if e_prev is not None:
                cl = [-e_prev] + cl
            self.clauses.append(cl)
            e = self.new()
            # e_prev & (x == y) -> e
            base = [] if e_prev is None else [-e_prev]
            self.clauses.append(base + [-x, -y, e])
            self.clauses.append(base + [x, y, e])
            e_prev = e

    def write(self, path, comment=''):
        with open(path, 'w') as f:
            if comment:
                for line in comment.splitlines():
                    f.write('c ' + line + '\n')
            f.write(f'p cnf {self.nv} {len(self.clauses)}\n')
            for c in self.clauses:
                f.write(' '.join(map(str, c)) + ' 0\n')

    # ---- decoding --------------------------------------------------------
    def decode(self, model):
        """Return sigma dict {(i,j,k): +1/-1} from a model (list of ints)."""
        pos = set(l for l in model if l > 0)
        return {t: (1 if v in pos else -1) for t, v in self.sig.items()}


# ---------------------------------------------------------------------------
# Independent (encoding-free) analysis of a signotope
# ---------------------------------------------------------------------------
def check_signotope(n, sigma):
    for a, b, c, d in itertools.combinations(range(1, n + 1), 4):
        s = [sigma[(a, b, c)], sigma[(a, b, d)], sigma[(a, c, d)], sigma[(b, c, d)]]
        changes = sum(1 for p in range(3) if s[p] != s[p + 1])
        if changes > 1:
            return False
    return True


def local_sequences(n, sigma):
    """Order of crossings along each line, from (*).  Also verifies that the induced
    'before' relation is a strict total order on each line."""
    seqs = {}
    for r in range(1, n + 1):
        others = [x for x in range(1, n + 1) if x != r]

        def before(a, b):
            s = sigma[tuple(sorted((r, a, b)))]
            return (s == -1) if a < b else (s == 1)

        # transitivity check
        for a, b, c in itertools.permutations(others, 3):
            if before(a, b) and before(b, c) and not before(a, c):
                raise ValueError(f'before-relation on line {r} is not transitive')
        import functools
        seqs[r] = sorted(others, key=functools.cmp_to_key(lambda a, b: -1 if before(a, b) else 1))
    return seqs


def wiring_sweep(n, seqs):
    """Realise the local sequences as a wiring diagram by a left-to-right sweep.
    Returns the list of swaps (p,q) in sweep order, or raises if stuck."""
    order = list(range(1, n + 1))          # bottom to top
    ptr = {r: 0 for r in range(1, n + 1)}
    swaps = []
    total = n * (n - 1) // 2
    while len(swaps) < total:
        done = False
        for pos in range(n - 1):
            p, q = order[pos], order[pos + 1]
            if ptr[p] < n - 1 and ptr[q] < n - 1 and seqs[p][ptr[p]] == q and seqs[q][ptr[q]] == p:
                order[pos], order[pos + 1] = q, p
                ptr[p] += 1
                ptr[q] += 1
                swaps.append((p, q))
                done = True
                break
        if not done:
            raise ValueError('sweep stuck: local sequences not realisable')
    assert order == list(range(n, 0, -1))
    return swaps


def triangles(n, seqs):
    """Triangular faces = triples pairwise adjacent along all three lines."""
    idx = {r: {x: p for p, x in enumerate(seqs[r])} for r in seqs}
    tris = []
    for i, j, k in itertools.combinations(range(1, n + 1), 3):
        if (abs(idx[i][j] - idx[i][k]) == 1 and abs(idx[j][i] - idx[j][k]) == 1
                and abs(idx[k][i] - idx[k][j]) == 1):
            tris.append((i, j, k))
    return tris


def faces_from_sweep(n, swaps):
    """Independent triangle count: build the planar cell structure of the wiring diagram
    from the sweep and count bounded faces with exactly three sides.
    Faces are tracked as the gaps between adjacent wires; each swap closes the face
    between the two swapped wires and opens a new one."""
    # face between positions pos and pos+1 ; record number of vertices on its boundary
    # Represent each bounded face by the list of crossing events on its boundary.
    order = list(range(1, n + 1))
    # gaps[g] = (creation_event_index or None if unbounded-left, side_count)
    gaps = [None] * (n - 1)   # None: unbounded (left side open)
    bounded = []
    posof = {r: p for p, r in enumerate(order)}
    for ev, (p, q) in enumerate(swaps):
        pos = posof[p]
        assert order[pos] == p and order[pos + 1] == q
        # gap `pos` (between p and q) is closed by this crossing
        g = gaps[pos]
        if g is not None:
            bounded.append(g['edges'])
        # neighbouring gaps gain a vertex: gap pos-1 (between order[pos-1] and p) and gap pos+1
        if pos - 1 >= 0 and gaps[pos - 1] is not None:
            gaps[pos - 1]['edges'] += 1
        if pos + 1 < n - 1 and gaps[pos + 1] is not None:
            gaps[pos + 1]['edges'] += 1
        order[pos], order[pos + 1] = q, p
        posof[p], posof[q] = pos + 1, pos
        gaps[pos] = {'edges': 2}   # new face: two edges (one on p, one on q) so far
    # at the end all gaps are unbounded on the right
    return bounded


def analyse(n, sigma):
    assert check_signotope(n, sigma)
    seqs = local_sequences(n, sigma)
    swaps = wiring_sweep(n, seqs)
    tris = triangles(n, seqs)
    faces = faces_from_sweep(n, swaps)
    ntri_faces = sum(1 for e in faces if e == 3)
    return seqs, swaps, tris, ntri_faces


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('tmin', type=int)
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--nosym', action='store_true')
    ap.add_argument('--lexdepth', type=int, default=40)
    ap.add_argument('--card', default='totalizer')
    a = ap.parse_args()
    E = Encoder(a.n, a.tmin, full=a.full, symbreak=not a.nosym, lexdepth=a.lexdepth, card=a.card)
    E.write(a.out, comment=f'kobon_sat n={a.n} tmin={a.tmin} full={a.full} sym={not a.nosym} '
                            f'lexdepth={a.lexdepth} card={a.card} nsig={E.nsig}')
    print(f'n={a.n} tmin={a.tmin}: {E.nv} vars, {len(E.clauses)} clauses -> {a.out}')
