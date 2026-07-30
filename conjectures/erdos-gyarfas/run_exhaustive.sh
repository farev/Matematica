#!/bin/bash
# run_exhaustive.sh — exhaustive sweep of a C4-free graph class on n vertices,
# keeping every graph that also has no 8-cycle ({4,8}-free census).
#
# Usage: ./run_exhaustive.sh <n> <mod> <jobs> [class]
#   n     order
#   mod   number of geng work parts (res/mod splitting)
#   jobs  how many parts run concurrently
#   class cubic (default) | bipcubic | mindeg3
#
# Classes (all C4-free via geng -f; cyclecheck re-verifies C4 absence):
#   cubic    geng -c -d3 -D3 -f n e:e   connected cubic, e = 3n/2
#   bipcubic geng -b -c -d3 -D3 -f n e:e  connected bipartite cubic (girth>=6)
#   mindeg3  geng -c -d3 -f n           connected, min degree >= 3, any max
#
# Output: data/c48free_<class>_n<n>.g6   {4,8}-free survivors (graph6)
#         logs/<class>_n<n>_part<i>.*.log
#         appends a row to data/counts_<class>_c4free.tsv
set -euo pipefail
cd "$(dirname "$0")"
n=$1; mod=$2; jobs=$3; class=${4:-cubic}

case "$class" in
  cubic)    e=$((3 * n / 2)); gargs="-c -d3 -D3 -f $n $e:$e" ;;
  bipcubic) e=$((3 * n / 2)); gargs="-b -c -d3 -D3 -f $n $e:$e" ;;
  mindeg3)  gargs="-c -d3 -f $n" ;;
  *) echo "unknown class $class" >&2; exit 2 ;;
esac

mkdir -p data logs
rm -f "logs/${class}_n${n}_part"*.log "data/.part_${class}_${n}_"*.g6
out="data/c48free_${class}_n${n}.g6"
: > "$out"
t0=$(date +%s)

run_part() {
    local res=$1
    # shellcheck disable=SC2086
    nauty-geng $gargs "$res/$mod" 2> "logs/${class}_n${n}_part${res}.geng.log" \
      | ./cyclecheck -a 4,8 2> "logs/${class}_n${n}_part${res}.cc.log" \
      > "data/.part_${class}_${n}_${res}.g6"
}
export -f run_part; export gargs mod class n

seq 0 $((mod - 1)) | xargs -P "$jobs" -I{} bash -c 'run_part {}'

cat "data/.part_${class}_${n}_"*.g6 > "$out"; rm -f "data/.part_${class}_${n}_"*.g6
t1=$(date +%s)

total=$(grep -ho '>Z [0-9]*' "logs/${class}_n${n}_part"*.geng.log | awk '{s+=$2} END {print s+0}')
read_sum=$(grep -ho 'read [0-9]*' "logs/${class}_n${n}_part"*.cc.log | awk '{s+=$2} END {print s+0}')
surv=$(wc -l < "$out")
tsv="data/counts_${class}_c4free.tsv"
[ -f "$tsv" ] || printf "date\tclass\tn\tgenerated\tchecked\tsurvivors48\ttime\tcmd\n" > "$tsv"
printf "%s\t%s\t%d\t%d\t%d\t%d\t%ds\tgeng %s [mod=%d]\n" \
    "$(date -u +%F)" "$class" "$n" "$total" "$read_sum" "$surv" "$((t1 - t0))" \
    "$gargs" "$mod" >> "$tsv"
echo "n=$n class=$class: generated=$total checked=$read_sum {4,8}-free=$surv time=$((t1 - t0))s"
