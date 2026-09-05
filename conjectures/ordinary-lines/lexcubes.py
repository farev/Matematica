#!/usr/bin/env python3
"""lexcubes.py -- the two-5-line cubes at n = 15 with sound symmetry breaking:
  * phi-array over rows a in L1\L2, columns b in L2\L1, cell value in {*} u F
    (the free point on line ab, or * if ab is ordinary);
  * double-lex: rows in non-decreasing lexicographic order (row-major comparison of cells),
    columns in non-decreasing lexicographic order (top-to-bottom comparison);
  * value precedence: free point F[v] (v >= 1) occurs in row-major reading order only after
    F[v-1] has occurred;
  * optional split by the number s of stars (ordinary L1-L2 pairs), 0 <= s <= m.
Soundness (NOTE, Lemma): the row/column permutations and the relabelling of free points
act on the array as a direct product; sorting rows, sorting columns and relabelling by first
occurrence each weakly decrease the row-major word, so iterating them from any solution
reaches a solution satisfying all three constraints.  Hence every sub-instance family that
covers all s is exhaustive.

Cell order for lex comparisons: * < F[0] < F[1] < ... .
usage: python3 lexcubes.py {A|B} m [--s LIST] [--jobs J] [--timeout S] [--outdir D] [--dry]
"""
import sys, os, json, time, argparse, subprocess, hashlib
from concurrent.futures import ThreadPoolExecutor
from pysat.card import CardEnc, EncType
from ordlines_sat import OrdLinesEncoder

K = os.environ.get('KISSAT', 'kissat')
DT = os.environ.get('DRATTRIM', 'drat-trim')
N = 15
CUBES = {'A': dict(L1=(0, 1, 2, 3, 4), L2=(4, 5, 6, 7, 8)),
         'B': dict(L1=(0, 1, 2, 3, 4), L2=(5, 6, 7, 8, 9))}


class LexBuilder:
    def __init__(self, enc, F):
        self.enc, self.F, self.cnf, self.pool = enc, F, enc.cnf, enc.pool

    def cellvars(self, a, b):
        return [self.enc.z(a, b, f) for f in self.F]  # one-hot over F; all false = *

    def star_lit(self, a, b):
        """aux s with s -> cell is *  (upper bound only)"""
        s = self.pool.id(('star', a, b))
        for zv in self.cellvars(a, b):
            self.cnf.append([-s, -zv])
        # also s <- cell is *, to make the star count exact
        self.cnf.append([s] + self.cellvars(a, b))
        return s

    def eq_lit(self, c1, c2):
        """aux e exactly equivalent to cell c1 == cell c2 (as one-hot vectors)"""
        z1, z2 = self.cellvars(*c1), self.cellvars(*c2)
        ds = []
        for x, y in zip(z1, z2):
            d = self.pool.id()
            # d <-> x xor y
            self.cnf.append([-x, y, d]); self.cnf.append([x, -y, d])
            self.cnf.append([-d, x, y]); self.cnf.append([-d, -x, -y])
            ds.append(d)
        e = self.pool.id()
        for d in ds:
            self.cnf.append([-e, -d])
        self.cnf.append([e] + ds)
        return e

    def lt_lit(self, c1, c2):
        """aux l with l -> cell c1 < cell c2 in the order * < F0 < F1 < ... (upper bound)"""
        z1, z2 = self.cellvars(*c1), self.cellvars(*c2)
        l = self.pool.id()
        s1 = self.star_lit(*c1)
        # c2 is not *
        self.cnf.append([-l] + z2)
        # for each value v' of c2: c1 is * or some v < v'
        for vp in range(len(self.F)):
            self.cnf.append([-l, -z2[vp], s1] + [z1[v] for v in range(vp)])
        return l

    def lex_leq(self, cells1, cells2):
        """cells1 <=_lex cells2 (same length), comparing cell by cell in the given order"""
        E = None  # prefix-equal literal; None means true
        for k, (c1, c2) in enumerate(zip(cells1, cells2)):
            e = self.eq_lit(c1, c2)
            l = self.lt_lit(c1, c2)
            # (E and not e) -> l
            if E is None:
                self.cnf.append([e, l])
            else:
                self.cnf.append([-E, e, l])
            # new prefix-equal literal: E' <-> E and e
            if E is None:
                E = e
            else:
                E2 = self.pool.id()
                self.cnf.append([-E2, E]); self.cnf.append([-E2, e]); self.cnf.append([E2, -E, -e])
                E = E2

    def value_precedence(self, cells_in_reading_order):
        F = self.F
        for v in range(1, len(F)):
            for p, (a, b) in enumerate(cells_in_reading_order):
                self.cnf.append([-self.enc.z(a, b, F[v])] + [self.enc.z(a2, b2, F[v - 1]) for (a2, b2) in cells_in_reading_order[:p]])


