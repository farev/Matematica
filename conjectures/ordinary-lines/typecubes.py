#!/usr/bin/env python3
"""typecubes.py -- star-pattern sub-cubes of subcubes.py refined by the *type vector* of a
t_2 = 7 configuration with two 5-point lines, plus exact cardinality constraints.

Within such a configuration (Cor. 5.3: t_2 = 7, t_3 = 26, no other line of size >= 4) every
3-point line has one of the following types, and the numbers of lines of each type satisfy
linear identities obtained by counting the pairs of each kind exactly once:

Cube B (L1, L2 disjoint; R = L1, C = L2, |F| = 5), s = number of stars, M = 25 - s mixed lines
(a, b, f):
   RFF: (a, f, f')  count A3      CFF: (b, f, f')  count B3      FFF: (f, f', f'') count C3
   26 = M + A3 + B3 + C3,   ord_RF = 25 - M - 2 A3 >= 0,   ord_CF = 25 - M - 2 B3 >= 0,
   ord_FF = 10 - A3 - B3 - 3 C3 >= 0.
Cube A (L1 ∩ L2 = {q}; R, C of size 4, |F| = 6), M = 16 - s:
   additionally qFF: (q, f, f') count Q3, 0 <= Q3 <= 3, ord_qF = 6 - 2 Q3;
   26 = M + A3 + B3 + Q3 + C3,  ord_RF = 24 - M - 2 A3,  ord_CF = 24 - M - 2 B3,
   ord_FF = 15 - A3 - B3 - Q3 - 3 C3, all >= 0.
In both cases the total number of ordinary lines then equals 7 identically.

Every solution of a sub-cube has exactly one type vector, so running one instance per
(star class, type vector) with the counts imposed as exact cardinality constraints is an
exhaustive refinement (sound: the constraints are consequences of t_2 = 7 and t_3 = 26,
which Cor. 5.3 forces in these cubes).  The ordinary-line indicators O_ij are made exact
(O_ij <-> pair ij ordinary) so that "exactly 7 ordinary lines" and the per-kind ordinary
counts can be imposed as well.

usage: python3 typecubes.py {A|B} m [--only i,j,...] [--jobs J] [--timeout S] [--outdir D] [--dry]
"""
import sys, os, json, itertools, argparse, time
from concurrent.futures import ThreadPoolExecutor
from pysat.card import CardEnc, EncType
import subcubes
from subcubes import star_classes, build_subcube, run_one, latin_square_classes, CUBES, N


def type_vectors(cube, s):
    out = []
    if cube == 'B':
        M = 25 - s
        for A3 in range(0, 6):
            for B3 in range(0, 6):
                C3 = 26 - M - A3 - B3
                if C3 < 0:
                    continue
                ord_RF, ord_CF, ord_FF = 25 - M - 2 * A3, 25 - M - 2 * B3, 10 - A3 - B3 - 3 * C3
                if min(ord_RF, ord_CF, ord_FF) < 0:
                    continue
                assert s + ord_RF + ord_CF + ord_FF == 7
                out.append(dict(A3=A3, B3=B3, C3=C3, ord_RF=ord_RF, ord_CF=ord_CF, ord_FF=ord_FF))
    else:
        M = 16 - s
        for Q3 in range(0, 4):
            for A3 in range(0, 13):
                for B3 in range(0, 13):
                    C3 = 26 - M - A3 - B3 - Q3
                    if C3 < 0:
                        continue
                    ord_RF, ord_CF = 24 - M - 2 * A3, 24 - M - 2 * B3
                    ord_FF, ord_qF = 15 - A3 - B3 - Q3 - 3 * C3, 6 - 2 * Q3
                    if min(ord_RF, ord_CF, ord_FF, ord_qF) < 0:
                        continue
                    assert s + ord_qF + ord_RF + ord_CF + ord_FF == 7
                    out.append(dict(Q3=Q3, A3=A3, B3=B3, C3=C3, ord_RF=ord_RF, ord_CF=ord_CF, ord_FF=ord_FF, ord_qF=ord_qF))
    return out


