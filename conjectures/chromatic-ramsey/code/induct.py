#!/usr/bin/env python3
"""Parametrised inductive construction for colourings of E_k (even # zeros) and O_k (odd # zeros)
in {+1,-1,0}^k, and a from-definition validity check.

E_{k+1} = E_k x {+,-}  u  O_k x {0};   O_{k+1} = O_k x {+,-}  u  E_k x {0}.
Given colourings colA of A = "same-parity" set and colB of B = "other-parity" set (colours 0..k-1):
 (i)   (x,+)-(x,-): new colour k.
 (ii)  (x,e)-(y,-e), x != y in A, c = colA(x,y):
         sign flip at c (x_c = -y_c != 0): new iff e == t1 * x_c, else old c
         support change (x_c != 0 = y_c): new iff e == t2 * x_c ; (x_c = 0 != y_c): new iff -e == t2*y_c
 (iii) (x,e)-(z,0), x in A, z in B: c = pick(D(x,z)); if x_c != 0: old c iff e == t3 * x_c
         if x_c == 0 (so z_c != 0): old c iff e == t4 * z_c ;   otherwise new.
usage: induct.py kmax   (tries all parameter combinations, reports which survive to kmax)
"""
import itertools
import sys


def pick_rules():
    def sc(x, z): return [c for c in range(len(x)) if (x[c] == 0) != (z[c] == 0)]
    def sf(x, z): return [c for c in range(len(x)) if x[c] * z[c] == -1]
    D = lambda x, z: [c for c in range(len(x)) if x[c] != z[c]]
    return {
        'minD': lambda x, z: min(D(x, z)),
        'maxD': lambda x, z: max(D(x, z)),
        'minSC': lambda x, z: min(sc(x, z)),
        'maxSC': lambda x, z: max(sc(x, z)),
        'minSFelseSC': lambda x, z: (min(sf(x, z)) if sf(x, z) else min(sc(x, z))),
        'maxSFelseSC': lambda x, z: (max(sf(x, z)) if sf(x, z) else max(sc(x, z))),
    }

def lift(colA, A, colB, B, k, t1, t2, t3, t4, pick):
    """colour the set A x {+,-} u B x {0} in dimension k+1 (new coordinate index k)."""
    col = {}
    def put(u, v, c):
        if u > v: u, v = v, u
        col[(u, v)] = c
    for (x, y), c in colA.items():
        for e in (1, -1):
            put(x + (e,), y + (e,), c)
    for (x, y), c in colB.items():
        put(x + (0,), y + (0,), c)
    for x in A:
        put(x + (1,), x + (-1,), k)
    for (x, y), c in colA.items():
        for (u, v) in ((x, y), (y, x)):   # u in layer e, v in layer -e
            for e in (1, -1):
                if u[c] * v[c] == -1:
                    new = (e == t1 * u[c])
                elif u[c] != 0:
                    new = (e == t2 * u[c])
                else:
                    new = (-e == t2 * v[c])
                put(u + (e,), v + (-e,), k if new else c)
    for x in A:
        for z in B:
            c = pick(x, z)
            for e in (1, -1):
                if x[c] != 0: old = (e == t3 * x[c])
                else: old = (e == t4 * z[c])
                put(x + (e,), z + (0,), c if old else k)
    return col

def valid(col, V):
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    M = [[-1] * n for _ in range(n)]
    for (u, v), c in col.items():
        assert u[c] != v[c], ("bad colour", u, v, c)
        M[idx[u]][idx[v]] = M[idx[v]][idx[u]] = c
    for i in range(n):
        for j in range(i + 1, n):
            if M[i][j] < 0: return False, ("uncoloured", V[i], V[j])
    for i in range(n):
        Mi = M[i]
        for j in range(i + 1, n):
            c = Mi[j]; Mj = M[j]
            for l in range(j + 1, n):
                if Mi[l] == c and Mj[l] == c: return False, ("triangle", V[i], V[j], V[l], c)
    return True, None

def run(kmax, t1, t2, t3, t4, pickname, verbose=False):
    pick = pick_rules()[pickname]
    E = [(1,), (-1,)]; O = [(0,)]
    colE = {((-1,), (1,)): 0}; colO = {}
    for k in range(1, kmax):
        newE = [x + (e,) for x in E for e in (1, -1)] + [z + (0,) for z in O]
        newO = [x + (e,) for x in O for e in (1, -1)] + [z + (0,) for z in E]
        cE = lift(colE, E, colO, O, k, t1, t2, t3, t4, pick)
        cO = lift(colO, O, colE, E, k, t1, t2, t3, t4, pick)
        okE, whyE = valid(cE, newE); okO, whyO = valid(cO, newO)
        if verbose: print(f"  k={k+1}: E {'ok' if okE else whyE}  O {'ok' if okO else whyO}")
        if not (okE and okO): return k + 1, (whyE or whyO)
        E, O, colE, colO = newE, newO, cE, cO
    return None, None

if __name__ == '__main__':
    kmax = int(sys.argv[1])
    best = []
    for pickname in pick_rules():
        for t1, t2, t3, t4 in itertools.product((1, -1), repeat=4):
            fail_k, why = run(kmax, t1, t2, t3, t4, pickname)
            tag = f"pick={pickname} t=({t1},{t2},{t3},{t4})"
            if fail_k is None: print("SURVIVES to k =", kmax, ":", tag); best.append(tag)
            else: print(f"fails at k={fail_k}: {tag}  {why}")
    print("survivors:", best)
