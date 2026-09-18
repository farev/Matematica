"""Independent SAT engine for Leech's covering tree problem (OEIS A007187).
For each unlabeled tree shape on n vertices, encode: positive integer edge weights
(unary), all pairwise path sums (unary, capped at k+1), and coverage of 1..k.
a(n) >= k  iff  some shape is SAT.  UNSAT for every shape refutes k.
Usage: python3 satcover.py n k [--solver glucose42] [--proofdir DIR] [--shapes i,j,...]
"""
import sys, time, argparse, os
from pysat.formula import CNF
from pysat.solvers import Solver
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trees import free_trees

class Enc:
    def __init__(self):
        self.nv = 0; self.clauses = []
    def var(self):
        self.nv += 1; return self.nv
    def unary(self, cap):
        """bits[t] for t=1..cap meaning value >= t; returns list indexed 1..cap (index 0 unused)"""
        bits = [None] + [self.var() for _ in range(cap)]
        for t in range(1, cap):
            self.clauses.append([-bits[t+1], bits[t]])   # monotone
        return bits
    def add(self, X, Y, cz):
        """Z = min(X+Y, cz) as unary with cap cz. X, Y unary lists (index 0 unused)."""
        cx, cy = len(X) - 1, len(Y) - 1
        Z = self.unary(cz)
        # (i) X>=s and Y>=u -> Z >= min(s+u, cz)
        for s in range(0, cx + 1):
            for u in range(0, cy + 1):
                if s + u == 0: continue
                z = min(s + u, cz)
                cl = [Z[z]]
                if s >= 1: cl.append(-X[s])
                if u >= 1: cl.append(-Y[u])
                self.clauses.append(cl)
        # (ii) not(X>=s) and not(Y>=u) -> not(Z >= s+u-1), s in 1..cx+1, u in 1..cy+1
        for s in range(1, cx + 2):
            for u in range(1, cy + 2):
                z = s + u - 1
                if z > cz: continue
                if z < 1: continue
                cl = [-Z[z]]
                if s <= cx: cl.append(X[s])
                if u <= cy: cl.append(Y[u])
                self.clauses.append(cl)
        return Z

def encode(n, k, edges):
    N = n * (n - 1) // 2; B = N - k
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges): adj[a].append((b, i)); adj[b].append((a, i))
    # root at 0; parent, depth, parent edge
    parent = [-1] * n; pedge = [-1] * n; depth = [0] * n
    order = [0]; seen = [False] * n; seen[0] = True
    for v in order:
        for u, ei in adj[v]:
            if not seen[u]: seen[u] = True; parent[u] = v; pedge[u] = ei; depth[u] = depth[v] + 1; order.append(u)
    # subtree sizes for load bound
    size = [1] * n
    for v in reversed(order):
        if parent[v] >= 0: size[parent[v]] += size[v]
    enc = Enc()
    W = [None] * (n - 1)
    for v in range(1, n) if True else []:
        pass
    for v in order:
        if parent[v] < 0: continue
        load = size[v] * (n - size[v])
        wmax = k + 1 + B - load
        assert wmax >= 1, "edge weight bound < 1: shape impossible"
        W[pedge[v]] = enc.unary(wmax)
        enc.clauses.append([W[pedge[v]][1]])   # weight >= 1
    cap = k + 1
    # U[v][a] = unary distance from v up to ancestor a
    U = {}
    for v in order:
        if parent[v] < 0: continue
        U[(v, parent[v])] = W[pedge[v]]
        a = parent[v]
        while parent[a] >= 0:
            U[(v, parent[a])] = enc.add(U[(v, a)], W[pedge[a]], cap)
            a = parent[a]
    # pair distances
    def lca(x, y):
        while depth[x] > depth[y]: x = parent[x]
        while depth[y] > depth[x]: y = parent[y]
        while x != y: x = parent[x]; y = parent[y]
        return x
    D = {}
    for x in range(n):
        for y in range(x + 1, n):
            l = lca(x, y)
            if l == x: Dxy = U[(y, x)]
            elif l == y: Dxy = U[(x, y)]
            else: Dxy = enc.add(U[(x, l)], U[(y, l)], cap)
            D[(x, y)] = Dxy
    # coverage
    for v in range(1, k + 1):
        cl = []
        for (x, y), Dxy in D.items():
            c = len(Dxy) - 1
            if v > c: continue
            e = enc.var()
            enc.clauses.append([-e, Dxy[v]])
            if v + 1 <= c: enc.clauses.append([-e, -Dxy[v + 1]])
            cl.append(e)
        enc.clauses.append(cl)
    return enc, W, D

def decode(model, W, edges):
    ms = set(l for l in model if l > 0)
    ws = []
    for i, bits in enumerate(W):
        w = sum(1 for t in range(1, len(bits)) if bits[t] in ms)
        ws.append(w)
    return [(a, b, w) for (a, b), w in zip(edges, ws)]

def check_witness(n, k, wedges):
    # independent check: BFS distances
    adj = [[] for _ in range(n)]
    for a, b, w in wedges: adj[a].append((b, w)); adj[b].append((a, w))
    vals = set()
    for s in range(n):
        dist = [-1] * n; dist[s] = 0; st = [s]
        while st:
            v = st.pop()
            for u, w in adj[v]:
                if dist[u] < 0: dist[u] = dist[v] + w; st.append(u)
        vals.update(dist[t] for t in range(s + 1, n))
    return all(v in vals for v in range(1, k + 1))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int); ap.add_argument('k', type=int)
    ap.add_argument('--solver', default='cadical153')
    ap.add_argument('--proofdir', default=None)
    ap.add_argument('--shapes', default=None)
    ap.add_argument('--stop', action='store_true', help='stop at first SAT shape')
    args = ap.parse_args()
    n, k = args.n, args.k
    shapes = free_trees(n)
    idxs = list(range(len(shapes))) if args.shapes is None else [int(s) for s in args.shapes.split(',')]
    print(f"n={n} k={k} shapes={len(shapes)} solver={args.solver}", flush=True)
    t0 = time.time(); nsat = 0
    for i in idxs:
        edges = shapes[i]
        try:
            enc, W, D = encode(n, k, edges)
        except AssertionError as e:
            print(f"shape {i}: skipped ({e})", flush=True); continue
        with Solver(name=args.solver, bootstrap_with=enc.clauses, with_proof=(args.proofdir is not None)) as s:
            t1 = time.time()
            r = s.solve()
            dt = time.time() - t1
            if r:
                wedges = decode(s.get_model(), W, edges)
                ok = check_witness(n, k, wedges)
                print(f"shape {i}: SAT in {dt:.1f}s vars={enc.nv} clauses={len(enc.clauses)} witness={wedges} check={ok}", flush=True)
                nsat += 1
                if args.stop: break
            else:
                line = f"shape {i}: UNSAT in {dt:.1f}s vars={enc.nv} clauses={len(enc.clauses)}"
                if args.proofdir:
                    os.makedirs(args.proofdir, exist_ok=True)
                    cnfp = os.path.join(args.proofdir, f"n{n}_k{k}_s{i}.cnf")
                    CNF(from_clauses=enc.clauses).to_file(cnfp)
                    prf = s.get_proof()
                    with open(os.path.join(args.proofdir, f"n{n}_k{k}_s{i}.drup"), 'w') as f:
                        f.write('\n'.join(prf) + '\n')
                    line += f" proof_lines={len(prf)}"
                print(line, flush=True)
    print(f"DONE n={n} k={k} sat_shapes={nsat} total_time={time.time()-t0:.1f}s", flush=True)
