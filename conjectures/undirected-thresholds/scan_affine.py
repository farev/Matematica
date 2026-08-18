"""Background scan driver: affine ansatz over multipliers m and block sizes k."""
import sys
from affine_search import search_k

ks = [22, 23, 24, 25, 26, 28, 30, 33]
ms = [3, 5, 7, 9, 13, 15, 17, 19, 21]
for k in ks:
    for m in ms:
        surv, reached, nodes, dt = search_k(k, 4 * k, maxnodes=400_000, m=m)
        ex = "EXHAUSTED" if nodes < 400_000 else "CAPPED"
        line = (f"k={k} m={m}: reach {reached} (2k={2*k}), nodes {nodes}, "
                f"surv {len(surv)}, {ex} [{dt:.0f}s]")
        print(line, flush=True)
        if surv:
            print("SURVIVOR FOUND — stopping scan for inspection", flush=True)
            sys.exit(0)
