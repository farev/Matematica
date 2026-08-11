#!/usr/bin/env python3
"""compare_prior.py — formal diff of this session's census against the
prior-art scan log (conglu1997/erdos_699_rust, run 2026-01-03), pinned at
data/prior_art_scan.jsonl.

Their file has one JSON line per n that produced near-misses; a near-miss
(i, j, shared_primes_geq_i == [] meaning no prime STRICTLY > i — their
field name notwithstanding, weak_counterexample false + p = i is how the
9 known triples read) corresponds to this session's EXC (n, i, j).

Checks:
  * their triple set (n <= LIMIT) == our triple set (n <= LIMIT);
  * they report weak_counterexample: false on every line (as do we).
Usage: python3 compare_prior.py merged_exc.txt [LIMIT=10000000]
"""
import sys, json


def main():
    ours_fn = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10**7
    ours = set()
    for line in open(ours_fn):
        p = line.split()
        if p and p[0] == "EXC" and int(p[1]) <= limit:
            ours.add((int(p[1]), int(p[2]), int(p[3])))
    theirs = set()
    weakflags = 0
    for line in open("data/prior_art_scan.jsonl"):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("weak_counterexample"):
            weakflags += 1
        n = rec["n"]
        if n <= limit:
            for nm in rec.get("near_misses", []):
                theirs.add((n, nm["i"], nm["j"]))
    print(f"prior-art triples (n <= {limit}): {len(theirs)}")
    print(f"this-session triples (n <= {limit}): {len(ours)}")
    only_theirs = theirs - ours
    only_ours = ours - theirs
    if only_theirs:
        print(f"IN PRIOR ART ONLY (we missed?): {sorted(only_theirs)}")
    if only_ours:
        print(f"IN OURS ONLY (they missed?): {sorted(only_ours)}")
    if weakflags:
        print(f"prior art flags {weakflags} weak counterexamples?!")
    ok = not only_theirs and not only_ours and weakflags == 0
    print("PRIOR-ART CONCORDANCE", "PASS" if ok else "DIVERGES (investigate)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
