"""Independent re-verification of an orientation.
Usage: python3 verify.py p ta tb ga gb (model.model | orientation.txt)
Rebuilds the Cayley graph, re-enumerates every cycle of length <= 16 with the C
enumerator, and checks a(C) <= 3*len(C) - 33 for every cycle, where a(C) is the
number of vertices of C whose chosen neighbour is adjacent to it along C.
A .model file (DIMACS model, variables 3x+j+1) is converted first and the
orientation is written next to it as vertex -> chosen neighbour."""
import sys, os
from orient import build, enumerate_cycles, HERE

p, ta, tb, ga, gb = map(int, sys.argv[1:6])
src = sys.argv[6]
G, S, adj = build(p, ta, tb, ga, gb)
n = G.n
if src.endswith(".model"):
    lits = list(map(int, open(src).read().split()))
    tv = set(v for v in lits if v > 0)
    choice = []
    for x in range(n):
        js = [j for j in range(3) if 3 * x + j + 1 in tv]
        assert len(js) == 1, (x, js)
        choice.append(int(adj[x][js[0]]))
    out = src[:-6] + "_orientation.txt"
    with open(out, "w") as f:
        f.write(f"# p={p} t=({ta},{tb}) g=({ga},{gb}); line: vertex chosen_neighbour (u-edge)\n")
        for x in range(n):
            f.write(f"{x} {choice[x]}\n")
    print("orientation written to", out)
else:
    choice = [None] * n
    for line in open(src):
        if line.startswith("#"):
            continue
        x, y = map(int, line.split())
        choice[x] = y
assert all(c is not None for c in choice)
assert all(choice[x] in [int(v) for v in adj[x]] for x in range(n)), "chosen neighbour not adjacent"
counts, cycles, dt = enumerate_cycles(adj, f"verify_p{p}_t{ta}_{tb}_g{ga}_{gb}")
print("cycle counts:", {l: counts[l] for l in range(14, 17)}, "shorter:", sum(counts[l] for l in range(3, 14)))
bad = 0
hist = {}
for cyc in cycles:
    L = len(cyc)
    a = sum(1 for i, x in enumerate(cyc) if choice[x] in (cyc[i - 1], cyc[(i + 1) % L]))
    hist.setdefault(L, {}); hist[L][a] = hist[L].get(a, 0) + 1
    if a > 3 * L - 33:
        bad += 1
print("a(C) histogram by length:", {L: dict(sorted(h.items())) for L, h in sorted(hist.items())})
print("VIOLATED CYCLES:", bad, "->", "ORIENTATION VALID" if bad == 0 else "INVALID")
