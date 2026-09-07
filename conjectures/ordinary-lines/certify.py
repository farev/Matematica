#!/usr/bin/env python3
"""certify.py -- run every cube of (n, m) through kissat with DRAT proof logging, verify each
UNSAT proof with drat-trim, and record a machine-readable ledger.

usage: python3 certify.py n m [--jobs J] [--timeout S] [--outdir DIR] [--only i,j,...]
Each cube i produces DIR/n{n}m{m}_c{i}.cnf, .drat (deleted after verification unless
--keep-proofs), .log, and a line in DIR/ledger_n{n}m{m}.jsonl with
  {"cube": i, "big": [...], "t3": .., "result": "UNSAT"|"SAT"|"TIMEOUT", "solve_s": ..,
   "proof_bytes": .., "drat_trim": "VERIFIED"|"FAILED"|"n/a", "verify_s": .., "sha256_cnf": ..}
A SAT cube additionally writes the model to DIR/n{n}m{m}_c{i}.model and the decoded lines.
"""
import sys, os, json, time, subprocess, hashlib, argparse
from concurrent.futures import ThreadPoolExecutor
from cubes import placements
from distributions import distributions
from ordlines_sat import OrdLinesEncoder

HERE = os.path.dirname(os.path.abspath(__file__))
K = os.environ.get('KISSAT', 'kissat')
DT = os.environ.get('DRATTRIM', 'drat-trim')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def all_cubes(n, m):
    cubes = []
    for d in distributions(n, m):
        sizes = [k for k, c in d.items() if k >= 4 for _ in range(c)]
        for lines in (placements(n, sizes) if sizes else [[]]):
            cubes.append((d[3], [tuple(L) for L in lines]))
    return cubes


def run_cube(n, m, idx, t3, lines, outdir, timeout, keep_proofs):
    base = os.path.join(outdir, f"n{n}m{m}_c{idx}")
    cnf, drat, log = base + '.cnf', base + '.drat', base + '.log'
    enc = OrdLinesEncoder(n, m, big_lines=lines, exact_big=True)
    enc.write_dimacs(cnf, comment=f"cube {idx} t3={t3}")
    rec = {'cube': idx, 'n': n, 'm': m, 'big': [list(L) for L in lines], 't3': t3,
           'vars': enc.stats['vars'], 'clauses': enc.stats['clauses'], 'sha256_cnf': sha256(cnf)}
    t0 = time.time()
    try:
        with open(log, 'w') as lf:
            p = subprocess.run([K, '--no-binary', cnf, drat], stdout=lf, stderr=subprocess.STDOUT,
                               text=True, timeout=timeout)
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
            rec['drat_trim_tail'] = q.stdout.strip().splitlines()[-1] if q.stdout.strip() else ''
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
        lines_found, chi = enc.decode(model)
        with open(base + '.model', 'w') as f:
            f.write(' '.join(map(str, model)) + '\n')
        rec['lines'] = [list(L) for L in lines_found]
        rec['ordinary'] = sum(1 for L in lines_found if len(L) == 2)
        if os.path.exists(drat):
            os.remove(drat)
    else:
        if os.path.exists(drat):
            os.remove(drat)
    return rec


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('m', type=int)
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--timeout', type=int, default=7200)
    ap.add_argument('--outdir', default=None)
    ap.add_argument('--only', default=None)
    ap.add_argument('--keep-proofs', action='store_true')
    a = ap.parse_args()
    outdir = a.outdir or os.path.join(HERE, f"cert_n{a.n}m{a.m}")
    os.makedirs(outdir, exist_ok=True)
    cubes = all_cubes(a.n, a.m)
    sel = list(range(len(cubes))) if a.only is None else [int(x) for x in a.only.split(',')]
    ledger = os.path.join(outdir, f"ledger_n{a.n}m{a.m}.jsonl")
    print(f"n={a.n} m={a.m}: {len(cubes)} cubes, running {len(sel)} with {a.jobs} jobs; ledger {ledger}", flush=True)

    def work(idx):
        t3, lines = cubes[idx]
        rec = run_cube(a.n, a.m, idx, t3, lines, outdir, a.timeout, a.keep_proofs)
        with open(ledger, 'a') as f:
            f.write(json.dumps(rec) + '\n')
        print(json.dumps({k: rec[k] for k in ('cube', 'big', 't3', 'result', 'solve_s', 'proof_bytes', 'drat_trim') if k in rec}), flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        recs = list(ex.map(work, sel))
    summary = {}
    for r in recs:
        summary[r['result']] = summary.get(r['result'], 0) + 1
    print('summary', summary, 'verified', sum(1 for r in recs if r.get('drat_trim') == 'VERIFIED'), flush=True)
