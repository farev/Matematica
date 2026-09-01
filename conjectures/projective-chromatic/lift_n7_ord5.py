"""Solve n7_ord5.cnf, lift the cell coloring to the 127 points, verify from
the definition, and confirm the coloring is genuinely order-5 invariant."""
from pysat.formula import CNF
from pysat.solvers import Glucose42
from lines import check_coloring
from matrix_ansatz import GF16, mul

K = 5
M7 = 127
H5 = GF16[0][3]

m7map = [0] * (M7 + 1)
for p in range(1, M7 + 1):
    a, b = p & 0xF, (p >> 4) & 0x7
    m7map[p] = mul(GF16, 4, a, H5) | (b << 4)

cell = [-1] * (M7 + 1)
nc = 0
for p in range(1, M7 + 1):
    if cell[p] != -1:
        continue
    stack = [p]
    cell[p] = nc
    while stack:
        q = stack.pop()
        r = m7map[q]
        if cell[r] == -1:
            cell[r] = nc
            stack.append(r)
    nc += 1
assert nc == 31

cnf = CNF(from_file="n7_ord5.cnf")
with Glucose42(bootstrap_with=cnf) as s:
    assert s.solve()
    model = set(l for l in s.get_model() if l > 0)

cellcolor = {}
for cid in range(nc):
    for c in range(K):
        if cid * K + c + 1 in model:
            cellcolor[cid] = c
            break
color = [None] * (M7 + 1)
for p in range(1, M7 + 1):
    color[p] = cellcolor[cell[p]]

bad = check_coloring(7, color, K)
assert not bad, bad[:3]
# invariance check
for p in range(1, M7 + 1):
    assert color[p] == color[m7map[p]]
sizes = sorted(sum(1 for p in range(1, M7 + 1) if color[p] == c) for c in range(K))
print("n=7 order-5-invariant witness VERIFIED (proper + invariant).")
print("class sizes:", sizes)
print("witness:", ",".join(str(color[p]) for p in range(1, M7 + 1)))
with open("witness_n7_ord5.txt", "w") as f:
    f.write(",".join(str(color[p]) for p in range(1, M7 + 1)) + "\n")
