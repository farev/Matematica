#!/usr/bin/env python3
"""Production sweep: decide SDS cells with the validated C engine,
verify witnesses independently, write certificates and results.csv.

Usage (from inside conjectures/signed-difference-sets/):
    python3 sweep.py --vmax 24                 # all statuses (concordance + new)
    python3 sweep.py --vmax 32 --open-only     # only Open cells
    python3 sweep.py --cells "SDS(20,11,2,[20])" --allmode
    python3 sweep.py --vmax 30 --jobs 4

Appends to data/results.csv (append-only run log). Certificates for
decisions of previously-Open cells and for audit reruns go to certs/.
"""

import argparse
import csv
import hashlib
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from math import comb

import sdslib


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def coords_of(idx, G):
    c = []
    for n in reversed(G):
        c.append(idx % n)
        idx //= n
    return list(reversed(c)) if len(G) > 1 else c[0]


def cost_of(v, k, lam):
    s = sdslib.s_of(v, k, lam)
    if s is None or (k + s) % 2:
        return 0
    nP, nM = (k + s) // 2, (k - s) // 2
    if nP < 1:
        return comb(v, nP) * comb(v - nP, nM)
    return comb(v - 1, nP - 1) * comb(v - nP, nM)


def run_cell(job):
    name, status, comment, v, k, lam, G, allmode, nodelimit = job
    facs = ",".join(str(x) for x in G)
    cmd = ["./sds_search", str(v), str(k), str(lam), facs, "--cap=50"]
    if allmode:
        cmd.append("--all")
    if nodelimit:
        cmd.append(f"--nodelimit={nodelimit}")
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    wall = time.time() - t0
    out = r.stdout
    result_line = next((l for l in out.splitlines() if l.startswith("RESULT")), "")
    wit = []
    for line in out.splitlines():
        if line.startswith("WITNESS"):
            p_part = line.split("P=")[1].split(" M=")[0]
            m_part = line.split("M=")[1].strip()
            P = [int(x) for x in p_part.split(",") if x != ""]
            M = [int(x) for x in m_part.split(",") if x != ""]
            wit.append((P, M))
    if "ABORTED" in result_line:
        decision = "ABORTED"
    elif " EXIST" in result_line:
        decision = "EXIST"
    elif "NONEXIST" in result_line:
        decision = "NONEXIST"
    else:
        decision = "ERROR"
    # independent verification of every reported witness
    ver_all = True
    ver_msgs = []
    for (P, M) in wit:
        ok, msg = sdslib.check_sds(v, k, lam, G,
                                   [coords_of(i, G) for i in P],
                                   [coords_of(i, G) for i in M])
        ver_all &= ok
        ver_msgs.append(msg)
    return dict(name=name, status=status, comment=comment, v=v, k=k,
                lam=lam, G=G, decision=decision, result_line=result_line,
                witnesses=wit, verified=ver_all, wall=wall,
                cmd=" ".join(cmd))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vmax", type=int, default=0)
    ap.add_argument("--vmin", type=int, default=1)
    ap.add_argument("--open-only", action="store_true")
    ap.add_argument("--cells", type=str, default="")
    ap.add_argument("--allmode", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--maxcost", type=float, default=5e9)
    ap.add_argument("--nodelimit", type=int, default=0)
    args = ap.parse_args()

    db = sdslib.load_db()
    jobs = []
    skipped_cost = 0
    for name, e in sorted(db.items()):
        v, k, lam, G = sdslib.parse_name(name)
        if args.cells:
            if name not in [c.strip() for c in args.cells.split(";")]:
                continue
        else:
            if not args.vmax or v > args.vmax or v < args.vmin:
                continue
            if args.open_only and e.get("status") != "Open":
                continue
            if cost_of(v, k, lam) > args.maxcost:
                skipped_cost += 1
                continue
        jobs.append((name, e.get("status"), e.get("comment", ""), v, k, lam,
                     G, args.allmode, args.nodelimit))

    print(f"{len(jobs)} cells queued ({skipped_cost} skipped by cost cap)")
    engine_hash = sha256("sds_search")
    src_hash = sha256("sds_search.c")

    os.makedirs("data", exist_ok=True)
    os.makedirs("certs", exist_ok=True)
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(run_cell, j): j[0] for j in jobs}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            mark = ""
            if r["status"] == "Open" and r["decision"] in ("EXIST", "NONEXIST"):
                mark = "  <-- NEW DECISION"
            elif r["status"] in ("Yes", "All") and r["decision"] == "NONEXIST":
                mark = "  <-- CONTRADICTS DB"
            elif r["status"] == "No" and r["decision"] == "EXIST":
                mark = "  <-- CONTRADICTS DB"
            print(f"{r['name']:30s} db={r['status']:4s} -> {r['decision']:8s} "
                  f"verified={r['verified']} wall={r['wall']:.2f}s{mark}")

    # append-only run log
    csv_path = "data/results.csv"
    new_file = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["utc", "name", "db_status", "decision", "witnesses",
                        "verified", "wall_s", "result_line", "cmd",
                        "engine_sha256", "source_sha256"])
        for r in sorted(results, key=lambda x: x["name"]):
            w.writerow([time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        r["name"], r["status"], r["decision"],
                        len(r["witnesses"]), r["verified"], f"{r['wall']:.3f}",
                        r["result_line"], r["cmd"], engine_hash, src_hash])

    # certificates for new decisions and DB contradictions
    for r in sorted(results, key=lambda x: x["name"]):
        newdec = r["status"] == "Open" and r["decision"] in ("EXIST", "NONEXIST")
        contra = (r["status"] in ("Yes", "All") and r["decision"] == "NONEXIST") or \
                 (r["status"] == "No" and r["decision"] == "EXIST")
        if not (newdec or contra or r["name"] in ("SDS(20,11,2,[20])",)):
            continue
        fn = "certs/" + r["name"].replace("(", "_").replace(")", "") \
                                 .replace(",", "_").replace("[", "").replace("]", "") + ".txt"
        with open(fn, "w") as f:
            f.write(f"# Certificate: decision of {r['name']}\n")
            f.write(f"# Date: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n")
            f.write(f"# Database status at fetch (2026-08-09, sha256 "
                    f"39bab9fce78d5c4353c22ba482ff5c3bb8b8b9931edc5ca0fc60062dfe80ca85): "
                    f"{r['status']} ({r['comment']})\n")
            f.write(f"# Engine: sds_search.c sha256={src_hash}\n")
            f.write(f"#         binary     sha256={engine_hash}\n")
            f.write(f"# Command: {r['cmd']}\n")
            f.write(f"# Decision: {r['decision']}\n")
            f.write(f"# {r['result_line']}\n")
            if r["decision"] == "NONEXIST":
                f.write("# Exhaustive search relative to the translation "
                        "reduction (0 in P), which is existence-preserving;\n"
                        "# independent verification: engine cross-validated "
                        "against a pure-Python exhaust (check_engine.py).\n")
            for (P, M) in r["witnesses"]:
                Pc = [coords_of(i, r["G"]) for i in P]
                Mc = [coords_of(i, r["G"]) for i in M]
                f.write(f"WITNESS_INDICES P={P} M={M}\n")
                f.write(f"WITNESS_COORDS  P={Pc} M={Mc}  "
                        f"(independently verified: {r['verified']})\n")
    n_new = sum(1 for r in results if r["status"] == "Open"
                and r["decision"] in ("EXIST", "NONEXIST"))
    n_contra = sum(1 for r in results
                   if (r["status"] in ("Yes", "All") and r["decision"] == "NONEXIST")
                   or (r["status"] == "No" and r["decision"] == "EXIST"))
    n_mismatch_ver = sum(1 for r in results if not r["verified"])
    print(f"\nsummary: {len(results)} cells, {n_new} new decisions, "
          f"{n_contra} DB contradictions, {n_mismatch_ver} verification failures")


if __name__ == "__main__":
    main()
