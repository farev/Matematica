#!/usr/bin/env python3
"""Decide and certify mixed van der Waerden cells w(2; s, t).

Pipeline per (s, t, n):
  fast path : CaDiCaL 1.9.5 (pysat 'cd19'), no proof -- bracketing only.
  cert path : Glucose 4.2 with DRUP proof.
      SAT   -> coloring extracted, re-verified by vdw_cnf.coloring_is_good
               (independent AP enumeration), witness saved to data/.
      UNSAT -> CNF + DRUP written to certs/, checked by tools/satcert/rup_check
               (from-definition C checker, no code shared with any solver).

Correctness of a cell value rests only on the two boundary certificates plus
restriction monotonicity (a good partition of [1,n] restricts to [1,m]):
  witness at w-1 (verified)  +  UNSAT at w (RUP-VERIFIED)  ==>  w(2;s,t) = w.

Usage:
  python3 solve_cell.py fast  s t n         # cadical decide, print SAT/UNSAT
  python3 solve_cell.py cert  s t w         # certify cell value = w
  python3 solve_cell.py unsat s t n         # certified UNSAT at a single n
  python3 solve_cell.py wit   s t n         # witness at a single n (SAT side)
"""
import os
import subprocess
import sys
import time
import hashlib

from pysat.solvers import Glucose42, Cadical195

from vdw_cnf import vdw_clauses, coloring_is_good, write_dimacs

HERE = os.path.dirname(os.path.abspath(__file__))
RUP_CHECK = os.path.join(HERE, "..", "..", "tools", "satcert", "rup_check")
DATA = os.path.join(HERE, "data")
CERTS = os.path.join(HERE, "certs")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def model_to_coloring(model, n):
    col = [0] * (n + 1)
    for lit in model:
        v = abs(lit)
        if 1 <= v <= n:
            col[v] = 1 if lit > 0 else 0
    return col


def decide_fast(n, s, t, return_witness=False):
    cls = vdw_clauses(n, s, t)
    with Cadical195(bootstrap_with=cls) as S:
        t0 = time.time()
        sat = S.solve()
        el = time.time() - t0
        if sat and return_witness:
            return True, el, model_to_coloring(S.get_model(), n)
        return sat, el, None


def save_witness(col, n, s, t, tag=""):
    if not coloring_is_good(col, s, t):
        raise RuntimeError("witness FAILED independent verification")
    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, f"witness_{s}_{t}_n{n}{tag}.txt")
    with open(path, "w") as f:
        f.write(f"# good partition of [1,{n}] for (s,t)=({s},{t}): "
                f"no {s}-AP in color 0, no {t}-AP in color 1\n")
        f.write("".join(str(col[i]) for i in range(1, n + 1)) + "\n")
    return path


def certified_unsat(n, s, t, budget=None):
    """Glucose42 + DRUP + rup_check. Returns dict or 'SAT'/'INDET'."""
    cls = vdw_clauses(n, s, t)
    os.makedirs(CERTS, exist_ok=True)
    with Glucose42(bootstrap_with=cls, with_proof=True) as S:
        t0 = time.time()
        if budget:
            S.conf_budget(budget)
            res = S.solve_limited()
        else:
            res = S.solve()
        el = time.time() - t0
        if res is None:
            return {"status": "INDET", "seconds": el}
        if res:
            col = model_to_coloring(S.get_model(), n)
            wpath = save_witness(col, n, s, t)
            return {"status": "SAT", "seconds": el, "witness": wpath}
        proof = S.get_proof()
        stats = S.accum_stats()
    cnff = os.path.join(CERTS, f"vdw_{s}_{t}_n{n}.cnf")
    prf = os.path.join(CERTS, f"vdw_{s}_{t}_n{n}.drup")
    write_dimacs(cnff, n, cls)
    with open(prf, "w") as f:
        f.write("\n".join(proof) + ("\n" if proof else ""))
    t1 = time.time()
    chk = subprocess.run([RUP_CHECK, cnff, prf], capture_output=True, text=True)
    tchk = time.time() - t1
    verified = chk.returncode == 0 and "VERIFIED" in chk.stdout
    return {
        "status": "UNSAT", "seconds": el, "proof_lines": len(proof),
        "conflicts": stats.get("conflicts"), "cnf": cnff, "drup": prf,
        "rup_verified": verified, "check_seconds": tchk,
        "drup_sha256": sha256(prf), "cnf_sha256": sha256(cnff),
    }


def certify_cell(s, t, w):
    """Full boundary certification that w(2;s,t) = w."""
    print(f"[cell ({s},{t})] certifying value {w}")
    sat, el, col = decide_fast(w - 1, s, t, return_witness=True)
    if not sat:
        raise RuntimeError(f"boundary mismatch: n={w-1} came back UNSAT")
    wpath = save_witness(col, w - 1, s, t)
    print(f"  witness at {w-1}: found in {el:.2f}s (cadical), "
          f"independently verified, saved {os.path.basename(wpath)}")
    r = certified_unsat(w, s, t)
    if r["status"] != "UNSAT":
        raise RuntimeError(f"boundary mismatch at n={w}: {r['status']}")
    if not r["rup_verified"]:
        raise RuntimeError(f"RUP CHECK FAILED for {r['drup']}")
    print(f"  UNSAT at {w}: glucose {r['seconds']:.2f}s, "
          f"{r['proof_lines']} proof lines, RUP-VERIFIED "
          f"in {r['check_seconds']:.2f}s")
    print(f"  drup sha256 {r['drup_sha256'][:16]}...  ==> w(2;{s},{t}) = {w}")
    return r


if __name__ == "__main__":
    cmd, s, t, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    if cmd == "fast":
        sat, el, _ = decide_fast(n, s, t)
        print(f"({s},{t}) n={n}: {'SAT' if sat else 'UNSAT'} in {el:.2f}s")
    elif cmd == "cert":
        certify_cell(s, t, n)
    elif cmd == "unsat":
        r = certified_unsat(n, s, t)
        print(r)
    elif cmd == "wit":
        sat, el, col = decide_fast(n, s, t, return_witness=True)
        if sat:
            p = save_witness(col, n, s, t)
            print(f"SAT in {el:.2f}s, witness verified, saved {p}")
        else:
            print(f"UNSAT in {el:.2f}s")
    else:
        sys.exit("unknown command")
