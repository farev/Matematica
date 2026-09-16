#!/usr/bin/env python3
"""Certification pass for an UNSAT instance written by nrsat.py.

1. validate_nrsat: every clause is a necessary condition (independent code);
2. Glucose 4.2 (proof-logging) re-solves <tag>.cnf from the file and writes
   <tag>.drup;
3. drat-trim (Heule) and rup_check (this repository's from-the-definition
   DRUP checker, tools/satcert/rup_check.c) both check the proof.
usage: certify.py TAG [rup_check_path] [drat_trim_path]"""
import sys, time, subprocess, os, hashlib
from pysat.formula import CNF
from pysat.solvers import Glucose42

tag = sys.argv[1]
rup = sys.argv[2] if len(sys.argv) > 2 else './rup_check'
drat = sys.argv[3] if len(sys.argv) > 3 else './drat-trim'
r = subprocess.run([sys.executable, 'validate_nrsat.py', tag], capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip()[-500:])
assert r.returncode == 0, "encoding validation failed"
cnf = CNF(from_file=f'{tag}.cnf')
t0 = time.time()
with Glucose42(bootstrap_with=cnf.clauses, with_proof=True) as s:
    res = s.solve()
    proof = s.get_proof()
t1 = time.time()
print(f"glucose42: {'UNSAT' if not res else 'SAT'} in {t1-t0:.1f}s, proof {len(proof)} lines")
assert res is False
with open(f'{tag}.drup', 'w') as f:
    f.write('\n'.join(proof) + '\n')
for name, cmd in [('drat-trim', [drat, f'{tag}.cnf', f'{tag}.drup']), ('rup_check', [rup, f'{tag}.cnf', f'{tag}.drup'])]:
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    verdict = [l for l in out if 'VERIFIED' in l or 'FAIL' in l or 'ERROR' in l or 'error' in l]
    print(f"{name}: exit {r.returncode}, {time.time()-t:.1f}s: {verdict[-1] if verdict else out[-1:]}")
h = hashlib.sha256(open(f'{tag}.cnf', 'rb').read()).hexdigest()[:16]
print(f"sha256({tag}.cnf)[:16] = {h}; clauses {len(cnf.clauses)}, vars {cnf.nv}, proof lines {len(proof)}")
