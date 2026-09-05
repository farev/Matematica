#!/usr/bin/env python3
"""Feasibility probe: minimum number of ordinary lines of an n-point configuration,
abstracted to rank-3 chirotopes (possibly non-uniform, i.e. collinear triples allowed).

Variables per unordered triple i<j<k:  Z[ijk]  (chi = 0, collinear)
                                       P[ijk]  (chi = +1 if not zero, else -1)
Alternating extension to ordered triples by permutation sign.
Axioms: (B0) some triple nonzero; simple: every pair lies in a nonzero triple;
        (B2') three-term Grassmann-Pluecker relations for every 5-set and apex a:
        { chi(a,b,c)chi(a,d,e), -chi(a,b,d)chi(a,c,e), chi(a,b,e)chi(a,c,d) }
        contains both signs or is all zero.
Ordinary line through i,j:  o[ij] <- AND_k not Z[ijk];  constraint: sum o <= m.

UNSAT => no real configuration of n points has <= m ordinary lines (chirotopes of
real configurations satisfy the axioms).  SAT => abstract witness only.
"""
import sys, itertools, random, time
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


def perm_sign(a, b, c):
    """sign of the permutation sorting (a,b,c); returns (sorted tuple, sign)"""
    s = 1
    x = [a, b, c]
    # bubble sort with sign tracking
    for i in range(3):
        for j in range(2 - i):
            if x[j] > x[j + 1]:
                x[j], x[j + 1] = x[j + 1], x[j]
                s = -s
    return tuple(x), s


def numeric_gp_selfcheck(trials=2000):
    """check the 3-term GP identity on random integer points (homogeneous coords)."""
    rnd = random.Random(1)
    def det(p, q, r):
        return (p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0])
                + p[2] * (q[0] * r[1] - q[1] * r[0]))
    for _ in range(trials):
        pts = [tuple(rnd.randint(-9, 9) for _ in range(3)) for _ in range(5)]
        a, b, c, d, e = pts
        val = det(a, b, c) * det(a, d, e) - det(a, b, d) * det(a, c, e) + det(a, b, e) * det(a, c, d)
        assert val == 0, val
    return True


