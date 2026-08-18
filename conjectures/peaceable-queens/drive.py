#!/usr/bin/env python3
"""Parallel driver: split the row-set loop across 4 stride workers.
Usage: drive.py n m [workers] -> aggregates UNSAT (sum nodes) or SAT.
Each completed (n, m) UNSAT is a permanent certified bound a(n) <= m-1.
"""
import subprocess, sys, time, os

n, m = int(sys.argv[1]), int(sys.argv[2])
K = int(sys.argv[3]) if len(sys.argv) > 3 else 4
t0 = time.time()
procs = [subprocess.Popen(["./bnb", str(n), str(m), str(K), str(k)],
                          stdout=subprocess.PIPE, text=True)
         for k in range(K)]
status, total_nodes, wit = "UNSAT", 0, None
for p in procs:
    out, _ = p.communicate()
    first = out.splitlines()[0] if out else ""
    if first.startswith("SAT"):
        status = "SAT"
        wit = "\n".join(out.splitlines()[1:])
        for q in procs:
            if q is not p:
                q.kill()
    for tok in first.split():
        if tok.startswith("nodes="):
            total_nodes += int(tok[6:])
dt = time.time() - t0
print(f"n={n} m={m}: {status} total_nodes={total_nodes} wall={dt:.1f}s "
      f"workers={K}")
if wit:
    print(wit)
