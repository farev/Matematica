#!/usr/bin/env python3
"""Emit familydata.csv: the C_p + C_3p family status for primes p < 100.

Columns: p, order 3p^2, t = p / 2^floor(log2 p), pinned (sandwich closes
the window), lb, cap, status/value.  The pinned rows are PROVED
(Proposition B); p = 5, 7 are the CERTIFIED theorems; other window rows
are open (p = 19 search status per run_1083.log if present).
"""

import csv
from math import prod


def flog2(x):
    return x.bit_length() - 1


primes = [p for p in range(2, 100)
          if all(p % d for d in range(2, int(p ** 0.5) + 1))]

rows = []
for p in primes:
    order = 3 * p * p
    lb = flog2(p) + flog2(3 * p)
    cap = flog2(order)
    t = p / (1 << flog2(p))
    pinned = lb == cap
    if pinned:
        status = f"D=lmax+1={cap + 1} (PROVED, pinned)"
    elif p == 5:
        status = "D=6=cap (CERTIFIED deficient, Theorem A)"
    elif p == 7:
        status = "D=8=cap+1 (CERTIFIED attained, Theorem B)"
    else:
        status = "OPEN (window)"
    rows.append(dict(p=p, order=order, t=f"{t:.4f}", lb=lb, cap=cap,
                     pinned=pinned, status=status))

with open("familydata.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

npin = sum(r["pinned"] for r in rows)
print(f"{len(rows)} primes < 100: {npin} pinned, "
      f"{len(rows) - npin} windows: "
      f"{[r['p'] for r in rows if not r['pinned']]}")
