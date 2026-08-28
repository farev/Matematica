#!/usr/bin/env bash
# run_census.sh N [PARTS] [CONCURRENCY] — exhaustive winning-da-tree census
# over all lattices with N elements (interior posets on k = N-2 points from
# nauty-genposetg).  Aggregates part results, checks the poset count against
# OEIS A000112 and the lattice count against OEIS A006966, and appends a row
# to data/census_summary.tsv.  Any NONWINNING line in a part log is a
# candidate counterexample to the (already-refuted) NCI conjecture and by far
# the most interesting possible output; re-verify it with verify_witness.py.
#
# Usage: ./run_census.sh 14 8 4      # n=14 via 8 parts, 4 concurrent
set -euo pipefail
N=$1; PARTS=${2:-8}; CONC=${3:-4}
K=$((N-2))
command -v nauty-genposetg >/dev/null || { echo "needs nauty (Debian: apt install nauty)"; exit 1; }
[ -x ./lattscan ] || gcc -O3 -march=native -o lattscan lattscan.c
mkdir -p data/parts_n$N
# ground truth (OEIS b-files, fetched 2026-08-28): index = number of points
A000112=(1 1 2 5 16 63 318 2045 16999 183231 2567284 46749427 1104891746 33823827452)
A006966=(1 1 1 1 2 5 15 53 222 1078 5994 37622 262776 2018305 16873364 152233518)
seq $((PARTS-1)) -1 0 | while read -r x; do
  echo "nauty-genposetg $K t q m $x $PARTS 2>/dev/null | ./lattscan $K > data/parts_n$N/part_$x.log 2>&1"
done | xargs -P"$CONC" -I{} bash -c '{}'
python3 - "$N" "$PARTS" "${A000112[$K]}" "${A006966[$N]}" <<'EOF'
import re, sys, glob
n, parts, expp, expl = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
tp = tl = tw = tn = s0 = s1 = s2 = 0; mx = 0
hist = [0]*5
for f in sorted(glob.glob(f"data/parts_n{n}/part_*.log")):
    s = open(f).read()
    for line in s.splitlines():
        if line.startswith("NONWINNING"):
            print("!!! CANDIDATE COUNTEREXAMPLE:", line)
    m = re.search(r"posets=(\d+) lattices=(\d+) winning=(\d+) nonwinning=(\d+)", s)
    tp += int(m.group(1)); tl += int(m.group(2)); tw += int(m.group(3)); tn += int(m.group(4))
    m = re.search(r"fastpath=(\d+) leafclosure=(\d+) fullclosure=(\d+)", s)
    s0 += int(m.group(1)); s1 += int(m.group(2)); s2 += int(m.group(3))
    m = re.search(r"=(\d+),(\d+),(\d+),(\d+),(\d+) maxleaf=\d+ maxfull=(\d+)", s)
    for i in range(5): hist[i] += int(m.group(i+1))
    mx = max(mx, int(m.group(6)))
ok_p = "OK" if tp == expp else f"MISMATCH(exp {expp})"
ok_l = "OK" if tl == expl else f"MISMATCH(exp {expl})"
row = f"{n}\t{tp}\t{tl}\t{tw}\t{tn}\t{s0}\t{s1}\t{s2}\t{mx}\t{ok_p}\t{ok_l}"
print("n\tposets\tlattices\twinning\tnonwinning\tfastpath\tleafclosure\tfullclosure\tmax_states\tA000112\tA006966")
print(row)
with open("data/census_summary.tsv", "a") as f:
    f.write(row + "\n")
if tn or tp != expp or tl != expl:
    sys.exit(1)
EOF
echo "census n=$N complete"
