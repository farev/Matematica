"""Parallel CERTIFIED exact computation of c_6."""

import itertools
import time
from fractions import Fraction
from multiprocessing import Pool

from ck_exact_certified import compute_ci_certified


def work(prefix):
    I, Z, leaves, fb = compute_ci_certified(6, prefix=prefix, verbose=False)
    return I, Z, leaves, fb


if __name__ == "__main__":
    t0 = time.time()
    prefixes = list(itertools.product((1, -1), repeat=6))
    Itot, Ztot, leaves, fbs = Fraction(0), Fraction(0), 0, 0
    with Pool(11) as pool:
        for n, (I, Z, lv, fb) in enumerate(pool.imap_unordered(work, prefixes), 1):
            Itot += I
            Ztot += Z
            leaves += lv
            fbs += fb
            if n % 8 == 0:
                print(f"  {n}/64 prefixes, {leaves:,} chambers, {fbs:,} "
                      f"fallbacks, {time.time()-t0:.0f}s", flush=True)
    print(f"\nchambers: {leaves:,} (expect 2,097,152); exact fallbacks: {fbs:,}")
    print(f"partition check: {'PASS - CERTIFIED' if Ztot == 1 else '*** FAIL: ' + str(Ztot)}")
    print(f"c_6 = {Itot}")
    print(f"c_6 = {float(Itot):.9f}   ({time.time()-t0:.0f}s)")
    with open("c6_certified.txt", "w") as f:
        f.write(f"{Itot}\n")
