#!/usr/bin/env python3
"""Law-hunting on the S(3;3,t,u) table: difference structure and exact-fit
tests against candidate closed forms. Purely arithmetic — no fitting in the
statistical sense; a candidate either matches a row segment exactly or it
does not. Reads published + session values; prints per-t rows, first
differences, and which candidates match which segments.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))


def table():
    vals = {}
    with open(os.path.join(HERE, "data", "published_values.csv")) as f:
        for row in csv.DictReader(l for l in f if not l.startswith("#")):
            if row["k"] == "3" and row["t0"] == "3":
                vals[(int(row["t1"]), int(row["t2"]))] = int(row["value"])
    p = os.path.join(HERE, "data", "new_values.csv")
    if os.path.exists(p):
        with open(p) as f:
            for row in csv.DictReader(f):
                if row["s"] == "3":
                    vals[(int(row["t"]), int(row["u"]))] = int(row["S"])
    return vals


CANDIDATES = {
    "sandwich 2tu-u-1": lambda t, u: 2 * t * u - u - 1,
    "u*S2(3,t)-1 alt":  lambda t, u: u * (3 * t - 4 if t % 2 else 3 * t - 5) - 1,
    "9u-13 (t=3)":      lambda t, u: 9 * u - 13 if t == 3 else None,
    "8u-7 (t=3)":       lambda t, u: 8 * u - 7 if t == 3 else None,
    "7u (t=3)":         lambda t, u: 7 * u if t == 3 else None,
    "12u-2t^2+... n/a": lambda t, u: None,
    "(2t+1)u-c guess":  lambda t, u: (2 * t + 1) * u - (t * t - t + 1),
    "3tu-tu-u+? = 2tu-u+3": lambda t, u: 2 * t * u - u + 3,
}


def main():
    vals = table()
    ts = sorted(set(t for t, _ in vals))
    for t in ts:
        us = sorted(u for tt, u in vals if tt == t)
        row = [vals[(t, u)] for u in us]
        diffs = [b - a for a, b in zip(row, row[1:])]
        print(f"t={t}: u={us}")
        print(f"   S     = {row}")
        print(f"   diffs = {diffs}")
        for name, f in CANDIDATES.items():
            try:
                pred = [f(t, u) for u in us]
            except Exception:
                continue
            if any(p is None for p in pred):
                continue
            match = [u for u, p, v in zip(us, pred, row) if p == v]
            if len(match) >= 2:
                print(f"   {name}: exact at u∈{match}")
        print()


if __name__ == "__main__":
    main()
