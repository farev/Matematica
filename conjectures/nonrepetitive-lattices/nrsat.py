#!/usr/bin/env python3
"""Lazy-path SAT search for nonrepetitive colourings of lattice patches.

usage: nrsat.py LATTICE SHAPE C LBASE KMAX [cap] [tag]

LATTICE: square | tri | king   (vertex set Z^2 in sheared coordinates (r,c);
         steps square {(1,0),(0,1)}, tri {(1,0),(0,1),(1,-1)}, king
         {(1,0),(0,1),(1,1),(1,-1)})
SHAPE:   rect:M:N        rows 0..M-1, columns 0..N-1
         hex:K           tri only: hexagon of radius K around the origin
                         (|r|<=K, |c|<=K, |r+c|<=K), 3K^2+3K+1 vertices
         offset:M:N      tri only: M rows of N vertices in the offset-row
                         (brick) picture, row r using c = c' - floor(r/2)
         disc:R2         lattice points with squared Euclidean distance <= R2
                         from the origin in the natural embedding
Every simple path with <= LBASE vertices is encoded up front; longer
repetitive paths (up to 2*KMAX vertices) are added lazily from
counterexample colourings found by repcheck.
UNSAT => the patch has no nonrepetitive C-colouring (every clause is a
necessary condition; symmetry breaking is a colour relabelling).
SAT   => a C-colouring with no repetition on paths of <= 2*KMAX vertices.
On UNSAT: <tag>.cnf, <tag>.paths (path per clause), <tag>.verts (vertex list).
"""
import sys, time, subprocess, os, math
from pysat.solvers import Cadical153

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = {'square': [(1, 0), (0, 1)], 'tri': [(1, 0), (0, 1), (1, -1)],
         'king': [(1, 0), (0, 1), (1, 1), (1, -1)]}

def embed(kind, r, c):
    if kind == 'tri':
        return (c + r / 2.0, r * math.sqrt(3) / 2.0)
    return (float(c), float(r))

