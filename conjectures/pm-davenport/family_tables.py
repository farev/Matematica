#!/usr/bin/env python3
"""Read sweep.csv (+ optional heavies transcripts) and print the family
tables for NOTE.md: C_3+C_3n, C_5+C_5n, C_7+C_7n, homocyclic C_p^2,
with bracket data (concat lower bound, log2 upper bound), the decided
value, and attainment. Pure reporting; no new computation.

Usage: python3 family_tables.py [sweep.csv]
"""

import csv
import re
import sys


def flog2(n):
    return n.bit_length() - 1


def load_sweep(path):
    vals = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            key = tuple(int(x) for x in row["invariant_factors"].split("x"))
            vals[key] = int(row["mu"])
    return vals


def load_heavies(paths):
    vals = {}
    pat_g = re.compile(r"G =((?: Z_\d+)+)\s+\|G\| = (\d+)")
    pat_d = re.compile(r"d_pm = (\d+)")
    for p in paths:
        try:
            txt = open(p).read()
        except OSError:
            continue
        blocks = txt.split("G =")
        for b in blocks[1:]:
            b = "G =" + b
            mg = pat_g.search(b)
            md = pat_d.search(b)
            if mg and md:
                orders = tuple(int(x) for x in re.findall(r"Z_(\d+)", mg.group(1)))
                vals[tuple(sorted(orders))] = int(md.group(1))
    return vals


def main():
    sweep_path = sys.argv[1] if len(sys.argv) > 1 else "sweep.csv"
    vals = load_sweep(sweep_path)
    vals.update(load_heavies(["heavies.txt", "heavies2.txt", "heavies3.txt"]))

    for m, nmax in [(3, 33), (5, 13), (7, 8)]:
        print(f"\n## family C_{m} + C_{m}n")
        print("| n | group | N | concat | log2 bound | mu | verdict |")
        print("|---|---|---|---|---|---|---|")
        for n in range(1, nmax + 1):
            key = tuple(sorted((m, m * n)))
            N = m * m * n
            t = flog2(N)
            concat = flog2(m) + flog2(m * n)
            mu = vals.get(key)
            if mu is None:
                verdict = "PENDING"
                mus = "?"
            else:
                mus = str(mu)
                verdict = ("attained" if mu == t else
                           f"DEFICIENT by {t - mu}")
                if concat == t:
                    verdict += " (forced)"
            print(f"| {n} | C_{m}+C_{m*n} | {N} | {concat} | {t} | {mus} |"
                  f" {verdict} |")

    print("\n## homocyclic C_p^2")
    print("| p | N | concat | log2 bound | mu | verdict |")
    print("|---|---|---|---|---|---|")
    for p in [2, 3, 5, 7, 11, 13]:
        key = (p, p)
        N = p * p
        t = flog2(N)
        concat = 2 * flog2(p)
        mu = vals.get(key)
        mus = "?" if mu is None else str(mu)
        verdict = ("PENDING" if mu is None else
                   "attained" if mu == t else f"DEFICIENT by {t - mu}")
        if concat == t and mu is not None:
            verdict += " (forced)"
        print(f"| {p} | {N} | {concat} | {t} | {mus} | {verdict} |")


if __name__ == "__main__":
    main()
