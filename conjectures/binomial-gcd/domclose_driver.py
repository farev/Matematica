#!/usr/bin/env python3
"""Generate domclose jobs for the UNKNOWN family levels (complete admissible
lists via full factorization of the windows), plus positive controls."""
import sys
import family699 as F

# positive controls: levels known to contain a tight triple
controls = [(2 ** 41, 2), (3 ** 13 + 1, 3), (2 ** 11, 2)]
# the UNKNOWN levels recorded 2026-08-12, from the committed CSV (i >= 2
# only; i = 1 rows are vacuous by NOTE Prop 0)
unknown = []
csv = "/home/user/Matematica/conjectures/binomial-gcd/data/family_unknown_levels.csv"
for line in open(csv):
    if line.startswith("#"):
        continue
    fam, n, i, size = line.strip().split(",")
    n, i = int(n), int(i)
    if i >= 2:
        unknown.append((n, i))
print(f"# {len(unknown)} unknown levels loaded from CSV", file=sys.stderr)

for (n, i) in controls + unknown:
    fac = {}
    ok = True
    for t in range(i):
        f = F.factor_or_none(n - t)
        if f is None:
            print(f"# FACTORING FAILED n={n} t={t} -> job skipped", file=sys.stderr)
            ok = False
            break
        fac[t] = f
    if not ok:
        continue
    adm = []
    for t in range(i):
        for q in fac[t]:
            if q > i:
                adm.append((q, t))
    parts = [str(n), str(i)]
    for (q, t) in sorted(adm):
        parts += [str(q), str(t)]
    print(" ".join(parts))