def vertex_set(kind, shape):
    parts = shape.split(':')
    if parts[0] == 'rect':
        M, N = int(parts[1]), int(parts[2])
        return [(r, c) for r in range(M) for c in range(N)]
    if parts[0] == 'hex':
        assert kind == 'tri'
        K = int(parts[1])
        return [(r, c) for r in range(-K, K + 1) for c in range(-K, K + 1) if abs(r + c) <= K]
    if parts[0] == 'offset':
        assert kind == 'tri'
        M, N = int(parts[1]), int(parts[2])
        return [(r, cp - r // 2) for r in range(M) for cp in range(N)]
    if parts[0] in ('spiral', 'spiraloff'):
        # Figure 3 spiral of arXiv:2510.11263 in picture coordinates (row, col):
        # H = 2x2 block, then column k rows 0..k-1, then row k columns k..0.
        N = int(parts[1])
        order = [(0, 0), (0, 1), (1, 0), (1, 1)]
        k = 2
        while len(order) < N:
            order += [(r, k) for r in range(k)] + [(k, c) for c in range(k, -1, -1)]
            k += 1
        order = order[:N]
        if parts[0] == 'spiraloff':
            assert kind == 'tri'
            return [(r, c - r // 2) for r, c in order]
        return order
    if parts[0] == 'disc':
        R2 = float(parts[1]); K = int(math.sqrt(R2)) + 2
        out = []
        for r in range(-K, K + 1):
            for c in range(-2 * K, 2 * K + 1):
                x, y = embed(kind, r, c)
                if x * x + y * y <= R2 + 1e-9:
                    out.append((r, c))
        return out
    raise ValueError(shape)

def build_graph(kind, verts):
    idx = {v: i for i, v in enumerate(verts)}
    nbrs = [[] for _ in verts]
    for (r, c), i in idx.items():
        for dr, dc in STEPS[kind]:
            j = idx.get((r + dr, c + dc))
            if j is not None:
                nbrs[i].append(j); nbrs[j].append(i)
    return nbrs

def paths_upto(nbrs, L):
    out = []
    def rec(path, used):
        l = len(path)
        if l % 2 == 0 and path[0] < path[-1]:
            out.append(tuple(path))
        if l == L:
            return
        for w in nbrs[path[-1]]:
            if w not in used:
                used.add(w); path.append(w)
                rec(path, used)
                path.pop(); used.discard(w)
    for s in range(len(nbrs)):
        rec([s], {s})
    return out

class Enc:
    def __init__(self, V, C):
        self.V, self.C = V, C
        self.nv = V * C
        self.eq = {}
        self.clauses = []
        self.paths = []
    def x(self, v, c):
        return v * self.C + c + 1
    def E(self, u, v):
        key = (min(u, v), max(u, v))
        e = self.eq.get(key)
        if e is None:
            self.nv += 1
            e = self.eq[key] = self.nv
            for c in range(self.C):
                self.add([-self.x(u, c), -self.x(v, c), e], None)
        return e
    def add(self, cl, path):
        self.clauses.append(cl); self.paths.append(path)
    def path_clause(self, p):
        k = len(p) // 2
        if k == 1:
            for c in range(self.C):
                self.add([-self.x(p[0], c), -self.x(p[1], c)], p)
            return
        self.add([-self.E(p[i], p[i + k]) for i in range(k)], p)

def write(enc, tag, kind, shape, C, Lbase, kmax, verts, v0):
    with open(f"{tag}.cnf", "w") as f:
        f.write(f"c nonrepetitive {kind} {shape} colours {C} base<={Lbase} lazy<={2*kmax}\n")
        f.write(f"p cnf {enc.nv} {len(enc.clauses)}\n")
        for cl in enc.clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    with open(f"{tag}.paths", "w") as f:
        f.write(f"{kind} {shape} {C} {v0}\n")
        for p in enc.paths:
            f.write(("-" if p is None else " ".join(map(str, p))) + "\n")
    with open(f"{tag}.verts", "w") as f:
        f.write(f"{kind} {shape} {len(verts)}\n")
        for r, c in verts:
            f.write(f"{r} {c}\n")

def main():
    kind, shape, C, Lbase, kmax = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    cap = int(sys.argv[6]) if len(sys.argv) > 6 else 5000
    tag = sys.argv[7] if len(sys.argv) > 7 else f"{kind}_{shape.replace(':','_')}_c{C}"
    verts = vertex_set(kind, shape)
    nbrs = build_graph(kind, verts)
    V = len(verts)
    # centre vertex: closest to the centroid of the embedding
    pts = [embed(kind, r, c) for r, c in verts]
    cx = sum(p[0] for p in pts) / V; cy = sum(p[1] for p in pts) / V
    v0 = min(range(V), key=lambda i: (pts[i][0] - cx) ** 2 + (pts[i][1] - cy) ** 2)
    enc = Enc(V, C)
    for v in range(V):
        enc.add([enc.x(v, c) for c in range(C)], None)
        for c1 in range(C):
            for c2 in range(c1 + 1, C):
                enc.add([-enc.x(v, c1), -enc.x(v, c2)], None)
    t0 = time.time()
    base = paths_upto(nbrs, Lbase)
    seen = set(base)
    for p in base:
        enc.path_clause(p)
    enc.add([enc.x(v0, 0)], None)
    nb0 = sorted(nbrs[v0])
    enc.add([enc.x(nb0[0], 1)], None)
    if len(nb0) > 1 and C > 2:
        enc.add([enc.x(nb0[1], 1), enc.x(nb0[1], 2)], None)
    solver = Cadical153(bootstrap_with=enc.clauses)
    pushed = nbase = len(enc.clauses)
    print(f"[{tag}] {kind} {shape}: {V} vertices, {sum(map(len, nbrs))//2} edges, C={C}, base paths<={Lbase}: "
          f"{len(base)} paths, {nbase} clauses, built {time.time()-t0:.1f}s; lazy <= {2*kmax} vertices; centre {verts[v0]}", flush=True)
    graph_hdr = f"{V} {C} {kmax} {cap}\n" + "".join(f"{len(nbrs[v])} " + " ".join(map(str, nbrs[v])) + "\n" for v in range(V))
    it = 0; t0 = time.time(); tcheck = 0.0
    while True:
        it += 1
        ts = time.time()
        sat = solver.solve()
        tsolve = time.time() - ts
        if not sat:
            print(f"[{tag}] UNSAT after {it} iterations, {len(enc.clauses)-nbase} lazy clauses, "
                  f"{len(enc.clauses)} clauses, {enc.nv} vars, {time.time()-t0:.1f}s (checker {tcheck:.1f}s)", flush=True)
            write(enc, tag, kind, shape, C, Lbase, kmax, verts, v0)
            return 20
        model = solver.get_model()
        col = [0] * V
        for v in range(V):
            for c in range(C):
                if model[enc.x(v, c) - 1] > 0:
                    col[v] = c
        ts = time.time()
        r = subprocess.run([os.path.join(HERE, 'repcheck')], input=graph_hdr + " ".join(map(str, col)) + "\n",
                           capture_output=True, text=True)
        tcheck += time.time() - ts
        reps = [tuple(map(int, line.split())) for line in r.stdout.splitlines() if line.strip()]
        new = 0
        for p in reps:
            if p not in seen:
                seen.add(p); enc.path_clause(p); new += 1
        for cl in enc.clauses[pushed:]:
            solver.add_clause(cl)
        pushed = len(enc.clauses)
        if it % 20 == 1 or new == 0:
            print(f"[{tag}] it {it}: solve {tsolve:.1f}s, {len(reps)} reps, {new} new, lazy {pushed-nbase}, "
                  f"lengths {sorted(set(len(p) for p in reps))}, {time.time()-t0:.0f}s (checker {tcheck:.0f}s)", flush=True)
        if new == 0:
            print(f"[{tag}] SAT: colouring with no repetition on paths <= {2*kmax} vertices", flush=True)
            with open(f"{tag}.sat.txt", "w") as f:
                f.write(f"{kind} {shape} {C} {kmax}\n")
                for (rr, cc), cl in zip(verts, col):
                    f.write(f"{rr} {cc} {cl}\n")
            return 10

if __name__ == "__main__":
    sys.exit(main())
