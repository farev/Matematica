#!/usr/bin/env python3
"""Driver for the peaceable-queens SAT pipeline.

Subcommands:
  ladder NMIN NMAX [--start-m K] [--symbreak]
      For each n, climb m until the first UNSAT; report a(n) = last SAT m.
      Records wall times to results/ladder.csv (appends).
  certify N M [--symbreak]
      Produce and verify the boundary certificate pair for a(N) = M:
        SAT witness at m = M   -> certs/witness_n{N}_m{M}.txt
                                  (verified by ./check_peaceable)
        UNSAT proof at m = M+1 -> certs/pq_n{N}_m{M+1}.cnf + .drat
                                  (cadical --plain, verified by rup_check)
  solve N M [--symbreak] [--plain] [--proof FILE]
      One decision instance, prints status and time.

Solver: system cadical (reports 1.7.3; Ubuntu package 1.7.4-1).
cadical is deterministic for a fixed instance and options; no seeds.
"""

import argparse
import csv
import hashlib
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RUP_CHECK = os.path.join(HERE, "..", "..", "tools", "satcert", "rup_check")
CHECKER = os.path.join(HERE, "check_peaceable")

sys.path.insert(0, HERE)
from encode import build, cell_vars  # noqa: E402
from encode_lines import build_lines, decode_grid  # noqa: E402


def write_cnf(nvars, clauses, path, header=""):
    with open(path, "w") as f:
        if header:
            for line in header.strip().split("\n"):
                f.write(f"c {line}\n")
        f.write(f"p cnf {nvars} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")


def run_cadical(cnf_path, proof_path=None, plain=False, timeout=None):
    cmd = ["cadical", "-q"]
    if plain:
        cmd.append("--plain")
    cmd.append(cnf_path)
    if proof_path:
        cmd += [proof_path, "--no-binary"]
    t0 = time.time()
    try:
        res = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", None, time.time() - t0
    dt = time.time() - t0
    out = res.stdout
    if res.returncode == 10:
        model = set()
        for line in out.splitlines():
            if line.startswith("v "):
                for tok in line[2:].split():
                    v = int(tok)
                    if v > 0:
                        model.add(v)
        return "SAT", model, dt
    if res.returncode == 20:
        return "UNSAT", None, dt
    raise RuntimeError(f"cadical rc={res.returncode}: {out}\n{res.stderr}")


def model_to_grid(n, model):
    w, b = cell_vars(n)
    rows = []
    for r in range(n):
        row = ""
        for c in range(n):
            if w(r, c) in model:
                row += "W"
            elif b(r, c) in model:
                row += "B"
            else:
                row += "."
        rows.append(row)
    return rows


def verify_witness(n, m, grid_rows):
    inp = f"{n} {m}\n" + "\n".join(grid_rows) + "\n"
    res = subprocess.run([CHECKER], input=inp, capture_output=True, text=True)
    return res.returncode == 0, res.stdout.strip() or res.stderr.strip()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def solve_instance(n, m, symbreak=False, plain=False, proof=None,
                   timeout=None, rowvars=False, lines=False, cuts=False):
    if lines:
        nvars, clauses = build_lines(n, m, symbreak=symbreak, cuts=cuts)
    else:
        nvars, clauses, _ = build(n, m, symbreak=symbreak, rowvars=rowvars)
    tmp = os.path.join(HERE, f".tmp_n{n}_m{m}.cnf")
    write_cnf(nvars, clauses, tmp,
              f"peaceable queens n={n} m={m} symbreak={symbreak} "
              f"lines={lines}")
    status, model, dt = run_cadical(tmp, proof_path=proof, plain=plain,
                                    timeout=timeout)
    if proof is None:
        os.remove(tmp)
        return status, model, dt, nvars, len(clauses)
    return status, model, dt, nvars, len(clauses), tmp


