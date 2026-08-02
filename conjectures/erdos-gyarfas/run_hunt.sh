#!/bin/bash
# run_hunt.sh — batch of annealing chains hunting {4,8,16}-free cubic graphs.
#
# Usage: ./run_hunt.sh <n> <nchains> <moves> <jobs>
#
# Chains alternate two energy weightings:
#   even seed:  w = (100, 50, 1)  — pin the {4,8}-free manifold, minimize C16
#   odd  seed:  w = (4, 2, 1)     — balanced
# Each chain's best graph is post-screened with cyclecheck -p (exact, incl.
# C32/C64 when n allows) and the spectrum is appended to the summary row in
# hunts/results_n<n>.tsv.
#
# Interpretation of a zero-energy hit (E=0, i.e. no C4/C8/C16):
#   n <= 31          : counterexample to Erdos-Gyarfas outright
#   33 <= n <= 62    : first known {4,8,16}-free cubic graph (Markström's
#                      unpublished search: none exist with n <= 52); it is a
#                      counterexample iff the C32 screen also comes back empty
set -euo pipefail
cd "$(dirname "$0")"
n=$1; nchains=$2; moves=$3; jobs=$4; soff=${5:-0}
mkdir -p hunts

run_chain() {
    local s=$1
    local w="4 2 1"
    if [ $((s % 2)) -eq 0 ]; then w="100 50 1"; fi
    ./hunt "$n" "$s" "$moves" 16 $w > "hunts/n${n}_seed${s}.out" 2> "hunts/n${n}_seed${s}.log"
    local res g6 spec
    res=$(grep '^RESULT' "hunts/n${n}_seed${s}.out" | tail -1)
    g6=$(tail -1 "hunts/n${n}_seed${s}.out")
    spec=$(printf '%s\n' "$g6" | ./cyclecheck -p 2>/dev/null | cut -f2)
    printf '%s\tspectrum=%s\t%s\n' "$res" "$spec" "$g6" >> "hunts/results_n${n}.tsv"
    if grep -q '^HIT' "hunts/n${n}_seed${s}.out"; then
        echo "*** HIT at n=$n seed=$s — spectrum $spec — VERIFY NOW ***" >&2
    fi
}
export -f run_chain; export n moves

seq $((soff + 1)) $((soff + nchains)) | xargs -P "$jobs" -I{} bash -c 'run_chain {}'
echo "== n=$n done:"
sort -t'=' -k4 -n "hunts/results_n${n}.tsv" 2>/dev/null | head -5 || true
