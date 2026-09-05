#!/usr/bin/env python3
"""subcubes.py -- finer case split for the n = 15, t_2 <= 7 instances (two 5-point lines).

Setting.  Big lines L1, L2 (|L1| = |L2| = 5), free points F = the rest.  For a in L1\L2 and
b in L2\L1 the line ab contains no further point of L1 or L2 (it would be L1 or L2), and by
the cube's "no other line of size >= 4" clause it contains at most one free point.  So
  phi(a, b) = the free point on line ab, or * ("ordinary").
Each free point f appears at most once in every row and column of phi (f, a, b, b' collinear
would put a on L2).  The number of stars is at most m (every star is an ordinary line).

Sub-cube = (star pattern S up to row/column permutations) + symbol value-precedence.
* The star pattern is a 0/1 matrix; classes are enumerated as multisets of rows minimised
  over column permutations (complete invariant under row perms x column perms).
* Symbol symmetry (relabelling the free points) is broken by value precedence in row-major
  reading order: free point number v+1 may only appear after free point number v has
  appeared.  Sound: any solution can be relabelled to satisfy it.
* For s = 0 in the disjoint case phi is a Latin square of order 5; we fix it to one of the
  isotopy-class representatives (computed here, expected 2).
Every sub-cube is a *restriction* of the parent cube by unit/precedence clauses, and the
family of sub-cubes covers the parent cube up to the symmetries above, so "all sub-cubes
UNSAT" implies "parent cube UNSAT" (Lemma in NOTE).

usage: python3 subcubes.py {A|B} m [--jobs J] [--timeout S] [--dry]
"""
import sys, os, json, time, itertools, argparse, subprocess, hashlib
from concurrent.futures import ThreadPoolExecutor
from ordlines_sat import OrdLinesEncoder

K = os.environ.get('KISSAT', 'kissat')
DT = os.environ.get('DRATTRIM', 'drat-trim')
N = 15

CUBES = {
    'A': dict(L1=(0, 1, 2, 3, 4), L2=(4, 5, 6, 7, 8)),
    'B': dict(L1=(0, 1, 2, 3, 4), L2=(5, 6, 7, 8, 9)),
}


def star_classes(rows, cols, max_stars):
    """0/1 rows x cols matrices with <= max_stars ones, up to row and column permutations.
    Returned as sorted tuples of row bitmasks (canonical)."""
    row_patterns = list(range(1 << cols))
    classes = set()
    colperms = list(itertools.permutations(range(cols)))

    def apply(perm, mask):
        out = 0
        for j in range(cols):
            if mask >> j & 1:
                out |= 1 << perm[j]
        return out

    def rec(start, chosen, ones):
        if len(chosen) == rows:
            best = None
            for perm in colperms:
                key = tuple(sorted(apply(perm, r) for r in chosen))
                if best is None or key < best:
                    best = key
            classes.add(best)
            return
        for p in range(start, len(row_patterns)):
            c = bin(row_patterns[p]).count('1')
            if ones + c > max_stars:
                continue
            rec(p, chosen + [row_patterns[p]], ones + c)

    rec(0, [], 0)
    return sorted(classes, key=lambda k: (sum(bin(r).count('1') for r in k), k))


def latin_square_classes(k):
    """isotopy classes of Latin squares of order k (k = 5 -> expected 2), by brute force:
    for each Latin square with first row 0..k-1 in order (reduced on the row), canonical form
    = min over row perms x column perms of the square relabelled by first occurrence."""
    squares = []

    def rec(rowsdone):
        if len(rowsdone) == k:
            squares.append([list(r) for r in rowsdone])
            return
        used_cols = [set(r[j] for r in rowsdone) for j in range(k)]
        for perm in itertools.permutations(range(k)):
            if all(perm[j] not in used_cols[j] for j in range(k)):
                rec(rowsdone + [perm])

    rec([tuple(range(k))])
    rowperms = list(itertools.permutations(range(k)))
    classes = {}
    for sq in squares:
        best = None
        for rp in rowperms:
            for cp in rowperms:
                relabel = {}
                key = []
                for i in range(k):
                    for j in range(k):
                        v = sq[rp[i]][cp[j]]
                        if v not in relabel:
                            relabel[v] = len(relabel)
                        key.append(relabel[v])
                key = tuple(key)
                if best is None or key < best:
                    best = key
        if best not in classes:
            classes[best] = sq
    return list(classes.values())


