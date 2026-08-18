#!/usr/bin/env python3
"""Mine the committed artifacts out of the (large, uncommitted) chunk
censuses:

  data/stats_by_decade.csv  per-decade aggregates
  data/tight.csv            every row of every gap with Hall margin <= 0
  data/multi.csv            every row of every gap with >= SMIN criticals
  data/extremes.csv         record-setting gaps (max s, last tight p, ...)
  data/crit_by_k.csv        critical-row count by gap length k
  data/census_hashes.txt    sha256 + row count of each chunk census

Usage: mine_stats.py c1 c2 c3 c4   (chunk prefixes under data/)
"""
import csv, hashlib, sys, os
from collections import defaultdict

MARGIN_CUT = 0
SMIN = 4

def decade_of(p):
    d = 0
    while p >= 10:
        p //= 10
        d += 1
    return d

def main(chunks):
    decs = defaultdict(lambda: dict(ngaps=0, rows=0, maxs=0, minmarg=10**9,
                                    maxL=0, maxk=0, tight=0, lastp_tight=0))
    tight, multi = [], []
    kdist = defaultdict(int)
    hashes = []
    extremes = dict(max_s=(0, None), last_margin0=(0, None),
                    max_L=(0, None), max_m=(0, None))

    def flush(pk, rws):
        s = len(rws)
        marg = int(rws[0]["margin"])
        p, k = pk
        D = decs[decade_of(p)]
        D["ngaps"] += 1
        D["rows"] += s
        D["maxs"] = max(D["maxs"], s)
        D["minmarg"] = min(D["minmarg"], marg)
        D["maxk"] = max(D["maxk"], k)
        if s >= SMIN:
            multi.extend(rws)
        if marg <= MARGIN_CUT:
            tight.extend(rws)
            D["tight"] += 1
            D["lastp_tight"] = max(D["lastp_tight"], p)
            if marg <= 0 and p > extremes["last_margin0"][0]:
                extremes["last_margin0"] = (p, dict(k=k, s=s, margin=marg))
        if s > extremes["max_s"][0]:
            extremes["max_s"] = (s, dict(p=p, k=k, margin=marg))

    for ch in chunks:
        fn = f"data/{ch}.census.csv"
        h = hashlib.sha256()
        with open(fn, "rb") as fb:
            for blob in iter(lambda: fb.read(1 << 20), b""):
                h.update(blob)
        rows = 0
        curpk, cur = None, []
        with open(fn) as f:
            for row in csv.DictReader(f):
                rows += 1
                p, k = int(row["p"]), int(row["k"])
                L, m = int(row["L"]), int(row["m"])
                kdist[k] += 1
                decs[decade_of(p)]["maxL"] = max(decs[decade_of(p)]["maxL"], L)
                if L > extremes["max_L"][0]:
                    extremes["max_L"] = (L, dict(p=p, k=k, m=m))
                if m > extremes["max_m"][0]:
                    extremes["max_m"] = (m, dict(p=p, k=k))
                if curpk != (p, k):
                    if curpk is not None:
                        flush(curpk, cur)
                    curpk, cur = (p, k), []
                cur.append(row)
            if curpk is not None:
                flush(curpk, cur)
        hashes.append((fn, h.hexdigest(), rows))

    os.makedirs("data", exist_ok=True)
    with open("data/stats_by_decade.csv", "w") as f:
        f.write("decade,gaps_with_criticals,critical_rows,max_s,min_margin,"
                "tight_gaps,last_tight_p,max_L,max_k_with_critical\n")
        for d in sorted(decs):
            D = decs[d]
            f.write(f"{d},{D['ngaps']},{D['rows']},{D['maxs']},{D['minmarg']},"
                    f"{D['tight']},{D['lastp_tight']},{D['maxL']},{D['maxk']}\n")
    hdr = "p,k,m,factorization,L,assigned,margin\n"
    for name, rows_ in (("tight", tight), ("multi", multi)):
        with open(f"data/{name}.csv", "w") as f:
            f.write(hdr)
            for r in rows_:
                f.write(",".join(r[c] for c in
                        ("p", "k", "m", "factorization", "L", "assigned", "margin")) + "\n")
    with open("data/extremes.csv", "w") as f:
        f.write("record,value,detail\n")
        for key, (v, detail) in extremes.items():
            f.write(f"{key},{v},\"{detail}\"\n")
    with open("data/crit_by_k.csv", "w") as f:
        f.write("k,critical_rows\n")
        for k in sorted(kdist):
            f.write(f"{k},{kdist[k]}\n")
    with open("data/census_hashes.txt", "w") as f:
        for fn, hx, rows in hashes:
            f.write(f"{fn}  sha256={hx}  rows={rows}\n")
    print("mined:", {d: decs[d]["rows"] for d in sorted(decs)},
          "tight rows:", len(tight), "multi rows:", len(multi))

if __name__ == "__main__":
    main(sys.argv[1:])