class Encoder:
    def __init__(self, n, m, card=EncType.seqcounter):
        self.n, self.m = n, m
        self.pool = IDPool()
        self.cnf = CNF()
        self.Z = {}
        self.P = {}
        for t in itertools.combinations(range(n), 3):
            self.Z[t] = self.pool.id(('Z',) + t)
            self.P[t] = self.pool.id(('P',) + t)
        self.build(card)

    def chi_lits(self, a, b, c):
        """return (zvar, pvar, sign) so that chi(a,b,c) = 0 if Z else sign*(+1 if P else -1)"""
        t, s = perm_sign(a, b, c)
        return self.Z[t], self.P[t], s

    def build(self, card):
        n, cnf, pool = self.n, self.cnf, self.pool
        # simple matroid: every pair in some nonzero triple (also implies B0)
        for i, j in itertools.combinations(range(n), 2):
            cnf.append([-self.Z[tuple(sorted((i, j, k)))] for k in range(n) if k not in (i, j)])
        # GP relations
        ngp = 0
        for five in itertools.combinations(range(n), 5):
            for a in five:
                rest = [x for x in five if x != a]
                w, x, y, z = rest
                terms = [((a, w, x), (a, y, z), +1), ((a, w, y), (a, x, z), -1), ((a, w, z), (a, x, y), +1)]
                pos, neg = [], []
                for (t1, t2, sgn) in terms:
                    z1, p1, s1 = self.chi_lits(*t1)
                    z2, p2, s2 = self.chi_lits(*t2)
                    # product sign = sgn*s1*s2 * (P1?+1:-1)*(P2?+1:-1)
                    fixed = sgn * s1 * s2
                    pv = pool.id()
                    nv = pool.id()
                    pos.append(pv); neg.append(nv)
                    # pv <-> !z1 & !z2 & (P1 == P2 if fixed>0 else P1 != P2)
                    # nv <-> !z1 & !z2 & (P1 != P2 if fixed>0 else P1 == P2)
                    for v in (pv, nv):
                        cnf.append([-v, -z1]); cnf.append([-v, -z2])
                    if fixed > 0:
                        # pv -> P1==P2 ; nv -> P1!=P2
                        cnf.append([-pv, -p1, p2]); cnf.append([-pv, p1, -p2])
                        cnf.append([-nv, p1, p2]); cnf.append([-nv, -p1, -p2])
                        # (!z1 & !z2 & P1==P2) -> pv ; (!z1 & !z2 & P1!=P2) -> nv
                        cnf.append([z1, z2, -p1, -p2, pv]); cnf.append([z1, z2, p1, p2, pv])
                        cnf.append([z1, z2, -p1, p2, nv]); cnf.append([z1, z2, p1, -p2, nv])
                    else:
                        cnf.append([-pv, p1, p2]); cnf.append([-pv, -p1, -p2])
                        cnf.append([-nv, -p1, p2]); cnf.append([-nv, p1, -p2])
                        cnf.append([z1, z2, -p1, p2, pv]); cnf.append([z1, z2, p1, -p2, pv])
                        cnf.append([z1, z2, -p1, -p2, nv]); cnf.append([z1, z2, p1, p2, nv])
                # pos_i -> OR_{j!=i} neg_j ; neg_i -> OR_{j!=i} pos_j
                for i in range(3):
                    cnf.append([-pos[i]] + [neg[j] for j in range(3) if j != i])
                    cnf.append([-neg[i]] + [pos[j] for j in range(3) if j != i])
                ngp += 1
        self.ngp = ngp
        # ordinary-line indicators
        self.O = {}
        for i, j in itertools.combinations(range(n), 2):
            o = pool.id(('O', i, j))
            self.O[(i, j)] = o
            cnf.append([o] + [self.Z[tuple(sorted((i, j, k)))] for k in range(n) if k not in (i, j)])
        if self.m is not None:
            enc = CardEnc.atmost(lits=list(self.O.values()), bound=self.m, vpool=pool, encoding=card)
            cnf.extend(enc.clauses)

    def decode(self, model):
        mset = set(l for l in model if l > 0)
        n = self.n
        coll = [t for t in self.Z if self.Z[t] in mset]
        # lines: closure of pairs
        lines = set()
        for i, j in itertools.combinations(range(n), 2):
            pts = {i, j} | {k for k in range(n) if k not in (i, j) and self.Z[tuple(sorted((i, j, k)))] in mset}
            lines.add(tuple(sorted(pts)))
        ordinary = [L for L in lines if len(L) == 2]
        return coll, sorted(lines, key=lambda L: (-len(L), L)), ordinary


def run(n, m, solver='cadical153', verbose=True):
    t0 = time.time()
    enc = Encoder(n, m)
    t1 = time.time()
    with Solver(name=solver, bootstrap_with=enc.cnf.clauses) as s:
        sat = s.solve()
        model = s.get_model() if sat else None
    t2 = time.time()
    res = {'n': n, 'm': m, 'sat': sat, 'vars': enc.pool.top, 'clauses': len(enc.cnf.clauses),
           'gp': enc.ngp, 'enc_s': t1 - t0, 'solve_s': t2 - t1}
    if verbose:
        print(f"n={n} m={m}: {'SAT' if sat else 'UNSAT'}  vars={res['vars']} clauses={res['clauses']} "
              f"enc {res['enc_s']:.1f}s solve {res['solve_s']:.1f}s", flush=True)
    if sat and verbose:
        coll, lines, ordinary = enc.decode(model)
        big = [L for L in lines if len(L) >= 3]
        print(f"   ordinary lines: {len(ordinary)}; lines with >=3 points: {[len(L) for L in big]}")
        print(f"   {big}")
    return res, enc, model


if __name__ == '__main__':
    assert numeric_gp_selfcheck()
    print("GP identity self-check passed")
    args = sys.argv[1:]
    if len(args) >= 2:
        n, m = int(args[0]), int(args[1])
        run(n, m)
    else:
        # positive/negative controls against known t_2(n) (values to be re-verified from literature):
        # n: 3:3 4:3 5:4 6:3 7:3 8:4 9:6 10:5 11:6 12:6 13:6 14:7
        for n, t in [(5, 4), (6, 3), (7, 3), (8, 4), (9, 6), (10, 5)]:
            run(n, t - 1)
            run(n, t)
