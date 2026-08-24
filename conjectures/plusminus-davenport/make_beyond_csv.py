"""Convert raw dpm_fast output lines (data/dpm_fast_runs.txt) into
data/beyond.csv with the same columns as the sweep tables.

Sharded runs of the same group are merged: node counts are summed minus
(k-1) root recounts, dpm is the max, and the run is exhaustive only if every
shard was uncapped/unstopped and shards 0..k-1 are all present exactly once.

Line format: moduli=13,13 N=169 nclasses=84 dpm=7 nodes=... capped=0 stopped=0 witness=...
Optionally prefixed by "shard=i/k " (added manually when assembling the txt).
"""

import csv
import re
import sys
from collections import defaultdict

from dpm_core import AbelianGroup

runs = defaultdict(list)
with open("data/dpm_fast_runs.txt") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(
            r"(?:shard=(\d+)/(\d+)\s+)?moduli=([\d,]+)\s+N=\d+\s+nclasses=\d+\s+"
            r"dpm=(\d+)\s+nodes=(\d+)\s+capped=(\d)\s+stopped=(\d)\s+witness=(\S*)",
            line)
        assert m, f"unparsed line: {line}"
        shard, nsh, mods, dpm, nodes, capped, stopped, wit = m.groups()
        mods = tuple(sorted((int(x) for x in mods.split(",")), reverse=True))
        runs[mods].append({
            "shard": (int(shard), int(nsh)) if shard else None,
            "dpm": int(dpm), "nodes": int(nodes),
            "capped": capped == "1", "stopped": stopped == "1", "wit": wit,
        })

rows = []
for mods, rr in runs.items():
    G = AbelianGroup(list(mods))
    lo, up = G.lower_d(), G.upper_d()
    shards = [r for r in rr if r["shard"]]
    if shards:
        ks = {r["shard"][1] for r in shards}
        assert len(ks) == 1, mods
        k = ks.pop()
        idxs = sorted(r["shard"][0] for r in shards)
        complete = idxs == list(range(k))
        nodes = sum(r["nodes"] for r in shards) - (k - 1)
        dpm = max(r["dpm"] for r in shards)
        exhaustive = complete and not any(r["capped"] or r["stopped"] for r in shards)
        wit = max(shards, key=lambda r: r["dpm"])["wit"]
    else:
        assert len(rr) == 1, (mods, "duplicate unsharded runs")
        r = rr[0]
        nodes, dpm, wit = r["nodes"], r["dpm"], r["wit"]
        exhaustive = not (r["capped"] or r["stopped"])
    # a found dpm equal to the proved upper bound decides the cell even if
    # the search was not exhaustive; otherwise exhaustiveness is required
    if exhaustive:
        status = "gap:search-decided" if lo != up else "forced+confirmed"
        val = dpm
    elif dpm == up:
        status = "gap:witness-at-upper-bound"
        val = dpm
    else:
        status = "INCOMPLETE"
        val = None
    assert dpm <= up, (mods, "search exceeds proved upper bound!")
    rows.append({
        "order": G.N, "moduli": " ".join(map(str, mods)),
        "invariant_factors": " ".join(map(str, G.invfacs)),
        "lower_d": lo, "upper_d": up, "dpm": val,
        "Dpm": val + 1 if val is not None else None,
        "status": status, "nodes": nodes, "seconds": "",
        "witness": wit,
    })

rows.sort(key=lambda r: (r["order"], r["moduli"]))
with open("data/beyond.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print(f"{len(rows)} groups -> data/beyond.csv")
for r in rows:
    print(r["moduli"], "order", r["order"], "d=", r["dpm"], r["status"], "nodes", r["nodes"])
