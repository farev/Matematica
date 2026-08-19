#!/usr/bin/env python3
"""cross_check.py — run engine E2 (dpm_python.py) on every completed sweep
cell with |G| <= LIMIT and compare (maxlen, nodes) against E1's output.
The node counts must agree EXACTLY (both engines enumerate the set of ±zsf
multisets with no pruning; #nodes − 1 = #multisets).

Usage: python3 cross_check.py [LIMIT]     (default 100)
Writes data/cross_check.log; exits nonzero on any mismatch.
"""
import os
import re
import subprocess
import sys

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 100
base = os.path.dirname(os.path.abspath(__file__))
sweep = os.path.join(base, "data", "sweep")
rows = []
for fn in sorted(os.listdir(sweep)):
    txt = open(os.path.join(sweep, fn)).read().strip()
    m = re.match(r"(\d+) (\d+) (\d+) (\d+) (\d+) maxlen=(\d+) dpm=\d+ nodes=(\d+)", txt)
    if not m:
        continue
    a, b, c, d, n, ml, nodes = (int(m.group(i)) for i in range(1, 8))
    if n <= LIMIT:
        rows.append(((a, b, c, d), n, ml, nodes))

ok = mismatches = 0
lines = []
for mods, n, ml, nodes in sorted(rows, key=lambda r: r[1]):
    args = [str(x) for x in mods if x > 1] or ["2"]
    if args == ["2"] and n != 2:
        continue
    out = subprocess.run(
        [sys.executable, os.path.join(base, "dpm_python.py")] + args,
        capture_output=True, text=True).stdout
    m2 = re.search(r"maxlen=(\d+) dpm=\d+ nodes=(\d+)", out)
    ml2, nodes2 = int(m2.group(1)), int(m2.group(2))
    good = (ml, nodes) == (ml2, nodes2)
    ok += good
    mismatches += not good
    lines.append(f"{'OK ' if good else 'MISMATCH'} G={args} |G|={n} "
                 f"E1=(maxlen {ml}, nodes {nodes}) E2=(maxlen {ml2}, nodes {nodes2})")

with open(os.path.join(base, "data", "cross_check.log"), "w") as f:
    f.write("\n".join(lines) + f"\n\nTOTAL {ok} ok, {mismatches} mismatches "
            f"(cells with |G| <= {LIMIT})\n")
print(f"{ok} ok, {mismatches} mismatches")
sys.exit(1 if mismatches else 0)
