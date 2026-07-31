"""X0 — exact verification of the R3 parity machinery (Lemmas R3.1-R3.3).

Checks, all exact over F_2:
  1. S^2 = I                       (Sierpinski involution)
  2. path-cell parity at depth s = z_s, z = S . rev(y)   (path-parity identity)
  3. difference/shift conjugation: D(Sz) = S(sigma z)     (S sigma S = I + sigma)
  4. dyadic doubling: z^{(2m)} = (zeta, zeta + z^{(m)}),  zeta = S . rev(new block)
  5. nilpotency: right-anchored 2^B-periodic prefix => parity rows >= 2^B vanish
     on the dependency cone; in particular all path parities z_s = 0 for s >= 2^B.
"""

import numpy as np
from r3_common import (sierpinski, parity_triangle, path_parity_direct,
                       z_transform, anchored_periodic, de_bruijn)

rng = np.random.default_rng(1878)
ok = True


def check(name, cond):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    ok = ok and cond


# 1. involution
m = 256
S = sierpinski(m).astype(np.uint64)
check("S^2 = I  (m=256)", np.array_equal(S @ S % 2, np.eye(m, dtype=np.uint64)))

# 2. path-parity identity, random parities, several m
for m in (37, 128, 300, 1024):
    y = rng.integers(0, 2, size=m).astype(np.uint8)
    direct = path_parity_direct(y, m)
    z = z_transform(y)
    check(f"path parity = S.rev(y)  (m={m})", np.array_equal(direct, z))

# 3. shift conjugation: (Sz)_{u+1} + (Sz)_u = (S sigma z)_u
m = 512
z = rng.integers(0, 2, size=m).astype(np.uint8)
S = sierpinski(m).astype(np.uint64)
Sz = (S @ z % 2).astype(np.uint8)
sig_z = np.concatenate([z[1:], [0]]).astype(np.uint8)   # (sigma z)_r = z_{r+1}
S_sig_z = (S @ sig_z % 2).astype(np.uint8)
check("D(Sz) = S(sigma z)  (m=512)",
      np.array_equal(Sz[:-1] ^ Sz[1:], S_sig_z[:-1]))

# 4. dyadic doubling: m power of 2, y on [0, 2m) with new segment on [m, 2m)
m = 256
y = rng.integers(0, 2, size=2 * m).astype(np.uint8)
z2 = z_transform(y)                       # scale 2m
z1 = z_transform(y[:m])                   # scale m (deep prefix)
zeta = z_transform(y[m:])                 # transform of the new segment
check("doubling z^(2m) = (zeta, zeta+z^(m))  (m=256)",
      np.array_equal(z2, np.concatenate([zeta, zeta ^ z1])))

# 4b. Lemma R3.6: lead parity vanishing beyond s0 forces exact 2^B-periodicity
#     (B = ceil(log2 s0)); and the converse with the same threshold.
for s0 in (5, 16, 100):
    m = 2048
    B = int(np.ceil(np.log2(s0)))
    S = sierpinski(m).astype(np.uint64)
    # forward: y = S z with z supported on [0, s0) => y is 2^B-periodic
    z = np.zeros(m, dtype=np.uint8)
    z[:s0] = rng.integers(0, 2, s0)
    y = (S @ z % 2).astype(np.uint8)
    per = np.array_equal(y[2 ** B:], y[:-2 ** B])
    # converse: exact 2^B-periodic y has lead parities (S y) vanishing >= 2^B
    yp = np.tile(rng.integers(0, 2, 2 ** B).astype(np.uint8), m // 2 ** B)
    lam = (S @ yp.astype(np.uint64) % 2).astype(np.uint8)
    conv = not lam[2 ** B:].any()
    check(f"R3.6 (s0={s0}, B={B}): S(z<[s0)) is 2^B-periodic and converse",
          per and conv)

# 5. nilpotency for anchored-periodic prefixes
for B in (3, 5):
    P = 2 ** B
    m = 1200
    y = anchored_periodic(m, de_bruijn(B))
    rows = parity_triangle(y, m - 1)
    deep_ok = all(not rows[s].any() for s in range(P, m - 1))
    z = z_transform(y)
    check(f"P=2^{B} anchored-periodic: parity rows >= {P} vanish on cone "
          f"and z_s = 0 for s >= {P}",
      deep_ok and not z[P:].any() and z[:P].any())

print("\nALL PASS" if ok else "\nSOME CHECKS FAILED")
