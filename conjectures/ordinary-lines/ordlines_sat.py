#!/usr/bin/env python3
"""ordlines_sat.py -- SAT encoding of "n-point rank-3 configuration (chirotope, collinearities
allowed) with at most m ordinary (2-point) lines", with optional cubes fixing the lines of
size >= 4.

Soundness of the UNSAT direction rests only on: every real point configuration (indeed every
rank-3 oriented matroid) has a chirotope chi: triples -> {-1,0,+1} that is alternating, whose
support is a simple matroid (no loops/parallels), and that satisfies the three-term
Grassmann-Pluecker sign relations for every 5-set and apex.  These are all encoded as
necessary conditions, so UNSAT => no such configuration exists.

Variables (all integers, DIMACS): for i<j<k
    Z[ijk]  chi(i,j,k) == 0     (collinear)
    P[ijk]  chi(i,j,k) == +1 given nonzero
Ordinary-line indicator for i<j:  O[ij], with clause  O[ij] OR Z[ijk] for some k  (so an
ordinary pair forces O[ij] true); cardinality: sum O <= m.
"""
import sys, os, itertools, argparse, subprocess, time, json
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType


def perm_sign(a, b, c):
    s = 1
    x = [a, b, c]
    for i in range(3):
        for j in range(2 - i):
            if x[j] > x[j + 1]:
                x[j], x[j + 1] = x[j + 1], x[j]
                s = -s
    return tuple(x), s


class OrdLinesEncoder:
    def __init__(self, n, m, big_lines=(), exact_big=True, transitivity=True,
                 card=EncType.seqcounter, forbid_sizes=()):
        """
        n: points 0..n-1; m: at most m ordinary lines (None = no bound).
        big_lines: list of point sets; each is forced to be a line (all triples collinear,
                   no outside point collinear with two of its points).
        exact_big: if True, every line not among big_lines has at most 3 points.
        forbid_sizes: additional forbidden line sizes k (encoded as: no k points pairwise
                   collinear with a common pair... implemented only for k=4 via exact_big).
        """
        self.n, self.m = n, m
        self.big_lines = [tuple(sorted(L)) for L in big_lines]
        self.pool = IDPool()
        self.cnf = CNF()
        self.Z, self.P = {}, {}
        for t in itertools.combinations(range(n), 3):
            self.Z[t] = self.pool.id(('Z',) + t)
            self.P[t] = self.pool.id(('P',) + t)
        self.stats = {}
        self._build(exact_big, transitivity, card)

    def z(self, i, j, k):
        return self.Z[tuple(sorted((i, j, k)))]

    def chi(self, a, b, c):
        t, s = perm_sign(a, b, c)
        return self.Z[t], self.P[t], s

    def _build(self, exact_big, transitivity, card):
        n, cnf, pool = self.n, self.cnf, self.pool
        nc0 = len(cnf.clauses)
        # (S) simple: every pair lies in a nonzero triple
        for i, j in itertools.combinations(range(n), 2):
            cnf.append([-self.z(i, j, k) for k in range(n) if k not in (i, j)])
        # (T) transitivity of collinearity (redundant w.r.t. GP, helps propagation):
        # within any 4-set, two collinear triples force the other two.
        if transitivity:
            for q in itertools.combinations(range(n), 4):
                trips = list(itertools.combinations(q, 3))
                for a, b in itertools.combinations(trips, 2):
                    for c in trips:
                        if c != a and c != b:
                            cnf.append([-self.Z[a], -self.Z[b], self.Z[c]])
        self.stats['clauses_simple_trans'] = len(cnf.clauses) - nc0
        nc0 = len(cnf.clauses)
        # (GP) three-term Grassmann-Pluecker sign relations
        ngp = 0
        for five in itertools.combinations(range(n), 5):
            for a in five:
                w, x, y, zz = [v for v in five if v != a]
                terms = [((a, w, x), (a, y, zz), +1), ((a, w, y), (a, x, zz), -1), ((a, w, zz), (a, x, y), +1)]
                pos, neg = [], []
                for (t1, t2, sgn) in terms:
                    z1, p1, s1 = self.chi(*t1)
                    z2, p2, s2 = self.chi(*t2)
                    fixed = sgn * s1 * s2
                    pv, nv = pool.id(), pool.id()
                    pos.append(pv); neg.append(nv)
                    for v in (pv, nv):
                        cnf.append([-v, -z1]); cnf.append([-v, -z2])
                    if fixed > 0:
                        cnf.append([-pv, -p1, p2]); cnf.append([-pv, p1, -p2])
                        cnf.append([-nv, p1, p2]); cnf.append([-nv, -p1, -p2])
                        cnf.append([z1, z2, -p1, -p2, pv]); cnf.append([z1, z2, p1, p2, pv])
                        cnf.append([z1, z2, -p1, p2, nv]); cnf.append([z1, z2, p1, -p2, nv])
                    else:
                        cnf.append([-pv, p1, p2]); cnf.append([-pv, -p1, -p2])
                        cnf.append([-nv, -p1, p2]); cnf.append([-nv, p1, -p2])
                        cnf.append([z1, z2, -p1, p2, pv]); cnf.append([z1, z2, p1, -p2, pv])
                        cnf.append([z1, z2, -p1, -p2, nv]); cnf.append([z1, z2, p1, p2, nv])
                for i in range(3):
                    cnf.append([-pos[i]] + [neg[j] for j in range(3) if j != i])
                    cnf.append([-neg[i]] + [pos[j] for j in range(3) if j != i])
                ngp += 1
        self.stats['gp_relations'] = ngp
        self.stats['clauses_gp'] = len(cnf.clauses) - nc0
        nc0 = len(cnf.clauses)
        # (L) big lines
        big_pairs = set()
        for L in self.big_lines:
            Ls = set(L)
            for t in itertools.combinations(L, 3):
                cnf.append([self.Z[t]])
            for i, j in itertools.combinations(L, 2):
                big_pairs.add((i, j))
                for k in range(n):
                    if k not in Ls:
                        cnf.append([-self.z(i, j, k)])
        if exact_big:
            # every other line has <= 3 points: for a pair not inside a big line, no two
            # further points are both collinear with it
            for i, j in itertools.combinations(range(n), 2):
                if (i, j) in big_pairs:
                    continue
                others = [k for k in range(n) if k not in (i, j)]
                for k, l in itertools.combinations(others, 2):
                    cnf.append([-self.z(i, j, k), -self.z(i, j, l)])
        self.stats['clauses_lines'] = len(cnf.clauses) - nc0
        nc0 = len(cnf.clauses)
        # (O) ordinary-line indicators and cardinality
        self.O = {}
        for i, j in itertools.combinations(range(n), 2):
            o = pool.id(('O', i, j))
            self.O[(i, j)] = o
            cnf.append([o] + [self.z(i, j, k) for k in range(n) if k not in (i, j)])
        if self.m is not None:
            enc = CardEnc.atmost(lits=list(self.O.values()), bound=self.m, vpool=pool, encoding=card)
            cnf.extend(enc.clauses)
        self.stats['clauses_card'] = len(cnf.clauses) - nc0
        self.stats['vars'] = pool.top
        self.stats['clauses'] = len(cnf.clauses)

    def write_dimacs(self, path, comment=''):
        with open(path, 'w') as f:
            f.write(f"c ordlines n={self.n} m={self.m} big_lines={self.big_lines} {comment}\n")
            f.write(f"p cnf {self.pool.top} {len(self.cnf.clauses)}\n")
            for cl in self.cnf.clauses:
                f.write(' '.join(map(str, cl)) + ' 0\n')

    def decode(self, model):
        mset = set(l for l in model if l > 0)
        n = self.n
        lines = set()
        for i, j in itertools.combinations(range(n), 2):
            pts = {i, j} | {k for k in range(n) if k not in (i, j) and self.z(i, j, k) in mset}
            lines.add(tuple(sorted(pts)))
        chi = {}
        for t in self.Z:
            chi[t] = 0 if self.Z[t] in mset else (1 if self.P[t] in mset else -1)
        return sorted(lines, key=lambda L: (-len(L), L)), chi


