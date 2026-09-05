#!/usr/bin/env python3
"""fillcubes.py -- "fill mode" for a slow sub-cube: fix the whole free-point array.

Given a cube (A or B), m, and the index of a star class from subcubes.py, enumerate every
filling of the non-star cells by free points (at most once per row and column) up to the
residual symmetry Aut(S) x (relabelling of free points), and run each filling as its own
instance.  Canonical form: for each (row perm, col perm) in Aut(S), relabel symbols by first
occurrence in row-major order; take the minimum.  Value precedence is then automatic.
Soundness: every solution of the sub-cube has an array; applying an element of Aut(S) and a
relabelling maps it to a solution whose array is the canonical representative, which is one
of the instances run.  So "all fillings UNSAT" implies "sub-cube UNSAT".

usage: python3 fillcubes.py {A|B} m star_index [--jobs J] [--timeout S] [--outdir D] [--count]
"""
import sys, os, json, itertools, argparse, time
from concurrent.futures import ThreadPoolExecutor
import subcubes
from subcubes import star_classes, build_subcube, run_one, CUBES, N


def aut(star_rows, nrows, ncols):
    """(row perm, col perm) pairs preserving the star matrix"""
    S = [[star_rows[i] >> j & 1 for j in range(ncols)] for i in range(nrows)]
    out = []
    for rp in itertools.permutations(range(nrows)):
        for cp in itertools.permutations(range(ncols)):
            if all(S[rp[i]][cp[j]] == S[i][j] for i in range(nrows) for j in range(ncols)):
                out.append((rp, cp))
    return out


def fillings(star_rows, nrows, ncols, nsym):
    S = [[star_rows[i] >> j & 1 for j in range(ncols)] for i in range(nrows)]
    cells = [(i, j) for i in range(nrows) for j in range(ncols) if not S[i][j]]
    A = aut(star_rows, nrows, ncols)
    found = {}
    grid = [[None] * ncols for _ in range(nrows)]

    def canon(g):
        best = None
        for rp, cp in A:
            relabel = {}
            key = []
            for i in range(nrows):
                for j in range(ncols):
                    v = g[rp[i]][cp[j]]
                    if v is None:
                        key.append(-1)
                    else:
                        if v not in relabel:
                            relabel[v] = len(relabel)
                        key.append(relabel[v])
            key = tuple(key)
            if best is None or key < best:
                best = key
        return best

    def rec(k, maxsym):
        if k == len(cells):
            key = canon(grid)
            if key not in found:
                found[key] = [row[:] for row in grid]
            return
        i, j = cells[k]
        used = {grid[i][jj] for jj in range(ncols)} | {grid[ii][j] for ii in range(nrows)}
        # value precedence: allow symbols 0..maxsym+1
        for v in range(min(nsym, maxsym + 2)):
            if v in used:
                continue
            grid[i][j] = v
            rec(k + 1, max(maxsym, v))
            grid[i][j] = None

    rec(0, -1)
    return list(found.values()), len(A)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cube', choices=['A', 'B'])
    ap.add_argument('m', type=int)
    ap.add_argument('star_index', type=int)
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--timeout', type=int, default=1800)
    ap.add_argument('--outdir', default=None)
    ap.add_argument('--count', action='store_true')
    a = ap.parse_args()
    L1, L2 = CUBES[a.cube]['L1'], CUBES[a.cube]['L2']
    shared = set(L1) & set(L2)
    nrows = ncols = 5 - len(shared)
    nsym = N - len(set(L1) | set(L2))
    classes = star_classes(nrows, ncols, a.m)
    sc = classes[a.star_index]
    t0 = time.time()
    fills, naut = fillings(sc, nrows, ncols, nsym)
    print(f"cube {a.cube} m={a.m} star class {a.star_index} rows={[bin(r)[2:].zfill(ncols) for r in sc]}: |Aut(S)|={naut}, {len(fills)} fillings up to symmetry ({time.time()-t0:.1f}s)", flush=True)
    if a.count:
        sys.exit(0)
    outdir = a.outdir or f"fill_{a.cube}_m{a.m}_c{a.star_index}"
    os.makedirs(outdir, exist_ok=True)
    ledger = os.path.join(outdir, 'ledger.jsonl')

    def work(i):
        enc, desc = build_subcube(a.cube, a.m, sc, fills[i])
        desc['star_index'] = a.star_index
        desc['fill_index'] = i
        rec = run_one(i, enc, desc, outdir, a.timeout, False)
        with open(ledger, 'a') as f:
            f.write(json.dumps(rec) + '\n')
        print(json.dumps({k: rec[k] for k in ('idx', 'result', 'solve_s', 'proof_bytes', 'drat_trim') if k in rec}), flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        recs = list(ex.map(work, range(len(fills))))
    summ = {}
    for r in recs:
        summ[r['result']] = summ.get(r['result'], 0) + 1
    print('summary', summ, 'verified', sum(1 for r in recs if r.get('drat_trim') == 'VERIFIED'), flush=True)
