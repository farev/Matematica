#!/usr/bin/env python3
"""Merge and audit the composite L=600 census campaign.

Structure: the depth-130 task split of the L=600 tree makes task 0 (the
all-zero prefix) the entire [0, 3^470) subtree.  That subtree was run as
its own depth-130 sub-campaign at L=470 — identical thresholds and values,
so nodes/terms/fingerprints compose exactly:

  full600 = tg600_nodes + sum(tasks 1..3753 of the L=600 split)
                        + [ tg470_nodes + sum(tasks 0..4905 of the L=470 split) ]

Checks: L=600 rows cover exactly {1..3753} (task 0 must be absent);
L=470 rows cover exactly {0..4905}; per-task term sums match worker TOTAL
rows; N1155 == 3 overall.  Emits data/census600_summary.txt.
Exits nonzero on any failure."""
import glob
import sys

M = 1 << 64
MODP = 1_000_000_007

def read_campaign(pattern, expect_ids, label):
    ids = {}
    tot = dict(nodes=0, terms=0, sum64=0, xor64=0, summp=0, n1155=0)
    per_task_terms = per_task_nodes = 0
    for fn in sorted(glob.glob(pattern)):
        for line in open(fn):
            p = line.rstrip("\n").split(",")
            if p[0] == "TOTAL":
                tot["nodes"] += int(p[1]); tot["terms"] += int(p[2])
                tot["sum64"] = (tot["sum64"] + int(p[3])) % M
                tot["xor64"] ^= int(p[4])
                tot["summp"] = (tot["summp"] + int(p[5])) % MODP
                tot["n1155"] += int(p[6])
                continue
            tid = int(p[0])
            if tid in ids:
                raise SystemExit(f"{label}: DUPLICATE task {tid}")
            ids[tid] = True
            per_task_nodes += int(p[1])
            per_task_terms += int(p[2])
    missing = expect_ids - set(ids)
    extra = set(ids) - expect_ids
    if missing:
        raise SystemExit(f"{label}: {len(missing)} tasks missing, first {sorted(missing)[:6]}")
    if extra:
        raise SystemExit(f"{label}: unexpected task ids {sorted(extra)[:6]}")
    if per_task_terms != tot["terms"]:
        raise SystemExit(f"{label}: per-task terms {per_task_terms} != TOTAL {tot['terms']}")
    if per_task_nodes != tot["nodes"]:
        raise SystemExit(f"{label}: per-task nodes {per_task_nodes} != TOTAL {tot['nodes']}")
    return tot

def tg_nodes(path):
    return int(open(path).read().split()[1])

def main():
    c600 = read_campaign("data/prod600_w*.csv", set(range(1, 3754)), "L=600 split")
    c470 = read_campaign("data/prod470_s*.csv", set(range(0, 4906)), "L=470 sub-campaign")
    tg6, tg4 = tg_nodes("data/tg600.log"), tg_nodes("data/tg470.log")
    nodes = tg6 + c600["nodes"] + tg4 + c470["nodes"]
    terms = c600["terms"] + c470["terms"]
    sum64 = (c600["sum64"] + c470["sum64"]) % M
    xor64 = c600["xor64"] ^ c470["xor64"]
    summp = (c600["summp"] + c470["summp"]) % MODP
    n1155 = c600["n1155"] + c470["n1155"]
    if n1155 != 3:
        raise SystemExit(f"N1155 = {n1155} != 3 — INVESTIGATE (expected 0, 1, 3160 only)")
    out = (f"L=600 census merge: 3753 top-split tasks + 4906 sub-campaign tasks, all present exactly once\n"
           f"nodes: tg600={tg6} + split={c600['nodes']} + tg470={tg4} + sub={c470['nodes']}"
           f" => full-tree nodes={nodes}\n"
           f"terms={terms}\n"
           f"sum64={sum64}\nxor64={xor64}\nsummodp={summp}\n"
           f"n1155={n1155} (terms 0, 1, 3160)\n")
    open("data/census600_summary.txt", "w").write(out)
    print(out)
    return 0

if __name__ == "__main__":
    sys.exit(main())
