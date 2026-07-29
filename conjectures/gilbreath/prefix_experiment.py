"""How much of the actual prime sequence does Gilbreath's conjecture need?

Row k's leading entry depends only on the first k+1 primes.  So shuffling
all gaps after position M can only change rows k >= M.  If the property
still holds for the whole triangle after such a shuffle, the specific
arrangement of gaps beyond the prefix is irrelevant -- only their
statistics matter.

We keep the first M prime gaps, shuffle the rest, and test the full
triangle (primes < 10^8, ~5.7M rows), for M from 0 upward.
"""

import numpy as np

from experiments import gaps_of_primes, kstar_and_defects

if __name__ == "__main__":
    g = gaps_of_primes(10**8)
    rng = np.random.default_rng(1878)  # Proth's year

    print(f"{'M (kept prefix)':>16} {'trials ok':>10} {'k* values':>24}")
    for M in (0, 1, 2, 4, 8, 16, 32, 64, 128, 256):
        oks, kstars = 0, []
        for _ in range(5):
            gs = g.copy()
            tail = gs[M:]
            rng.shuffle(tail)
            gs[M:] = tail
            k, ok, _ = kstar_and_defects(gs)
            oks += ok
            kstars.append(k if ok else f"FAIL@{k}")
        print(f"{M:>16} {oks:>7}/5 {str(kstars):>24}")
