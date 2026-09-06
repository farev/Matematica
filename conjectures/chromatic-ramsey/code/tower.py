#!/usr/bin/env python3
"""Tower search: colour E_k / O_k (even / odd number of 2's in [3]^k) so that the three layers
by the LAST coordinate restrict to prescribed colourings of E_{k-1} / O_{k-1}.
Writes col_tower_{E|O}_k{k}.txt. Prints statistics of the cross colourings."""
import sys, itertools, time, collections
from pysat.solvers import Solver

def parse(fn):
    col = {}
    for l in open(fn):
        a, b, c = l.split(); col[(tuple(map(int, a)), tuple(map(int, b)))] = int(c)
    return col

def vertex_set(k, parity):
    return [v for v in itertools.product(range(3), repeat=k) if v.count(2) % 2 == parity]

def solve_with_fixed(V, k, fixed, name='cadical153'):
    idx = {v: i for i, v in enumerate(V)}; n = len(V)
    E = {}; nv = 0
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(k):
                if V[a][c] != V[b][c]:
                    nv += 1; E[(a, b, c)] = nv
    def ev(a, b, c):
        if a > b: a, b = b, a
        return E.get((a, b, c))
    clauses = []
    for a in range(n):
        for b in range(a + 1, n):
            clauses.append([E[(a, b, c)] for c in range(k) if (a, b, c) in E])
    for a in range(n):
        for b in range(a + 1, n):
            for d in range(b + 1, n):
                for c in range(k):
                    x, y, z = ev(a, b, c), ev(a, d, c), ev(b, d, c)
                    if x and y and z: clauses.append([-x, -y, -z])
    for (x, y), c in fixed.items():
        clauses.append([ev(idx[x], idx[y], c)])
    t0 = time.time()
    with Solver(name=name, bootstrap_with=clauses) as sol:
        r = sol.solve()
        print(f"  n={n} vars={nv} clauses={len(clauses)} fixed={len(fixed)} -> {'SAT' if r else 'UNSAT'} {time.time()-t0:.1f}s", flush=True)
        if not r: return None
        m = set(l for l in sol.get_model() if l > 0)
        col = {}
        for a in range(n):
            for b in range(a + 1, n):
                cs = [c for c in range(k) if (a, b, c) in E and E[(a, b, c)] in m]
                col[(V[a], V[b])] = cs[0]
        for a, b, d in itertools.combinations(range(n), 3):
            assert not (col[(V[a], V[b])] == col[(V[a], V[d])] == col[(V[b], V[d])])
        return col

def lift(colE, colO, k):
    """colE, colO: colourings of E_{k-1}, O_{k-1}. Returns colourings of E_k and O_k."""
    out = {}
    for parity, name in ((0, 'E'), (1, 'O')):
        V = vertex_set(k, parity)
        low_same = colE if parity == 0 else colO   # layers 0,1
        low_other = colO if parity == 0 else colE  # layer 2
        fixed = {}
        for (x, y), c in low_same.items():
            for i in (0, 1):
                fixed[(x + (i,), y + (i,))] = c
        for (x, y), c in low_other.items():
            fixed[(x + (2,), y + (2,))] = c
        print(f"lifting {name}_{k}:", flush=True)
        col = solve_with_fixed(V, k, fixed)
        if col is None: return None
        out[name] = col
        with open(f"col_tower_{name}_k{k}.txt", "w") as f:
            for (a, b), c in sorted(col.items()):
                f.write(f"{''.join(map(str,a))} {''.join(map(str,b))} {c}\n")
    return out

if __name__ == '__main__':
    kmax = int(sys.argv[1])
    # base k=1: E_1={0,1} colour 0 ; O_1={2}
    colE = {((0,), (1,)): 0}; colO = {}
    for k in range(2, kmax + 1):
        res = lift(colE, colO, k)
        if res is None:
            print("tower broke at k =", k); sys.exit(1)
        colE, colO = res['E'], res['O']
    print("tower reached k =", kmax)
