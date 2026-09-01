"""Combined instance: does ANY chi_2(8)=5 witness restrict, on the fixed
hyperplane H = F_2^7 (points 1..127 inside F_2^8), to an order-5-invariant
coloring of PG(6,2)?

Since (i) all order-5 subgroups of GL(7,2) are conjugate (unique class
[C,I_3], Phi_5 irreducible of degree 4), (ii) GL(8,2) is transitive on
hyperplanes, and (iii) conjugation transports witnesses, UNSAT of this one
instance proves: NO proper 5-coloring of PG(7,2) has any hyperplane whose
restriction admits an order-5 automorphism.

Encoding: 31 cell-color vars blocks (order-5 orbits of H under
phi = (zeta_5 on low nibble, identity on bits 4-6)) with the contracted
in-H constraints, + 128 affine point-color vars, + for each h in H* and
affine pair {(v,1),(v+h,1)}: not both colored cell-color(h).
Writes combined_ord5_ext.cnf. Lift/verify on SAT: any model gives a full
chi_2(8)=5 witness (checked from the definition by the caller).
"""
from lines import lines

K = 5
M7 = 127

P16 = 0b10011


def mul16(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 0x10:
            a ^= P16
    return r


z5 = mul16(mul16(2, 2), 2)  # 2^3, order 5 in GF(16)*
x = 1
for _ in range(5):
    x = mul16(x, z5)
assert x == 1 and z5 != 1

pm = [0] * (M7 + 1)
for p in range(1, M7 + 1):
    pm[p] = mul16(p & 0xF, z5) | (p & 0x70)

cell = [-1] * (M7 + 1)
nc = 0
for p in range(1, M7 + 1):
    if cell[p] != -1:
        continue
    q = p
    while cell[q] == -1:
        cell[q] = nc
        q = pm[q]
    nc += 1
assert nc == 31

cvar = lambda cid, c: cid * K + c + 1            # 1..155
avar = lambda v, c: 155 + v * K + c + 1          # v in 0..127 -> 156..795
cnf = []
# cell constraints (contract the 2667 in-H lines)
for cid in range(nc):
    cnf.append([cvar(cid, c) for c in range(K)])
    for c1 in range(K):
        for c2 in range(c1 + 1, K):
            cnf.append([-cvar(cid, c1), -cvar(cid, c2)])
dead = False
for (x_, y_, z_) in lines(7):
    s = {cell[x_], cell[y_], cell[z_]}
    if len(s) == 1:
        dead = True
    elif len(s) == 2:
        u, v = sorted(s)
        for c in range(K):
            cnf.append([-cvar(u, c), -cvar(v, c)])
    else:
        u, v, w = sorted(s)
        for c in range(K):
            cnf.append([-cvar(u, c), -cvar(v, c), -cvar(w, c)])
assert not dead
# affine ALO
for v in range(128):
    cnf.append([avar(v, c) for c in range(K)])
# mixed lines {(v,1),(v^h,1),(h,0)}: forbidden joint color = color of cell(h)
for h in range(1, M7 + 1):
    ch = cell[h]
    for v in range(128):
        w = v ^ h
        if v < w:
            for c in range(K):
                cnf.append([-cvar(ch, c), -avar(v, c), -avar(w, c)])

nv = 155 + 128 * K
with open("combined_ord5_ext.cnf", "w") as f:
    f.write(f"p cnf {nv} {len(cnf)}\n")
    for cl in cnf:
        f.write(" ".join(map(str, cl)) + " 0\n")
print(f"combined_ord5_ext.cnf: {nv} vars {len(cnf)} clauses (31 cells + 128 affine)")