def build(cube, m, s=None, latin=None):
    L1, L2 = CUBES[cube]['L1'], CUBES[cube]['L2']
    shared = set(L1) & set(L2)
    rows = [a for a in L1 if a not in shared]
    cols = [b for b in L2 if b not in shared]
    F = [p for p in range(N) if p not in L1 and p not in L2]
    enc = OrdLinesEncoder(N, m, big_lines=[L1, L2], exact_big=True)
    lb = LexBuilder(enc, F)
    cells = [(a, b) for a in rows for b in cols]
    # rows lex-ordered, columns lex-ordered
    for i in range(len(rows) - 1):
        lb.lex_leq([(rows[i], b) for b in cols], [(rows[i + 1], b) for b in cols])
    for j in range(len(cols) - 1):
        lb.lex_leq([(a, cols[j]) for a in rows], [(a, cols[j + 1]) for a in rows])
    lb.value_precedence(cells)
    stars = [lb.star_lit(a, b) for (a, b) in cells]
    if s is not None:
        eq = CardEnc.equals(lits=stars, bound=s, vpool=enc.pool, encoding=EncType.seqcounter)
        enc.cnf.extend(eq.clauses)
    if latin is not None:
        for i, a in enumerate(rows):
            for j, b in enumerate(cols):
                enc.cnf.append([enc.z(a, b, F[latin[i][j]])])
    desc = dict(cube=cube, m=m, L1=list(L1), L2=list(L2), F=F, rows=rows, cols=cols, s=s, latin=latin,
                symmetry_breaking='double-lex + value precedence')
    return enc, desc


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def run_one(tag, enc, desc, outdir, timeout, keep_proofs):
    base = os.path.join(outdir, tag)
    cnf, drat, log = base + '.cnf', base + '.drat', base + '.log'
    enc.write_dimacs(cnf, comment=json.dumps(desc))
    rec = dict(tag=tag, **desc, vars=enc.pool.top, clauses=len(enc.cnf.clauses), sha256_cnf=sha256(cnf))
    t0 = time.time()
    try:
        with open(log, 'w') as lf:
            subprocess.run([K, '--no-binary', cnf, drat], stdout=lf, stderr=subprocess.STDOUT, text=True, timeout=timeout)
        out = open(log).read()
        res = [l for l in out.splitlines() if l.startswith('s ')]
        res = res[0][2:].strip() if res else 'UNKNOWN'
    except subprocess.TimeoutExpired:
        res = 'TIMEOUT'
    rec['solve_s'] = round(time.time() - t0, 1)
    rec['result'] = {'UNSATISFIABLE': 'UNSAT', 'SATISFIABLE': 'SAT'}.get(res, res)
    rec['proof_bytes'] = os.path.getsize(drat) if os.path.exists(drat) else 0
    rec['drat_trim'] = 'n/a'
    if rec['result'] == 'UNSAT':
        t1 = time.time()
        try:
            q = subprocess.run([DT, cnf, drat], capture_output=True, text=True, timeout=max(4 * timeout, 3600))
            rec['drat_trim'] = 'VERIFIED' if 's VERIFIED' in q.stdout else 'FAILED'
        except subprocess.TimeoutExpired:
            rec['drat_trim'] = 'TIMEOUT'
        rec['verify_s'] = round(time.time() - t1, 1)
        if not keep_proofs and rec['drat_trim'] == 'VERIFIED':
            os.remove(drat)
    elif rec['result'] == 'SAT':
        out = open(log).read()
        lits = []
        for l in out.splitlines():
            if l.startswith('v '):
                lits += [int(x) for x in l[2:].split()]
        model = [x for x in lits if x != 0]
        with open(base + '.model', 'w') as f:
            f.write(' '.join(map(str, model)) + '\n')
        lines, chi = enc.decode(model)
        rec['lines'] = [list(L) for L in lines]
        rec['ordinary'] = sum(1 for L in lines if len(L) == 2)
        if os.path.exists(drat):
            os.remove(drat)
    else:
        if os.path.exists(drat):
            os.remove(drat)
    return rec


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cube', choices=['A', 'B'])
    ap.add_argument('m', type=int)
    ap.add_argument('--s', default=None, help='comma list of star counts; default 0..m as separate instances; "all" for one instance')
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--timeout', type=int, default=7200)
    ap.add_argument('--outdir', default=None)
    ap.add_argument('--keep-proofs', action='store_true')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    if a.s == 'all':
        svals = [None]
    elif a.s is None:
        svals = list(range(0, a.m + 1))
    else:
        svals = [int(x) for x in a.s.split(',')]
    outdir = a.outdir or f"lex_{a.cube}_m{a.m}"
    os.makedirs(outdir, exist_ok=True)
    ledger = os.path.join(outdir, 'ledger.jsonl')
    jobs = [(f"lex_{a.cube}_m{a.m}_s{'all' if s is None else s}", s) for s in svals]
    if a.dry:
        enc, desc = build(a.cube, a.m, svals[0])
        print(enc.stats, enc.pool.top, len(enc.cnf.clauses))
        sys.exit(0)

    def work(job):
        tag, s = job
        enc, desc = build(a.cube, a.m, s)
        rec = run_one(tag, enc, desc, outdir, a.timeout, a.keep_proofs)
        with open(ledger, 'a') as f:
            f.write(json.dumps(rec) + '\n')
        print(json.dumps({k: rec[k] for k in ('tag', 's', 'result', 'solve_s', 'proof_bytes', 'drat_trim', 'verify_s', 'ordinary') if k in rec}), flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        recs = list(ex.map(work, jobs))
    summ = {}
    for r in recs:
        summ[r['result']] = summ.get(r['result'], 0) + 1
    print('summary', summ, 'verified', sum(1 for r in recs if r.get('drat_trim') == 'VERIFIED'), flush=True)
