#!/usr/bin/env python3
"""NUMERICAL artifact for NOTE R5: measured digit-coincidence densities for
the i=2 mechanism at n = 2^k.

For each k (4..64) with the full factorization of 2^k - 1, compute EXACTLY
(digit dynamic programming, no enumeration):
  - D_q = |{j in [0, n/2]: j base-q dominated by n}| for each prime q | 2^k-1
  - under an independence heuristic the expected number of tight j is
        E_k = (n/2+1) * prod_q ( D_q / (n/2+1) )
  - the observed count (0 or 1) from the certified censuses.
The table lets a reader judge whether E_k decays (finite family plausible)
or not (infinite family plausible). Exact integer arithmetic; the only
floating point is in the final printed ratio.
"""
import sys
from family699 import factor_or_none

def digits(n, p):
    d = []
    while n:
        d.append(n % p)
        n //= p
    return d  # LSB first

def dom_count_upto(n, p, X):
    """|{ j in [0, X] : every base-p digit of j <= that of n }| exactly."""
    dn = digits(n, p)[::-1]   # MSB first
    dx = digits(X, p)
    dx = [0] * (len(dn) - len(dx)) + dx[::-1]  # pad to same length, MSB first
    # DP over positions: count_free = completions when already < X prefix
    # walk with tight prefix
    total = 0
    tight_ok = True
    free_tail = [1] * (len(dn) + 1)
    for pos in range(len(dn) - 1, -1, -1):
        free_tail[pos] = free_tail[pos + 1] * (dn[pos] + 1)
    for pos in range(len(dn)):
        if not tight_ok:
            break
        lim = min(dn[pos], dx[pos] - 1)
        if lim >= 0:
            total += (lim + 1) * free_tail[pos + 1]
        if dx[pos] > dn[pos]:
            # digit dx[pos] itself not allowed; all tight continuations die
            tight_ok = False
        # else: continue tight with digit dx[pos]
    if tight_ok:
        total += 1  # X itself is dominated
    return total

observed = {4: 1, 9: 1, 11: 1, 41: 1}

print("k,omega,factors,E_heuristic,observed,decided")
undecided = {45: [2,3,4], 50: [2], 53: [2], 54: [3], 55: [2,3,4,5],
             56: [2,3,4,5], 58: [2], 60: [2], 63: [2,3], 64: [2]}
for k in range(4, 65):
    n = 2 ** k
    nh = n // 2
    f = factor_or_none(n - 1)
    if f is None:
        print(f"{k},?,FACTORING-FAILED,,,")
        continue
    qs = sorted(f)
    if len(qs) == 1 and f[qs[0]] == 1 and qs[0] == n - 1:
        # Mersenne prime: excluded by Theorem 7(b)
        print(f"{k},1,mersenne-prime,0,0,theorem")
        continue
    E_num = 1
    E_den = 1
    for q in qs:
        Dq = dom_count_upto(n, q, nh)
        E_num *= Dq
        E_den *= (nh + 1)
    E = (nh + 1) * E_num / E_den
    dec = "undecided-levels" if k in undecided and 2 in undecided.get(k, []) \
        else "decided"
    print(f"{k},{len(qs)},{'*'.join(str(q) for q in qs)},{E:.3g},"
          f"{observed.get(k, 0)},{dec}")
