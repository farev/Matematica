#!/usr/bin/env python3
"""Brute-force verify a colouring written by nrsat.py (<tag>.sat.txt):
rebuild the graph from the vertex list and lattice steps, then run
brute_check (enumerates every simple path).  usage: brute_verify.py TAG..."""
import sys, subprocess
STEPS = {'square': [(1, 0), (0, 1)], 'tri': [(1, 0), (0, 1), (1, -1)],
         'king': [(1, 0), (0, 1), (1, 1), (1, -1)]}
for tag in sys.argv[1:]:
    lines = open(f'{tag}.sat.txt').read().strip().split('\n')
    kind, shape, C, kmax = lines[0].split()
    verts, col = [], []
    for l in lines[1:]:
        r, c, cl = map(int, l.split()); verts.append((r, c)); col.append(cl)
    idx = {v: i for i, v in enumerate(verts)}
    nbrs = [[] for _ in verts]
    for (r, c), i in idx.items():
        for dr, dc in STEPS[kind]:
            j = idx.get((r + dr, c + dc))
            if j is not None:
                nbrs[i].append(j); nbrs[j].append(i)
    inp = f"{len(verts)}\n" + "".join(f"{len(nbrs[i])} " + " ".join(map(str, nbrs[i])) + "\n" for i in range(len(verts))) + " ".join(map(str, col)) + "\n"
    r = subprocess.run(['./brute_check'], input=inp, capture_output=True, text=True)
    print(f"{tag}: {kind} {shape} V={len(verts)} E={sum(map(len, nbrs))//2} C={C} :: {r.stdout.strip().replace(chr(10), ' | ')} (exit {r.returncode})", flush=True)
