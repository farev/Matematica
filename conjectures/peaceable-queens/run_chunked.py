#!/usr/bin/env python3
"""Chunked, resumable parallel run: split the odd-S loop into CHUNKS
stride pieces; each completed chunk writes results/<tag>_chunk<k>.txt
and is skipped on re-run.  All chunks UNSAT => exhaustive refutation
(sum the node counts); any SAT => witness in that chunk file.

Usage: run_chunked.py n m [chunks] [workers] [engine]
Chunk files are tagged with the engine name: stride semantics differ
between builds (plain: odd-S index; sym: raw S), so chunks from
different engines must never be mixed in one aggregation.
"""
import os
import subprocess
import sys
import time

n, m = int(sys.argv[1]), int(sys.argv[2])
CHUNKS = int(sys.argv[3]) if len(sys.argv) > 3 else 16
WORKERS = int(sys.argv[4]) if len(sys.argv) > 4 else 4
ENGINE = sys.argv[5] if len(sys.argv) > 5 else "./bnb"
tag = f"n{n}_m{m}_{os.path.basename(ENGINE)}"
os.makedirs("results", exist_ok=True)

pending = [k for k in range(CHUNKS)
           if not os.path.exists(f"results/{tag}_chunk{k}.txt")]
print(f"{tag}: {CHUNKS - len(pending)}/{CHUNKS} chunks already done; "
      f"running {len(pending)} on {WORKERS} workers", flush=True)

t0 = time.time()
running = {}
sat_seen = False
while pending or running:
    while pending and len(running) < WORKERS and not sat_seen:
        k = pending.pop(0)
        f = open(f"results/{tag}_chunk{k}.txt.part", "w")
        p = subprocess.Popen([ENGINE, str(n), str(m), str(CHUNKS), str(k)],
                             stdout=f, text=True)
        running[k] = (p, f)
    if not running:
        break
    time.sleep(2)
    for k in list(running):
        p, f = running[k]
        if p.poll() is not None:
            f.close()
            os.rename(f"results/{tag}_chunk{k}.txt.part",
                      f"results/{tag}_chunk{k}.txt")
            first = open(f"results/{tag}_chunk{k}.txt").readline().strip()
            print(f"chunk {k}: {first} "
                  f"[{time.time()-t0:.0f}s elapsed]", flush=True)
            if first.startswith("SAT"):
                sat_seen = True
            del running[k]

# aggregate
verdicts, nodes = [], 0
for k in range(CHUNKS):
    path = f"results/{tag}_chunk{k}.txt"
    if not os.path.exists(path):
        verdicts.append("MISSING")
        continue
    first = open(path).readline().strip()
    verdicts.append(first.split()[0])
    for tok in first.split():
        if tok.startswith("nodes="):
            nodes += int(tok[6:])
if any(v == "SAT" for v in verdicts):
    print(f"RESULT n={n} m={m}: SAT (see chunk file)", flush=True)
elif all(v == "UNSAT" for v in verdicts):
    print(f"RESULT n={n} m={m}: UNSAT total_nodes={nodes} "
          f"chunks={CHUNKS} wall={time.time()-t0:.0f}s", flush=True)
else:
    print(f"RESULT n={n} m={m}: INCOMPLETE {verdicts}", flush=True)
