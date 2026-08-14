#!/usr/bin/env python3
"""Merge and audit the L=600 task-mode campaign.

Checks: every task id 0..NTASKS-1 appears exactly once across the worker
CSVs; per-worker TOTAL rows combine to global fingerprints; the global
term count equals the sum of per-task term counts; N1155 == 3.
Emits data/census600_summary.txt.  Exits nonzero on any failure."""
import glob
import sys

NTASKS = 3754
M = 1 << 64
MODP = 1_000_000_007

def main():
    ids = {}
    tot_nodes = tot_terms = 0
    sum64 = xor64 = summp = n1155 = 0
    per_task_terms = 0
    for fn in sorted(glob.glob("data/prod600_w*.csv")):
        for line in open(fn):
            p = line.rstrip("\n").split(",")
            if p[0] == "TOTAL":
                tot_nodes += int(p[1])
                tot_terms += int(p[2])
                sum64 = (sum64 + int(p[3])) % M
                xor64 ^= int(p[4])
                summp = (summp + int(p[5])) % MODP
                n1155 += int(p[6])
                continue
            tid = int(p[0])
            if tid in ids:
                print(f"DUPLICATE task {tid}")
                return 1
            ids[tid] = fn
            per_task_terms += int(p[2])
    missing = [i for i in range(NTASKS) if i not in ids]
    if missing:
        print(f"MISSING {len(missing)} tasks, first: {missing[:10]}")
        return 1
    if len(ids) != NTASKS:
        print(f"UNEXPECTED extra tasks: {len(ids)} != {NTASKS}")
        return 1
    if per_task_terms != tot_terms:
        print(f"terms mismatch: per-task {per_task_terms} != totals {tot_terms}")
        return 1
    if n1155 != 3:
        print(f"N1155 = {n1155} != 3 — INVESTIGATE (expected 0, 1, 3160 only)")
        return 1
    tg = open("data/tg600.log").read().split()
    tgnodes = int(tg[1])
    out = (f"L=600 census merge: {NTASKS} tasks, all present exactly once\n"
           f"nodes(workers)={tot_nodes} + taskgen={tgnodes} => full-tree nodes={tot_nodes + tgnodes}\n"
           f"terms={tot_terms}\n"
           f"sum64={sum64}\nxor64={xor64}\nsummodp={summp}\n"
           f"n1155={n1155} (0, 1, 3160)\n")
    open("data/census600_summary.txt", "w").write(out)
    print(out)
    return 0

if __name__ == "__main__":
    sys.exit(main())
