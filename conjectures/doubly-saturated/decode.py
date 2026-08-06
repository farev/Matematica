"""Reconstruct a sigma-invariant graph from (m,k,mask), replicating semireg.c's orbit indexing,
   then check double saturation straight from the definition and emit a witness certificate."""
import sys
from itertools import combinations

m, k, mask, s, t = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
n = m*k
idx = {}
norb = 0
for i in range(k):
    for j in range(i, k):
        for d in range(m):
            if i == j and d == 0: continue
            if (i,j,d) in idx: continue
            idx[(i,j,d)] = norb
            idx[(j,i,(m-d) % m)] = norb
            norb += 1
def orb(u, v):
    xu, iu = u % m, u // m
    xv, iv = v % m, v // m
    return idx[(iu, iv, (xv-xu) % m)]
Eset = {(u,v) for u,v in combinations(range(n),2) if mask >> orb(u,v) & 1}
E = lambda u,v: (min(u,v),max(u,v)) in Eset
print(f"n={n} m={m} k={k} mask={mask} edges={len(Eset)} degrees={sorted({sum(1 for w in range(n) if w!=v and E(v,w)) for v in range(n)})}")

assert not any(all(E(a,b) for a,b in combinations(c,2)) for c in combinations(range(n),s)), "has K_s!"
assert not any(all(not E(a,b) for a,b in combinations(c,2)) for c in combinations(range(n),t)), "has independent t-set!"
out = [f"# CERTIFICATE: doubly saturated ({s},{t})-Ramsey graph on {n} vertices",
       f"# invariant under the fixed-point-free automorphism (x,i) -> (x+1,i) of order {m}, k={k} orbits",
       f"# reconstructed from semireg.c mask={mask}",
       f"n {n}", f"s {s}", f"t {t}",
       "edges " + " ".join(f"{u},{v}" for u,v in sorted(Eset))]
nfa = nfd = 0
for u,v in combinations(range(n),2):
    if not E(u,v):
        C = [w for w in range(n) if w not in (u,v) and E(u,w) and E(v,w)]
        w = next((c for c in combinations(C, s-2) if all(E(a,b) for a,b in combinations(c,2))), None)
        if w is None: nfa += 1
        else: out.append("ADD " + " ".join(map(str,(u,v)+w)))
    else:
        C = [w for w in range(n) if w not in (u,v) and not E(u,w) and not E(v,w)]
        w = next((c for c in combinations(C, t-2) if all(not E(a,b) for a,b in combinations(c,2))), None)
        if w is None: nfd += 1
        else: out.append("DEL " + " ".join(map(str,(u,v)+w)))
print("unsaturated additions:", nfa, " non-critical deletions:", nfd)
if nfa == 0 and nfd == 0:
    open(sys.argv[6], "w").write("\n".join(out) + "\n")
    print("certificate written to", sys.argv[6])
