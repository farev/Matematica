"""brute.py -- SAT-free exhaustive enumeration of 4-total colorings of a cubic graph,
written from the definition (no pysat, no shared code with tc.py except graph6 parsing
which is re-implemented here).

A 4-total coloring = a proper vertex 4-coloring + a proper edge coloring such that every
edge's color differs from both endpoint colors.  We enumerate proper vertex colorings by
backtracking (colors introduced in increasing order to kill the S4 color symmetry), and for
each one enumerate the compatible edge colorings by backtracking (each edge has exactly
two admissible colors).  Class sizes are counted directly over all elements.

Optional pruning for the equitable question (derived from the definition, see REPORT):
the color-i class has size v_i + |M_i| with |M_i| <= (n - v_i)/2, hence
v_i <= |c_i| <= (n + v_i)/2.  Equitable at N = 5n/2 elements forces
   2*lo - n <= v_i <= hi   with lo = floor(N/4), hi = ceil(N/4).
With --equitable we prune vertex classes exceeding hi (upper bound) and check the final
lower bound and the class-size condition directly on each completed total coloring.

usage: python3 brute.py [--equitable] [--first] graph6 [graph6 ...]
prints, per graph, the number of 4-total colorings found (up to color permutation),
and the set of class-size configurations attained.
"""
import sys


def parse_g6(s):
    s = s.strip()
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        d = ord(ch) - 63
        for k in range(5, -1, -1):
            bits.append((d >> k) & 1)
    edges = []
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                edges.append((i, j))
            idx += 1
    return n, edges


def enumerate_total_colorings(n, edges, equitable=False, first_only=False):
    m = len(edges)
    N = n + m
    lo, hi = N // 4, -(-N // 4)
    adj = [[] for _ in range(n)]
    inc = [[] for _ in range(n)]
    for ei, (u, v) in enumerate(edges):
        adj[u].append(v); adj[v].append(u)
        inc[u].append(ei); inc[v].append(ei)
    # vertex order: BFS from 0 for better pruning
    order = []
    seen = [False] * n
    from collections import deque
    dq = deque([0]); seen[0] = True
    while dq:
        x = dq.popleft(); order.append(x)
        for y in adj[x]:
            if not seen[y]:
                seen[y] = True; dq.append(y)
    assert len(order) == n
    pos = {v: i for i, v in enumerate(order)}
    eorder_global = sorted(range(m), key=lambda ei: (min(pos[edges[ei][0]], pos[edges[ei][1]]),
                                                     max(pos[edges[ei][0]], pos[edges[ei][1]])))
    lb = 2 * lo - n  # definition-derived lower bound on v_i for an equitable coloring (see docstring)
    vcol = [-1] * n
    vcount = [0] * 4
    configs = {}
    total = [0]
    ecol = [-1] * m
    stop = [False]

    def edge_colorings(k, eorder):
        # backtrack over edges in eorder; count each complete edge coloring
        if stop[0]:
            return
        if k == m:
            sizes = [0] * 4
            for c in vcol:
                sizes[c] += 1
            for c in ecol:
                sizes[c] += 1
            key = tuple(sorted(sizes, reverse=True))
            if equitable and key[0] - key[-1] > 1:
                return
            configs[key] = configs.get(key, 0) + 1
            total[0] += 1
            if first_only:
                stop[0] = True
            return
        ei = eorder[k]
        u, v = edges[ei]
        used = set()
        for f in inc[u] + inc[v]:
            if ecol[f] >= 0:
                used.add(ecol[f])
        for c in range(4):
            if c == vcol[u] or c == vcol[v] or c in used:
                continue
            ecol[ei] = c
            edge_colorings(k + 1, eorder)
            ecol[ei] = -1
            if stop[0]:
                return

    def vertex_colorings(k, maxc):
        if stop[0]:
            return
        if k == n:
            if equitable:
                for i in range(4):
                    if vcount[i] < lb:
                        return
            edge_colorings(0, eorder_global)
            return
        x = order[k]
        forb = set(vcol[y] for y in adj[x] if vcol[y] >= 0)
        for c in range(min(maxc + 2, 4)):   # colors 0..maxc+1 (new color only the next unused one)
            if c in forb:
                continue
            if equitable and vcount[c] + 1 > hi:
                continue
            vcol[x] = c; vcount[c] += 1
            # equitable: the remaining n-k-1 vertices must be able to lift every class to >= lb
            if not equitable or sum(max(0, lb - vcount[i]) for i in range(4)) <= n - k - 1:
                vertex_colorings(k + 1, max(maxc, c))
            vcol[x] = -1; vcount[c] -= 1
            if stop[0]:
                return

    vertex_colorings(0, -1)
    return total[0], configs


if __name__ == "__main__":
    args = sys.argv[1:]
    equitable = "--equitable" in args
    first = "--first" in args
    gs = [a for a in args if not a.startswith("--")]
    for g6 in gs:
        n, E = parse_g6(g6)
        import time
        t = time.time()
        tot, cfg = enumerate_total_colorings(n, E, equitable=equitable, first_only=first)
        print(f"{g6}\tn={n}\t{'equitable-only' if equitable else 'all'}\tcolorings(up to color perm)={tot}\tconfigs={dict(sorted(cfg.items()))}\t{time.time()-t:.1f}s", flush=True)