def add_type_constraints(enc, desc, tv):
    cnf, pool = enc.cnf, enc.pool
    L1, L2 = desc['L1'], desc['L2']
    shared = set(L1) & set(L2)
    R, C, F = desc['rows'], desc['cols'], desc['F']
    n = N

    def eq(lits, k):
        if k == 0:
            for l in lits:
                cnf.append([-l])
            return
        if k == len(lits):
            for l in lits:
                cnf.append([l])
            return
        e = CardEnc.equals(lits=lits, bound=k, vpool=pool, encoding=EncType.seqcounter)
        cnf.extend(e.clauses)

    # exact ordinary indicators: O_ij -> not Z_ijk for all k
    for (i, j), o in enc.O.items():
        for k in range(n):
            if k not in (i, j):
                cnf.append([-o, -enc.z(i, j, k)])
    # exactly 7 ordinary lines in total
    eq(list(enc.O.values()), 7)
    # type counts
    eq([enc.z(a, f, g) for a in R for f, g in itertools.combinations(F, 2)], tv['A3'])
    eq([enc.z(b, f, g) for b in C for f, g in itertools.combinations(F, 2)], tv['B3'])
    eq([enc.z(f, g, h) for f, g, h in itertools.combinations(F, 3)], tv['C3'])
    if shared:
        q = next(iter(shared))
        eq([enc.z(q, f, g) for f, g in itertools.combinations(F, 2)], tv['Q3'])
        eq([enc.O[tuple(sorted((q, f)))] for f in F], tv['ord_qF'])
    eq([enc.O[tuple(sorted((a, f)))] for a in R for f in F], tv['ord_RF'])
    eq([enc.O[tuple(sorted((b, f)))] for b in C for f in F], tv['ord_CF'])
    eq([enc.O[tuple(sorted((f, g)))] for f, g in itertools.combinations(F, 2)], tv['ord_FF'])
    # per-point parity: every point lies on an even number of ordinary lines
    # (sum over lines through p of (|line|-1) = 14; 3-lines contribute 2, 5-lines 4)
    if PARITY:
        for p in range(n):
            lits = [enc.O[tuple(sorted((p, x)))] for x in range(n) if x != p]
            xor_zero(cnf, pool, lits)


PARITY = True


def xor_zero(cnf, pool, lits):
    """clauses forcing XOR(lits) = 0 via a chain of auxiliaries"""
    t = lits[0]
    for x in lits[1:]:
        u = pool.id()
        # u <-> t xor x
        cnf.append([-u, t, x]); cnf.append([-u, -t, -x])
        cnf.append([u, -t, x]); cnf.append([u, t, -x])
        t = u
    cnf.append([-t])


def instances(cube, m):
    L1, L2 = CUBES[cube]['L1'], CUBES[cube]['L2']
    shared = set(L1) & set(L2)
    nrc = 5 - len(shared)
    classes = star_classes(nrc, nrc, m)
    inst = []
    for ci, sc in enumerate(classes):
        s = sum(bin(r).count('1') for r in sc)
        tvs = type_vectors(cube, s)
        if s == 0 and cube == 'B':
            for li, latin in enumerate(latin_square_classes(5)):
                for tv in tvs:
                    inst.append(dict(star_index=ci, stars=sc, s=s, latin=latin, tv=tv))
        else:
            for tv in tvs:
                inst.append(dict(star_index=ci, stars=sc, s=s, latin=None, tv=tv))
    return inst


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cube', choices=['A', 'B'])
    ap.add_argument('m', type=int)
    ap.add_argument('--only', default=None, help='comma list of star-class indices')
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--timeout', type=int, default=3600)
    ap.add_argument('--outdir', default=None)
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    assert a.m == 7, 'type identities are derived for t_2 = 7'
    inst = instances(a.cube, a.m)
    if a.only:
        keep = set(int(x) for x in a.only.split(','))
        inst = [d for d in inst if d['star_index'] in keep]
    print(f"cube {a.cube}: {len(inst)} (star class, type) instances", flush=True)
    if a.dry:
        import collections
        print('instances per star class:', sorted(collections.Counter(d['star_index'] for d in inst).items())[:12], '...')
        print('per s:', sorted(collections.Counter(d['s'] for d in inst).items()))
        sys.exit(0)
    outdir = a.outdir or f"type_{a.cube}_m{a.m}"
    os.makedirs(outdir, exist_ok=True)
    ledger = os.path.join(outdir, 'ledger.jsonl')

    def work(i):
        d = inst[i]
        enc, desc = build_subcube(a.cube, a.m, d['stars'], d['latin'])
        add_type_constraints(enc, desc, d['tv'])
        desc['star_index'] = d['star_index']
        desc['type'] = d['tv']
        rec = run_one(i, enc, desc, outdir, a.timeout, False)
        with open(ledger, 'a') as f:
            f.write(json.dumps(rec) + '\n')
        print(json.dumps({k: rec[k] for k in ('idx', 'star_index', 's', 'type', 'result', 'solve_s', 'proof_bytes', 'drat_trim') if k in rec}), flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        recs = list(ex.map(work, range(len(inst))))
    summ = {}
    for r in recs:
        summ[r['result']] = summ.get(r['result'], 0) + 1
    print('summary', summ, 'verified', sum(1 for r in recs if r.get('drat_trim') == 'VERIFIED'), flush=True)
