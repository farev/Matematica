import sys, itertools
def read_planar_code(f):
    hdr = f.read(15); assert hdr == b'>>planar_code<<', hdr
    while True:
        b = f.read(1)
        if not b: return
        n = b[0]; adj = []
        for v in range(n):
            lst = []
            while True:
                u = f.read(1)[0]
                if u == 0: break
                lst.append(u-1)
            adj.append(lst)
        yield n, adj
def faces_of(n, adj):
    pos = [{u:i for i,u in enumerate(a)} for a in adj]
    seen = set(); faces = []
    for v in range(n):
        for i in range(len(adj[v])):
            if (v,i) in seen: continue
            a, ai, fv = v, i, []
            while (a,ai) not in seen:
                seen.add((a,ai)); b = adj[a][ai]; fv.append(a)
                j = pos[b][a]; ai = (j - 1) % len(adj[b]); a = b
            faces.append(tuple(fv))
    return faces
hist = {}
cnt = 0
for n, adj in read_planar_code(sys.stdin.buffer):
    F = faces_of(n, adj); assert all(len(f)==3 for f in F)
    best = None
    for mask in range(1 << (n-1)):      # vertex n-1 fixed blue (colour exchange)
        R = [(mask >> v) & 1 for v in range(n-1)] + [0]
        ok = all(0 < R[a]+R[b]+R[c] < 3 for a,b,c in F)
        if ok:
            d = abs(2*sum(R) - n)
            if best is None or d < best: best = d
    hist[best] = hist.get(best, 0) + 1; cnt += 1
print("n=%d graphs=%d" % (n, cnt), dict(sorted(hist.items())))
