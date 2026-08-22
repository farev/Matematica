#!/usr/bin/env python3
"""analyze_tables.py — post-sweep analysis of the D± tables.

Reads the sweep CSVs and reports, for the NOTE:
  - group counts and any control mismatches/timeouts;
  - every cell with D± strictly between the MOS Theorem 3.1 bounds
    (invariant-factor lower, binary upper);
  - every cell at/below the bounds (endpoint attribution);
  - the >100 cells where the bounds differ = the genuinely new
    determinations (everything else was already forced by Theorem 3.1);
  - family rows C₅⊕C₅ₙ, C₇⊕C₇ₙ, C₃⊕C₃ₙ;
  - groups strictly below the binary bound.
"""
import csv
import sys
from math import log2

rows = []
for path in sys.argv[1:]:
    for r in csv.DictReader(open(path)):
        if r["DPM"]:
            rows.append(r)
print(f"groups loaded: {len(rows)}")

middle, below_binary, newcells, at_lower, at_upper, at_both = [], [], [], [], [], []
for r in rows:
    n = int(r["order"])
    inv = [int(x) for x in r["invariant"].split("+")]
    dpm = int(r["DPM"])
    lb = sum(int(log2(d)) for d in inv) + 1
    ub = int(log2(n)) + 1
    tag = (n, r["invariant"], dpm, lb, ub)
    if dpm < lb or dpm > ub:
        print("BOUND VIOLATION (impossible if Thm 3.1 holds):", tag)
    if lb < dpm < ub:
        middle.append(tag)
    if dpm < ub:
        below_binary.append(tag)
    if lb == dpm == ub:
        at_both.append(tag)
    elif dpm == lb:
        at_lower.append(tag)
    elif dpm == ub:
        at_upper.append(tag)
    if n > 100 and lb != ub:
        newcells.append(tag + (("MIDDLE" if lb < dpm < ub else
                                ("lower" if dpm == lb else "upper")),))

print(f"\nendpoint attribution: both-coincide {len(at_both)}, "
      f"lower-only {len(at_lower)}, upper-only {len(at_upper)}, "
      f"STRICTLY BETWEEN {len(middle)}")
print("\nstrictly-between cells:", middle)
print("\nbelow binary bound:", below_binary)
print(f"\nnew determinations >100 (Thm 3.1 gap cells): {len(newcells)}")
for t in newcells:
    print("  ", t)

for fam, name in ((5, "C5+C5n"), (7, "C7+C7n"), (3, "C3+C3n")):
    vals = sorted((int(r["order"]), r["DPM"]) for r in rows
                  if r["invariant"].startswith(f"{fam}+")
                  and len(r["invariant"].split("+")) == 2
                  and int(r["invariant"].split("+")[1]) % fam == 0)
    print(f"\nfamily {name}: {vals}")
