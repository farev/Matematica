#!/usr/bin/env python3
"""
Cube-and-conquer for the tight case n = 18, t = 94 (budget 6) by the set of imperfect lines.

By (T1) a 94-triangle arrangement of 18 pseudolines has exactly 6 imperfect lines (one unused
segment each) and 12 perfect lines.  The symmetry group of the signotope model acts on the
line labels as the dihedral group D_18 on Z_18 (shift: n->1, i->i+1; mirror: i->n+1-i), see
kobon_sym.py.  Hence it suffices to decide, for one representative S of every D_18-orbit of
6-subsets of {1..18}, the instance "tight + (lines in S imperfect, lines outside S perfect)"
WITHOUT the sigma lex-leader constraints (only sigma(1,2,3) = - , the global flip, which
fixes every label set).  If every cube is UNSAT then no 94-triangle simple arrangement
exists; a SAT cube yields an explicit arrangement.

usage: cubes.py gen            -> writes cubes/cube_<k>.cnf and cubes/index.txt
       cubes.py run K0 K1 [solver] [proofs]  -> solves cubes K0..K1-1 sequentially
"""
import itertools
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kobon_sat2 import Encoder2
from kobon_sat import analyse

HERE = os.path.dirname(os.path.abspath(__file__))
N, T = 18, 94
VARIANT = os.environ.get('CUBE_VARIANT', 'T2')
# 'T2'   : tight (T1 + T2) clauses, cubes = D_18-orbit reps of the 6-set of imperfect lines
# 'noT2' : tight T1 only, same cubes
# 'plain': NO structural lemma at all: cubes = D_18-orbit reps of the set S of lines carrying an
#          unused segment, |S| <= 6 (pure counting: at most 6 unused segments), no per-line AMO
CUBEDIR = os.path.join(HERE, {'T2': 'cubes', 'noT2': 'cubes_noT2', 'plain': 'cubes_plain'}[VARIANT])
KISSAT = os.path.join(HERE, '..', 'solvers', 'kissat', 'build', 'kissat')
CADICAL = os.path.join(HERE, '..', 'solvers', 'cadical', 'build', 'cadical')


def dihedral_reps(n, k):
    """Orbit representatives of k-subsets of {1..n} under D_n (labels on a cycle)."""
    def canon(S):
        best = None
        for a in range(n):
            for mir in (False, True):
                img = []
                for x in S:
                    y = (x - 1 + a) % n + 1          # shift by a
                    if mir:
                        y = n + 1 - y
                    img.append(y)
                key = tuple(sorted(img))
                if best is None or key < best:
                    best = key
        return best
    reps = {}
    for S in itertools.combinations(range(1, n + 1), k):
        c = canon(S)
        if c not in reps:
            reps[c] = 0
        reps[c] += 1
    return reps   # canonical rep -> orbit size


def base_encoder():
    if VARIANT == 'plain':
        E = Encoder2(N, T, symbreak=False, tight=False)
    else:
        E = Encoder2(N, T, symbreak=False, tight=True, t2=(VARIANT == 'T2'))
    E.clauses.append([-E.sig[(1, 2, 3)]])        # global flip
    return E


def gen():
    os.makedirs(CUBEDIR, exist_ok=True)
    if VARIANT == 'plain':
        reps = {}
        for k in range(0, 7):
            reps.update(dihedral_reps(N, k))
        total = sum(reps.values())
        assert total == sum(len(list(itertools.combinations(range(N), k))) for k in range(7)), total
    else:
        reps = dihedral_reps(N, 6)
        total = sum(reps.values())
        assert total == 18564, total
    E = base_encoder()
    base = list(E.clauses)
    with open(os.path.join(CUBEDIR, 'index.txt'), 'w') as idx:
        idx.write(f'# n={N} t={T} variant={VARIANT}; {len(reps)} D_18-orbit representatives (orbits cover {total} subsets)\n')
        for k, (S, osz) in enumerate(sorted(reps.items(), key=lambda kv: (len(kv[0]), kv[0]))):
            cl = list(base)
            for r in range(1, N + 1):
                segs = [E.uns[(r, a, b)] for a, b in itertools.combinations([x for x in range(1, N + 1) if x != r], 2)]
                if r in S:
                    cl.append(segs)                 # at least one unused segment (AMO already in tight)
                else:
                    for u in segs:
                        cl.append([-u])             # perfect line
            path = os.path.join(CUBEDIR, f'cube_{k:04d}.cnf')
            with open(path, 'w') as f:
                f.write(f'c cube {k} imperfect={list(S)} orbit={osz} n={N} tmin={T} variant={VARIANT} sym=flip-only nsig={E.nsig}\n')
                f.write(f'p cnf {E.nv} {len(cl)}\n')
                for c in cl:
                    f.write(' '.join(map(str, c)) + ' 0\n')
            idx.write(f'{k} {",".join(map(str, S))} {osz}\n')
    print(f'{len(reps)} cubes written to {CUBEDIR}')


def run(k0, k1, solver='kissat', proofs=False, reverse=False):
    E = None
    log = open(os.path.join(CUBEDIR, f'run_{k0:04d}_{k1:04d}{"_rev" if reverse else ""}.log'), 'a')
    order = range(k1 - 1, k0 - 1, -1) if reverse else range(k0, k1)
    for k in order:
        path = os.path.join(CUBEDIR, f'cube_{k:04d}.cnf')
        proof = os.path.join(CUBEDIR, f'cube_{k:04d}.drat')
        done = os.path.join(CUBEDIR, f'cube_{k:04d}.done')
        if os.path.exists(done):
            continue
        cmd = [KISSAT if solver == 'kissat' else CADICAL, path] + ([proof] if proofs else [])
        t0 = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True)
        dt = time.time() - t0
        out = p.stdout
        status = 'SAT' if 's SATISFIABLE' in out else ('UNSAT' if 's UNSATISFIABLE' in out else 'UNKNOWN')
        extra = ''
        if status == 'SAT':
            if E is None:
                E = base_encoder()
            lits = []
            for line in out.splitlines():
                if line.startswith('v '):
                    lits += [int(x) for x in line[2:].split()]
            sigma = E.decode([l for l in lits if l != 0])
            seqs, swaps, tris, nfaces = analyse(N, sigma)
            extra = f' TRIANGLES={len(tris)} faces={nfaces}'
            with open(os.path.join(CUBEDIR, f'cube_{k:04d}.model'), 'w') as f:
                f.write(out)
        line = f'cube {k} {status} {dt:.1f}s{extra}'
        print(line, flush=True)
        log.write(line + '\n')
        log.flush()
        if proofs and status == 'UNSAT' and os.path.exists(proof):
            subprocess.run(['gzip', '-1', '-f', proof])     # disk: verifier gunzips on demand
        with open(done, 'w') as f:
            f.write(line + '\n')


if __name__ == '__main__':
    if sys.argv[1] == 'gen':
        gen()
    else:
        k0, k1 = int(sys.argv[2]), int(sys.argv[3])
        solver = sys.argv[4] if len(sys.argv) > 4 else 'kissat'
        proofs = len(sys.argv) > 5 and sys.argv[5] == 'proofs'
        reverse = len(sys.argv) > 6 and sys.argv[6] == 'reverse'
        run(k0, k1, solver, proofs, reverse)
