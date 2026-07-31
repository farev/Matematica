"""Phase-1 exploration: look at Liouville correlations at 10^7 scale.

- S_h(x) = sum_{n<=x} lambda(n)lambda(n+h) for h=1..12, compared to sqrt(x)
- control 1: same statistic on a Fisher-Yates shuffle of the lambda values
- control 2 (near-miss): a completely multiplicative +-1 function that FAILS
  Chowla -- the real Dirichlet character chi mod 3 (extended by chi(3)= -1 to
  keep it +-1-valued), where S_3 has a positive density main term.

Run:  python3 explore.py
"""

import numpy as np
from liouville import lambda_block

X = 10**7
lam = lambda_block(1, X + 64).astype(np.int64)
rng = np.random.default_rng(1)

print(f"x = {X:.0e},  sqrt(x) = {X**0.5:.0f}")
print(f"L(x) = {lam[:X].sum()}")

print("\n-- real Liouville --")
for h in range(1, 13):
    S = int((lam[:X] * lam[h:X + h]).sum())
    print(f"  S_{h:<2d}(x) = {S:>8d}   S/sqrt(x) = {S/X**0.5:+7.2f}   S/x = {S/X:+.2e}")

print("\n-- shuffled control (same multiset of values) --")
sh = lam[:X].copy()
rng.shuffle(sh)
for h in [1, 2, 3]:
    S = int((sh[:X - h] * sh[h:X]).sum())
    print(f"  S_{h}(x) = {S:>8d}   S/sqrt(x) = {S/X**0.5:+7.2f}")

print("\n-- near-miss: completely multiplicative chi3-like (fails Chowla) --")
# f multiplicative with f(p) = legendre(p|3) for p != 3, f(3) = -1
# then f(n)f(n+3) correlates: for n coprime to 3, f(n)f(n+3) has bias.
n = np.arange(1, X + 64, dtype=np.int64)
chi = np.zeros_like(n)
chi[n % 3 == 1] = 1
chi[n % 3 == 2] = -1
# build completely multiplicative extension with f(3) = -1 via 3-adic valuation
v3 = np.zeros_like(n)
m = n.copy()
while True:
    mask = m % 3 == 0
    if not mask.any():
        break
    v3[mask] += 1
    m[mask] //= 3
f = np.where(m % 3 == 1, 1, -1) * np.where(v3 & 1, -1, 1)
for h in [1, 2, 3, 6]:
    S = int((f[:X] * f[h:X + h]).sum())
    print(f"  S_{h}(x) = {S:>9d}   S/x = {S/X:+.3f}")
