#!/usr/bin/env python3
"""sweep10.py — the a(10) sweep: for m = 161..308 ascending, decide whether a
10-element DSS set with largest element exactly m exists.

Every completed m with status NONE is a certified statement f(10) > m (given
the ladder's f(1..9), which the engine's fmin prunes consume). Completing all
m <= 308 proves f(10) = 309, since the Conway-Guy 10-set (validated by
validate_set.py, independent of both engines) shows f(10) <= 309.
A FOUND at any m (all smaller m having been cleared) proves f(10) = m and
refutes Conway-Guy optimality at n = 10.

Resumable: state in data/n10_sweep.csv (one row per completed m, appended and
flushed immediately); on restart, completed m are skipped. Solutions, if any,
are appended to data/n10_solutions.txt and validated on the spot.

Usage: python3 sweep10.py [--from M] [--to M] [--engine ./dss_search]
"""
import csv
import os
import re
import subprocess
import sys
import time

from validate_set import is_dss

CSV = "data/n10_sweep.csv"
SOLS = "data/n10_solutions.txt"
RESULT_RE = re.compile(
    r"RESULT n=(\d+) m=(\d+) status=(\w+) solutions=(\d+) nodes=(\d+) "
    r"depth_nodes=([\d,]+) tasks=(\d+) time=([\d.]+) threads=(\d+)")
SOL_RE = re.compile(r"SOLUTION n=\d+ m=\d+ set=([\d,]+)")


def completed():
    done = {}
    if os.path.exists(CSV):
        with open(CSV) as fh:
            for row in csv.DictReader(fh):
                done[int(row["m"])] = row["status"]
    return done


def main():
    lo, hi, engine = 161, 308, "./dss_search"
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == "--from": lo = int(args.pop(0))
        elif a == "--to": hi = int(args.pop(0))
        elif a == "--engine": engine = args.pop(0)
    done = completed()
    newfile = not os.path.exists(CSV)
    fh = open(CSV, "a", newline="")
    w = csv.writer(fh)
    if newfile:
        w.writerow(["n", "m", "status", "solutions", "nodes", "depth_nodes",
                    "tasks", "seconds", "threads", "engine"])
        fh.flush()
    for m in range(lo, hi + 1):
        if m in done:
            continue
        t0 = time.time()
        out = subprocess.run([engine, "10", str(m)], capture_output=True,
                             text=True, check=True).stdout
        g = RESULT_RE.search(out)
        assert g, out
        status = g.group(3)
        sols = [[int(x) for x in s.split(",")] for s in SOL_RE.findall(out)]
        for s in sols:
            assert is_dss(s) and len(s) == 10 and max(s) == m, f"BAD SOLUTION {s}"
            with open(SOLS, "a") as sfh:
                sfh.write(f"m={m} set={s} validated=True\n")
        w.writerow([10, m, status, g.group(4), g.group(5), g.group(6),
                    g.group(7), g.group(8), g.group(9), os.path.basename(engine)])
        fh.flush()
        print(f"[{time.strftime('%H:%M:%S')}] m={m} {status} "
              f"nodes={g.group(5)} {float(g.group(8)):.1f}s", flush=True)
        if status == "FOUND":
            print(f"*** DSS 10-set with max {m} exists — f(10) = {m} if all "
                  f"smaller m are cleared. Conway-Guy optimality REFUTED. ***",
                  flush=True)
            break
    fh.close()


if __name__ == "__main__":
    main()
