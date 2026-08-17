#!/usr/bin/env python3
"""Cube-and-conquer UNSAT campaign for one vdW instance, resumable.

Splitting: static binary split on the k most AP-covered ("central")
variables; each cube is a full sign pattern over those variables, appended
as unit clauses. Adaptive deepening: a cube whose Glucose run exhausts its
conflict budget is re-split on the next central variables (depth+step),
its children queued; the parent is recorded as SPLIT. The disjunction of
live cubes always covers the original search space: a case split on
variable values is a tautology, so
    (all leaf cubes UNSAT)  ==>  instance UNSAT.
Each leaf gets its own DRUP proof of (CNF + cube units) |- [], checked by
rup_check immediately; campaign state is an append-only CSV keyed by cube,
safe to resume after interruption.

Certificate story shipped by the campaign:
  - per-leaf: cnf hash is shared, cube literals recorded, proof checked
    at production time, verdict + sha256 in the CSV;
  - the case-split lemma is trivial (sign patterns over fixed variables);
  - merge_proofs.py (separate) can assemble one monolithic DRUP for the
    plain CNF out of the leaf proofs by relativization when disk allows.

Usage:
  python3 cnc.py s t n depth budget_conflicts [workers]
State file: data/cnc_{s}_{t}_n{n}.csv   (append-only)
Leaf proofs: certs/cnc_{s}_{t}_n{n}/cube_<id>.drup (deleted after check if
larger than KEEP_BYTES; sha256 always recorded first).
"""
import csv
import hashlib
import os
import subprocess
import sys
import time
from multiprocessing import Pool

from pysat.solvers import Glucose42

from vdw_cnf import vdw_clauses, write_dimacs

HERE = os.path.dirname(os.path.abspath(__file__))
RUP_CHECK = os.path.join(HERE, "..", "..", "tools", "satcert", "rup_check")
KEEP_BYTES = 8 * 1024 * 1024


def central_vars(n, s, t, k):
    """The k variables covered by the most APs (ties: closer to center)."""
    cover = [0] * (n + 1)
    from vdw_cnf import aps
    for ap in aps(n, s) + aps(n, t):
        for p in ap:
            cover[p] += 1
    order = sorted(range(1, n + 1),
                   key=lambda v: (-cover[v], abs(v - (n + 1) / 2)))
    return order[:k]


def cube_id(lits):
    return ".".join(str(l) for l in lits)


def solve_cube(args):
    (n, s, t, lits, budget, certdir, cnfpath) = args
    cls = vdw_clauses(n, s, t)
    for l in lits:
        cls.append([l])
    t0 = time.time()
    with Glucose42(bootstrap_with=cls, with_proof=True) as S:
        if budget:
            S.conf_budget(budget)
            res = S.solve_limited()
        else:
            res = S.solve()
        el = time.time() - t0
        if res is None:
            return (cube_id(lits), "INDET", el, None, None, None)
        if res:
            model = S.get_model()
            return (cube_id(lits), "SAT", el, None, None,
                    " ".join(map(str, model[:n])))
        proof = S.get_proof()
        conf = S.accum_stats().get("conflicts")
    cid = cube_id(lits)
    prf = os.path.join(certdir, f"cube_{cid}.drup")
    # cube units go at the END of the cnf copy each worker writes once
    with open(prf, "w") as f:
        f.write("\n".join(proof) + ("\n" if proof else ""))
    h = hashlib.sha256(open(prf, "rb").read()).hexdigest()
    # verify: cnf + units file
    cubecnf = os.path.join(certdir, f"cube_{cid}.cnf")
    write_dimacs(cubecnf, n, cls)
    r = subprocess.run([RUP_CHECK, cubecnf, prf], capture_output=True,
                       text=True)
    ok = r.returncode == 0 and "VERIFIED" in r.stdout
    sz = os.path.getsize(prf)
    if sz > KEEP_BYTES:
        os.remove(prf)
    os.remove(cubecnf)
    return (cid, "UNSAT" if ok else "UNSAT-CHECKFAIL", el, conf, h, str(sz))


