"""Count zeros and sign changes of L(n), n <= XMAX, in one streaming pass.

External certificate: BFM (Math. Comp. 77, 2008, p.1692) report 133 sign
changes and 252 zeros of L(n) for n < 10^9.

Also counts sign changes of S_1(n) (running pair-correlation sum) as a
descriptive statistic.  Usage: python3 signchange.py 1e9
"""

import math
import sys

import numpy as np

from liouville import lambda_block, primes_up_to


def main():
    xmax = int(float(sys.argv[1]))
    seg = 5 * 10**6
    primes = primes_up_to(math.isqrt(xmax + seg + 2))
    Lrun = 0
    S1run = 0
    zeros = 0
    changes = 0
    s1_changes = 0
    last_sign = 1   # L(1) = +1
    s1_last = 0
    for L0 in range(1, xmax + 1, seg):
        hi = min(L0 + seg, xmax + 1)
        lam = lambda_block(L0, hi + 1, primes).astype(np.int64)
        n = hi - L0
        cs = Lrun + np.cumsum(lam[:n])
        zeros += int((cs == 0).sum())
        sgn = np.sign(cs)
        nz = sgn[sgn != 0]
        if nz.size:
            allsigns = np.concatenate(([last_sign], nz))
            changes += int((np.diff(allsigns) != 0).sum())
            last_sign = int(nz[-1])
        Lrun = int(cs[-1])
        # S_1 path sign changes
        prod = lam[:n] * lam[1:n + 1]
        cs1 = S1run + np.cumsum(prod)
        sgn1 = np.sign(cs1)
        nz1 = sgn1[sgn1 != 0]
        if nz1.size:
            all1 = np.concatenate(([s1_last], nz1)) if s1_last else nz1
            s1_changes += int((np.diff(all1) != 0).sum())
            s1_last = int(nz1[-1])
        S1run = int(cs1[-1])
    print(f"x <= {xmax}: L zeros = {zeros}, L sign changes = {changes} "
          f"(BFM: 252 zeros, 133 changes below 1e9)")
    print(f"S_1 sign changes = {s1_changes}, final L = {Lrun}, "
          f"final S_1 = {S1run}")


if __name__ == "__main__":
    main()
