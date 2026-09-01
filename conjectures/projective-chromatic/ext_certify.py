"""DRUP-certify the non-extension of the first N sampled chi_2(7) witnesses.

Replays the exact sampling stream of sample_extend.py (same seed0 => same
GL(7,2) relabelings and kissat seeds => same witnesses), rebuilds each
extension instance, proves UNSAT with Glucose42+DRUP and checks each proof
with rup_check. Reports N/N verified. Proof files are not kept (each is
re-derivable in milliseconds); this certifies the *claim*, the pipeline
stays the certificate generator.

Usage: python3 ext_certify.py [N=50] [seed0=20000]
(seed0 must match the sample_extend.py run being certified.)
"""
import random
import subprocess
import sys
import tempfile
import os
from pysat.solvers import Glucose42
from sample_extend import sample_witness, M7, K

RUP = "./rup_check"


def extension_cnf(color7):
    var = lambda v, c: v * K + c + 1
    cnf = [[var(v, c) for c in range(K)] for v in range(128)]
    for h in range(1, 128):
        ch = color7[h]
        for v in range(128):
            w = v ^ h
            if v < w:
                cnf.append([-var(v, ch), -var(w, ch)])
    return cnf, 128 * K


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    rng = random.Random(seed0)
    nver = 0
    for i in range(n):
        w = sample_witness(seed0 + i, rng)
        cnf, nv = extension_cnf(w)
        with Glucose42(bootstrap_with=cnf, with_proof=True) as s:
            r = s.solve()
            if r:
                print(f"[{i}] EXTENDS — a chi_2(8)=5 witness exists! investigate immediately")
                return 1
            proof = s.get_proof()
        with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as fc:
            fc.write(f"p cnf {nv} {len(cnf)}\n")
            for cl in cnf:
                fc.write(" ".join(map(str, cl)) + " 0\n")
            cpath = fc.name
        with tempfile.NamedTemporaryFile("w", suffix=".drup", delete=False) as fp:
            for line in proof:
                fp.write(line + "\n")
            fp.write("0\n")
            ppath = fp.name
        rc = subprocess.run([RUP, cpath, ppath], capture_output=True, text=True)
        os.unlink(cpath)
        os.unlink(ppath)
        if rc.returncode == 0 and "VERIFIED" in rc.stdout:
            nver += 1
        else:
            print(f"[{i}] proof check FAILED: {rc.stdout.strip()}")
            return 1
    print(f"{nver}/{n} non-extensions DRUP-verified (seed0={seed0})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
