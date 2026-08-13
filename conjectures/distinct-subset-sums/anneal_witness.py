#!/usr/bin/env python3
"""anneal_witness.py — heuristic search for a 10-element DSS set with largest
element BELOW the Conway-Guy value 309 (which would refute Conway-Guy
optimality at n = 10 and pin f(10) < 309).

Pure NUMERICAL evidence: a hit would be validated exactly (validate_set.py)
and would be a theorem-grade witness; a miss proves nothing.

Method: simulated annealing over 10-subsets of [1, cap]. Energy = number of
duplicated subset sums (0 <=> DSS), computed exactly via Python bigint
bitsets by cardinality-free collision counting: for the incremental bitset
union we count |S & (S << a)| overlaps aggregated over a full rebuild.
Moves: replace one element by a uniform random non-member of [1, cap].
Restarts with recorded seeds. Also usable as a sanity probe at cap = 309,
where it should quickly rediscover a valid set (the Conway-Guy one or a
rearrangement), serving as a positive control of the energy function.

Usage: python3 anneal_witness.py [cap] [restarts] [iters] [seed0]
"""
import random
import sys
import time


def energy(s):
    """number of pairwise subset-sum collisions introduced, exactly"""
    e = 0
    sums = 1
    for a in sorted(s):
        sh = sums << a
        e += bin(sums & sh).count("1")
        sums |= sh
    return e


def anneal(cap, iters, rng):
    s = rng.sample(range(1, cap + 1), 10)
    e = energy(s)
    t0, t1 = 3.0, 0.02
    best = (e, sorted(s))
    for it in range(iters):
        if e == 0:
            return 0, sorted(s), it
        T = t0 * (t1 / t0) ** (it / iters)
        i = rng.randrange(10)
        old = s[i]
        if rng.random() < 0.7:
            # local move: DSS-ness is about exact integer relations, so
            # small shifts explore the neighborhood far better than resampling
            new = old + rng.choice((-3, -2, -1, 1, 2, 3))
            if not (1 <= new <= cap) or new in s:
                continue
        else:
            new = rng.randrange(1, cap + 1)
            while new in s:
                new = rng.randrange(1, cap + 1)
        s[i] = new
        e2 = energy(s)
        if e2 <= e or rng.random() < pow(2.718281828, (e - e2) / T):
            e = e2
            if e < best[0]:
                best = (e, sorted(s))
        else:
            s[i] = old
    return best[0], best[1], iters


def main():
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 308
    restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
    seed0 = int(sys.argv[4]) if len(sys.argv) > 4 else 20260813
    t0 = time.time()
    best_overall = None
    for r in range(restarts):
        seed = seed0 + r
        rng = random.Random(seed)
        e, s, it = anneal(cap, iters, rng)
        if best_overall is None or e < best_overall[0]:
            best_overall = (e, s, seed, it)
            print(f"[restart {r} seed {seed}] energy={e} set={s}"
                  + (" *** DSS WITNESS ***" if e == 0 else ""), flush=True)
        if e == 0:
            print(f"WITNESS max={max(s)} set={s} seed={seed} iter={it}")
            print("validate with: python3 validate_set.py "
                  + ",".join(map(str, s)))
            return
    e, s, seed, it = best_overall
    print(f"NO WITNESS at cap={cap} after {restarts} restarts x {iters} iters "
          f"({time.time()-t0:.0f}s); best energy={e} (seed {seed}) set={s}")


if __name__ == "__main__":
    main()
