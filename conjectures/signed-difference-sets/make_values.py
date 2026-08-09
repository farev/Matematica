#!/usr/bin/env python3
"""Aggregate data/results.csv (append-only run log) into data/values.csv,
the authoritative table of decisions of previously-Open cells. Aborts on
any conflicting decision for the same cell. Annotates each row with
whether a §2 criterion independently proves the nonexistence."""

import csv
import sys

import sdslib
from theory import test_cell


def main():
    runs = {}
    with open("data/results.csv") as f:
        for row in csv.DictReader(f):
            if row["decision"] not in ("EXIST", "NONEXIST"):
                continue
            nm = row["name"]
            if nm in runs and runs[nm]["decision"] != row["decision"]:
                print(f"CONFLICT for {nm}: {runs[nm]['decision']} vs "
                      f"{row['decision']}")
                sys.exit(1)
            runs[nm] = row

    out = []
    for nm, row in sorted(runs.items()):
        if row["db_status"] != "Open":
            continue
        v, k, lam, G = sdslib.parse_name(nm)
        verdict, reason = test_cell(v, k, lam, G)
        agrees = ""
        if verdict == "NO":
            agrees = reason if row["decision"] == "NONEXIST" else "CONFLICT"
            if agrees == "CONFLICT":
                print(f"CONFLICT: criterion kills {nm} but exhaust EXIST")
                sys.exit(1)
        out.append([nm, row["decision"],
                    "exhaust+criterion" if agrees else "exhaust",
                    row["witnesses"], row["verified"], row["wall_s"],
                    agrees])
    with open("data/values.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "decision", "method", "witnesses_found",
                    "witnesses_verified", "wall_s", "criterion_note"])
        w.writerows(out)
    ne = sum(1 for r in out if r[1] == "NONEXIST")
    ex = sum(1 for r in out if r[1] == "EXIST")
    print(f"values.csv: {len(out)} previously-Open cells decided "
          f"({ex} EXIST, {ne} NONEXIST)")


if __name__ == "__main__":
    main()
