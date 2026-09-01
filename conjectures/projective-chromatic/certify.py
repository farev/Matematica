"""Certified UNSAT runs: Glucose42 with DRUP proof, checked by rup_check.
Usage: certify.py file.cnf [file2.cnf ...]
On SAT: prints the model summary (caller should lift+verify).
On UNSAT: writes file.drup, runs rup_check, reports VERIFIED or not.
"""
import subprocess
import sys
import time
from pysat.formula import CNF
from pysat.solvers import Glucose42

RUP = "./rup_check"  # build: gcc -O2 -o rup_check ../../tools/satcert/rup_check.c

for path in sys.argv[1:]:
    cnf = CNF(from_file=path)
    t0 = time.time()
    with Glucose42(bootstrap_with=cnf, with_proof=True) as s:
        r = s.solve()
        dt = time.time() - t0
        if r:
            print(f"{path}: SAT ({dt:.1f}s) — needs lifting/verification!", flush=True)
        else:
            proof = s.get_proof()
            ppath = path.replace(".cnf", ".drup")
            with open(ppath, "w") as f:
                for line in proof:
                    f.write(line + "\n")
                f.write("0\n")  # ensure empty clause terminates proof
            rc = subprocess.run([RUP, path, ppath], capture_output=True, text=True)
            print(f"{path}: UNSAT ({dt:.1f}s), proof {len(proof)} lines -> "
                  f"rup_check: {rc.stdout.strip() or rc.stderr.strip()} (exit {rc.returncode})", flush=True)
