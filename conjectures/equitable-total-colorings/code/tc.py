"""tc.py -- SAT encodings for 4-total colorings of cubic graphs (plain and equitable).

Variable convention (shared with verify_tc.decode_model, and nothing else):
  element index i = vertex v (i = v) or edge j in sorted order (i = n + j),
  color c in 0..3  ->  variable i*4 + c + 1.

Clauses (all from the definitions in arXiv:2609.05259 Sec. 1-2):
  E1  each element gets at least one color            (1 clause per element)
  E2  each element gets at most one color             (6 binary clauses per element)
  T1  adjacent vertices get distinct colors           (4 binary clauses per edge)
  T2  an edge and each endpoint get distinct colors   (8 binary clauses per edge)
  T3  adjacent edges get distinct colors              (4 binary clauses per pair of edges at a vertex)
  Q   [equitable only] every color class has size in {floor(N/4), ceil(N/4)}, N = n + m,
      via pysat CardEnc atleast/atmost (sequential counter by default).
  S   [optional, sound symmetry breaking] vertex 0 has color 0 and its three incident
      edges, in order of increasing other endpoint, have colors 1,2,3.  Sound because
      vertex 0 and its three edges are pairwise adjacent/incident, so in any 4-total
      coloring they carry four distinct colors, and a color permutation maps them to
      (0,1,2,3); color permutations preserve the total-coloring property and the
      multiset of class sizes, hence equitability.
"""
import itertools
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


# ---------- graph6 ----------
def parse_graph6(s):
    s = s.strip()
    if s.startswith('>>graph6<<'):
        s = s[10:]
    data = [ord(ch) - 63 for ch in s]
    if data[0] <= 62:
        n = data[0]; bits_start = 1
    else:
        raise ValueError("n > 62 not supported")
    bits = []
    for d in data[bits_start:]:
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


def to_graph6(n, edges):
    es = set(tuple(sorted(e)) for e in edges)
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if (i, j) in es else 0)
    while len(bits) % 6:
        bits.append(0)
    out = chr(n + 63)
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k + 6]:
            v = (v << 1) | b
        out += chr(v + 63)
    return out


# ---------- encoding ----------
def encode(n, edges, equitable, symbreak=True, card_enc=EncType.seqcounter):
    es = sorted(tuple(sorted(e)) for e in edges)
    m = len(es)
    N = n + m
    K = 4
    var = lambda i, c: i * K + c + 1
    eidx = {e: n + j for j, e in enumerate(es)}
    cl = []
    # E1, E2
    for i in range(N):
        cl.append([var(i, c) for c in range(K)])
        for c1, c2 in itertools.combinations(range(K), 2):
            cl.append([-var(i, c1), -var(i, c2)])
    inc = {v: [] for v in range(n)}
    for (u, v) in es:
        inc[u].append(eidx[(u, v)]); inc[v].append(eidx[(u, v)])
        for c in range(K):
            cl.append([-var(u, c), -var(v, c)])                 # T1
            cl.append([-var(eidx[(u, v)], c), -var(u, c)])      # T2
            cl.append([-var(eidx[(u, v)], c), -var(v, c)])      # T2
    for v in range(n):
        for a, b in itertools.combinations(inc[v], 2):
            for c in range(K):
                cl.append([-var(a, c), -var(b, c)])             # T3
    top = N * K
    if equitable:
        lo, hi = N // K, -(-N // K)
        for c in range(K):
            lits = [var(i, c) for i in range(N)]
            cnf = CardEnc.atleast(lits=lits, bound=lo, top_id=top, encoding=card_enc)
            cl.extend(cnf.clauses); top = max(top, cnf.nv)
            cnf = CardEnc.atmost(lits=lits, bound=hi, top_id=top, encoding=card_enc)
            cl.extend(cnf.clauses); top = max(top, cnf.nv)
    if symbreak:
        cl.append([var(0, 0)])
        nb = sorted(inc[0], key=lambda ei: es[ei - n][1] if es[ei - n][0] == 0 else es[ei - n][0])
        for k, ei in enumerate(nb):
            cl.append([var(ei, k + 1)])
    return cl, top


def solve(clauses, solver='cadical195'):
    with Solver(name=solver, bootstrap_with=clauses) as s:
        sat = s.solve()
        return sat, (s.get_model() if sat else None)


