#!/usr/bin/env python3
"""Aggregate certified results from lane logs into data/new_values.csv and a
markdown table. Sources of truth:
  - data/lane_a*.log lines:  "(4, 4, 8) S=87 CONFIRMED unsat=..s sat=..s proof=..B rup=VERIFIED wit=OK"
  - data/lane_b*.log lines:  "(3, 6, 7) S = 107 CERTIFIED (drup VERIFIED at 107, witness OK at 106)"
Cross-checks against data/published_values.csv: a value that matches a
published triple is a CONTROL (must equal the published value or we abort);
an unpublished triple is NEW. Conjecture 2.1 status is derived for s>=4.
"""
import csv, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def published():
    pub = {}
    with open(os.path.join(HERE, "data", "published_values.csv")) as f:
        for row in csv.DictReader(l for l in f if not l.startswith("#")):
            if row["k"] == "3":
                pub[(int(row["t0"]), int(row["t1"]), int(row["t2"]))] = int(row["value"])
    return pub


def scan_logs():
    got = {}  # (s,t,u) -> (S, how)
    pat_a = re.compile(r"\((\d+), (\d+), (\d+)\) S=(\d+) CONFIRMED")
    pat_b = re.compile(r"\((\d+), (\d+), (\d+)\) S = (\d+) CERTIFIED")
    for path in sorted(glob.glob(os.path.join(HERE, "data", "lane_*.log"))):
        for line in open(path):
            m = pat_a.search(line) or pat_b.search(line)
            if m:
                ts = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
                S = int(m.group(4))
                if ts in got and got[ts][0] != S:
                    sys.exit(f"CONFLICT: {ts} recorded as {got[ts][0]} and {S}")
                got[ts] = (S, os.path.basename(path))
    return got


def main():
    pub = published()
    got = scan_logs()
    rows = []
    for ts in sorted(got, key=lambda x: (x[0], x[1], x[2])):
        S, src = got[ts]
        s, t, u = ts
        conj = s * t * u - t * u - u - 1
        if ts in pub:
            status = "CONTROL"
            if pub[ts] != S:
                sys.exit(f"CONTROL MISMATCH at {ts}: computed {S}, published {pub[ts]}")
        else:
            status = "NEW"
        c21 = ""
        if s >= 4:
            c21 = "confirms Conj 2.1" if S == conj else f"REFUTES Conj 2.1 (predicted {conj})"
        rows.append(dict(s=s, t=t, u=u, S=S, conjectured=conj, status=status,
                         conj21=c21, source=src))
    out = os.path.join(HERE, "data", "new_values.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["s", "t", "u", "S", "conjectured",
                                          "status", "conj21", "source"])
        w.writeheader()
        w.writerows(rows)
    new = [r for r in rows if r["status"] == "NEW"]
    ctrl = [r for r in rows if r["status"] == "CONTROL"]
    print(f"{len(ctrl)} controls (all match published), {len(new)} NEW values:")
    for r in new:
        extra = f"  [{r['conj21']}]" if r["conj21"] else ""
        print(f"  S(3;{r['s']},{r['t']},{r['u']}) = {r['S']}{extra}")
    print(f"-> {out}")


if __name__ == "__main__":
    main()
