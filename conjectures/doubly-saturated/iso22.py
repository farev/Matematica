"""Group the 220 n=22 hits into orbits under the obvious symmetries of the Z_11-bicirculant family:
   multipliers x->a*x, relative shift of the second class, class swap.  (Negation x->-x is a multiplier.)"""
from itertools import combinations
m, k = 11, 2
n = m*k
idx, norb = {}, 0
for i in range(k):
    for j in range(i,k):
        for d in range(m):
            if i==j and d==0: continue
            if (i,j,d) in idx: continue
            idx[(i,j,d)] = norb; idx[(j,i,(m-d)%m)] = norb; norb += 1
def edges_of(mask):
    return {(u,v) for u,v in combinations(range(n),2) if mask >> idx[(u//m, v//m, (v-u)%m)] & 1}
def mask_of(E):
    mk = 0
    for u,v in E: mk |= 1 << idx[(u//m, v//m, (v-u)%m)]
    return mk
def apply(E, a, c, swap):
    def f(w):
        x, i = w % m, w // m
        x = (a*x) % m
        if i == 1: x = (x + c) % m
        if swap: i = 1 - i
        return i*m + x
    return {tuple(sorted((f(u), f(v)))) for u,v in E}

masks = sorted(set(int(x) for x in open("masks22.txt")))
seen, classes = set(), []
for mk in masks:
    if mk in seen: continue
    E = edges_of(mk); orb = set()
    for a in range(1, m):
        for c in range(m):
            for sw in (0,1):
                orb.add(mask_of(apply(E, a, c, sw)))
    cls = orb & set(masks)
    seen |= cls
    classes.append((mk, len(cls), len(orb)))
print(f"{len(masks)} masks -> {len(classes)} orbits under the obvious symmetry group")
for mk, sz, full in classes: print(f"   representative mask={mk}  hits in this orbit={sz}  full orbit size={full}")
