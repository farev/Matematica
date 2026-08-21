#!/usr/bin/env python3
"""Summary statistics of the census for NOTE.md — every number quoted in
the note about the census is emitted here.
Usage: summarize.py [census.csv ...]  (concatenates several census files)
"""

import csv
import sys

files = sys.argv[1:] or ["census.csv"]
rows = []
for fn in files:
    with open(fn) as f:
        rows.extend(csv.DictReader(f))

total = len(rows)
by_method = {}
deficient = []
for r in rows:
    by_method[r["method"]] = by_method.get(r["method"], 0) + 1
    if r["lmax"] not in ("", "TIMEOUT") and int(r["lmax"]) < int(r["cap"]):
        deficient.append(r)

print(f"groups: {total}")
print(f"methods: {by_method}")
print(f"deficient (lmax < cap): {len(deficient)}")
print()
print(f"{'order':>5} {'group':24s} {'lb':>3} {'cap':>3} {'lmax':>4} "
      f"{'D±':>3}  note")
for r in sorted(deficient, key=lambda r: (int(r["order"]), r["group"])):
    lb, cap, lm = int(r["lb"]), int(r["cap"]), int(r["lmax"])
    notes = []
    if lm > lb:
        notes.append("beats every product construction")
    if lm == lb:
        notes.append("product bound optimal")
    if cap - lm > 1:
        notes.append(f"deficiency {cap - lm}")
    print(f"{r['order']:>5} {r['group']:24s} {lb:>3} {cap:>3} {lm:>4} "
          f"{lm+1:>3}  {'; '.join(notes)}")

# attainment count
resolved = [r for r in rows if r["lmax"] not in ("", "TIMEOUT")]
att = sum(1 for r in resolved if int(r["lmax"]) == int(r["cap"]))
print(f"\nattain cap: {att}/{len(resolved)} resolved "
      f"({total - len(resolved)} unresolved/timeout)")

# sanity: number of abelian groups per order matches partition products
from dissoc import abelian_groups_of_order
orders = sorted({int(r["order"]) for r in rows})
lo, hi = min(orders), max(orders)
expect = sum(len(list(abelian_groups_of_order(n))) for n in range(lo, hi + 1))
print(f"group count over orders [{lo},{hi}]: {total} (generator gives "
      f"{expect}) {'OK' if total == expect else 'MISMATCH'}")
