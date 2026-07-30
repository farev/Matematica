"""Numerical verification of the session-2 microscope lenses (MICROSCOPE.md).

L2 (two-valued rigidity): a run of consecutive gaps with values in {2, B},
B = 2d+2, of length L >= q-1 is impossible for any odd prime q | (B-2),
q ∤ 2 (i.e. any odd q | 2d). Prediction: max run length over the primes is
< q0-1 where q0 = smallest odd prime factor of d; d a power of 2 has no
such obstruction and its runs may grow.

L3 (B-block collapse): maximal pure-B stretches inside {2,B}-runs are
CPAPs with difference B, so their length obeys the primorial bound
(every prime <= length+1 divides B).

Scans primes < 10^9 for {2, B}-runs for B = 4..40, reporting the maximal
run length containing at least one B-gap, and the maximal pure-B run.
"""

import numpy as np

from verify import primes_up_to
from microscope_bench import run_lengths


def smallest_odd_prime_factor(n):
    while n % 2 == 0:
        n //= 2
    if n == 1:
        return None  # d is a power of two: no odd obstruction
    q = 3
    while q * q <= n:
        if n % q == 0:
            return q
        q += 2
    return n


if __name__ == "__main__":
    g = np.diff(primes_up_to(10**9))[2:]  # gaps beyond (3,5)
    print(f"{'B':>4} {'d':>3} {'odd q0|d':>9} {'L2 bound':>9} "
          f"{'max {2,B} run':>14} {'max pure-B':>11} {'1.25logB+1':>11}")
    for d in range(1, 20):
        B = 2 * d + 2
        in_set = (g == 2) | (g == B)
        L = run_lengths(in_set)
        # keep only runs actually containing a B (pure-2 runs are twins-only)
        # approximate: max run overall minus check; do it exactly:
        c = in_set.astype(np.int8)
        dch = np.diff(c)
        starts = np.concatenate(([0] if c[0] else [], np.flatnonzero(dch == 1) + 1)).astype(int)
        ends = np.concatenate((np.flatnonzero(dch == -1) + 1, [len(c)] if c[-1] else [])).astype(int)
        best = 0
        for s, e in zip(starts, ends):
            if np.any(g[s:e] == B):
                best = max(best, e - s)
        pure = run_lengths(g == B)
        maxpure = int(pure.max()) if len(pure) else 0
        q0 = smallest_odd_prime_factor(d)
        bound = f"L<={q0-2}" if q0 else "none (2^s)"
        theo = 1.25 * np.log(B) + 1
        flag = ""
        if q0 and best > q0 - 2:
            flag = "  *** L2 VIOLATED ***"
        if maxpure > theo + 2:
            flag += "  *** L3 VIOLATED ***"
        print(f"{B:>4} {d:>3} {str(q0):>9} {bound:>9} {best:>14} "
              f"{maxpure:>11} {theo:>11.1f}{flag}")
