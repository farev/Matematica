#!/usr/bin/env python3
"""Aggregate data/results.csv (append-only run log) into data/values.csv
(authoritative value table) and print the markdown table for README/NOTE.

Rules: one row per (r,k). Where both a full-enumeration run (sweep.py) and
CEGAR runs exist, the full-enumeration row is authoritative and the CEGAR
row is recorded as an independent re-derivation (column `rederived`).
Conflicting f values for the same (r,k) abort loudly.
"""
import csv, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "data", "results.csv"))))
by = defaultdict(list)
for row in rows:
    by[(int(row["r"]), int(row["k"]))].append(row)

out = []
for (r, k), rs in sorted(by.items()):
    fs = set(int(x["f"]) for x in rs)
    if len(fs) != 1:
        sys.exit(f"CONFLICT at (r={r},k={k}): f values {fs}")
    f = fs.pop()
    full = [x for x in rs if x["enum_cap"] != "cegar"]
    ceg = [x for x in rs if x["enum_cap"] == "cegar"]
    prim = full[0] if full else ceg[0]
    out.append(dict(r=r, k=k, f=f,
                    method="full-enum" if full else "cegar",
                    rederived=("cegar" if (full and ceg) else
                               f"x{len(ceg)}" if len(ceg) > 1 else ""),
                    witness=prim["witness"], proof=prim["proof"],
                    cnf_sha=prim["cnf_sha"]))

with open(os.path.join(HERE, "data", "values.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0]))
    w.writeheader()
    for row in out:
        w.writerow(row)

print("| r | k | f_r(k) | 3k² | Δ | method | boundary certificates |")
print("|---|---|---|---|---|---|---|")
for row in out:
    k, f = row["k"], int(row["f"])
    tk = 3 * k * k
    print(f"| {row['r']} | {k} | **{f}** | {tk} | {f - tk:+d} | "
          f"{row['method']}{' (+' + row['rederived'] + ')' if row['rederived'] else ''} | "
          f"`{row['witness']}`, `{row['proof']}` |")
