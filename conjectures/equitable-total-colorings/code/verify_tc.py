"""verify_tc.py -- independent checker for (equitable) 4-total colorings, written
from the definitions in arXiv:2609.05259, Sections 1-2:

  * a k-total coloring assigns one of k colors to each vertex and each edge so
    that adjacent vertices, adjacent edges, and any incident vertex/edge pair
    receive distinct colors;
  * it is equitable if the cardinalities of any two color classes differ by at
    most one (classes are counted over ALL elements, vertices and edges).

Nothing here is shared with the SAT encoder except the trivial, documented
convention used to decode a model (decode_model), which is deliberately kept
in this file so the encoder never has to be trusted for decoding.
"""


def elements(n, edges):
    """Canonical element list: vertices 0..n-1, then edges as sorted (u,v) tuples."""
    es = sorted(tuple(sorted(e)) for e in edges)
    return list(range(n)), es


def decode_model(n, edges, model, k=4):
    """Model convention: element index i (vertices first, then sorted edges),
    color c in 0..k-1  <->  variable i*k + c + 1.  Returns (vcol, ecol)."""
    vs, es = elements(n, edges)
    pos = set(l for l in model if l > 0)
    vcol, ecol = {}, {}
    for i, v in enumerate(vs):
        cs = [c for c in range(k) if (i * k + c + 1) in pos]
        if len(cs) != 1:
            raise ValueError(f"vertex {v} has {len(cs)} colors")
        vcol[v] = cs[0]
    for j, e in enumerate(es):
        i = n + j
        cs = [c for c in range(k) if (i * k + c + 1) in pos]
        if len(cs) != 1:
            raise ValueError(f"edge {e} has {len(cs)} colors")
        ecol[e] = cs[0]
    return vcol, ecol


def check_total_coloring(n, edges, vcol, ecol, k=4, equitable=False):
    """Return (ok, message, class_sizes). Checks every constraint from scratch."""
    vs, es = elements(n, edges)
    # every element colored with a color in range
    for v in vs:
        if v not in vcol or not (0 <= vcol[v] < k):
            return False, f"vertex {v} uncolored or out of range", None
    for e in es:
        if e not in ecol or not (0 <= ecol[e] < k):
            return False, f"edge {e} uncolored or out of range", None
    inc = {v: [] for v in vs}
    for (u, v) in es:
        inc[u].append((u, v)); inc[v].append((u, v))
        # adjacent vertices
        if vcol[u] == vcol[v]:
            return False, f"adjacent vertices {u},{v} share color {vcol[u]}", None
        # incident vertex/edge
        if ecol[(u, v)] == vcol[u] or ecol[(u, v)] == vcol[v]:
            return False, f"edge {(u,v)} shares color with an endpoint", None
    # adjacent edges
    for v in vs:
        cols = [ecol[e] for e in inc[v]]
        if len(set(cols)) != len(cols):
            return False, f"two edges at vertex {v} share a color", None
    sizes = [0] * k
    for v in vs:
        sizes[vcol[v]] += 1
    for e in es:
        sizes[ecol[e]] += 1
    assert sum(sizes) == len(vs) + len(es)
    if equitable and max(sizes) - min(sizes) > 1:
        return False, f"not equitable: class sizes {sizes}", sizes
    return True, "ok", sizes


def is_cubic_simple(n, edges):
    es = set()
    for (u, v) in edges:
        if u == v or not (0 <= u < n and 0 <= v < n):
            return False
        e = tuple(sorted((u, v)))
        if e in es:
            return False
        es.add(e)
    deg = [0] * n
    for (u, v) in es:
        deg[u] += 1; deg[v] += 1
    return all(d == 3 for d in deg)


def is_connected(n, edges):
    adj = {v: [] for v in range(n)}
    for (u, v) in edges:
        adj[u].append(v); adj[v].append(u)
    seen = {0}; stack = [0]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y); stack.append(y)
    return len(seen) == n
