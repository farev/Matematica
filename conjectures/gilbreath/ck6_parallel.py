"""Parallel exact computation of c_6 (2^21 = 2,097,152 sign chambers).

Splits the DFS across the 2^6 = 64 sign prefixes of level 1 and runs them
in a process pool.  Certificate: the 64 partial partition functions must
sum exactly to 1.
"""

import itertools
import sys
import time
from fractions import Fraction
from multiprocessing import Pool

sys.argv = ["x", "--nolp"]
import ck_exact  # noqa: E402


def work(prefix):
    I, leaves, Z = ck_exact.compute_ci(6, verbose=False, prefix=prefix)
    return I, Z, leaves


if __name__ == "__main__":
    t0 = time.time()
    prefixes = list(itertools.product((1, -1), repeat=6))
    Itot, Ztot, leaves = Fraction(0), Fraction(0), 0
    with Pool(11) as pool:
        for n, (I, Z, lv) in enumerate(pool.imap_unordered(work, prefixes), 1):
            Itot += I
            Ztot += Z
            leaves += lv
            if n % 8 == 0:
                print(f"  {n}/64 prefixes, {leaves:,} chambers, "
                      f"{time.time()-t0:.0f}s", flush=True)
    print(f"\nchambers: {leaves:,} (expect 2,097,152)")
    print(f"partition check: {'PASS' if Ztot == 1 else '*** FAIL: ' + str(Ztot)}")
    print(f"c_6 = {Itot}")
    print(f"c_6 = {float(Itot):.6f}   ({time.time()-t0:.0f}s)")
    with open("c6_exact.txt", "w") as f:
        f.write(f"{Itot}\n")
