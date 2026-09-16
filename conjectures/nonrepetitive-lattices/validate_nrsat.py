#!/usr/bin/env python3
"""Independent validator for a CNF written by nrsat.py (UNSAT case).

Reads <tag>.cnf, <tag>.paths, <tag>.verts; rebuilds adjacency from the
lattice step rule with its own code; checks every clause is one of
  (a) at-least-one / at-most-one colour per vertex,
  (b) an equality-variable definition (-x_{u,c} v -x_{v,c} v E_uv), all C
      colours present for each E,
  (c) the clause of a listed simple path v1..v2k of the graph:
      k=1 -> (-x_{v1,c} v -x_{v2,c}) for each c; k>=2 -> OR_i -E(v_i,v_{i+k}),
  (d) the three colour-relabelling clauses on the recorded centre vertex.
Every clause of kind (a)-(c) is implied by "the colouring is nonrepetitive";
(d) is a relabelling.  Hence UNSAT proves the patch has no nonrepetitive
C-colouring.
"""
import sys
STEPS = {'square': [(1, 0), (0, 1)], 'tri': [(1, 0), (0, 1), (1, -1)],
         'king': [(1, 0), (0, 1), (1, 1), (1, -1)]}

def main(tag):
    with open(f"{tag}.verts") as f:
        kind, shape, V = f.readline().split(); V = int(V)
        verts = [tuple(map(int, f.readline().split())) for _ in range(V)]
    assert len(set(verts)) == V
    idx = {v: i for i, v in enumerate(verts)}
    adj = set()
    for (r, c), i in idx.items():
        for dr, dc in STEPS[kind]:
            j = idx.get((r + dr, c + dc))
            if j is not None:
                adj.add((i, j)); adj.add((j, i))
    with open(f"{tag}.paths") as f:
        k2, s2, C, v0 = f.readline().split(); C = int(C); v0 = int(v0)
        assert k2 == kind and s2 == shape
        plines = [l.strip() for l in f]
    clauses = []
    with open(f"{tag}.cnf") as f:
        for line in f:
            if line[0] in 'cp':
                continue
            lits = list(map(int, line.split())); assert lits[-1] == 0
            clauses.append(lits[:-1])
    assert len(clauses) == len(plines)
    x = lambda v, c: v * C + c + 1
    edef = {}
    for cl, pl in zip(clauses, plines):
        if pl == '-' and len(cl) == 3 and cl[0] < 0 and cl[1] < 0 and cl[2] > V * C:
            u, cu = divmod(-cl[0] - 1, C); v, cv = divmod(-cl[1] - 1, C)
            assert cu == cv and u != v and 0 <= u < V and 0 <= v < V, cl
            edef.setdefault(cl[2], set()).add((min(u, v), max(u, v), cu))
    Evar = {}
    for e, s in edef.items():
        pairs = set((u, v) for u, v, _ in s); cols = set(c for _, _, c in s)
        assert len(pairs) == 1 and cols == set(range(C)), (e, s)
        Evar[e] = next(iter(pairs))
    pair_to_E = {p: e for e, p in Evar.items()}
    nb0 = sorted(j for (i, j) in adj if i == v0)
    kinds = dict(alo=0, amo=0, edef=0, edge=0, path=0, sym=0)
    for cl, pl in zip(clauses, plines):
        if pl != '-':
            p = list(map(int, pl.split())); k = len(p) // 2
            assert len(p) == 2 * k and k >= 1 and len(set(p)) == len(p) and all(0 <= v < V for v in p), p
            assert all((p[i], p[i + 1]) in adj for i in range(len(p) - 1)), p
            if k == 1:
                assert len(cl) == 2 and cl[0] < 0 and cl[1] < 0
                u, cu = divmod(-cl[0] - 1, C); v, cv = divmod(-cl[1] - 1, C)
                assert cu == cv and {u, v} == set(p), (cl, p)
                kinds['edge'] += 1
            else:
                want = sorted(-pair_to_E[(min(p[i], p[i + k]), max(p[i], p[i + k]))] for i in range(k))
                assert sorted(cl) == want, (cl, want, p)
                kinds['path'] += 1
            continue
        if len(cl) == C and all(l > 0 for l in cl) and len(set((l - 1) // C for l in cl)) == 1 \
                and sorted((l - 1) % C for l in cl) == list(range(C)) and max(cl) <= V * C:
            kinds['alo'] += 1
        elif len(cl) == 2 and cl[0] < 0 and cl[1] < 0 and (-cl[0] - 1) // C == (-cl[1] - 1) // C \
                and -cl[0] <= V * C and -cl[1] <= V * C and cl[0] != cl[1]:
            kinds['amo'] += 1
        elif len(cl) == 3 and cl[2] in Evar:
            u, cu = divmod(-cl[0] - 1, C); v, cv = divmod(-cl[1] - 1, C)
            assert cu == cv and (min(u, v), max(u, v)) == Evar[cl[2]], cl
            kinds['edef'] += 1
        elif cl == [x(v0, 0)] or cl == [x(nb0[0], 1)] or (len(nb0) > 1 and cl == [x(nb0[1], 1), x(nb0[1], 2)]):
            kinds['sym'] += 1
        else:
            raise AssertionError(f"unexpected clause {cl} ({pl})")
    assert kinds['alo'] == V and kinds['amo'] == V * C * (C - 1) // 2 and kinds['sym'] == 3, kinds
    assert kinds['edef'] == C * len(Evar)
    # edge clauses: each edge of the graph must be covered by C clauses (properness)
    print(f"VALID {tag}: {kind} {shape} V={V} C={C} centre={verts[v0]} {kinds}: every clause is a necessary "
          f"condition for a nonrepetitive colouring, up to colour relabelling")

if __name__ == "__main__":
    main(sys.argv[1])