# ---------- named graphs ----------
def K4():
    return 4, [(i, j) for i in range(4) for j in range(i + 1, 4)]


def K33():
    return 6, [(i, j) for i in range(3) for j in range(3, 6)]


def prism(k):
    """circular ladder L_{2k} = C_k box K_2 ; vertices 0..k-1 outer, k..2k-1 inner"""
    es = []
    for i in range(k):
        es.append((i, (i + 1) % k)); es.append((k + i, k + (i + 1) % k)); es.append((i, k + i))
    return 2 * k, es


def mobius(k):
    """Moebius ladder M_{2k}: cycle C_{2k} plus the k long diagonals"""
    es = [(i, (i + 1) % (2 * k)) for i in range(2 * k)] + [(i, i + k) for i in range(k)]
    return 2 * k, es


def gpetersen(p, k):
    es = []
    for i in range(p):
        es.append((i, (i + 1) % p)); es.append((i, p + i)); es.append((p + i, p + (i + k) % p))
    return 2 * p, [tuple(sorted(e)) for e in es]


def graph_R():
    """The graph R of Dantas et al. (DAM 209, 2016), re-derived from Figure 1 of
    arXiv:2609.05259: four copies of K_{2,3} (poles T,B; ports L,C,R), wired by
    six edges:  Top.L-Left.R, Top.R-Right.L, Top.C-Bottom.C, Left.C-Right.C,
    Left.L-Bottom.L, Right.R-Bottom.R.
    Vertex numbering: gadget g in (0=Top,1=Left,2=Right,3=Bottom), vertex
    5g + (0=T,1=B,2=L,3=C,4=R)."""
    T, B, L, C, R = 0, 1, 2, 3, 4
    v = lambda g, x: 5 * g + x
    es = []
    for g in range(4):
        for port in (L, C, R):
            es.append((v(g, T), v(g, port))); es.append((v(g, B), v(g, port)))
    Top, Left, Right, Bottom = 0, 1, 2, 3
    es += [(v(Top, L), v(Left, R)), (v(Top, R), v(Right, L)), (v(Top, C), v(Bottom, C)),
           (v(Left, C), v(Right, C)), (v(Left, L), v(Bottom, L)), (v(Right, R), v(Bottom, R))]
    return 20, [tuple(sorted(e)) for e in es]


def figure1_coloring_of_R():
    """The coloring drawn in Figure 1 (colors 1..4 there -> 0..3 here)."""
    T, B, L, C, R = 0, 1, 2, 3, 4
    v = lambda g, x: 5 * g + x
    Top, Left, Right, Bottom = 0, 1, 2, 3
    vcol, ecol = {}, {}
    # (T color, B color, L,C,R colors, edge colors T-L,T-C,T-R,B-L,B-C,B-R) per gadget, 1-based as in figure
    spec = {
        Top:    (4, 4, (2, 1, 3), (1, 3, 2, 3, 2, 1)),
        Left:   (4, 4, (3, 2, 1), (1, 3, 2, 2, 1, 3)),   # L port is cropped in the figure; color 3 is forced
        Right:  (4, 4, (2, 3, 1), (1, 2, 3, 3, 1, 2)),   # R port cropped; color 1 forced
        Bottom: (4, 4, (1, 3, 2), (2, 1, 3, 3, 2, 1)),
    }
    for g, (tc, bc, ports, ecs) in spec.items():
        vcol[v(g, T)] = tc - 1; vcol[v(g, B)] = bc - 1
        for x, c in zip((L, C, R), ports):
            vcol[v(g, x)] = c - 1
        for x, c in zip((L, C, R), ecs[:3]):
            ecol[tuple(sorted((v(g, T), v(g, x))))] = c - 1
        for x, c in zip((L, C, R), ecs[3:]):
            ecol[tuple(sorted((v(g, B), v(g, x))))] = c - 1
    for (a, b) in [(v(Top, L), v(Left, R)), (v(Top, R), v(Right, L)), (v(Top, C), v(Bottom, C)),
                   (v(Left, C), v(Right, C)), (v(Left, L), v(Bottom, L)), (v(Right, R), v(Bottom, R))]:
        ecol[tuple(sorted((a, b)))] = 3
    return vcol, ecol