def solve_pysat(enc, solver='cadical153', conf_budget=None):
    from pysat.solvers import Solver
    with Solver(name=solver, bootstrap_with=enc.cnf.clauses) as s:
        if conf_budget:
            s.conf_budget(conf_budget)
            r = s.solve_limited()
        else:
            r = s.solve()
        model = s.get_model() if r else None
    return r, model


def run_external(cnf_path, solver_bin, proof_path=None, timeout=None, extra=()):
    """run kissat/cadical; returns (result, wall, stdout)"""
    cmd = [solver_bin, cnf_path]
    if proof_path:
        cmd.append(proof_path)
    cmd += list(extra)
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = p.stdout
    except subprocess.TimeoutExpired as e:
        return 'TIMEOUT', time.time() - t0, (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or '')
    wall = time.time() - t0
    res = 'UNKNOWN'
    for line in out.splitlines():
        if line.startswith('s '):
            res = line[2:].strip()
    return res, wall, out


def parse_model(out):
    lits = []
    for line in out.splitlines():
        if line.startswith('v '):
            lits += [int(x) for x in line[2:].split()]
    return [l for l in lits if l != 0]


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('m', type=int)
    ap.add_argument('--big', action='append', default=[], help='big line as comma list, e.g. 0,1,2,3,4')
    ap.add_argument('--no-exact-big', action='store_true')
    ap.add_argument('--no-trans', action='store_true')
    ap.add_argument('--out', default=None, help='write DIMACS here')
    ap.add_argument('--solver', default='cadical153')
    ap.add_argument('--budget', type=int, default=None)
    args = ap.parse_args()
    big = [tuple(int(x) for x in s.split(',')) for s in args.big]
    t0 = time.time()
    enc = OrdLinesEncoder(args.n, args.m, big_lines=big, exact_big=not args.no_exact_big,
                          transitivity=not args.no_trans)
    print(json.dumps(enc.stats), f"enc {time.time()-t0:.1f}s", flush=True)
    if args.out:
        enc.write_dimacs(args.out)
        print('wrote', args.out)
    else:
        t1 = time.time()
        r, model = solve_pysat(enc, args.solver, args.budget)
        print({True: 'SAT', False: 'UNSAT', None: 'BUDGET'}[r], f"{time.time()-t1:.1f}s")
        if r:
            lines, chi = enc.decode(model)
            ordinary = [L for L in lines if len(L) == 2]
            print('ordinary', len(ordinary), 'sizes', sorted((len(L) for L in lines), reverse=True))
            print([L for L in lines if len(L) >= 3])
