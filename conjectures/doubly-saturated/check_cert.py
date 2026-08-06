"""Independent certificate checker.  Reads only the edge list + witnesses; re-derives all claims.
   Usage: python3 check_cert.py cert_n19_45.txt"""
import sys
from itertools import combinations

L = {}
adds, dels = [], []
for line in open(sys.argv[1]):
    line = line.strip()
    if not line or line.startswith("#"): continue
    k, *rest = line.split()
    if   k == "ADD": adds.append(tuple(map(int, rest)))
    elif k == "DEL": dels.append(tuple(map(int, rest)))
    elif k == "edges": L["edges"] = [tuple(map(int, p.split(","))) for p in rest]
    else: L[k] = int(rest[0])

n, s, t = L["n"], L["s"], L["t"]
Eset = {tuple(sorted(e)) for e in L["edges"]}
E = lambda u, v: tuple(sorted((u, v))) in Eset
fail = []

# 1. no K_s
for c in combinations(range(n), s):
    if all(E(u, v) for u, v in combinations(c, 2)): fail.append(f"K{s} at {c}")
# 2. no independent t-set
for c in combinations(range(n), t):
    if all(not E(u, v) for u, v in combinations(c, 2)): fail.append(f"independent {t}-set at {c}")
# 3. every non-edge has an ADD witness that really is a K_s of G+uv
seen = set()
for w in adds:
    u, v = w[0], w[1]
    if E(u, v): fail.append(f"ADD witness on an existing edge {u}-{v}")
    for a, b in combinations(w, 2):
        if (a, b) != (u, v) and not E(a, b): fail.append(f"ADD {w}: {a}-{b} not an edge")
    if len(set(w)) != s: fail.append(f"ADD {w}: not {s} distinct vertices")
    seen.add(tuple(sorted((u, v))))
for u, v in combinations(range(n), 2):
    if not E(u, v) and (u, v) not in seen: fail.append(f"non-edge {u}-{v} has no ADD witness")
# 4. every edge has a DEL witness that really is independent in G-uv
seen = set()
for w in dels:
    u, v = w[0], w[1]
    if not E(u, v): fail.append(f"DEL witness on a non-edge {u}-{v}")
    for a, b in combinations(w, 2):
        if (a, b) != (u, v) and E(a, b): fail.append(f"DEL {w}: {a}-{b} is an edge")
    if len(set(w)) != t: fail.append(f"DEL {w}: not {t} distinct vertices")
    seen.add(tuple(sorted((u, v))))
for u, v in combinations(range(n), 2):
    if E(u, v) and (u, v) not in seen: fail.append(f"edge {u}-{v} has no DEL witness")

print(f"n={n} (s,t)=({s},{t}) edges={len(Eset)} ADD-witnesses={len(adds)} DEL-witnesses={len(dels)}")
if fail:
    print("FAILED:"); [print("  ", x) for x in fail[:20]]; sys.exit(1)
print(f"OK: G has no K{s}, no independent {t}-set, every edge addition creates a K{s},")
print(f"    every edge deletion creates an independent {t}-set.  DOUBLY SATURATED.")
