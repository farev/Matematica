#!/usr/bin/env python3
"""sweep.py — D±(G) for every abelian group in an order range, via dpm.

Enumerates all abelian groups of order n (multisets of prime-power cyclic
factors), runs ./dpm on each, parses the census, and writes a CSV row per
group: order, primary factors, invariant factors, #classes, L, D±,
free-subset counts, witness, nodes, seconds, and which control applies
(cyclic formula / elementary-2 / elementary-3 lemma) with its expected value.

Elementary 2- and 3-groups of large rank can be skipped (--lemma-skip R):
for p ∈ {2,3}, ±free = linearly independent over F_p (NOTE Lemma 2), so
L = rank with no search needed; rows are still emitted, marked "lemma".

Usage: python3 sweep.py NMIN NMAX [--timeout SECS] [--lemma-skip RANK] [--out FILE]
"""
import csv
import subprocess
import sys
import time
from functools import reduce
from math import log2


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def partitions(k):
    if k == 0:
        yield ()
        return
    def gen(k, maxpart):
        if k == 0:
            yield ()
            return
        for p in range(min(k, maxpart), 0, -1):
            for rest in gen(k - p, p):
                yield (p,) + rest
    yield from gen(k, k)


def abelian_groups(n):
    """All abelian groups of order n as sorted tuples of prime-power factors."""
    f = factorize(n)
    groups = [()]
    for p, e in sorted(f.items()):
        new = []
        for lam in partitions(e):
            factors = tuple(p ** a for a in lam)
            for g in groups:
                new.append(g + factors)
        groups = new
    return [tuple(sorted(g)) for g in groups]


def invariant_factors(primary):
    """Primary decomposition -> invariant factor chain d1 | d2 | ..."""
    byp = {}
    for q in primary:
        f = factorize(q)
        (p, e), = f.items()
        byp.setdefault(p, []).append(q)
    for p in byp:
        byp[p].sort(reverse=True)
    rank = max(len(v) for v in byp.values())
    inv = []
    for i in range(rank):
        d = 1
        for p, v in byp.items():
            if i < len(v):
                d *= v[i]
        inv.append(d)
    return sorted(inv)


def control(primary, n):
    """(kind, expected DPM) if a known formula/lemma applies."""
    if len(primary) == 1:
        return "cyclic", int(log2(n)) + 1
    ps = {tuple(factorize(q)) for q in primary}
    if all(q == 2 for q in primary):
        return "elem2", len(primary) + 1
    if all(q == 3 for q in primary):
        return "elem3", len(primary) + 1
    return "", None


def run_group(primary, timeout):
    cmd = ["./dpm"] + [str(q) for q in primary]
    t0 = time.time()
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    res = {"secs": time.time() - t0, "counts": {}}
    for line in out.stdout.splitlines():
        w = line.split()
        if not w:
            continue
        if w[0] == "CLASSES" or (w[0] == "N" and "CLASSES" in w):
            res["classes"] = int(w[w.index("CLASSES") + 1])
        elif w[0] == "FREE":
            res["counts"][int(w[1])] = int(w[2])
        elif w[0] == "L":
            res["L"] = int(w[1])
        elif w[0] == "DPM":
            res["DPM"] = int(w[1])
        elif w[0] == "WITNESS":
            res["witness"] = " ".join(w[1:])
        elif w[0] == "NODES":
            res["nodes"] = int(w[1])
    return res


def main():
    nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
    timeout = 900
    lemma_skip = 7
    out_path = f"table_{nmin}_{nmax}.csv"
    args = sys.argv[3:]
    if "--timeout" in args:
        timeout = int(args[args.index("--timeout") + 1])
    if "--lemma-skip" in args:
        lemma_skip = int(args[args.index("--lemma-skip") + 1])
    if "--out" in args:
        out_path = args[args.index("--out") + 1]

    with open(out_path, "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["order", "primary", "invariant", "classes", "L", "DPM",
                     "control", "expected_DPM", "match", "counts", "witness",
                     "nodes", "secs", "note"])
        for n in range(nmin, nmax + 1):
            for primary in abelian_groups(n):
                inv = invariant_factors(primary)
                kind, exp = control(primary, n)
                label = "+".join(map(str, primary))
                if kind in ("elem2", "elem3") and len(primary) >= lemma_skip:
                    wr.writerow([n, label, "+".join(map(str, inv)), "", len(primary),
                                 len(primary) + 1, kind, exp, "lemma", "", "", "", "",
                                 "value by NOTE Lemma 2 (linear independence), search skipped"])
                    fh.flush()
                    continue
                res = run_group(primary, timeout)
                if res is None:
                    wr.writerow([n, label, "+".join(map(str, inv)), "", "", "",
                                 kind, exp, "TIMEOUT", "", "", "", timeout, "timed out"])
                    fh.flush()
                    print(f"TIMEOUT {n} {label}", flush=True)
                    continue
                match = ""
                if exp is not None:
                    match = "OK" if res["DPM"] == exp else "MISMATCH"
                    if match == "MISMATCH":
                        print(f"MISMATCH {n} {label}: got {res['DPM']} expected {exp}",
                              flush=True)
                counts = ";".join(f"{k}:{v}" for k, v in sorted(res["counts"].items()))
                wr.writerow([n, label, "+".join(map(str, inv)), res.get("classes"),
                             res["L"], res["DPM"], kind, exp, match, counts,
                             res.get("witness", ""), res.get("nodes"),
                             f"{res['secs']:.2f}", ""])
                fh.flush()
                print(f"done {n} {label}: L={res['L']} DPM={res['DPM']} "
                      f"({res['secs']:.2f}s)", flush=True)


if __name__ == "__main__":
    main()
