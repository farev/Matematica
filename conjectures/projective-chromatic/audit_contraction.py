"""Independent audit of the certification instances.

Rebuilds ord17.cnf, frob.cnf, ord5_CC.cnf, ord5_CI.cnf from scratch with
implementations deliberately different from the generator:
  - orbits by cycle-walking a single permutation (generator uses BFS closure);
  - clause set built as a set of frozensets and compared exactly against the
    shipped file (same first-occurrence cell numbering convention);
  - the group-theoretic claims are re-verified by exact F_2 linear algebra:
    each map is checked linear, its order is computed, and its fixed-space
    dimension identifies the conjugacy class (order-5: rank(phi - I) = 8
    <=> [C,C], = 4 <=> [C,I]; Phi_5 irreducible makes these the only
    possibilities); |GL(8,2)| is recomputed and factored.

Run from this directory after gen_order5.py: python3 audit_contraction.py
Exits 0 with "AUDIT OK" iff everything matches.
"""
import sys

M, N, K = 255, 8, 5
POLY = 0x11D


def gf_mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 0x100:
            a ^= POLY
    return r


def gf_pow(a, e):
    r = 1
    while e:
        if e & 1:
            r = gf_mul(r, a)
        a = gf_mul(a, a)
        e >>= 1
    return r


# --- the four maps, rebuilt independently ---
G = 2
assert gf_pow(G, 255) == 1 and all(gf_pow(G, 255 // p) != 1 for p in (3, 5, 17))
h17 = gf_pow(G, 15)
maps = {}
maps["ord17"] = [0] + [gf_mul(h17, p) for p in range(1, M + 1)]
maps["frob"] = [0] + [gf_mul(p, p) for p in range(1, M + 1)]

# GF(16) inside split representation: low/high nibble, poly x^4+x+1
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


# order-5 element of GF(16)*: generator 2 has order 15; 2^3 has order 5
z5 = 1
for _ in range(3):
    z5 = mul16(z5, 2)
x = 1
for _ in range(5):
    x = mul16(x, z5)
assert x == 1 and z5 != 1
maps["ord5_CC"] = [0] + [(mul16(p & 0xF, z5) | (mul16(p >> 4, z5) << 4)) for p in range(1, M + 1)]
maps["ord5_CI"] = [0] + [(mul16(p & 0xF, z5) | ((p >> 4) << 4)) for p in range(1, M + 1)]


def check_linear_and_order(pm, expected_order):
    full = [0] * 256
    for p in range(1, 256):
        full[p] = pm[p]
    for a in range(256):
        for b in range(256):
            assert full[a ^ b] == full[a] ^ full[b], "not linear"
    # order
    cur = list(range(256))
    o = 0
    while True:
        cur = [full[c] for c in cur]
        o += 1
        if cur == list(range(256)):
            break
        assert o <= 300
    assert o == expected_order, (o, expected_order)
    # fixed space dimension (count fixed points = 2^dim)
    fixed = sum(1 for p in range(256) if full[p] == p)
    d = fixed.bit_length() - 1
    assert 1 << d == fixed
    return d


assert check_linear_and_order(maps["ord17"], 17) == 0
assert check_linear_and_order(maps["frob"], 8) == 1   # fixed field of x->x^2 is F_2: dim 1
assert check_linear_and_order(maps["ord5_CC"], 5) == 0  # [C,C]: no fixed space
assert check_linear_and_order(maps["ord5_CI"], 5) == 4  # [C,I]: fixed space F_2^4
print("maps: linearity, orders, fixed-space dims OK "
      "(ord17:[C8], frob fixes F2, ord5 classes [C,C]/[C,I])")

# --- |GL(8,2)| factorization ---
order = 1
for i in range(8):
    order *= (1 << 8) - (1 << i)
n = order
fac = {}
d = 2
while d * d <= n:
    while n % d == 0:
        fac[d] = fac.get(d, 0) + 1
        n //= d
    d += 1
if n > 1:
    fac[n] = fac.get(n, 0) + 1
assert fac == {2: 28, 3: 5, 5: 2, 7: 2, 17: 1, 31: 1, 127: 1}, fac
print(f"|GL(8,2)| = {order} = 2^28 3^5 5^2 7^2 17 31 127 OK "
      "(odd primes: 3,5,7,17,31,127; 17 exactly once => Sylow-17 cyclic conj.)")


def orbits_by_cycles(pm):
    """cells by cycle-walking, numbered by first occurrence over p=1..255."""
    cell = [-1] * (M + 1)
    nc = 0
    for p in range(1, M + 1):
        if cell[p] != -1:
            continue
        q = p
        while cell[q] == -1:
            cell[q] = nc
            q = pm[q]
        assert cell[q] == nc  # closed cycle
        nc += 1
    return cell, nc


def build_clauses(cell, nc):
    lines = []
    for x in range(1, M + 1):
        for y in range(x + 1, M + 1):
            z = x ^ y
            if z > y:
                lines.append((x, y, z))
    assert len(lines) == M * (M - 1) // 6
    var = lambda cid, c: cid * K + c + 1
    cls = set()
    for cid in range(nc):
        cls.add(frozenset(var(cid, c) for c in range(K)))
        for c1 in range(K):
            for c2 in range(c1 + 1, K):
                cls.add(frozenset({-var(cid, c1), -var(cid, c2)}))
    for (x, y, z) in lines:
        s = {cell[x], cell[y], cell[z]}
        if len(s) == 1:
            return None
        if len(s) == 2:
            u, v = sorted(s)
            for c in range(K):
                cls.add(frozenset({-var(u, c), -var(v, c)}))
        else:
            u, v, w = sorted(s)
            for c in range(K):
                cls.add(frozenset({-var(u, c), -var(v, c), -var(w, c)}))
    return cls


def read_cnf(path):
    cls = set()
    nv = None
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p cnf"):
            nv = int(line.split()[2])
            continue
        lits = [int(t) for t in line.split()]
        assert lits[-1] == 0
        cls.add(frozenset(lits[:-1]))
    return cls, nv


ok = True
for name, expected_cells in [("ord17", 15), ("frob", 35), ("ord5_CC", 51), ("ord5_CI", 63)]:
    cell, nc = orbits_by_cycles(maps[name])
    assert nc == expected_cells, (name, nc)
    mine = build_clauses(cell, nc)
    assert mine is not None, f"{name}: DEAD?!"
    theirs, nv = read_cnf(f"certs/{name}.cnf" if name in ("ord17", "frob") else f"{name}.cnf")
    if mine == theirs and nv == nc * K:
        print(f"{name}: {nc} cells, clause sets IDENTICAL ({len(mine)} distinct clauses) OK")
    else:
        print(f"{name}: MISMATCH mine={len(mine)} theirs={len(theirs)} nv={nv}")
        ok = False

print("AUDIT OK" if ok else "AUDIT FAILED")
sys.exit(0 if ok else 1)
