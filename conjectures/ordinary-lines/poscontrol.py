#!/usr/bin/env python3
"""poscontrol.py -- positive control for the sub-cube machinery of subcubes.py.

Builds an explicit real configuration of 15 points (exact rational coordinates) with two
disjoint 5-point lines L1, L2, five further points, no other line of size >= 4, computes its
ordinary-line count m*, relabels it so that its star pattern is the canonical representative
used by subcubes.star_classes and its free points obey value precedence, then asks the
solver for the corresponding sub-cube with m = m*.  Expected: SAT, and the model passes
verify_chirotope.  (A bug that over-constrains the sub-cubes would show up here as UNSAT.)
"""
import sys, itertools, json, subprocess, os, time
from fractions import Fraction as Fr
from subcubes import build_subcube, CUBES, N
from verify_chirotope import verify, decode as decode_model
import subcubes

K = subcubes.K


def det3(p, q, r):
    return (p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0])
            + p[2] * (q[0] * r[1] - q[1] * r[0]))


def line_through(p, q):
    # cross product in homogeneous coordinates
    return (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])


def meet(l1, l2):
    return line_through(l1, l2)


def configuration():
    L1 = [(Fr(i), Fr(0), Fr(1)) for i in range(5)]
    xs = [0, 1, 3, 6, 10]
    L2 = [(Fr(x), Fr(1), Fr(1)) for x in xs]
    pts = L1 + L2
    # candidate free points: intersections of two cross lines (a,b),(a',b') with a != a', b != b'
    cross = [(a, b) for a in range(5) for b in range(5)]
    cands = {}
    for (a, b), (a2, b2) in itertools.combinations(cross, 2):
        if a == a2 or b == b2:
            continue
        p = meet(line_through(L1[a], L2[b]), line_through(L1[a2], L2[b2]))
        if p[2] == 0:
            continue  # skip points at infinity for simplicity
        p = (p[0] / p[2], p[1] / p[2], Fr(1))
        if p[1] == 0 or p[1] == 1:
            continue
        cands.setdefault(p, set()).update({(a, b), (a2, b2)})
    # greedy: pick free points lying on many cross lines, keeping every line <= 3 points except L1, L2
    order = sorted(cands.items(), key=lambda kv: -len(kv[1]))
    free = []
    for p, _ in order:
        trial = pts + free + [p]
        if ok(trial):
            free.append(p)
        if len(free) == 5:
            break
    assert len(free) == 5
    return pts + free


def lines_of(P):
    n = len(P)
    lines = set()
    for i, j in itertools.combinations(range(n), 2):
        pts = tuple(sorted({i, j} | {k for k in range(n) if k not in (i, j) and det3(P[i], P[j], P[k]) == 0}))
        lines.add(pts)
    return lines


def ok(P):
    n = len(P)
    if len(set(P)) < n:
        return False
    for L in lines_of(P):
        if len(L) >= 4 and set(L) not in (set(range(5)), set(range(5, 10))):
            return False
    return True


if __name__ == '__main__':
    P = configuration()
    lines = lines_of(P)
    dist = {}
    for L in lines:
        dist[len(L)] = dist.get(len(L), 0) + 1
    mstar = dist.get(2, 0)
    print('configuration distribution', dict(sorted(dist.items())), 'ordinary m* =', mstar)
    # phi array: rows a=0..4 (L1), cols b=5..9 (L2); entry = free point index or None
    F = list(range(10, 15))
    phi = {}
    for a in range(5):
        for b in range(5, 10):
            fs = [f for f in F if det3(P[a], P[b], P[f]) == 0]
            assert len(fs) <= 1
            phi[(a, b)] = fs[0] if fs else None
    star_rows = [sum(1 << (b - 5) for b in range(5, 10) if phi[(a, b)] is None) for a in range(5)]
    # canonical star pattern: min over column perms of sorted rows, then apply the row order and
    # column perm to relabel the configuration
    best = None
    for perm in itertools.permutations(range(5)):
        rows = []
        for a in range(5):
            m = star_rows[a]
            out = 0
            for j in range(5):
                if m >> j & 1:
                    out |= 1 << perm[j]
            rows.append((out, a))
        rows.sort()
        key = tuple(r for r, _ in rows)
        if best is None or key < best[0]:
            best = (key, perm, [a for _, a in rows])
    key, colperm, roworder = best
    # relabel: new row i = old row roworder[i]; new column colperm[j] = old column j
    newP = [None] * 15
    for i, a in enumerate(roworder):
        newP[i] = P[a]
    for j in range(5):
        newP[5 + colperm[j]] = P[5 + j]
    # free points: value precedence in reading order of the new array
    seen = []
    for i in range(5):
        for j in range(5):
            a, b = roworder[i], 5 + [jj for jj in range(5) if colperm[jj] == j][0]
            f = phi[(a, b)]
            if f is not None and f not in seen:
                seen.append(f)
    for f in F:
        if f not in seen:
            seen.append(f)
    for v, f in enumerate(seen):
        newP[10 + v] = P[f]
    P2 = newP
    assert ok(P2)
    lines2 = lines_of(P2)
    assert sum(1 for L in lines2 if len(L) == 2) == mstar
    stars = [(i, 5 + j) for i in range(5) for j in range(5) if key[i] >> j & 1]
    print('canonical star pattern rows', [bin(r)[2:].zfill(5) for r in key], 'stars', len(stars))
    enc, desc = build_subcube('B', mstar, key, None)
    path = 'poscontrol_B.cnf'
    enc.write_dimacs(path, comment='positive control')
    t0 = time.time()
    out = subprocess.run([K, '-q', path], capture_output=True, text=True).stdout
    res = [l for l in out.splitlines() if l.startswith('s ')][0]
    print(res, f'{time.time()-t0:.1f}s')
    if 'SATISFIABLE' in res and 'UNSAT' not in res:
        lits = []
        for l in out.splitlines():
            if l.startswith('v '):
                lits += [int(x) for x in l[2:].split()]
        model = set(x for x in lits if x > 0)
        chi = decode_model(N, model)
        rep = verify(N, chi)
        print('model verify:', {k: rep[k] for k in ('simple', 'linear_space', 'axiom_B2', 'gp3', 'ordinary', 'distribution')})
    # also: the real configuration itself must satisfy the sub-cube CNF (direct check)
    chi_real = {}
    for t in itertools.combinations(range(N), 3):
        d = det3(P2[t[0]], P2[t[1]], P2[t[2]])
        chi_real[t] = 0 if d == 0 else (1 if d > 0 else -1)
    assign = {}
    for t in chi_real:
        assign[enc.Z[t]] = (chi_real[t] == 0)
        assign[enc.P[t]] = (chi_real[t] > 0)
    # check every clause mentioning only Z/P variables; clauses with auxiliaries are skipped
    # (they are definitional) -- report how many primary-only clauses are violated
    bad = 0; checked = 0
    for cl in enc.cnf.clauses:
        if all(abs(l) in assign for l in cl):
            checked += 1
            if not any(assign[abs(l)] if l > 0 else not assign[abs(l)] for l in cl):
                bad += 1
    print(f'real configuration vs primary-variable clauses: {checked} checked, {bad} violated')
