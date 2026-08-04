"""Emit a witness certificate for a circulant claimed doubly saturated.
   Usage: python3 mkcert.py n s t d1,d2,...  > cert.txt
   Independent of the C code: pure Python, explicit subset enumeration."""
import sys
from itertools import combinations

n, s, t = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
S0 = [int(x) for x in sys.argv[4].split(",")]
S  = set(S0) | {n-d for d in S0}
E  = lambda u, v: (v-u) % n in S

edges    = [(u,v) for u,v in combinations(range(n),2) if E(u,v)]
nonedges = [(u,v) for u,v in combinations(range(n),2) if not E(u,v)]
assert not any(all(E(a,b) for a,b in combinations(c,2)) for c in combinations(range(n),s)), "has K_s"
assert not any(all(not E(a,b) for a,b in combinations(c,2)) for c in combinations(range(n),t)), "has independent t-set"

out = [f"# CERTIFICATE: doubly saturated ({s},{t})-Ramsey graph on {n} vertices",
       f"# G = Cay(Z_{n}, +-{{{','.join(map(str,sorted(S0)))}}}), {len(S)}-regular, {len(edges)} edges",
       f"n {n}", f"s {s}", f"t {t}",
       "edges " + " ".join(f"{u},{v}" for u,v in edges),
       f"# ADD u v ... : the {s} listed vertices form a K{s} of G+uv (uv a non-edge of G)"]
for u,v in nonedges:                       # need a K_{s-2} inside N(u)&N(v)
    C = [w for w in range(n) if w!=u and w!=v and E(u,w) and E(v,w)]
    w = next((c for c in combinations(C, s-2) if all(E(a,b) for a,b in combinations(c,2))), None)
    assert w is not None, f"non-edge {u},{v} unsaturated"
    out.append("ADD " + " ".join(map(str,(u,v)+w)))
out.append(f"# DEL u v ... : the {t} listed vertices are independent in G-uv (uv an edge of G)")
for u,v in edges:                          # need an independent (t-2)-set in the common non-nbhd
    C = [w for w in range(n) if w!=u and w!=v and not E(u,w) and not E(v,w)]
    w = next((c for c in combinations(C, t-2) if all(not E(a,b) for a,b in combinations(c,2))), None)
    assert w is not None, f"edge {u},{v} not deletion-critical"
    out.append("DEL " + " ".join(map(str,(u,v)+w)))
print("\n".join(out))
