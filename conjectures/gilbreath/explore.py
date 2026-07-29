"""Small-scale exploration of Gilbreath's conjecture.

Write the primes in a row. Repeatedly take absolute differences of
adjacent entries. Conjecture (Proth 1878 / Gilbreath 1958): every row
after the first begins with 1.
"""

import numpy as np


def primes_up_to(n: int) -> np.ndarray:
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = False
    return np.nonzero(sieve)[0]


def triangle(seq, rows):
    """Return the first `rows` difference rows of seq."""
    out = []
    row = np.asarray(seq, dtype=np.int64)
    for _ in range(rows):
        row = np.abs(np.diff(row))
        out.append(row)
    return out


def show(seq, rows, width=20):
    print("seq :", " ".join(f"{x:3d}" for x in seq[:width]))
    for i, row in enumerate(triangle(seq, rows), 1):
        print(f"d^{i:<2d}:", " ".join(f"{x:3d}" for x in row[:width]))


if __name__ == "__main__":
    ps = primes_up_to(200)
    print("=== Gilbreath triangle on the primes ===")
    show(ps, 12)

    print("\n=== leading entries of first 30 rows (primes < 10^6) ===")
    ps = primes_up_to(10**6)
    leads = [row[0] for row in triangle(ps, 30)]
    print(leads)

    print("\n=== a non-prime sequence with the same parity shape can FAIL ===")
    # 2 followed by odd numbers, but with a big early jump
    bad = [2, 3, 9, 11, 13, 15, 17, 19, 21, 23]
    show(bad, 4, width=10)
