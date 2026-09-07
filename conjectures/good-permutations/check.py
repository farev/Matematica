#!/usr/bin/env python3
"""Independent checker for "good" permutations (MO 514690).

A permutation a_1..a_n of {1..n} is good iff for every 1 <= i < j <= n with
(i, j) != (1, n) and j - i + 1 >= 2, the block sum a_i + ... + a_j is NOT
divisible by the block length j - i + 1.  (Integer arithmetic only.)

Usage:
  python3 check.py 1 6 7 4 5 2 3        # check one permutation
  python3 check.py --construction 31    # check the asker's construction for p
  python3 check.py --file FILE          # one permutation per line
  python3 check.py --verbose ...        # also print the first offending block
"""
import sys


def is_good(a, verbose=False):
    n = len(a)
    assert sorted(a) == list(range(1, n + 1)), "not a permutation of 1..n"
    P = [0] * (n + 1)
    for i, v in enumerate(a, 1):
        P[i] = P[i - 1] + v
    for L in range(2, n):            # proper blocks: L <= n-1
        for i in range(0, n - L + 1):   # block a_{i+1} .. a_{i+L}
            s = P[i + L] - P[i]
            if s % L == 0:
                if verbose:
                    print(f"BAD: block positions {i+1}..{i+L} (length {L}) sum {s} "
                          f"= {L} * {s//L}")
                return False
    return True


def construction(p):
    """The asker's permutation 1, p-1, p, p-3, p-2, ..., 2, 3 (p odd)."""
    a = [1]
    x = p - 1
    while x >= 2:
        a += [x, x + 1]
        x -= 2
    assert len(a) == p
    return a


def even_construction(n):
    """Asker's comment: for even n, 2,1,4,3,...,n,n-1 is good."""
    a = []
    for k in range(1, n // 2 + 1):
        a += [2 * k, 2 * k - 1]
    return a


if __name__ == "__main__":
    args = sys.argv[1:]
    verbose = False
    if args and args[0] == "--verbose":
        verbose = True
        args = args[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    if args[0] == "--construction":
        p = int(args[1])
        a = construction(p)
        print("p =", p, "good =", is_good(a, verbose))
    elif args[0] == "--even":
        n = int(args[1])
        a = even_construction(n)
        print("n =", n, "good =", is_good(a, verbose))
    elif args[0] == "--file":
        cnt = 0
        for line in open(args[1]):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            a = [int(x) for x in line.replace(",", " ").split()]
            ok = is_good(a, verbose)
            cnt += 1
            print("good =", ok, ":", " ".join(map(str, a)))
        print(cnt, "permutations checked")
    else:
        a = [int(x) for x in args]
        print("good =", is_good(a, verbose))
