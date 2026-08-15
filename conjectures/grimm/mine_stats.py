#!/usr/bin/env python3
"""Mine the committed artifacts out of the (large, uncommitted) chunk
censuses:

  data/stats_by_decade.csv  per-decade aggregates
  data/tight.csv            every row of every gap with Hall margin <= MARGIN_CUT
  data/multi.csv            every row of every gap with >= SMIN criticals
  data/extremes.csv         record-setting gaps (max s, largest tight p, ...)
  data/census_hashes.txt    sha256 + row count of each chunk census

Usage: mine_stats.py c1 c2 c3 c4   (chunk prefixes under data/)
"""
import csv, hashlib, sys, os
from collections import defaultdict

MARGIN_CUT = 0
SMIN = 4

def decade(p):
    d = 0
    while p >= 10: p //= 10; d += 1
    return d

def main(chunks):
    dec = defaultdict(lambda: dict(rows=0, gaps=set(), maxs=0, minmarg=10**9,
                                   maxL=0, maxk=0, tight=0, lastp_tight=0))
    tight, multi = [], []
    kdist = defaultdict(int)       # gap length k -> critical-row count
    hashes = []
    extremes = dict(max_s=(0, None), last_margin0=(0, None),
                    max_L=(0, None), max_m=(0, None))
    for ch in chunks:
        fn = f"data/{ch}.census.csv"
        h = hashlib.sha256()
        rows = 0
        cur = {}          # (p,k) -> list of rows, flushed on p change
        curp = None
        with open(fn, "rb") as fb:
            for chunk in iter(lambda: fb.read(1 << 20), b""):
                h.update(chunk)
        with open(fn) as f:
            rd = csv.DictReader(f)
            def flush(pk, rws):
                s = len(rws)
                marg = int(rws[0]["margin"])
                p, k = pk
                d = dec(p)
                D = dec_stats = dec[d]
                D["rows"] += s
                D["maxs"] = max(D["maxs"], s)
                D["minmarg"] = min(D["minmarg"], marg)
                D["maxk"] = max(D["maxk"], k)
                if s >= SMIN: multi.extend(rws)
                if marg <= MARGIN_CUT:
                    tight.extend(rws)
                    D["tight"] += 1
                    D["lastp_tight"] = max(D["lastp_tight"], p)
                    if p > extremes["last_margin0"][0] and marg <= 0:
                        extremes["last_margin0"] = (p, dict(k=k, s=s, margin=marg))
                if s > extremes["max_s"][0]:
                    extremes["max_s"] = (s, dict(p=p, k=k, margin=marg))
                D.setdefault("ngaps", 0)
                D["ngaps"] = D.get("ngaps", 0) + 1
            for row in rd:
                rows += 1
                p, k = int(row["p"]), int(row["k"])
                L, m = int(row["L"]), int(row["m"])
                kdist[k] += 1
                d = dec(p)
                dec[d]["maxL"] = max(dec[d]["maxL"], L)
                if L > extremes["max_L"][0]:
                    extremes["max_L"] = (L, dict(p=p, k=k, m=m))
                if m > extremes["max_m"][0]:
                    extremes["max_m"] = (m, dict(p=p, k=k))
                if curp != (p, k):
                    if curp is not None: flush(curp, cur)
                    curp, cur = (p, k), []
                cur.append(row)
            if curp is not None: flush(curp, cur)
        hashes.append((fn, h.hexdigest(), rows))
    os.makedirs("data", exist_ok=True)
    with open("data/stats_by_decade.csv", "w") as f:
        f.write("decade,gaps_with_criticals,critical_rows,max_s,min_margin,"
                "tight_gaps,last_tight_p,max_L,max_k_with_critical\n")
        for d in sorted(dec):
            D = dec[d]
            f.write(f"{d},{D.get('ngaps',0)},{D['rows']},{D['maxs']},"
                    f"{D['minmarg']},{D['tight']},{D['lastp_tight']},"
                    f"{D['maxL']},{D['maxk']}\n")
    hdr = "p,k,m,factorization,L,assigned,margin\n"
    for name, rows_ in (("tight", tight), ("multi", multi)):
        with open(f"data/{name}.csv", "w") as f:
            f.write(hdr)
            for r in rows_:
                f.write(",".join(r[c] for c in
                        ("p","k","m","factorization","L","assigned","margin")) + "\n")
    with open("data/extremes.csv", "w") as f:
        f.write("record,value,detail\n")
        for k_, (v, detail) in extremes.items():
            f.write(f"{k_},{v},\"{detail}\"\n")
    with open("data/crit_by_k.csv", "w") as f:
        f.write("k,critical_rows\n")
        for k in sorted(kdist):
            f.write(f"{k},{kdist[k]}\n")
    with open("data/census_hashes.txt", "w") as f:
        for fn, hx, rows in hashes:
            f.write(f"{fn}  sha256={hx}  rows={rows}\n")
    print("mined:", {d: dec[d]["rows"] for d in sorted(dec)},
          "tight rows:", len(tight), "multi rows:", len(multi))

if __name__ == "__main__":
    main(sys.argv[1:])