def cmd_ladder(args):
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    csv_path = os.path.join(HERE, "results", "ladder.csv")
    new = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        wcsv = csv.writer(f)
        if new:
            wcsv.writerow(["n", "a_n", "m_unsat", "sat_s", "unsat_s",
                           "nvars", "nclauses", "symbreak"])
        m = args.start_m
        for n in range(args.nmin, args.nmax + 1):
            m = max(m, 1)
            last_sat, sat_time = None, 0.0
            while True:
                status, model, dt, nv, nc = solve_instance(
                    n, m, symbreak=args.symbreak, lines=args.lines,
                    cuts=args.cuts)
                print(f"n={n} m={m}: {status} in {dt:.2f}s", flush=True)
                if status == "SAT":
                    last_sat, sat_time = m, dt
                    m += 1
                elif status == "UNSAT":
                    wcsv.writerow([n, last_sat, m, f"{sat_time:.2f}",
                                   f"{dt:.2f}", nv, nc,
                                   f"{args.symbreak}/lines={args.lines}"
                                   f"/cuts={args.cuts}"])
                    f.flush()
                    print(f"  -> a({n}) = {last_sat} "
                          f"(UNSAT at {m} in {dt:.2f}s)", flush=True)
                    break
                else:
                    print(f"  -> {status}, aborting rung", flush=True)
                    return
            m = last_sat  # warm start next rung: a(n+1) >= a(n)


def cmd_certify(args):
    certs = os.path.join(HERE, "certs")
    os.makedirs(certs, exist_ok=True)
    n, m = args.n, args.m

    # SAT side: witness at m.
    status, model, dt, *_ = solve_instance(n, m, symbreak=args.symbreak)
    assert status == "SAT", f"expected SAT at m={m}, got {status}"
    grid = model_to_grid(n, model)
    ok, msg = verify_witness(n, m, grid)
    assert ok, f"witness verification failed: {msg}"
    wpath = os.path.join(certs, f"witness_n{n}_m{m}.txt")
    with open(wpath, "w") as f:
        f.write(f"{n} {m}\n")
        f.write("\n".join(grid) + "\n")
    print(f"witness at m={m}: verified, {dt:.1f}s -> {wpath}")
    print(f"  {msg}")

    # UNSAT side: DRUP proof at m+1, cadical --plain, checked by rup_check.
    cnf_path = os.path.join(certs, f"pq_n{n}_m{m+1}.cnf")
    proof_path = os.path.join(certs, f"pq_n{n}_m{m+1}.drat")
    nvars, clauses, _ = build(n, m + 1, symbreak=args.symbreak)
    write_cnf(nvars, clauses, cnf_path,
              f"peaceable queens n={n} m={m+1} symbreak={args.symbreak}\n"
              f"UNSAT here + verified witness at m={m} proves a({n})={m}\n"
              f"generated by encode.py, solved by cadical --plain")
    status, _, dt = run_cadical(cnf_path, proof_path=proof_path, plain=True)
    assert status == "UNSAT", f"expected UNSAT at m={m+1}, got {status}"
    res = subprocess.run([RUP_CHECK, cnf_path, proof_path],
                         capture_output=True, text=True)
    verified = res.returncode == 0
    print(f"UNSAT at m={m+1}: {dt:.1f}s, proof "
          f"{os.path.getsize(proof_path)} bytes, "
          f"rup_check: {res.stdout.strip() or res.stderr.strip()}")
    assert verified, "DRUP proof failed verification"
    for p in (cnf_path, proof_path, wpath):
        print(f"  sha256 {sha256(p)[:16]}…  {os.path.basename(p)}")


def cmd_solve(args):
    r = solve_instance(args.n, args.m, symbreak=args.symbreak,
                       plain=args.plain, proof=args.proof,
                       rowvars=args.rowvars, lines=args.lines,
                       cuts=args.cuts)
    status, model, dt, nv, nc = r[:5]
    print(f"n={args.n} m={args.m}: {status} in {dt:.2f}s "
          f"({nv} vars, {nc} clauses)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    lad = sub.add_parser("ladder")
    lad.add_argument("nmin", type=int)
    lad.add_argument("nmax", type=int)
    lad.add_argument("--start-m", type=int, default=1)
    lad.add_argument("--symbreak", action="store_true")
    lad.add_argument("--lines", action="store_true")
    lad.add_argument("--cuts", action="store_true")
    lad.set_defaults(func=cmd_ladder)

    cer = sub.add_parser("certify")
    cer.add_argument("n", type=int)
    cer.add_argument("m", type=int)
    cer.add_argument("--symbreak", action="store_true")
    cer.set_defaults(func=cmd_certify)

    sol = sub.add_parser("solve")
    sol.add_argument("n", type=int)
    sol.add_argument("m", type=int)
    sol.add_argument("--symbreak", action="store_true")
    sol.add_argument("--plain", action="store_true")
    sol.add_argument("--proof")
    sol.add_argument("--rowvars", action="store_true")
    sol.add_argument("--lines", action="store_true")
    sol.add_argument("--cuts", action="store_true")
    sol.set_defaults(func=cmd_solve)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
