#!/usr/bin/env python3
"""Periodic-ansatz witness search for good partitions of [1,n], (s,t).

Rationale (observed in this session's own witnesses, consistent with the
literature's description of vdW certificates): boundary good partitions are
(near-)periodic — witness_4_5_n54 is exactly 22-periodic, witness_5_5_n177
is 44-periodic with 3.8% defects. So search over period-p blocks
(2^p space instead of 2^n), then hand near-misses to the free-bit tabu
(witness_search.py) for defect repair.

Move engine: full one-flip neighborhood of the block, cost evaluated on the
whole [1,n] string with numpy fancy indexing (AP tables precomputed once).
Every zero-cost witness is re-verified by vdw_cnf.coloring_is_good before
being written.

Usage:
  python3 periodic_search.py s t n p1[,p2,...] [seconds] [outtag]
"""
import os
import sys
import time
import random

import numpy as np

from vdw_cnf import aps, coloring_is_good

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def ap_arrays(n, k):
    """Numpy array (num_aps, k) of 0-based positions."""
    a = np.array(aps(n, k), dtype=np.int32) - 1
    return a


def make_cost(n, s, t):
    S = ap_arrays(n, s)
    T = ap_arrays(n, t)

    def cost(bits01):     # bits01: np.array shape (n,), values 0/1
        cs = int(np.sum(np.all(bits01[S] == 0, axis=1)))
        ct = int(np.sum(np.all(bits01[T] == 1, axis=1)))
        return cs + ct
    return cost


def block_to_string(block, n):
    p = len(block)
    reps = (n + p - 1) // p
    return np.tile(block, reps)[:n]


def residue_seed_blocks(p, rng, count=6):
    """Rabung-flavored seeds for prime-ish p: color by index classes."""
    out = []
    for _ in range(count):
        # random threshold split of multiplicative order classes when p prime,
        # else random balanced-ish block
        blk = (np.array([rng.random() for _ in range(p)]) <
               rng.uniform(0.45, 0.7)).astype(np.int8)
        out.append(blk)
    return out


def search_period(n, s, t, p, budget_s, rng, cost, verbose=True):
    best_block, best_cost = None, 10 ** 9
    t_end = time.time() + budget_s
    while time.time() < t_end:
        blk = np.array([1 if rng.random() < rng.uniform(0.5, 0.68) else 0
                        for _ in range(p)], dtype=np.int8)
        cur = cost(block_to_string(blk, n))
        stall = 0
        while stall < 3 and time.time() < t_end:
            # full one-flip neighborhood
            improved = False
            order = list(range(p))
            rng.shuffle(order)
            for i in order:
                blk[i] ^= 1
                c = cost(block_to_string(blk, n))
                if c < cur:
                    cur = c
                    improved = True
                else:
                    blk[i] ^= 1
            if cur == 0:
                return blk.copy(), 0
            if not improved:
                # random 2-flip kick
                i, j = rng.randrange(p), rng.randrange(p)
                blk[i] ^= 1
                blk[j] ^= 1
                cur = cost(block_to_string(blk, n))
                stall += 1
        if cur < best_cost:
            best_cost, best_block = cur, blk.copy()
            if verbose:
                print(f"    p={p}: best cost {best_cost}", flush=True)
    return best_block, best_cost


def main():
    s, t, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    periods = [int(x) for x in sys.argv[4].split(",")]
    budget = float(sys.argv[5]) if len(sys.argv) > 5 else 600.0
    tag = sys.argv[6] if len(sys.argv) > 6 else "per"
    rng = random.Random(20260816)
    cost = make_cost(n, s, t)
    per_budget = budget / len(periods)
    overall = (None, 10 ** 9, None)
    for p in periods:
        blk, c = search_period(n, s, t, p, per_budget, rng, cost)
        print(f"  period {p}: cost {c}", flush=True)
        if c < overall[1]:
            overall = (blk, c, p)
    blk, c, p = overall
    bits = block_to_string(blk, n)
    if c == 0:
        col = [0] + [int(x) for x in bits]
        if not coloring_is_good(col, s, t):
            raise RuntimeError("periodic witness FAILED independent check")
        os.makedirs(DATA, exist_ok=True)
        path = os.path.join(DATA, f"witness_{s}_{t}_n{n}_{tag}p{p}.txt")
        with open(path, "w") as f:
            f.write(f"# good partition of [1,{n}] for ({s},{t}); "
                    f"exactly {p}-periodic block, verified\n")
            f.write("".join(map(str, bits)) + "\n")
        print(f"WITNESS n={n} period {p} -> {path}")
        sys.exit(0)
    # save best near-miss as seed for the free tabu
    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, f"seed_{s}_{t}_n{n}_{tag}p{p}_cost{c}.txt")
    with open(path, "w") as f:
        f.write(f"# NEAR-MISS cost {c}, {p}-periodic, for repair seeding\n")
        f.write("".join(map(str, bits)) + "\n")
    print(f"best: cost {c} at period {p} (seed saved {path})")
    sys.exit(3)


if __name__ == "__main__":
    main()
