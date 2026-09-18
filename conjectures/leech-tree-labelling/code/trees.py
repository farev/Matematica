"""Generate all unlabeled free trees on n vertices (as edge lists), via rooted level
sequences (Beyer-Hedetniemi successor) deduplicated by the center-rooted AHU canonical form.
Counts are checked against OEIS A000055."""
import sys

def rooted_level_sequences(n):
    """Yield all canonical level sequences of rooted trees on n vertices (Beyer-Hedetniemi 1980)."""
    if n == 1:
        yield [0]; return
    L = list(range(n))  # 0,1,2,...,n-1 : the path
    yield list(L)
    while True:
        # find p: last index with L[p] > 1
        p = n - 1
        while p >= 0 and L[p] <= 1: p -= 1
        if p < 0: return
        # find q: parent of p in the sequence: last index < p with L[q] == L[p]-1
        q = p - 1
        while L[q] != L[p] - 1: q -= 1
        for i in range(p, n): L[i] = L[i - (p - q)]
        yield list(L)

def level_seq_to_edges(L):
    n = len(L); parent = [-1]*n; stack = []
    edges = []
    for i, lv in enumerate(L):
        while len(stack) > lv: stack.pop()
        if stack:
            parent[i] = stack[-1]; edges.append((stack[-1], i))
        stack.append(i)
    return edges

def canon_free(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    # centers
    deg = [len(adj[v]) for v in range(n)]
    alive = [True]*n; cnt = n
    layer = [v for v in range(n) if deg[v] <= 1]
    while cnt > 2:
        nxt = []
        for v in layer:
            alive[v] = False; cnt -= 1
            for u in adj[v]:
                if alive[u]:
                    deg[u] -= 1
                    if deg[u] == 1: nxt.append(u)
        layer = nxt
    centers = [v for v in range(n) if alive[v]]
    def ahu(v, p):
        return '(' + ''.join(sorted(ahu(u, v) for u in adj[v] if u != p)) + ')'
    if len(centers) == 1: return 'C' + ahu(centers[0], -1)
    a, b = centers
    return 'B' + min(ahu(a, b) + ahu(b, a), ahu(b, a) + ahu(a, b))

def free_trees(n):
    seen = {}
    for L in rooted_level_sequences(n):
        e = level_seq_to_edges(L)
        c = canon_free(n, e)
        if c not in seen: seen[c] = e
    return list(seen.values())

if __name__ == '__main__':
    A000055 = {1:1,2:1,3:1,4:2,5:3,6:6,7:11,8:23,9:47,10:106,11:235,12:551,13:1301}
    for n in range(1, int(sys.argv[1]) + 1):
        t = free_trees(n)
        print(n, len(t), 'OK' if len(t) == A000055[n] else 'MISMATCH vs A000055=%d' % A000055[n])
