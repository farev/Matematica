#!/usr/bin/env python3
"""B&B vs SAT-encoder verdict agreement on every m, n=3..8."""
import sys, time
sys.path.insert(0, '.')
from bnb import solve as bnb_solve
from encode_lines import build_lines
from pysat.solvers import Cadical153

known = {3:1, 4:2, 5:4, 6:5, 7:7, 8:9}
rows = []
for n in range(3, 9):
    for m in range(1, known[n] + 3):
        s_bnb, wit, nodes = bnb_solve(n, m)
        nv, cl = build_lines(n, m)
        with Cadical153(bootstrap_with=cl) as s:
            s_sat = "SAT" if s.solve() else "UNSAT"
        ok = s_bnb == s_sat
        rows.append((n, m, s_bnb, s_sat, nodes, ok))
        if not ok:
            print(f"MISMATCH n={n} m={m}: bnb={s_bnb} sat={s_sat}")
agree = sum(1 for r in rows if r[5])
print(f"{agree}/{len(rows)} agreements")
with open("results/validation_bnb_vs_sat.csv", "w") as f:
    f.write("n,m,bnb,sat,bnb_nodes,agree\n")
    for r in rows:
        f.write(",".join(map(str, r)) + "\n")
