#!/usr/bin/env python3
"""Control battery for the pm-davenport engines.

Asserts, for both Engine A (dpm.py, imported) and Engine B (./dpm_fast,
subprocess), agreement with every independently PROVED or literature value
available:

  1. Cyclic groups, 2 <= n <= 64:  mu(C_n) = floor(log2 n)
     (proved: NOTE.md Lemma 3; literature: Adhikari et al., secondary).
  2. Elementary 2- and 3-groups:   mu(C_2^r) = mu(C_3^r) = r
     (proved: NOTE.md Lemma 4).
  3. Marchan-Ordaz-Schmid exceptional values (order <= 100, secondary,
     snippets 2026-08-25):  D+-(C_3^2) = 3, D+-(C_3^3) = 4,
     D+-(C_3^2 + C_9) = 6.
  4. A sample of MOS non-exceptional orders <= 100 (D+- = floor(log2|G|)+1,
     secondary):  C_5^2 -> 5, C_7^2 -> 6, C_7+C_14 -> 7, C_5+C_20 -> 7,
     C_3+C_6 -> 5, C_9^2 -> 7, C_2+C_2n for n <= 8 -> floor(log2 4n)+1.
  5. Verifier controls: a planted zero-sum set is rejected; the two
     headline witnesses are accepted.
  6. Engine A vs Engine B: identical (mu, n_extremal, nodes) on every
     group above (nodes = number of nonempty dissociated sets, an
     isomorphism invariant).

Exit 0 iff every assertion passes.
"""

import subprocess
import sys

from dpm import Group, search
from verify_witness import check


def engineB(orders):
    out = subprocess.run(["./dpm_fast"] + [str(o) for o in orders],
                         capture_output=True, text=True, check=True).stdout
    line = next(l for l in out.splitlines() if l.startswith("d_pm"))
    p = line.replace("=", " ").split()
    return int(p[1]), int(p[5]), int(p[7])   # mu, n_extremal, nodes


def both(orders):
    a = search(Group(orders))
    b = engineB(orders)
    assert (a["dpm"], a["nodes"]) == (b[0], b[2]), \
        f"A/B disagree on {orders}: {a['dpm'], a['nodes']} vs {b[0], b[2]}"
    return a["dpm"], b[1], b[2]


fails = 0


def expect(cond, msg):
    global fails
    if cond:
        print(f"  ok   {msg}")
    else:
        print(f"  FAIL {msg}")
        fails += 1


print("[1] cyclic groups 2..64: mu = floor(log2 n)")
for n in range(2, 65):
    mu, _, _ = both([n])
    expect(mu == n.bit_length() - 1, f"mu(C_{n}) = {mu}")

print("[2] elementary 2-/3-groups: mu = r")
for r in range(1, 7):
    mu, _, _ = both([2] * r)
    expect(mu == r, f"mu(C_2^{r}) = {mu}")
for r in range(1, 5):
    mu, _, _ = both([3] * r)
    expect(mu == r, f"mu(C_3^{r}) = {mu}")

print("[3] MOS exceptional values (secondary)")
for orders, dpm_expected in [([3, 3], 3), ([3, 3, 3], 4), ([3, 3, 9], 6)]:
    mu, _, _ = both(orders)
    expect(mu + 1 == dpm_expected, f"D+-({orders}) = {mu+1} (lit {dpm_expected})")

print("[4] MOS non-exceptional samples (secondary): D+- = floor(log2|G|)+1")
samples = [[5, 5], [7, 7], [7, 14], [5, 20], [3, 6], [9, 9]] + \
          [[2, 2 * n] for n in range(2, 9)]
for orders in samples:
    N = 1
    for o in orders:
        N *= o
    mu, _, _ = both(orders)
    expect(mu + 1 == N.bit_length() - 1 + 1,
           f"D+-({orders}) = {mu+1} = floor(log2 {N})+1")

print("[5] verifier controls")
expect(check([9], [(1,), (2,), (4,)]) is None, "C_9 {1,2,4} accepted")
expect(check([15], [(1,), (2,), (3,)]) is not None,
       "C_15 {1,2,3} rejected (1+2-3=0)")
expect(check([5, 15], [(0, 1), (0, 2), (0, 4), (1, 0), (2, 0)]) is None,
       "headline C_5+C_15 witness accepted")
expect(check([7, 21], [(0, 1), (0, 2), (1, 1), (1, 5), (2, 1), (2, 10),
                       (3, 19)]) is None,
       "headline C_7+C_21 witness accepted")
expect(check([5, 15], [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0)]) is not None,
       "planted zero-sum set rejected")

print(f"\n{'ALL CONTROLS PASS' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