def build_subcube(cube, m, star_rows, latin=None):
    """returns (encoder, description).  star_rows: tuple of row bitmasks over the column list."""
    L1, L2 = CUBES[cube]['L1'], CUBES[cube]['L2']
    shared = set(L1) & set(L2)
    rows = [a for a in L1 if a not in shared]
    cols = [b for b in L2 if b not in shared]
    F = [p for p in range(N) if p not in L1 and p not in L2]
    enc = OrdLinesEncoder(N, m, big_lines=[L1, L2], exact_big=True)
    cnf = enc.cnf
    cells = [(a, b) for a in rows for b in cols]  # row-major reading order
    star = {}
    for i, a in enumerate(rows):
        for j, b in enumerate(cols):
            star[(a, b)] = bool(star_rows[i] >> j & 1)
    for (a, b) in cells:
        if star[(a, b)]:
            for f in F:
                cnf.append([-enc.z(a, b, f)])
        else:
            cnf.append([enc.z(a, b, f) for f in F])
    if latin is not None:
        # fix phi completely: latin[i][j] = index into F
        for i, a in enumerate(rows):
            for j, b in enumerate(cols):
                f = F[latin[i][j]]
                cnf.append([enc.z(a, b, f)])
    else:
        # value precedence on symbols F[0], F[1], ... in reading order over non-star cells
        order = [(a, b) for (a, b) in cells if not star[(a, b)]]
        for v in range(1, len(F)):
            for p, (a, b) in enumerate(order):
                cnf.append([-enc.z(a, b, F[v])] + [enc.z(a2, b2, F[v - 1]) for (a2, b2) in order[:p]])
    desc = dict(cube=cube, m=m, L1=list(L1), L2=list(L2), F=F, rows=rows, cols=cols,
                stars=[[a, b] for (a, b) in cells if star[(a, b)]], latin=latin)
    return enc, desc


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def run_one(idx, enc, desc, outdir, timeout, keep_proofs):
    base = os.path.join(outdir, f"sub_{desc['cube']}_m{desc['m']}_{idx:04d}")
    cnf, drat, log = base + '.cnf', base + '.drat', base + '.log'
    enc.write_dimacs(cnf, comment=json.dumps(desc))
    rec = dict(idx=idx, **desc, vars=enc.pool.top, clauses=len(enc.cnf.clauses), sha256_cnf=sha256(cnf))
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
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--timeout', type=int, default=3600)
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--keep-proofs', action='store_true')
    ap.add_argument('--outdir', default=None)
    ap.add_argument('--only', default=None)
    a = ap.parse_args()
    L1, L2 = CUBES[a.cube]['L1'], CUBES[a.cube]['L2']
    shared = set(L1) & set(L2)
    nrows, ncols = 5 - len(shared), 5 - len(shared)
    classes = star_classes(nrows, ncols, a.m)
    subs = []
    for sc in classes:
        s = sum(bin(r).count('1') for r in sc)
        if s == 0 and a.cube == 'B':
            for latin in latin_square_classes(5):
                subs.append((sc, latin))
        else:
            subs.append((sc, None))
    print(f"cube {a.cube} m={a.m}: {len(classes)} star classes, {len(subs)} sub-cubes", flush=True)
    if a.dry:
        for i, (sc, latin) in enumerate(subs):
            print(i, [bin(r)[2:].zfill(ncols) for r in sc], 'latin' if latin else '')
        sys.exit(0)
    outdir = a.outdir or f"subcubes_{a.cube}_m{a.m}"
    os.makedirs(outdir, exist_ok=True)
    ledger = os.path.join(outdir, 'ledger.jsonl')
    sel = list(range(len(subs))) if a.only is None else [int(x) for x in a.only.split(',')]

    def work(i):
        sc, latin = subs[i]
        enc, desc = build_subcube(a.cube, a.m, sc, latin)
        rec = run_one(i, enc, desc, outdir, a.timeout, a.keep_proofs)
        with open(ledger, 'a') as f:
            f.write(json.dumps(rec) + '\n')
        print(json.dumps({k: rec[k] for k in ('idx', 'stars', 'latin', 'result', 'solve_s', 'proof_bytes', 'drat_trim') if k in rec}), flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        recs = list(ex.map(work, sel))
    summ = {}
    for r in recs:
        summ[r['result']] = summ.get(r['result'], 0) + 1
    print('summary', summ, 'verified', sum(1 for r in recs if r.get('drat_trim') == 'VERIFIED'), flush=True)
