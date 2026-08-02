"""Validation of the segmented Liouville sieve against brute force.

Run:  python3 test_liouville.py
"""

import numpy as np
from liouville import lambda_block, lambda_brute, primes_up_to


def main():
    rng = np.random.default_rng(20260729)

    # 1) full agreement on [1, 200000)
    blk = lambda_block(1, 200_000)
    for n in range(1, 200_000):
        assert blk[n - 1] == lambda_brute(n), f"mismatch at {n}"
    print("OK  [1, 2e5) full agreement with trial division")

    # 2) high random windows, including around powers of two (acc overflow risk)
    for base in [10**9, 10**12, 2**40, 3 * 10**10]:
        L = base + int(rng.integers(0, 1000))
        R = L + 2000
        blk = lambda_block(L, R)
        for i, n in enumerate(range(L, R)):
            assert blk[i] == lambda_brute(n), f"mismatch at {n}"
        print(f"OK  [{L}, {R}) agreement with trial division")

    # 3) block-splitting invariance: lambda on [1,N) equals concatenation
    N = 300_000
    whole = lambda_block(1, N)
    parts = np.concatenate([lambda_block(a, min(a + 7919, N))
                            for a in range(1, N, 7919)])
    assert np.array_equal(whole, parts)
    print("OK  segmentation invariance")

    # 4) L(x) spot values computed two ways
    print("L(10^6) =", int(lambda_block(1, 10**6 + 1).sum()))


if __name__ == "__main__":
    main()
