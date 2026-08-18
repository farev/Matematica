#!/usr/bin/env python3
"""Local search for good partitions of [1, n] for (s, t) -- lower-bound leg.

Cost of a coloring = (# s-APs monochromatic in color 0)
                   + (# t-APs monochromatic in color 1).
A zero-cost coloring is a good partition, i.e. a witness for w(2;s,t) > n.

Search: multi-restart tabu walk over single-bit flips with incremental
cost updates. Seeds: random balanced strings, plus (optionally) a witness
for a smaller n extended by random suffix bits -- extension of a good
partition tends to be much closer to feasible than a random string.

Every witness found is re-verified by vdw_cnf.coloring_is_good (independent
enumeration) before being written to data/.

Usage:
  python3 witness_search.py s t n [seconds] [seedfile]
Prints best cost achieved; writes witness and exits 0 the moment cost 0 is
verified. Exit 3 if the time budget ends with cost > 0.
"""
import os
import random
import sys
import time

from vdw_cnf import aps, coloring_is_good

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def build_index(n, s, t):
    """For each position, the list of (ap_id) it belongs to; AP tables."""
    s_aps = aps(n, s)
    t_aps = aps(n, t)
    pos2s = [[] for _ in range(n + 1)]
    pos2t = [[] for _ in range(n + 1)]
    for j, ap in enumerate(s_aps):
        for p in ap:
            pos2s[p].append(j)
    for j, ap in enumerate(t_aps):
        for p in ap:
            pos2t[p].append(j)
    return s_aps, t_aps, pos2s, pos2t


def search(n, s, t, budget_s, seed_coloring=None, rng=None, report=None):
    rng = rng or random.Random()
    s_aps, t_aps, pos2s, pos2t = build_index(n, s, t)
    slen, tlen = s, t
    t_end = time.time() + budget_s
    best_overall = None
    best_cost_overall = 10 ** 9
    restarts = 0
    while time.time() < t_end:
        restarts += 1
        col = [0] * (n + 1)
        if seed_coloring and restarts % 2 == 1:
            m = len(seed_coloring) - 1
            for i in range(1, min(m, n) + 1):
                col[i] = seed_coloring[i]
            for i in range(m + 1, n + 1):
                col[i] = rng.randint(0, 1)
        else:
            for i in range(1, n + 1):
                col[i] = rng.randint(0, 1)
        # zero-count[j] for s_aps = number of positions colored 0; an s-AP is
        # violated iff its zero-count == s. Similarly ones for t-APs.
        zc = [0] * len(s_aps)
        oc = [0] * len(t_aps)
        for j, ap in enumerate(s_aps):
            zc[j] = sum(1 for p in ap if col[p] == 0)
        for j, ap in enumerate(t_aps):
            oc[j] = sum(1 for p in ap if col[p] == 1)
        cost = sum(1 for j in range(len(s_aps)) if zc[j] == slen) + \
               sum(1 for j in range(len(t_aps)) if oc[j] == tlen)
        tabu = [0] * (n + 1)
        it = 0
        last_improve = 0
        best_cost = cost
        while cost > 0 and time.time() < t_end:
            it += 1
            # WalkSAT-style: focus on positions inside violated APs, with an
            # exploratory random sample mixed in
            viol_pos = set()
            for j in range(len(s_aps)):
                if zc[j] == slen:
                    viol_pos.update(s_aps[j])
            for j in range(len(t_aps)):
                if oc[j] == tlen:
                    viol_pos.update(t_aps[j])
            sample = list(viol_pos)
            if rng.random() < 0.25 or not sample:
                sample += rng.sample(range(1, n + 1), min(24, n))
            cand_best, cand_delta = None, 10 ** 9
            for p in sample:
                if tabu[p] > it and cost + 1 > best_cost:
                    continue
                d = 0
                if col[p] == 0:  # flip 0 -> 1
                    for j in pos2s[p]:
                        if zc[j] == slen:
                            d -= 1
                    for j in pos2t[p]:
                        if oc[j] == tlen - 1:
                            d += 1
                else:            # flip 1 -> 0
                    for j in pos2t[p]:
                        if oc[j] == tlen:
                            d -= 1
                    for j in pos2s[p]:
                        if zc[j] == slen - 1:
                            d += 1
                if d < cand_delta:
                    cand_delta, cand_best = d, p
            if cand_best is None:
                break
            p = cand_best
            if col[p] == 0:
                for j in pos2s[p]:
                    zc[j] -= 1
                for j in pos2t[p]:
                    oc[j] += 1
                col[p] = 1
            else:
                for j in pos2t[p]:
                    oc[j] -= 1
                for j in pos2s[p]:
                    zc[j] += 1
                col[p] = 0
            cost += cand_delta
            tabu[p] = it + rng.randint(6, 24)
            if cost < best_cost:
                best_cost, last_improve = cost, it
            if it - last_improve > 4000:   # stagnation -> restart
                break
        if best_cost < best_cost_overall:
            best_cost_overall = best_cost
            if report:
                report(best_cost_overall, restarts)
        if cost == 0:
            if not coloring_is_good(col, s, t):
                raise RuntimeError("zero-cost coloring FAILED independent check")
            return col, 0, restarts
    return best_overall, best_cost_overall, restarts


def main():
    s, t, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    budget = float(sys.argv[4]) if len(sys.argv) > 4 else 300.0
    seed = None
    if len(sys.argv) > 5:
        with open(sys.argv[5]) as f:
            bits = [l for l in f if not l.startswith("#")][0].strip()
        seed = [0] + [int(c) for c in bits]
        print(f"seeded with witness of length {len(bits)}")
    rng = random.Random(20260816)
    rep = lambda c, r: print(f"  best cost {c} (restart {r}, "
                             f"{time.time()-t0:.0f}s)", flush=True)
    t0 = time.time()
    col, cost, restarts = search(n, s, t, budget, seed, rng, rep)
    if cost == 0:
        os.makedirs(DATA, exist_ok=True)
        path = os.path.join(DATA, f"witness_{s}_{t}_n{n}_tabu.txt")
        with open(path, "w") as f:
            f.write(f"# good partition of [1,{n}] for ({s},{t}) -- tabu search, "
                    f"verified by coloring_is_good\n")
            f.write("".join(str(col[i]) for i in range(1, n + 1)) + "\n")
        print(f"WITNESS at n={n} after {restarts} restarts, "
              f"{time.time()-t0:.0f}s -> {path}")
        sys.exit(0)
    print(f"no witness at n={n}; best cost {cost} after {restarts} restarts, "
          f"{time.time()-t0:.0f}s")
    sys.exit(3)


if __name__ == "__main__":
    main()