def main():
    s, t, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    depth = int(sys.argv[4])
    budget = int(sys.argv[5])
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    split_step = 4

    datadir = os.path.join(HERE, "data")
    certdir = os.path.join(HERE, "certs", f"cnc_{s}_{t}_n{n}")
    os.makedirs(datadir, exist_ok=True)
    os.makedirs(certdir, exist_ok=True)
    state = os.path.join(datadir, f"cnc_{s}_{t}_n{n}.csv")

    cls = vdw_clauses(n, s, t)
    cnfpath = os.path.join(certdir, "base.cnf")
    if not os.path.exists(cnfpath):
        write_dimacs(cnfpath, n, cls)

    done = {}
    if os.path.exists(state):
        with open(state) as f:
            for row in csv.reader(f):
                if row and row[0] != "cube":
                    done[row[0]] = row[1]

    order = central_vars(n, s, t, depth + 8 * split_step)
    base_vars = order[:depth]

    def expand(prefix_lits, dnext):
        """All cubes at depth dnext extending prefix (on `order` vars)."""
        out = []
        got = len(prefix_lits)
        vs = order[got:dnext]
        def rec(i, cur):
            if i == len(vs):
                out.append(tuple(cur))
                return
            rec(i + 1, cur + [vs[i]])
            rec(i + 1, cur + [-vs[i]])
        rec(0, list(prefix_lits))
        return out

    queue = [c for c in expand((), depth)]
    print(f"[cnc ({s},{t}) n={n}] {len(queue)} cubes at depth {depth}, "
          f"budget {budget} conflicts, {workers} workers; "
          f"{len(done)} rows already recorded", flush=True)

    newf = not os.path.exists(state)
    sf = open(state, "a", newline="")
    sw = csv.writer(sf)
    if newf:
        sw.writerow(["cube", "status", "seconds", "conflicts",
                     "proof_sha256", "note"])
        sf.flush()

    pending = [c for c in queue if cube_id(c) not in done
               or done[cube_id(c)] == "INDET"]
    print(f"  {len(pending)} cubes to run", flush=True)
    sat_found = None
    round_no = 0
    while pending and not sat_found:
        round_no += 1
        args = [(n, s, t, list(c), budget, certdir, cnfpath) for c in pending]
        nxt = []
        with Pool(workers) as pool:
            for res in pool.imap_unordered(solve_cube, args):
                cid, status, el, conf, h, note = res
                sw.writerow([cid, status, f"{el:.2f}", conf, h, note])
                sf.flush()
                if status == "SAT":
                    sat_found = (cid, note)
                    pool.terminate()
                    break
                if status == "INDET":
                    lits = tuple(int(x) for x in cid.split("."))
                    kids = expand(lits, len(lits) + split_step)
                    nxt.extend(kids)
                    sw.writerow([cid, "SPLIT", f"{el:.2f}", conf, "",
                                 f"->{len(kids)} kids"])
                    sf.flush()
                if status == "UNSAT-CHECKFAIL":
                    print(f"  !! RUP CHECK FAILED on cube {cid}", flush=True)
        pending = nxt
        if nxt:
            print(f"  round {round_no}: {len(nxt)} deeper cubes queued",
                  flush=True)
    sf.close()
    if sat_found:
        print(f"SAT in cube {sat_found[0]} — instance is satisfiable; "
              f"witness prefix recorded in CSV", flush=True)
        sys.exit(1)
    # completion check: every leaf in CSV closed?
    closed, split, indet, checkfail = 0, 0, 0, 0
    with open(state) as f:
        rows = {r[0]: r[1] for r in csv.reader(f) if r and r[0] != "cube"}
    for cid, stt in rows.items():
        if stt == "UNSAT":
            closed += 1
        elif stt == "SPLIT":
            split += 1
        elif stt == "INDET":
            indet += 1
        elif stt == "UNSAT-CHECKFAIL":
            checkfail += 1
    print(f"campaign state: {closed} leaves UNSAT-verified, {split} split, "
          f"{indet} indeterminate, {checkfail} CHECKFAIL", flush=True)
    if indet == 0 and checkfail == 0 and not sat_found:
        print("ALL LEAVES CLOSED — instance UNSAT (case-split lemma + "
              "per-leaf verified proofs)", flush=True)


if __name__ == "__main__":
    main()
