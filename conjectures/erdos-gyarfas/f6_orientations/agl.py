"""AGL(1,p) = {x -> a x + b : a in F_p^*, b in F_p}, and Cayley graphs on it.

Element (a,b) is indexed by (a-1)*p + b, a in 1..p-1, b in 0..p-1.
Composition is composition of functions, right factor applied first:
    (a,b)*(c,d) : x -> a(cx+d)+b = (ac, ad+b).
The Cayley graph Cay(G,S) has x ~ x*s for s in S (right multiplication), so
left multiplication by any group element is a graph automorphism.
"""
import numpy as np


class AGL:
    def __init__(self, p):
        self.p = p
        self.n = p * (p - 1)
        p1 = p - 1
        # element tables
        self.a = np.empty(self.n, dtype=np.int64)
        self.b = np.empty(self.n, dtype=np.int64)
        for a in range(1, p):
            for b in range(p):
                i = (a - 1) * p + b
                self.a[i] = a
                self.b[i] = b
        # multiplication table mul[x, y] = x*y
        A = self.a[:, None]
        B = self.b[:, None]
        C = self.a[None, :]
        D = self.b[None, :]
        self.mul = ((A * C) % p - 1) * p + (A * D + B) % p
        self.e = self.idx(1, 0)
        self.inv = np.empty(self.n, dtype=np.int64)
        for x in range(self.n):
            a, b = int(self.a[x]), int(self.b[x])
            ai = pow(a, -1, p)
            self.inv[x] = self.idx(ai, (-ai * b) % p)
        assert all(self.mul[x, self.inv[x]] == self.e for x in range(self.n))

    def idx(self, a, b):
        return (a - 1) * self.p + b

    def pair(self, x):
        return int(self.a[x]), int(self.b[x])

    def order(self, x):
        k, y = 1, x
        while y != self.e:
            y = int(self.mul[y, x])
            k += 1
        return k

    def involutions(self):
        return [x for x in range(self.n) if x != self.e and self.inv[x] == x]

    def adjacency(self, S):
        """Neighbour table (n x |S|) of Cay(G,S): column j is x*S[j]."""
        return np.stack([self.mul[:, s] for s in S], axis=1)


def bfs_girth_and_connected(adj, root):
    """BFS from root. Returns (girth_estimate, connected).
    girth_estimate = min over non-tree edges (x,y) of d(x)+d(y)+1; for a
    vertex-transitive graph this equals the girth (the shortest cycle through
    root has that length and any closed walk of that form contains a cycle no
    longer than it)."""
    n = adj.shape[0]
    dist = [-1] * n
    parent = [-1] * n
    dist[root] = 0
    queue = [root]
    best = 10 ** 9
    qi = 0
    while qi < len(queue):
        x = queue[qi]
        qi += 1
        dx = dist[x]
        # any non-tree edge (x',y') still to come has d(x')>=dx, d(y')>=dx-1,
        # hence candidate >= 2*dx: safe to stop once that cannot beat best
        if 2 * dx >= best:
            break
        for y in adj[x]:
            y = int(y)
            if dist[y] < 0:
                dist[y] = dx + 1
                parent[y] = x
                queue.append(y)
            elif parent[x] != y:
                c = dx + dist[y] + 1
                if c < best:
                    best = c
    return best, len(queue)


def girth_all_roots(adj):
    n = adj.shape[0]
    g = 10 ** 9
    for r in range(n):
        c, _ = bfs_girth_and_connected(adj, r)
        g = min(g, c)
    return g


def connected(adj, root=0):
    n = adj.shape[0]
    seen = [False] * n
    seen[root] = True
    st = [root]
    cnt = 1
    while st:
        x = st.pop()
        for y in adj[x]:
            y = int(y)
            if not seen[y]:
                seen[y] = True
                cnt += 1
                st.append(y)
    return cnt == n
