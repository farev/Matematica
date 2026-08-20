"""make_tables.py — assemble and AUDIT the family tables from raw run logs.

Reads the committed run outputs in data/ (family_le200.txt, gap_probes.txt,
c3_n29.txt, c3_n30.txt, c3_n31.txt, plus the three certificate files),
re-verifies EVERY witness against the definition via
dis_reference.check_dissociated, recomputes the counting and split bounds,
and writes data/families.csv with one audited row per group:

  family, n, group, order, dis, Dpm, counting_bound, attains, source_line

Any witness that fails re-verification, or any dis outside
[split bound, counting bound], aborts loudly. Exit 0 = everything audited.
"""
import csv
import math
import os
import re
import sys

from dis_reference import check_dissociated


def parse_group(gstr):
    return [int(x) for x in gstr.split("x")]


def parse_witness(wstr, rank):
    if rank == 1:
        return [(int(x),) for x in wstr.split(",")]
    return [tuple(int(y) for y in t.split(","))
            for t in wstr.strip("()").split("),(")]


LINE = re.compile(r"group=(\S+) N=(\d+) (?:dis=(\d+) Dpm=\d+|T=(\d+) (?:exists=(YES|NO)|count=(\d+)|dissociated_T_subsets=(\d+)))"
                  r" nodes=(\d+)")


def floor_log2(n):
    return n.bit_length() - 1


def main():
    rows = {}      # (tuple mods) -> dict
    witnesses = {} # (tuple mods) -> (size, witness, srcfile)
    nonexist = {}  # (tuple mods) -> T shown absent

    for fname in sorted(os.listdir("data")):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join("data", fname)
        with open(path) as f:
            lines = f.readlines()
        for i, ln in enumerate(lines):
            m = LINE.search(ln)
            if not m:
                continue
            mods = tuple(parse_group(m.group(1)))
            N = int(m.group(2))
            if m.group(3):          # max mode: dis=
                dis = int(m.group(3))
                rows.setdefault(mods, {})["dis"] = dis
                rows[mods]["N"] = N
                rows[mods]["src"] = fname
                wm = re.search(r"witness=(\S+)", ln)
                if wm:
                    witnesses[mods] = (dis, wm.group(1), fname)
            elif m.group(5) == "YES":
                T = int(m.group(4))
                rows.setdefault(mods, {}).setdefault("ge", 0)
                rows[mods]["ge"] = max(rows[mods]["ge"], T)
                rows[mods]["N"] = N
                rows[mods].setdefault("src", fname)
                # witness printed on the following line
                if i + 1 < len(lines) and lines[i+1].startswith("witness="):
                    witnesses[mods] = (T, lines[i+1].strip().split("=", 1)[1], fname)
            elif m.group(5) == "NO":
                T = int(m.group(4))
                nonexist[mods] = min(nonexist.get(mods, 99), T)
                rows.setdefault(mods, {})["N"] = N
                rows[mods].setdefault("src", fname)
            elif m.group(6) is not None and int(m.group(6)) == 0:
                T = int(m.group(4))
                nonexist[mods] = min(nonexist.get(mods, 99), T)
            elif m.group(7) is not None and int(m.group(7)) == 0:
                T = int(m.group(4))
                nonexist[mods] = min(nonexist.get(mods, 99), T)

    bad = 0
    audited = []
    for mods, r in sorted(rows.items(), key=lambda kv: (len(kv[0]), kv[0])):
        N = r["N"]
        ub = floor_log2(N)
        split = sum(floor_log2(m) for m in mods)
        dis = r.get("dis")
        if dis is None:
            ge = r.get("ge")
            ne = nonexist.get(mods)
            if ge is not None and ge == ub:
                dis = ge                       # attained the counting bound
            elif ne is not None and ne == ub and ge is None:
                # exhausted at the counting bound; dis = ub - 1 only if a
                # witness of size ub-1 exists via split bound equality
                if split == ub - 1:
                    dis = ub - 1
                else:
                    print(f"UNRESOLVED {mods}: no {ne}-set, split={split}", file=sys.stderr)
                    continue
            else:
                continue
        # audit 1: bounds
        if not (split <= dis <= ub):
            print(f"AUDIT FAIL {mods}: dis={dis} outside [{split},{ub}]", file=sys.stderr)
            bad += 1
        # audit 2: witness re-verification from the definition
        if mods in witnesses:
            size, wstr, src = witnesses[mods]
            W = parse_witness(wstr, len(mods))
            if len(W) != size or not check_dissociated(list(mods), W):
                print(f"AUDIT FAIL {mods}: witness in {src} bad", file=sys.stderr)
                bad += 1
            wit_ok = size
        else:
            wit_ok = ""
        # audit 3: exhaustion consistency
        if mods in nonexist and nonexist[mods] <= dis:
            print(f"AUDIT FAIL {mods}: nonexistence at {nonexist[mods]} <= dis {dis}", file=sys.stderr)
            bad += 1
        audited.append({
            "group": "x".join(map(str, mods)), "order": N, "dis": dis,
            "Dpm": dis + 1, "counting_bound": ub,
            "attains": "yes" if dis == ub else "NO",
            "witness_checked_size": wit_ok,
            "nonexistence_at": nonexist.get(mods, ""),
            "source": r.get("src", ""),
        })

    with open("data/families.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(audited[0].keys()))
        w.writeheader()
        w.writerows(audited)
    print(f"audited {len(audited)} groups, witness-checked {sum(1 for a in audited if a['witness_checked_size'] != '')}, failures {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
