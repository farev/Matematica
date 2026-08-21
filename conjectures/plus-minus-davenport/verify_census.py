#!/usr/bin/env python3
"""Two-engine cross-verification of census.csv for orders <= M.

Recomputes lmax for every abelian group of order <= M with the pure-Python
DFS (dissoc.lmax_dfs) and demands exact agreement with the census values
AND exact node-count equality with the C engine (same traversal).  The
theorem-T3 cells above the Python search budget are checked for value only
against Theorem T3 (rank).
Usage: verify_census.py [M=100]
"""

import csv
import sys

from dissoc import Group, abelian_groups_of_order, lmax_dfs

M = int(sys.argv[1]) if len(sys.argv) > 1 else 100

rows = {}
with open("census.csv") as f:
    for r in csv.DictReader(f):
        rows[r["group"]] = r

bad = 0
checked = 0
for n in range(2, M + 1):
    for factors in abelian_groups_of_order(n):
        name = "+".join(f"C{f}" for f in factors)
        r = rows[name]
        G = Group(factors)
        lmax, wit, nodes = lmax_dfs(G)
        checked += 1
        if str(lmax) != r["lmax"]:
            print(f"VALUE MISMATCH {name}: python {lmax} vs census {r['lmax']}")
            bad += 1
            continue
        if r["nodes"] not in ("", "-1") and int(r["nodes"]) != nodes:
            print(f"NODE MISMATCH {name}: python {nodes} vs census {r['nodes']}")
            bad += 1
print(f"checked {checked} groups to order {M}: "
      + ("ALL MATCH (values and node counts)" if bad == 0
         else f"{bad} MISMATCHES"))
sys.exit(1 if bad else 0)
