"""Sweep d_pm / D_pm over all abelian group types in an order range.

For each group: elementary bounds (lower = sum floor(log2) over invariant
factors, upper = floor(log2 |G|), both proved in NOTE.md). If the bounds meet,
the value is PROVED ("forced"); the search then only confirms (node-capped,
optional). If they do not meet ("gap"), the exhaustive search decides the
value; a gap cell whose search hits the cap is a loud failure, never a value.

Usage: python3 run_table.py LO HI OUTPREFIX [--cap N] [--jobs J]
Writes data/OUTPREFIX.csv and data/OUTPREFIX_certs.json.
"""

import csv
import json
import sys
import time
from multiprocessing import Pool

from dpm_core import AbelianGroup, search_dpm, verify_pm_zsf


def partitions(n):
    if n == 0:
        yield ()
        return
    for first in range(n, 0, -1):
        for rest in partitions(n - first):
            if not rest or rest[0] <= first:
                yield (first,) + rest


def factorize(n):
    out = []
    d = 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e:
            out.append((d, e))
        d += 1
    if n > 1:
        out.append((n, 1))
    return out


def abelian_types(order):
    """All abelian groups of this order, as primary-decomposition moduli lists."""
    fac = factorize(order)
    types = [[]]
    for p, e in fac:
        new = []
        for part in partitions(e):
            comp = [p ** a for a in part]
            for t in types:
                new.append(t + comp)
        types = new
    return [sorted(t, reverse=True) for t in types]


def work(task):
    moduli, cap_forced, cap_gap = task
    t0 = time.time()
    G = AbelianGroup(moduli)
    lo, up = G.lower_d(), G.upper_d()
    forced = lo == up
    cap = cap_forced if forced else cap_gap
    r = search_dpm(G, node_cap=cap)
    dt = time.time() - t0
    if forced:
        dpm = lo
        if r["exhaustive"]:
            status = "forced+confirmed"
            assert r["dpm"] == lo, (moduli, r["dpm"], lo, "SEARCH CONTRADICTS PROVED BOUNDS")
        else:
            status = "forced (search capped)"
            assert r["dpm"] <= lo, (moduli, r["dpm"], lo, "SEARCH EXCEEDS PROVED UPPER BOUND")
    elif not r["exhaustive"]:
        dpm = None
        status = "gap:UNDECIDED (node cap; needs dpm_fast)"
    else:
        dpm = r["dpm"]
        status = "gap:search-decided"
    wit = r["witness"] if r["witness"] else None
    if wit:
        ok, bad = verify_pm_zsf(G.moduli, wit)
        assert ok, (moduli, wit, bad)
    return {
        "order": G.N, "moduli": list(G.moduli), "invfacs": G.invfacs,
        "lower_d": lo, "upper_d": up, "dpm": dpm,
        "Dpm": (dpm + 1) if dpm is not None else None,
        "status": status, "search_dpm": r["dpm"], "nodes": r["nodes"],
        "exhaustive": r["exhaustive"], "seconds": round(dt, 3),
        "witness": wit,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    lo_ord, hi_ord, prefix = int(args[0]), int(args[1]), args[2]
    cap = 20_000_000
    cap_gap = None
    jobs = 4
    for a in sys.argv[1:]:
        if a.startswith("--cap="):
            cap = int(a.split("=")[1])
        if a.startswith("--gap-cap="):
            cap_gap = int(a.split("=")[1])
        if a.startswith("--jobs="):
            jobs = int(a.split("=")[1])
    tasks = []
    for order in range(lo_ord, hi_ord + 1):
        for t in abelian_types(order):
            tasks.append((t, cap, cap_gap))
    # big groups first for better load balance
    tasks.sort(key=lambda t: -__import__("math").prod(t[0]))
    print(f"{len(tasks)} group types, orders {lo_ord}..{hi_ord}", flush=True)
    rows = []
    with Pool(jobs) as pool:
        for i, rec in enumerate(pool.imap_unordered(work, tasks)):
            rows.append(rec)
            tag = f"{rec['moduli']} d={rec['dpm']} [{rec['status']}] nodes={rec['nodes']} {rec['seconds']}s"
            print(f"({i+1}/{len(tasks)}) {tag}", flush=True)
    rows.sort(key=lambda r: (r["order"], r["moduli"]))
    with open(f"data/{prefix}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["order", "moduli", "invariant_factors", "lower_d", "upper_d",
                    "dpm", "Dpm", "status", "nodes", "seconds", "witness"])
        for r in rows:
            w.writerow([r["order"], " ".join(map(str, r["moduli"])),
                        " ".join(map(str, r["invfacs"])), r["lower_d"], r["upper_d"],
                        r["dpm"], r["Dpm"], r["status"], r["nodes"], r["seconds"],
                        json.dumps(r["witness"])])
    rows_undec = [r for r in rows if r["dpm"] is None]
    if rows_undec:
        print(f"\nUNDECIDED gap cells (finish with dpm_fast): "
              f"{[r['moduli'] for r in rows_undec]}")
    with open(f"data/{prefix}_certs.json", "w") as f:
        json.dump(rows, f, indent=0)
    gaps = [r for r in rows if r["status"] == "gap:search-decided"]
    print(f"\n{len(rows)} groups; {len(gaps)} gap cells decided by search:")
    for r in gaps:
        print(f"  {r['moduli']}: d in [{r['lower_d']},{r['upper_d']}] -> {r['dpm']} "
              f"(D_pm = {r['Dpm']}), {r['nodes']} nodes")


if __name__ == "__main__":
    main()
