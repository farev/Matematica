#!/usr/bin/env python3
"""Replicate Tables 1-3 of arXiv:2510.11263 with count_colourings.

Vertex order: Figure 3 spiral in picture coordinates (row, col):
H = (0,0),(0,1),(1,0),(1,1); then for k = 2,3,...: column k rows 0..k-1,
then row k columns k..0.  Lattice embeddings of the picture coordinates:
  square : Z^2 grid (P box P)
  king   : Z^2 with both diagonals (P strong P)
  tri-off: triangular lattice drawn with offset rows (Figure 1 of the paper):
           picture (row, col) -> sheared (r, c) = (row, col - floor(row/2))
  tri-sh : triangular lattice as Z^2 plus the (1,-1) diagonal (sheared picture)
usage: replicate_tables.py LATTICE C NVERT
"""
import sys, subprocess
STEPS = {'square': [(1, 0), (0, 1)], 'tri': [(1, 0), (0, 1), (1, -1)],
         'king': [(1, 0), (0, 1), (1, 1), (1, -1)]}

def spiral(nv):
    order = [(0, 0), (0, 1), (1, 0), (1, 1)]
    k = 2
    while len(order) < nv:
        for r in range(k):
            order.append((r, k))
        for c in range(k, -1, -1):
            order.append((k, c))
        k += 1
    return order[:nv]

def main():
    lat, C, nv = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    pic = spiral(nv)
    if lat == 'tri-off':
        kind = 'tri'; verts = [(r, c - r // 2) for r, c in pic]
    elif lat == 'tri-sh':
        kind = 'tri'; verts = pic
    else:
        kind = lat; verts = pic
    idx = {v: i for i, v in enumerate(verts)}
    nbrs = [[] for _ in verts]
    for (r, c), i in idx.items():
        for dr, dc in STEPS[kind]:
            j = idx.get((r + dr, c + dc))
            if j is not None:
                nbrs[i].append(j); nbrs[j].append(i)
    inp = f"{nv} {C}\n" + "".join(f"{len(nbrs[i])} " + " ".join(map(str, nbrs[i])) + "\n" for i in range(nv))
    r = subprocess.run(['./count_colourings'], input=inp, capture_output=True, text=True)
    print(f"# {lat} C={C} spiral of {nv} vertices, {sum(map(len, nbrs))//2} edges")
    print(r.stdout.strip())

if __name__ == '__main__':
    main()
