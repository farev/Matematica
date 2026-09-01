"""Emit DIMACS for the contracted chi_2(8) k=5 instances under the two
conjugacy classes of order-5 elements of GL(8,2), plus order-17 and pure
Frobenius, for kissat+DRUP certification. Also the n=7 order-5 instance.

Order-5 classes (deg-4 cyclotomic poly x^4+x^3+x^2+x+1 = companion C):
  [C,C]: on F_2^8 = F_2^4 + F_2^4, phi(a,b) = (Ca, Cb).
         Realized as mult by h5 = zeta_5 in GF(16) acting diagonally.
  [C,I]: phi(a,b) = (Ca, b).
n=7: [C,I3] on F_2^7 = F_2^4 + F_2^3 (only order-5 class there).
Order-17: mult by g^15 in GF(256) (deg-8 irreducible block, unique class).
Frobenius: x -> x^2 on GF(256) (order 8; its orbits = cyclotomic classes).
"""
import sys
sys.path.insert(0, ".")
from matrix_ansatz import GF16, mul, pointmap, split44, join44, M
from ansatz import contract as contract8, orbits_of as orbits8, EXP
import lines as lines_mod

K = 5

# order-5 element of GF(16)*: g^3 where g generates (order 15)
H5 = GF16[0][3]
# verify order 5: h^5 == 1 and h != 1
assert H5 != 1
x = 1
for _ in range(5):
    x = mul(GF16, 4, x, H5)
assert x == 1


def emit(cnf, nv, path):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {len(cnf)}\n")
        for cl in cnf:
            f.write(" ".join(map(str, cl)) + " 0\n")
    print(f"{path}: {nv} vars {len(cnf)} clauses")


def gen_n8(name, gens):
    cell, nc = orbits8(gens)
    cnf, nv = contract8(cell, nc, K)
    assert cnf is not None, f"{name} is DEAD?!"
    emit(cnf, nv, name)
    return cell, nc


# --- n=8 [C,C]: (a,b) -> (h5 a, h5 b)
cc = pointmap(lambda p: join44(mul(GF16, 4, split44(p)[0], H5),
                               mul(GF16, 4, split44(p)[1], H5)))
gen_n8("ord5_CC.cnf", [cc])

# --- n=8 [C,I]: (a,b) -> (h5 a, b)
ci = pointmap(lambda p: join44(mul(GF16, 4, split44(p)[0], H5), split44(p)[1]))
gen_n8("ord5_CI.cnf", [ci])

# --- n=8 order 17: mult by EXP[15] in GF(256)
h17 = EXP[15]
from ansatz import gf_mul
m17 = [0] + [gf_mul(h17, p) for p in range(1, M + 1)]
gen_n8("ord17.cnf", [m17])

# --- n=8 Frobenius x -> x^2
fr = [0] + [gf_mul(p, p) for p in range(1, M + 1)]
gen_n8("frob.cnf", [fr])

# --- n=7 [C,I3]: points 1..127, low 4 bits GF(16) block, high 3 bits fixed
M7 = 127


def orbits7(gens):
    cell = [-1] * (M7 + 1)
    nc = 0
    for p in range(1, M7 + 1):
        if cell[p] != -1:
            continue
        stack = [p]
        cell[p] = nc
        while stack:
            q = stack.pop()
            for gm in gens:
                r = gm[q]
                if cell[r] == -1:
                    cell[r] = nc
                    stack.append(r)
        nc += 1
    return cell, nc


L7 = lines_mod.lines(7)


def contract7(cell, nc, k):
    var = lambda cid, c: cid * k + c + 1
    edges, naes = set(), set()
    for (x, y, z) in L7:
        a, b, c3 = cell[x], cell[y], cell[z]
        s = {a, b, c3}
        if len(s) == 1:
            return None, 0
        elif len(s) == 2:
            u, v = sorted(s)
            edges.add((u, v))
        else:
            naes.add(tuple(sorted(s)))
    cnf = []
    for cid in range(nc):
        cnf.append([var(cid, c) for c in range(k)])
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(cid, c1), -var(cid, c2)])
    for (u, v) in edges:
        for c in range(k):
            cnf.append([-var(u, c), -var(v, c)])
    for (u, v, w) in naes:
        for c in range(k):
            cnf.append([-var(u, c), -var(v, c), -var(w, c)])
    return cnf, nc * k


c7 = [0] * (M7 + 1)
m7map = [0] * (M7 + 1)
for p in range(1, M7 + 1):
    a, b = p & 0xF, (p >> 4) & 0x7
    m7map[p] = mul(GF16, 4, a, H5) | (b << 4)
cell7, nc7 = orbits7([m7map])
cnf7, nv7 = contract7(cell7, nc7, K)
if cnf7 is None:
    print("n7 ord5: DEAD")
else:
    emit(cnf7, nv7, "n7_ord5.cnf")
    print(f"n7 ord5 cells: {nc7}")
