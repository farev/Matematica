#!/usr/bin/env python3
"""Report campaign frontier: largest contiguous completed task prefix and the
certified bound it implies."""
import glob, sys

K, W = 45, 30
TOT = 1 << (K - W)

def base_of(p):
    return sum(3 ** (W + i) for i in range(K - W) if p >> i & 1)

rows = {}
for fn in glob.glob("data/grid45_w*.csv"):
    for line in open(fn):
        parts = line.rstrip("\n").split(",")
        if len(parts) < 7:
            continue
        try:
            pid = int(parts[0])
        except ValueError:
            continue
        rows[pid] = parts

F = -1
while F + 1 in rows:
    F += 1
leaves = sum(int(rows[p][2]) for p in range(F + 1))
hits = []
for p in range(F + 1):
    h = rows[p][6]
    if h != "-":
        for tok in h.split(" "):
            n, f11 = tok.split(":")
            hits.append((int(n), int(f11)))
hits.sort()
bound = (3 ** K - 1) // 2 if F == TOT - 1 else base_of(F + 1) - 1
exp_leaves = (F + 1) * (1 << W)
print(f"tasks done (contiguous prefix): {F+1}/{TOT}")
print(f"leaves counted: {leaves}  expected: {exp_leaves}  match: {leaves == exp_leaves}")
print(f"CERTIFIED exhaustive bound: {bound}  (~{bound:.3e})")
print(f"hits: {len(hits)}")
for n, f11 in hits:
    print(f"  {n}  coprime1155={f11}")
straggler = [p for p in rows if p > F]
print(f"rows beyond prefix: {len(straggler)}")
