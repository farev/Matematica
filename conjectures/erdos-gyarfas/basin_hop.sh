#!/bin/bash
# basin_hop.sh — alternate warm-started annealing and steepest-descent polish
# on the {4,8}-free manifold, tracking the minimum C16 count reached.
#
# Usage: ./basin_hop.sh <n> <rounds> <moves-per-anneal> <tag>
#   tag must be NUMERIC (it is folded into the RNG seed).
#
# Round r: anneal (weights 100/50/1, warm-started from the current best) with
# seed derived from tag+round, then polish to a depth-1 local minimum; keep
# the result iff it improves (E under 100/50/1, i.e. C16 count when the
# graph is {4,8}-free). State in hunts/bh_<tag>_n<n>.g6, log in
# hunts/bh_<tag>_n<n>.log, summary rows appended to hunts/basinhop.tsv.
# E=0 at any point = {4,8,16}-free graph: screen C32 via cyclecheck and
# verify with verify_hit.py before believing anything.
set -euo pipefail
cd "$(dirname "$0")"
n=$1; rounds=$2; moves=$3; tag=$4
mkdir -p hunts
state="hunts/bh_${tag}_n${n}.g6"
log="hunts/bh_${tag}_n${n}.log"

bestE=999999999
if [ ! -f "$state" ]; then
    # cold start: one anneal from random produces the initial state
    ./hunt "$n" "$((900000 + tag))" "$moves" 16 100 50 1 > "hunts/bh_${tag}_n${n}.init" 2>> "$log"
    tail -1 "hunts/bh_${tag}_n${n}.init" > "$state"
fi

for r in $(seq 1 "$rounds"); do
    seed=$((700000 + 1000 * tag + r))
    ./hunt "$n" "$seed" "$moves" 16 100 50 1 0 "$state" > "hunts/.bh_${tag}_${n}_a.out" 2>> "$log"
    tail -1 "hunts/.bh_${tag}_${n}_a.out" > "hunts/.bh_${tag}_${n}_a.g6"
    ./hunt "$n" "$seed" 0 16 100 50 1 0 "hunts/.bh_${tag}_${n}_a.g6" > "hunts/.bh_${tag}_${n}_p.out" 2>> "$log"
    pline=$(grep '^POLISH' "hunts/.bh_${tag}_${n}_p.out")
    E=$(sed 's/.*localmin E=\([0-9]*\).*/\1/' <<< "$pline")
    if [ "$E" -lt "$bestE" ]; then
        bestE=$E
        tail -1 "hunts/.bh_${tag}_${n}_p.out" > "$state"
        printf '%s\tn=%d\ttag=%s\tround=%d\t%s\n' "$(date -u +%FT%TZ)" "$n" "$tag" "$r" "$pline" >> hunts/basinhop.tsv
    fi
    if [ "$E" -eq 0 ]; then
        echo "*** E=0 at n=$n tag=$tag round=$r — verify ${state} NOW ***"
        break
    fi
done
echo "basin_hop n=$n tag=$tag done: bestE=$bestE"
